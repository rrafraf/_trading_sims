from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class Bar:
    timestamp: datetime
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TargetSignal:
    timestamp: datetime
    symbol: str
    target_quantity: float
    reason: str


@dataclass(frozen=True)
class Fill:
    timestamp: datetime
    symbol: str
    side: str
    quantity: float
    price: float
    fee: float
    source_signal_timestamp: datetime


@dataclass
class PortfolioState:
    cash: float
    positions: dict[str, float] = field(default_factory=dict)

    def position(self, symbol: str) -> float:
        return self.positions.get(symbol, 0.0)

    def set_position(self, symbol: str, quantity: float) -> None:
        if abs(quantity) < 1e-12:
            self.positions.pop(symbol, None)
        else:
            self.positions[symbol] = quantity


@dataclass(frozen=True)
class RunResult:
    run_id: str
    adapter: str
    strategy: str
    dataset: str
    symbol: str
    initial_cash: float
    final_cash: float
    final_position: float
    final_price: float
    final_equity: float
    return_pct: float
    fill_count: int
    signal_count: int
    notes: list[str]
    fills: list[Fill]

