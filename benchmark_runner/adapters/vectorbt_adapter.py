from __future__ import annotations

import importlib
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from .types import AdapterContext
from ..models import Fill, RunResult, TargetSignal


class VectorBTAdapter:
    name = "vectorbt"

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
            pd, vbt = self._load_dependencies()
        except Exception as exc:
            return self._unavailable_result(
                context,
                notes
                + [
                    "vectorbt unavailable: import failed after checking installed "
                    f"packages and candidates/vectorbt: {exc}"
                ],
            )

        order_plan = self._build_order_plan(context, notes)
        index = pd.DatetimeIndex([bar.timestamp for bar in context.bars])
        close = pd.Series(
            [bar.close for bar in context.bars],
            index=index,
            name=context.symbol,
            dtype="float64",
        )
        open_ = pd.Series(
            [bar.open for bar in context.bars],
            index=index,
            name=context.symbol,
            dtype="float64",
        )
        size = pd.Series(
            [order_plan.sizes.get(bar.timestamp, 0.0) for bar in context.bars],
            index=index,
            name=context.symbol,
            dtype="float64",
        )

        portfolio = vbt.Portfolio.from_orders(
            close=close,
            size=size,
            price=open_,
            init_cash=self.initial_cash,
            fees=self.fee_bps / 10_000.0,
            slippage=self.slippage_bps / 10_000.0,
            direction="both",
            allow_partial=True,
            raise_reject=False,
        )
        fills = self._normalize_fills(
            portfolio=portfolio,
            pd=pd,
            context=context,
            source_by_fill_timestamp=order_plan.source_by_fill_timestamp,
        )

        final_price = context.bars[-1].close
        final_cash = _last_scalar(portfolio.cash())
        final_position = _last_scalar(portfolio.assets())
        final_equity = _last_scalar(portfolio.value())
        return_pct = (final_equity / self.initial_cash - 1.0) * 100.0

        if len(fills) != order_plan.order_count:
            notes.append(
                "vectorbt filled "
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
            vbt = importlib.import_module("vectorbt")
        except ModuleNotFoundError:
            candidate_path = Path(__file__).resolve().parents[2] / "candidates" / "vectorbt"
            if str(candidate_path) not in sys.path:
                sys.path.insert(0, str(candidate_path))
            vbt = importlib.import_module("vectorbt")
        return pd, vbt

    def _build_order_plan(self, context: AdapterContext, notes: list[str]) -> "_OrderPlan":
        signals = sorted(
            [signal for signal in context.signals if signal.symbol == context.symbol],
            key=lambda signal: signal.timestamp,
        )
        sizes: dict[datetime, float] = {}
        source_by_fill_timestamp: dict[datetime, datetime] = {}
        signal_index = 0
        pending_signal: TargetSignal | None = None
        planned_position = 0.0

        for bar in context.bars:
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
            sizes[bar.timestamp] = signed_size
            source_by_fill_timestamp[bar.timestamp] = pending_signal.timestamp
            planned_position += signed_size

            if quantity >= abs(delta) - 1e-12:
                pending_signal = None

        ignored = len(context.signals) - len(signals)
        if ignored:
            notes.append(f"ignored {ignored} signal(s) for symbols other than {context.symbol}")
        return _OrderPlan(sizes=sizes, source_by_fill_timestamp=source_by_fill_timestamp)

    def _normalize_fills(
        self,
        portfolio: Any,
        pd: Any,
        context: AdapterContext,
        source_by_fill_timestamp: dict[datetime, datetime],
    ) -> list[Fill]:
        records = portfolio.orders.records_readable
        fills: list[Fill] = []
        for _, row in records.iterrows():
            timestamp = _to_datetime(row["Timestamp"], pd)
            side = str(row["Side"]).lower()
            fills.append(
                Fill(
                    timestamp=timestamp,
                    symbol=context.symbol,
                    side=side,
                    quantity=float(row["Size"]),
                    price=float(row["Price"]),
                    fee=float(row["Fees"]),
                    source_signal_timestamp=source_by_fill_timestamp.get(timestamp, timestamp),
                )
            )
        return fills

    def _verify_single_symbol(self, context: AdapterContext) -> None:
        symbols = {bar.symbol for bar in context.bars}
        if symbols != {context.symbol}:
            raise ValueError(
                f"{context.run_id}: vectorbt adapter expects single-symbol bars for "
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


class _OrderPlan:
    def __init__(self, sizes: dict[datetime, float], source_by_fill_timestamp: dict[datetime, datetime]):
        self.sizes = sizes
        self.source_by_fill_timestamp = source_by_fill_timestamp

    @property
    def order_count(self) -> int:
        return sum(1 for size in self.sizes.values() if not math.isclose(size, 0.0, abs_tol=1e-12))


def _last_scalar(value: Any) -> float:
    if hasattr(value, "iloc"):
        value = value.iloc[-1]
        if hasattr(value, "iloc"):
            value = value.iloc[0]
    return float(value)


def _to_datetime(value: Any, pd: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    return pd.Timestamp(value).to_pydatetime()
