from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .types import AdapterContext
from ..models import Bar, RunResult


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def unavailable_result(
    context: AdapterContext,
    adapter_name: str,
    initial_cash: float,
    reason: str,
    extra_notes: list[str] | None = None,
) -> RunResult:
    bars = context.bars
    final_price = bars[-1].close if bars else 0.0
    notes = list(context.data_notes)
    notes.append(f"UNAVAILABLE: {reason}")
    if extra_notes:
        notes.extend(extra_notes)
    return RunResult(
        run_id=context.run_id,
        adapter=adapter_name,
        strategy=context.strategy_name,
        dataset=str(context.dataset),
        symbol=context.symbol,
        initial_cash=initial_cash,
        final_cash=initial_cash,
        final_position=0.0,
        final_price=final_price,
        final_equity=initial_cash,
        return_pct=0.0,
        fill_count=0,
        signal_count=len(context.signals),
        notes=notes,
        fills=[],
    )


def target_delta_by_bar(context: AdapterContext) -> dict[datetime, float]:
    """Return target-position deltas keyed by execution bar timestamp.

    The harness convention is: a signal emitted at bar close becomes executable
    on the next strictly later bar. This is the simplest baseline that most bar
    engines can express.
    """
    bars = context.bars
    signals = sorted(context.signals, key=lambda signal: signal.timestamp)
    current_target = 0.0
    signal_index = 0
    pending_target: float | None = None
    deltas: dict[datetime, float] = {}

    for bar in bars:
        while signal_index < len(signals) and signals[signal_index].timestamp < bar.timestamp:
            pending_target = signals[signal_index].target_quantity
            signal_index += 1
        if pending_target is None:
            continue
        delta = pending_target - current_target
        if abs(delta) > 1e-12:
            deltas[bar.timestamp] = delta
            current_target = pending_target
        pending_target = None
    return deltas


def bars_to_pandas_frame(bars: list[Bar]) -> Any:
    import pandas as pd

    return pd.DataFrame(
        {
            "timestamp": [bar.timestamp for bar in bars],
            "open": [bar.open for bar in bars],
            "high": [bar.high for bar in bars],
            "low": [bar.low for bar in bars],
            "close": [bar.close for bar in bars],
            "volume": [bar.volume for bar in bars],
        }
    ).set_index("timestamp")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

