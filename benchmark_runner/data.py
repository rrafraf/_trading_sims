from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from .models import Bar


def parse_timestamp(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def load_bars(path: Path, symbol: str | None = None) -> list[Bar]:
    bars: list[Bar] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp", "symbol", "open", "high", "low", "close", "volume"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} is missing required columns: {sorted(missing)}")

        for row in reader:
            row_symbol = row["symbol"]
            if symbol is not None and row_symbol != symbol:
                continue
            extra = {
                key: value
                for key, value in row.items()
                if key not in required and value not in (None, "")
            }
            bars.append(
                Bar(
                    timestamp=parse_timestamp(row["timestamp"]),
                    symbol=row_symbol,
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]),
                    extra=extra,
                )
            )

    return bars


def validate_bars(bars: list[Bar]) -> list[str]:
    notes: list[str] = []
    seen: set[tuple[str, datetime]] = set()
    previous_by_symbol: dict[str, datetime] = {}
    expected_delta_by_symbol = {}

    for bar in bars:
        key = (bar.symbol, bar.timestamp)
        if key in seen:
            notes.append(f"duplicate timestamp for {bar.symbol} at {bar.timestamp.isoformat()}")
        seen.add(key)

        previous = previous_by_symbol.get(bar.symbol)
        if previous is not None and bar.timestamp <= previous:
            notes.append(f"out-of-order timestamp for {bar.symbol} at {bar.timestamp.isoformat()}")
        elif previous is not None:
            delta = bar.timestamp - previous
            expected_delta = expected_delta_by_symbol.get(bar.symbol)
            if expected_delta is None:
                expected_delta_by_symbol[bar.symbol] = delta
            elif delta != expected_delta:
                notes.append(
                    f"irregular timestamp gap for {bar.symbol} before {bar.timestamp.isoformat()}: "
                    f"expected {expected_delta}, got {delta}"
                )
        previous_by_symbol[bar.symbol] = bar.timestamp

        if bar.high < max(bar.open, bar.close) or bar.low > min(bar.open, bar.close):
            notes.append(f"invalid OHLC range for {bar.symbol} at {bar.timestamp.isoformat()}")
        if min(bar.open, bar.high, bar.low, bar.close) <= 0:
            notes.append(f"non-positive OHLC value for {bar.symbol} at {bar.timestamp.isoformat()}")
        if bar.volume < 0:
            notes.append(f"negative volume for {bar.symbol} at {bar.timestamp.isoformat()}")
        if bar.volume == 0:
            notes.append(f"zero-volume bar for {bar.symbol} at {bar.timestamp.isoformat()}")

    return notes
