from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..models import Bar, TargetSignal


@dataclass(frozen=True)
class AdapterContext:
    run_id: str
    strategy_name: str
    dataset: Path
    symbol: str
    bars: list[Bar]
    signals: list[TargetSignal]
    data_notes: list[str]

