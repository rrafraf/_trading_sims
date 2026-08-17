from __future__ import annotations

import importlib
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .types import AdapterContext
from ..models import Bar, Fill, RunResult, TargetSignal


class BacktraderAdapter:
    name = "backtrader"

    def __init__(
        self,
        initial_cash: float,
        fee_bps: float = 0.0,
        slippage_bps: float = 0.0,
        enforce_volume: bool = False,
    ):
        self.initial_cash = initial_cash
        self.fee_bps = fee_bps
        self.slippage_bps = slippage_bps
        self.enforce_volume = enforce_volume

    def run(self, context: AdapterContext) -> RunResult:
        bt = _import_backtrader()
        bars = list(context.bars)
        signals = sorted(context.signals, key=lambda signal: signal.timestamp)
        notes = list(context.data_notes)

        if not bars:
            raise ValueError(f"{context.run_id}: no bars for {context.symbol}")

        unexpected_symbols = sorted({bar.symbol for bar in bars if bar.symbol != context.symbol})
        if unexpected_symbols:
            raise ValueError(
                f"{context.run_id}: BacktraderAdapter is single-symbol only; "
                f"got {context.symbol!r} plus {unexpected_symbols!r}"
            )

        fill_log: list[Fill] = []
        strategy_notes: list[str] = []

        data = _build_data_feed(bt, bars, context.symbol)
        strategy_type = _build_target_signal_strategy(bt)

        cerebro = bt.Cerebro(stdstats=False)
        cerebro.adddata(data, name=context.symbol)
        cerebro.broker.setcash(self.initial_cash)
        cerebro.broker.setcommission(
            commission=self.fee_bps / 10_000.0,
            percabs=True,
            stocklike=True,
        )

        if self.slippage_bps:
            cerebro.broker.set_slippage_perc(
                self.slippage_bps / 10_000.0,
                slip_open=True,
                slip_match=True,
                slip_out=True,
            )

        if self.enforce_volume:
            cerebro.broker.set_filler(bt.broker.fillers.FixedSize())
            notes.append("Backtrader volume filler enabled with FixedSize(size=None)")

        cerebro.addstrategy(
            strategy_type,
            signals=signals,
            symbol=context.symbol,
            fills=fill_log,
            notes=strategy_notes,
        )

        try:
            cerebro.run()
        except Exception as exc:
            raise RuntimeError(
                f"{context.run_id}: Backtrader run failed for {context.symbol}: {exc}"
            ) from exc

        final_cash = float(cerebro.broker.getcash())
        final_position = float(cerebro.broker.getposition(data).size)
        final_price = float(bars[-1].close)
        final_equity = final_cash + final_position * final_price
        return_pct = (final_equity / self.initial_cash - 1.0) * 100.0

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
            fill_count=len(fill_log),
            signal_count=len(signals),
            notes=notes + strategy_notes,
            fills=fill_log,
        )


def _import_backtrader() -> Any:
    try:
        return importlib.import_module("backtrader")
    except ModuleNotFoundError as exc:
        if exc.name != "backtrader":
            raise RuntimeError(
                f"Backtrader import failed because dependency {exc.name!r} is missing"
            ) from exc

    candidate_path = Path(__file__).resolve().parents[2] / "candidates" / "backtrader"
    if candidate_path.exists():
        candidate_text = str(candidate_path)
        if candidate_text not in sys.path:
            sys.path.insert(0, candidate_text)
        try:
            return importlib.import_module("backtrader")
        except Exception as exc:
            raise RuntimeError(
                f"Backtrader is present at {candidate_path}, but importing it failed: {exc}"
            ) from exc

    raise RuntimeError(
        "Backtrader is unavailable. Install the backtrader package or clone it "
        "to candidates/backtrader."
    )


def _build_data_feed(bt: Any, bars: list[Bar], symbol: str) -> Any:
    class InMemoryOHLCV(bt.feed.DataBase):
        params = (("bars", None),)

        def __init__(self):
            super().__init__()
            self._idx = -1

        def start(self):
            super().start()
            self._idx = -1

        def _load(self):
            self._idx += 1
            if self._idx >= len(self.p.bars):
                return False

            bar = self.p.bars[self._idx]
            self.lines.datetime[0] = bt.date2num(_to_backtrader_datetime(bar.timestamp))
            self.lines.open[0] = float(bar.open)
            self.lines.high[0] = float(bar.high)
            self.lines.low[0] = float(bar.low)
            self.lines.close[0] = float(bar.close)
            self.lines.volume[0] = float(bar.volume)
            self.lines.openinterest[0] = 0.0
            return True

    return InMemoryOHLCV(bars=bars, name=symbol)


def _build_target_signal_strategy(bt: Any) -> type:
    class TargetSignalStrategy(bt.Strategy):
        params = (
            ("signals", None),
            ("symbol", ""),
            ("fills", None),
            ("notes", None),
        )

        def __init__(self):
            self._signals: list[TargetSignal] = list(self.p.signals or [])
            self._signal_index = 0
            self._order_sources: dict[int, datetime] = {}

        def next(self):
            current_timestamp = _from_backtrader_datetime(bt, self.data.datetime[0])
            signal = self._next_signal_for_bar(current_timestamp)
            if signal is None:
                return

            order = self.order_target_size(target=signal.target_quantity)
            if order is not None:
                self._order_sources[order.ref] = signal.timestamp

        def notify_order(self, order):
            if order.status in (order.Submitted, order.Accepted):
                return

            if order.status in (order.Partial, order.Completed):
                self._capture_execution_bits(order)

            if order.status in (order.Canceled, order.Expired, order.Margin, order.Rejected):
                source = self._order_sources.get(order.ref)
                source_text = source.isoformat() if source is not None else "unknown signal"
                self.p.notes.append(
                    f"Backtrader order {order.ref} {order.getstatusname()} for {source_text}"
                )

            if not order.alive():
                self._order_sources.pop(order.ref, None)

        def _next_signal_for_bar(self, current_timestamp: datetime) -> TargetSignal | None:
            latest_signal = None
            while self._signal_index < len(self._signals):
                candidate = self._signals[self._signal_index]
                if _normalize_timestamp(candidate.timestamp) > current_timestamp:
                    break
                self._signal_index += 1
                if candidate.symbol == self.p.symbol:
                    latest_signal = candidate
            return latest_signal

        def _capture_execution_bits(self, order) -> None:
            source_timestamp = self._order_sources.get(order.ref)
            if source_timestamp is None:
                source_timestamp = _from_backtrader_datetime(bt, order.created.dt)
                self.p.notes.append(
                    f"Backtrader order {order.ref} had no mapped source signal; "
                    f"using order creation timestamp"
                )

            pending_bits = list(order.executed.getpending())
            if pending_bits:
                for bit in pending_bits:
                    self._append_fill(bit.dt, bit.size, bit.price, bit.comm, source_timestamp)
                return

            if order.status == order.Completed and abs(order.executed.size) > 1e-12:
                self._append_fill(
                    order.executed.dt,
                    order.executed.size,
                    order.executed.price,
                    order.executed.comm,
                    source_timestamp,
                )

        def _append_fill(
            self,
            executed_dt: float,
            size: float,
            price: float,
            commission: float,
            source_timestamp: datetime,
        ) -> None:
            if abs(size) < 1e-12:
                return

            side = "buy" if size > 0 else "sell"
            self.p.fills.append(
                Fill(
                    timestamp=_from_backtrader_datetime(bt, executed_dt),
                    symbol=self.p.symbol,
                    side=side,
                    quantity=abs(float(size)),
                    price=float(price),
                    fee=float(commission),
                    source_signal_timestamp=_normalize_timestamp(source_timestamp),
                )
            )

    return TargetSignalStrategy


def _to_backtrader_datetime(timestamp: datetime) -> datetime:
    if timestamp.tzinfo is None:
        return timestamp
    return timestamp.astimezone(timezone.utc).replace(tzinfo=None)


def _from_backtrader_datetime(bt: Any, value: float) -> datetime:
    timestamp = bt.num2date(value)
    return _normalize_timestamp(timestamp)


def _normalize_timestamp(timestamp: datetime) -> datetime:
    if timestamp.tzinfo is None:
        return timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(timezone.utc)


__all__ = ["BacktraderAdapter"]
