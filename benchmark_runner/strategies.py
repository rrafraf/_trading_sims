from __future__ import annotations

from abc import ABC, abstractmethod
from statistics import mean, pstdev

from .models import Bar, TargetSignal


class SignalStrategy(ABC):
    name: str

    def __init__(self, symbol: str, quantity: float, **params):
        self.symbol = symbol
        self.quantity = quantity
        self.params = params

    @abstractmethod
    def generate(self, bars: list[Bar]) -> list[TargetSignal]:
        raise NotImplementedError


class BuyAndHoldStrategy(SignalStrategy):
    name = "buy_hold"

    def generate(self, bars: list[Bar]) -> list[TargetSignal]:
        start_index = int(self.params.get("start_index", 0))
        if not bars or start_index >= len(bars):
            return []
        return [
            TargetSignal(
                timestamp=bars[start_index].timestamp,
                symbol=self.symbol,
                target_quantity=self.quantity,
                reason=f"buy_hold:start_index={start_index}",
            )
        ]


class SmaCrossStrategy(SignalStrategy):
    name = "sma_cross"

    def generate(self, bars: list[Bar]) -> list[TargetSignal]:
        fast = int(self.params.get("fast", 5))
        slow = int(self.params.get("slow", 20))
        if fast <= 0 or slow <= 0 or fast >= slow:
            raise ValueError("sma_cross requires 0 < fast < slow")

        signals: list[TargetSignal] = []
        current_target: float | None = None
        closes: list[float] = []
        for bar in bars:
            closes.append(bar.close)
            if len(closes) < slow:
                continue
            fast_sma = mean(closes[-fast:])
            slow_sma = mean(closes[-slow:])
            target = self.quantity if fast_sma > slow_sma else 0.0
            if current_target is None or abs(target - current_target) > 1e-12:
                signals.append(
                    TargetSignal(
                        timestamp=bar.timestamp,
                        symbol=self.symbol,
                        target_quantity=target,
                        reason=f"sma_cross:fast={fast}:slow={slow}:fast_sma={fast_sma:.6f}:slow_sma={slow_sma:.6f}",
                    )
                )
                current_target = target
        return signals


class BreakoutChannelStrategy(SignalStrategy):
    name = "breakout_channel"

    def generate(self, bars: list[Bar]) -> list[TargetSignal]:
        lookback = int(self.params.get("lookback", 20))
        if lookback <= 1:
            raise ValueError("breakout_channel requires lookback > 1")

        signals: list[TargetSignal] = []
        current_target = 0.0
        for index, bar in enumerate(bars):
            if index < lookback:
                continue
            window = bars[index - lookback : index]
            high_break = max(item.high for item in window)
            low_break = min(item.low for item in window)
            target = current_target
            if bar.close > high_break:
                target = self.quantity
            elif bar.close < low_break:
                target = 0.0
            if abs(target - current_target) > 1e-12:
                signals.append(
                    TargetSignal(
                        timestamp=bar.timestamp,
                        symbol=self.symbol,
                        target_quantity=target,
                        reason=f"breakout_channel:lookback={lookback}:high={high_break:.6f}:low={low_break:.6f}",
                    )
                )
                current_target = target
        return signals


class MeanReversionZScoreStrategy(SignalStrategy):
    name = "mean_reversion_zscore"

    def generate(self, bars: list[Bar]) -> list[TargetSignal]:
        lookback = int(self.params.get("lookback", 20))
        entry_z = float(self.params.get("entry_z", 1.5))
        exit_z = float(self.params.get("exit_z", 0.25))
        allow_short = bool(self.params.get("allow_short", False))
        if lookback <= 1:
            raise ValueError("mean_reversion_zscore requires lookback > 1")

        signals: list[TargetSignal] = []
        current_target = 0.0
        closes: list[float] = []
        for bar in bars:
            closes.append(bar.close)
            if len(closes) < lookback:
                continue
            window = closes[-lookback:]
            sigma = pstdev(window)
            if sigma == 0:
                continue
            z_score = (bar.close - mean(window)) / sigma
            target = current_target
            if z_score <= -entry_z:
                target = self.quantity
            elif allow_short and z_score >= entry_z:
                target = -self.quantity
            elif abs(z_score) <= exit_z:
                target = 0.0
            if abs(target - current_target) > 1e-12:
                signals.append(
                    TargetSignal(
                        timestamp=bar.timestamp,
                        symbol=self.symbol,
                        target_quantity=target,
                        reason=f"mean_reversion_zscore:lookback={lookback}:z={z_score:.6f}",
                    )
                )
                current_target = target
        return signals


class ScheduledTargetsStrategy(SignalStrategy):
    name = "scheduled_targets"

    def generate(self, bars: list[Bar]) -> list[TargetSignal]:
        steps = self.params.get("steps", [])
        if not isinstance(steps, list):
            raise ValueError("scheduled_targets requires params.steps to be a list")

        signals: list[TargetSignal] = []
        for step_number, step in enumerate(steps):
            if not isinstance(step, dict):
                raise ValueError("scheduled_targets steps must be objects")
            index = int(step["index"])
            if index < 0 or index >= len(bars):
                continue
            target = float(step.get("target_quantity", self.quantity * float(step.get("target_multiplier", 1.0))))
            bar = bars[index]
            signals.append(
                TargetSignal(
                    timestamp=bar.timestamp,
                    symbol=self.symbol,
                    target_quantity=target,
                    reason=f"scheduled_targets:step={step_number}:index={index}:target={target:.8f}",
                )
            )
        return signals


class FlipEveryNStrategy(SignalStrategy):
    name = "flip_every_n"

    def generate(self, bars: list[Bar]) -> list[TargetSignal]:
        interval = int(self.params.get("interval", 10))
        start_index = int(self.params.get("start_index", 0))
        end_flat = bool(self.params.get("end_flat", True))
        if interval <= 0:
            raise ValueError("flip_every_n requires interval > 0")
        if start_index < 0:
            raise ValueError("flip_every_n requires start_index >= 0")

        signals: list[TargetSignal] = []
        target = 0.0
        for index in range(start_index, len(bars), interval):
            target = self.quantity if abs(target) < 1e-12 else 0.0
            signals.append(
                TargetSignal(
                    timestamp=bars[index].timestamp,
                    symbol=self.symbol,
                    target_quantity=target,
                    reason=f"flip_every_n:interval={interval}:index={index}:target={target:.8f}",
                )
            )

        if end_flat and bars and signals and abs(signals[-1].target_quantity) > 1e-12:
            final_index = len(bars) - 1
            if signals[-1].timestamp != bars[final_index].timestamp:
                signals.append(
                    TargetSignal(
                        timestamp=bars[final_index].timestamp,
                        symbol=self.symbol,
                        target_quantity=0.0,
                        reason=f"flip_every_n:end_flat:index={final_index}",
                    )
                )
        return signals


STRATEGIES = {
    BuyAndHoldStrategy.name: BuyAndHoldStrategy,
    SmaCrossStrategy.name: SmaCrossStrategy,
    BreakoutChannelStrategy.name: BreakoutChannelStrategy,
    MeanReversionZScoreStrategy.name: MeanReversionZScoreStrategy,
    ScheduledTargetsStrategy.name: ScheduledTargetsStrategy,
    FlipEveryNStrategy.name: FlipEveryNStrategy,
}


def build_strategy(name: str, symbol: str, quantity: float, params: dict) -> SignalStrategy:
    strategy_type = STRATEGIES.get(name)
    if strategy_type is None:
        raise ValueError(f"Unknown strategy: {name}")
    return strategy_type(symbol=symbol, quantity=quantity, **params)
