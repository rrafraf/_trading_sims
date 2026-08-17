#!/usr/bin/env python
from __future__ import annotations

import csv
import math
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


def make_bars(
    *,
    start: datetime,
    count: int,
    step: timedelta,
    symbol: str,
    start_price: float,
    scenario: str,
    drift: float,
    wave: float,
    shock_at: int | None = None,
    shock_size: float = 0.0,
    zero_volume_every: int | None = None,
    skip_every: int | None = None,
) -> list[dict]:
    rows: list[dict] = []
    dt = start
    close = start_price
    for index in range(count):
        if skip_every and index > 0 and index % skip_every == 0:
            dt += step
            continue

        open_ = close
        cycle = math.sin(index / 7.0) * wave
        micro = math.sin(index / 3.0) * wave * 0.35
        close = open_ * (1.0 + drift + cycle + micro)
        if shock_at is not None and index == shock_at:
            close *= 1.0 + shock_size

        high = max(open_, close) * (1.0 + 0.0008 + abs(cycle) * 0.25)
        low = min(open_, close) * (1.0 - 0.0008 - abs(cycle) * 0.25)
        volume = 12000 + (index % 20) * 350
        if zero_volume_every and index > 0 and index % zero_volume_every == 0:
            volume = 0

        rows.append(
            {
                "timestamp": iso(dt),
                "symbol": symbol,
                "open": round(open_, 6),
                "high": round(high, 6),
                "low": round(low, 6),
                "close": round(close, 6),
                "volume": volume,
                "scenario": scenario,
            }
        )
        dt += step
    return rows


def make_gap_open_bars(
    *,
    start: datetime,
    count: int,
    step: timedelta,
    symbol: str,
    start_price: float,
    scenario: str,
    gap_index: int,
    gap_size: float,
) -> list[dict]:
    rows: list[dict] = []
    dt = start
    close = start_price
    for index in range(count):
        open_ = close
        if index == gap_index:
            open_ = close * (1.0 + gap_size)
        close = open_ * (1.0 + 0.0001 + math.sin(index / 5.0) * 0.00035)
        high = max(open_, close) * 1.001
        low = min(open_, close) * 0.999
        rows.append(
            {
                "timestamp": iso(dt),
                "symbol": symbol,
                "open": round(open_, 6),
                "high": round(high, 6),
                "low": round(low, 6),
                "close": round(close, 6),
                "volume": 10000,
                "scenario": scenario,
            }
        )
        dt += step
    return rows


def make_partial_volume_bars(
    *,
    start: datetime,
    count: int,
    step: timedelta,
    symbol: str,
    start_price: float,
    scenario: str,
    volume: int,
) -> list[dict]:
    rows: list[dict] = []
    dt = start
    close = start_price
    for index in range(count):
        open_ = close
        close = open_ * (1.0 + math.sin(index / 4.0) * 0.0002)
        high = max(open_, close) * 1.0008
        low = min(open_, close) * 0.9992
        rows.append(
            {
                "timestamp": iso(dt),
                "symbol": symbol,
                "open": round(open_, 6),
                "high": round(high, 6),
                "low": round(low, 6),
                "close": round(close, 6),
                "volume": volume,
                "scenario": scenario,
            }
        )
        dt += step
    return rows


def make_bad_data_bars(
    *,
    start: datetime,
    symbol: str,
    start_price: float,
    scenario: str,
) -> list[dict]:
    rows = make_bars(
        start=start,
        count=40,
        step=timedelta(minutes=1),
        symbol=symbol,
        start_price=start_price,
        scenario=scenario,
        drift=0.00005,
        wave=0.00025,
    )

    duplicate = dict(rows[10])
    duplicate["close"] = round(float(duplicate["close"]) * 1.001, 6)
    rows.insert(11, duplicate)

    invalid = dict(rows[20])
    invalid["high"] = round(min(float(invalid["open"]), float(invalid["close"])) * 0.995, 6)
    invalid["low"] = round(max(float(invalid["open"]), float(invalid["close"])) * 1.005, 6)
    rows[20] = invalid
    return rows


def main() -> int:
    root = Path("data/experiments")
    start = datetime(2024, 1, 2, 14, 30, tzinfo=timezone.utc)

    write_rows(
        root / "trend_up_1m.csv",
        make_bars(
            start=start,
            count=240,
            step=timedelta(minutes=1),
            symbol="SIM",
            start_price=100.0,
            scenario="trend_up_1m",
            drift=0.00016,
            wave=0.00045,
        ),
    )
    write_rows(
        root / "chop_mean_revert_1m.csv",
        make_bars(
            start=start,
            count=240,
            step=timedelta(minutes=1),
            symbol="SIM",
            start_price=100.0,
            scenario="chop_mean_revert_1m",
            drift=0.0,
            wave=0.00105,
        ),
    )
    write_rows(
        root / "regime_shift_1m.csv",
        make_bars(
            start=start,
            count=240,
            step=timedelta(minutes=1),
            symbol="SIM",
            start_price=100.0,
            scenario="regime_shift_1m",
            drift=0.00009,
            wave=0.00055,
            shock_at=120,
            shock_size=-0.08,
        ),
    )
    write_rows(
        root / "liquidity_gap_1m.csv",
        make_bars(
            start=start,
            count=240,
            step=timedelta(minutes=1),
            symbol="SIM",
            start_price=100.0,
            scenario="liquidity_gap_1m",
            drift=0.00008,
            wave=0.0007,
            shock_at=90,
            shock_size=-0.05,
            zero_volume_every=37,
            skip_every=53,
        ),
    )
    write_rows(
        root / "trend_up_1h.csv",
        make_bars(
            start=start,
            count=160,
            step=timedelta(hours=1),
            symbol="SIM",
            start_price=100.0,
            scenario="trend_up_1h",
            drift=0.00055,
            wave=0.0011,
        ),
    )
    write_rows(
        root / "trend_up_30m.csv",
        make_bars(
            start=start,
            count=200,
            step=timedelta(minutes=30),
            symbol="SIM",
            start_price=100.0,
            scenario="trend_up_30m",
            drift=0.00038,
            wave=0.0009,
        ),
    )
    write_rows(
        root / "trend_up_4h.csv",
        make_bars(
            start=start,
            count=120,
            step=timedelta(hours=4),
            symbol="SIM",
            start_price=100.0,
            scenario="trend_up_4h",
            drift=0.0011,
            wave=0.0018,
        ),
    )
    write_rows(
        root / "gap_open_1m.csv",
        make_gap_open_bars(
            start=start,
            count=80,
            step=timedelta(minutes=1),
            symbol="SIM",
            start_price=100.0,
            scenario="gap_open_1m",
            gap_index=10,
            gap_size=-0.07,
        ),
    )
    write_rows(
        root / "partial_volume_1m.csv",
        make_partial_volume_bars(
            start=start,
            count=80,
            step=timedelta(minutes=1),
            symbol="SIM",
            start_price=100.0,
            scenario="partial_volume_1m",
            volume=25,
        ),
    )
    write_rows(
        root / "churn_noise_1m.csv",
        make_bars(
            start=start,
            count=180,
            step=timedelta(minutes=1),
            symbol="SIM",
            start_price=100.0,
            scenario="churn_noise_1m",
            drift=0.00002,
            wave=0.00135,
        ),
    )
    write_rows(
        root / "bad_data_1m.csv",
        make_bad_data_bars(
            start=start,
            symbol="SIM",
            start_price=100.0,
            scenario="bad_data_1m",
        ),
    )

    print(f"Wrote experiment fixtures under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
