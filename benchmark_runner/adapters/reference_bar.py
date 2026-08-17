from __future__ import annotations

from .types import AdapterContext
from ..models import Fill, PortfolioState, RunResult, TargetSignal


class ReferenceBarAdapter:
    name = "reference_bar"

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
        bars = context.bars
        signals = sorted(context.signals, key=lambda signal: signal.timestamp)
        notes = list(context.data_notes)
        portfolio = PortfolioState(cash=self.initial_cash)
        fills: list[Fill] = []
        signal_index = 0
        pending_signal: TargetSignal | None = None

        if not bars:
            raise ValueError(f"{context.run_id}: no bars for {context.symbol}")

        for bar in bars:
            while signal_index < len(signals) and signals[signal_index].timestamp < bar.timestamp:
                pending_signal = signals[signal_index]
                signal_index += 1

            if pending_signal is None:
                continue

            current_position = portfolio.position(context.symbol)
            delta = pending_signal.target_quantity - current_position
            if abs(delta) < 1e-12:
                pending_signal = None
                continue

            if self.enforce_volume and bar.volume <= 0:
                notes.append(f"deferred fill on zero-volume bar at {bar.timestamp.isoformat()}")
                continue

            side = "buy" if delta > 0 else "sell"
            quantity = abs(delta)
            if self.enforce_volume and bar.volume > 0:
                quantity = min(quantity, bar.volume)
                if quantity < abs(delta):
                    notes.append(
                        f"partial volume-limited fill at {bar.timestamp.isoformat()}: "
                        f"requested {abs(delta):.8f}, filled {quantity:.8f}"
                    )

            price = self._apply_slippage(bar.open, side)
            notional = quantity * price
            fee = notional * self.fee_bps / 10_000.0

            if side == "buy":
                portfolio.cash -= notional + fee
                portfolio.set_position(context.symbol, current_position + quantity)
            else:
                portfolio.cash += notional - fee
                portfolio.set_position(context.symbol, current_position - quantity)

            fills.append(
                Fill(
                    timestamp=bar.timestamp,
                    symbol=context.symbol,
                    side=side,
                    quantity=quantity,
                    price=price,
                    fee=fee,
                    source_signal_timestamp=pending_signal.timestamp,
                )
            )

            if quantity >= abs(delta) - 1e-12:
                pending_signal = None

        final_position = portfolio.position(context.symbol)
        final_price = bars[-1].close
        final_equity = portfolio.cash + final_position * final_price
        return_pct = (final_equity / self.initial_cash - 1.0) * 100.0
        return RunResult(
            run_id=context.run_id,
            adapter=self.name,
            strategy=context.strategy_name,
            dataset=str(context.dataset),
            symbol=context.symbol,
            initial_cash=self.initial_cash,
            final_cash=portfolio.cash,
            final_position=final_position,
            final_price=final_price,
            final_equity=final_equity,
            return_pct=return_pct,
            fill_count=len(fills),
            signal_count=len(signals),
            notes=notes,
            fills=fills,
        )

    def _apply_slippage(self, price: float, side: str) -> float:
        multiplier = self.slippage_bps / 10_000.0
        if side == "buy":
            return price * (1.0 + multiplier)
        return price * (1.0 - multiplier)

