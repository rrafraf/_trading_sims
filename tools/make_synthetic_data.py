#!/usr/bin/env python
from __future__ import annotations

import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path


FIELDS = ["timestamp", "symbol", "open", "high", "low", "close", "volume", "scenario"]


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def make_normal_daily(path: Path) -> None:
    rows = []
    dt = datetime(2024, 1, 2, tzinfo=timezone.utc)
    close = 100.0
    for index in range(40):
        if dt.weekday() >= 5:
            dt += timedelta(days=1)
            continue
        open_ = close
        close = round(close * (1.0 + ((index % 7) - 3) / 1000.0), 4)
        high = round(max(open_, close) + 0.75, 4)
        low = round(min(open_, close) - 0.65, 4)
        rows.append(
            {
                "timestamp": iso(dt),
                "symbol": "SIM",
                "open": open_,
                "high": high,
                "low": low,
                "close": close,
                "volume": 1_000_000 + index * 1000,
                "scenario": "normal_daily",
            }
        )
        dt += timedelta(days=1)
    write_rows(path, rows)


def make_edge_minute(path: Path) -> None:
    base = datetime(2024, 1, 3, 14, 30, tzinfo=timezone.utc)
    rows = [
        {
            "timestamp": iso(base),
            "symbol": "SIM",
            "open": 100.00,
            "high": 100.30,
            "low": 99.90,
            "close": 100.10,
            "volume": 12000,
            "scenario": "normal_open",
        },
        {
            "timestamp": iso(base + timedelta(minutes=1)),
            "symbol": "SIM",
            "open": 100.10,
            "high": 100.20,
            "low": 100.00,
            "close": 100.05,
            "volume": 0,
            "scenario": "zero_volume_bar",
        },
        {
            "timestamp": iso(base + timedelta(minutes=2)),
            "symbol": "SIM",
            "open": 100.05,
            "high": 101.00,
            "low": 99.00,
            "close": 100.50,
            "volume": 100,
            "scenario": "same_bar_stop_and_target_ambiguous",
        },
        # Intentionally skip base + 3 minutes.
        {
            "timestamp": iso(base + timedelta(minutes=4)),
            "symbol": "SIM",
            "open": 98.00,
            "high": 98.30,
            "low": 96.80,
            "close": 97.50,
            "volume": 22000,
            "scenario": "missing_candle_then_gap_through_stop",
        },
        {
            "timestamp": iso(base + timedelta(minutes=5)),
            "symbol": "SIM",
            "open": 49.00,
            "high": 50.00,
            "low": 48.80,
            "close": 49.50,
            "volume": 500000,
            "scenario": "split_like_discontinuity",
        },
        {
            "timestamp": iso(base + timedelta(minutes=6)),
            "symbol": "SIM",
            "open": 49.50,
            "high": 49.55,
            "low": 49.45,
            "close": 49.50,
            "volume": 10,
            "scenario": "thin_liquidity_flat_bar",
        },
    ]
    write_rows(path, rows)


def make_bad_timestamp_file(path: Path) -> None:
    base = datetime(2024, 1, 3, 14, 30, tzinfo=timezone.utc)
    rows = [
        {
            "timestamp": iso(base),
            "symbol": "SIM",
            "open": 100,
            "high": 101,
            "low": 99,
            "close": 100,
            "volume": 1000,
            "scenario": "first",
        },
        {
            "timestamp": iso(base),
            "symbol": "SIM",
            "open": 100,
            "high": 102,
            "low": 98,
            "close": 101,
            "volume": 1000,
            "scenario": "duplicate_timestamp",
        },
        {
            "timestamp": iso(base - timedelta(minutes=1)),
            "symbol": "SIM",
            "open": 99,
            "high": 100,
            "low": 98,
            "close": 99,
            "volume": 1000,
            "scenario": "out_of_order_timestamp",
        },
    ]
    write_rows(path, rows)


def main() -> int:
    root = Path("data/synthetic")
    make_normal_daily(root / "normal_daily.csv")
    make_edge_minute(root / "edge_case_minute.csv")
    make_bad_timestamp_file(root / "bad_timestamps.csv")
    print(f"Wrote synthetic fixtures under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

