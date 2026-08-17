from __future__ import annotations

import importlib
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .types import AdapterContext
from ..models import Fill, RunResult, TargetSignal


class PyBrokerAdapter:
    name = "pybroker"

    def __init__(
        self,
        initial_cash: float,
        fee_bps: float = 0.0,
        slippage_bps: float = 0.0,
        enforce_volume: bool = True,
    ):
        self.initial_cash = initial_cash
        self.fee_bps = fee_bps
        self.slippage_bps = slippage_bps
        self.enforce_volume = enforce_volume

    def run(self, context: AdapterContext) -> RunResult:
        if not context.bars:
            raise ValueError(f"{context.run_id}: no bars for {context.symbol}")
        self._verify_single_symbol(context)

        notes = list(context.data_notes)
        try:
            pd, pybroker = self._load_dependencies()
        except Exception as exc:
            return self._unavailable_result(
                context,
                notes
                + [
                    "pybroker unavailable: import failed after checking installed "
                    f"packages and candidates/pybroker/src: {exc}"
                ],
            )

        order_plan = self._build_order_plan(context, notes)
        data = self._bars_to_dataframe(pd, context)

        pybroker.disable_logging()
        pybroker.disable_progress_bar()

        config = pybroker.StrategyConfig(
            initial_cash=self.initial_cash,
            fee_mode=pybroker.FeeMode.ORDER_PERCENT if self.fee_bps else None,
            fee_amount=self.fee_bps / 100.0 if self.fee_bps else 0.0,
            enable_fractional_shares=True,
            round_fill_price=False,
            buy_delay=1,
            sell_delay=1,
            exit_on_last_bar=False,
            round_test_result=False,
        )
        strategy = pybroker.Strategy(
            data,
            start_date=data["date"].iloc[0],
            end_date=data["date"].iloc[-1],
            config=config,
        )
        emit_by_timestamp = order_plan.size_by_emit_timestamp
        buy_fill_price = self._fill_price_fn(+1.0)
        sell_fill_price = self._fill_price_fn(-1.0)

        def exec_fn(ctx):
            size = emit_by_timestamp.get(_naive_datetime(ctx.dt))
            if size is None or math.isclose(size, 0.0, abs_tol=1e-12):
                return
            if size > 0:
                ctx.buy_shares = abs(size)
                ctx.buy_fill_price = buy_fill_price
            else:
                ctx.sell_shares = abs(size)
                ctx.sell_fill_price = sell_fill_price

        strategy.add_execution(exec_fn, context.symbol)
        result = strategy.backtest(train_size=0, calc_bootstrap=False, disable_parallel=True)
        fills = self._normalize_fills(
            result=result,
            context=context,
            source_by_emit_timestamp=order_plan.source_by_emit_timestamp,
        )

        final_price = context.bars[-1].close
        final_cash = _last_dataframe_value(result.portfolio, "cash", self.initial_cash)
        final_position = self._position_from_fills(fills)
        final_equity = _last_dataframe_value(
            result.portfolio,
            "market_value",
            final_cash + final_position * final_price,
        )
        return_pct = (final_equity / self.initial_cash - 1.0) * 100.0

        if len(fills) != order_plan.order_count:
            notes.append(
                "pybroker filled "
                f"{len(fills)} of {order_plan.order_count} planned orders; "
                "cash, rejection, or partial-fill rules may differ from the reference adapter"
            )

        return RunResult(
            run_id=context.run_id,
            adapter=self.name,
            strategy=context.strategy_name,
            dataset=str(context.dataset),
            symbol=context.symbol,
            initial_cash=self.initial_cash,
            final_cash=final_cash,
            final_position=final_position,
            final_price=final_price,
            final_equity=final_equity,
            return_pct=return_pct,
            fill_count=len(fills),
            signal_count=len(context.signals),
            notes=notes,
            fills=fills,
        )

    def _load_dependencies(self) -> tuple[Any, Any]:
        pd = importlib.import_module("pandas")
        try:
            pybroker = importlib.import_module("pybroker")
        except ModuleNotFoundError:
            candidate_path = Path(__file__).resolve().parents[2] / "candidates" / "pybroker" / "src"
            if str(candidate_path) not in sys.path:
                sys.path.insert(0, str(candidate_path))
            pybroker = importlib.import_module("pybroker")
        return pd, pybroker

    def _bars_to_dataframe(self, pd: Any, context: AdapterContext) -> Any:
        return pd.DataFrame(
            {
                "date": [_naive_datetime(bar.timestamp) for bar in context.bars],
                "symbol": [bar.symbol for bar in context.bars],
                "open": [bar.open for bar in context.bars],
                "high": [bar.high for bar in context.bars],
                "low": [bar.low for bar in context.bars],
                "close": [bar.close for bar in context.bars],
                "volume": [bar.volume for bar in context.bars],
            }
        )

    def _build_order_plan(self, context: AdapterContext, notes: list[str]) -> "_PyBrokerOrderPlan":
        signals = sorted(
            [signal for signal in context.signals if signal.symbol == context.symbol],
            key=lambda signal: signal.timestamp,
        )
        size_by_emit_timestamp: dict[datetime, float] = {}
        source_by_emit_timestamp: dict[datetime, datetime] = {}
        signal_index = 0
        pending_signal: TargetSignal | None = None
        planned_position = 0.0

        for index, bar in enumerate(context.bars):
            while signal_index < len(signals) and signals[signal_index].timestamp < bar.timestamp:
                pending_signal = signals[signal_index]
                signal_index += 1

            if pending_signal is None:
                continue

            delta = pending_signal.target_quantity - planned_position
            if abs(delta) < 1e-12:
                pending_signal = None
                continue

            if self.enforce_volume and bar.volume <= 0:
                notes.append(f"deferred fill on zero-volume bar at {bar.timestamp.isoformat()}")
                continue

            if index == 0:
                notes.append(
                    f"pybroker cannot schedule a next-bar fill at first bar {bar.timestamp.isoformat()}"
                )
                continue

            side_multiplier = 1.0 if delta > 0 else -1.0
            quantity = abs(delta)
            if self.enforce_volume and bar.volume > 0:
                quantity = min(quantity, bar.volume)
                if quantity < abs(delta):
                    notes.append(
                        f"partial volume-limited fill at {bar.timestamp.isoformat()}: "
                        f"requested {abs(delta):.8f}, filled {quantity:.8f}"
                    )

            signed_size = side_multiplier * quantity
            emit_timestamp = _naive_datetime(context.bars[index - 1].timestamp)
            size_by_emit_timestamp[emit_timestamp] = signed_size
            source_by_emit_timestamp[emit_timestamp] = pending_signal.timestamp
            planned_position += signed_size

            if quantity >= abs(delta) - 1e-12:
                pending_signal = None

        ignored = len(context.signals) - len(signals)
        if ignored:
            notes.append(f"ignored {ignored} signal(s) for symbols other than {context.symbol}")
        return _PyBrokerOrderPlan(
            size_by_emit_timestamp=size_by_emit_timestamp,
            source_by_emit_timestamp=source_by_emit_timestamp,
        )

    def _fill_price_fn(self, side_multiplier: float):
        slippage = self.slippage_bps / 10_000.0

        def fill_price(_symbol, bar_data):
            return float(bar_data.open[-1]) * (1.0 + side_multiplier * slippage)

        return fill_price

    def _normalize_fills(
        self,
        result: Any,
        context: AdapterContext,
        source_by_emit_timestamp: dict[datetime, datetime],
    ) -> list[Fill]:
        fills: list[Fill] = []
        if result.orders.empty:
            return fills

        for _, row in result.orders.iterrows():
            created = _naive_datetime(row["created"])
            timestamp = _utc_datetime(row["date"])
            side = str(row["type"]).lower()
            fills.append(
                Fill(
                    timestamp=timestamp,
                    symbol=context.symbol,
                    side=side,
                    quantity=float(row["shares"]),
                    price=float(row["fill_price"]),
                    fee=float(row["fees"]),
                    source_signal_timestamp=source_by_emit_timestamp.get(created, _utc_datetime(created)),
                )
            )
        return fills

    def _position_from_fills(self, fills: list[Fill]) -> float:
        position = 0.0
        for fill in fills:
            if fill.side == "buy":
                position += fill.quantity
            else:
                position -= fill.quantity
        return position

    def _verify_single_symbol(self, context: AdapterContext) -> None:
        symbols = {bar.symbol for bar in context.bars}
        if symbols != {context.symbol}:
            raise ValueError(
                f"{context.run_id}: pybroker adapter expects single-symbol bars for "
                f"{context.symbol}, received {sorted(symbols)!r}"
            )

    def _unavailable_result(self, context: AdapterContext, notes: list[str]) -> RunResult:
        final_price = context.bars[-1].close if context.bars else 0.0
        return RunResult(
            run_id=context.run_id,
            adapter=self.name,
            strategy=context.strategy_name,
            dataset=str(context.dataset),
            symbol=context.symbol,
            initial_cash=self.initial_cash,
            final_cash=self.initial_cash,
            final_position=0.0,
            final_price=final_price,
            final_equity=self.initial_cash,
            return_pct=0.0,
            fill_count=0,
            signal_count=len(context.signals),
            notes=notes,
            fills=[],
        )


class _PyBrokerOrderPlan:
    def __init__(
        self,
        size_by_emit_timestamp: dict[datetime, float],
        source_by_emit_timestamp: dict[datetime, datetime],
    ):
        self.size_by_emit_timestamp = size_by_emit_timestamp
        self.source_by_emit_timestamp = source_by_emit_timestamp

    @property
    def order_count(self) -> int:
        return sum(
            1
            for size in self.size_by_emit_timestamp.values()
            if not math.isclose(size, 0.0, abs_tol=1e-12)
        )


def _naive_datetime(value: Any) -> datetime:
    if hasattr(value, "to_pydatetime"):
        value = value.to_pydatetime()
    elif not isinstance(value, datetime):
        value = datetime.fromisoformat(str(value))
    if value.tzinfo is not None:
        return value.astimezone(timezone.utc).replace(tzinfo=None)
    return value


def _utc_datetime(value: Any) -> datetime:
    value = _naive_datetime(value)
    return value.replace(tzinfo=timezone.utc)


def _last_dataframe_value(frame: Any, column: str, default: float) -> float:
    if frame.empty or column not in frame.columns:
        return float(default)
    return float(frame[column].iloc[-1])
