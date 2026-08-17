#!/usr/bin/env python
from __future__ import annotations

import argparse
import os
import re
from datetime import datetime, timezone
from pathlib import Path


def parse_datetime(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def load_alpaca_modules():
    try:
        from alpaca.data.enums import DataFeed
        from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
        from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest
        from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
    except ImportError as exc:
        raise SystemExit(
            "Missing alpaca-py. Install dependencies with: python -m pip install -r requirements.txt"
        ) from exc
    return {
        "DataFeed": DataFeed,
        "CryptoHistoricalDataClient": CryptoHistoricalDataClient,
        "StockHistoricalDataClient": StockHistoricalDataClient,
        "CryptoBarsRequest": CryptoBarsRequest,
        "StockBarsRequest": StockBarsRequest,
        "TimeFrame": TimeFrame,
        "TimeFrameUnit": TimeFrameUnit,
    }


def parse_timeframe(value: str, TimeFrame, TimeFrameUnit):
    normalized = value.strip().lower()
    aliases = {
        "1day": TimeFrame.Day,
        "day": TimeFrame.Day,
        "1d": TimeFrame.Day,
        "1hour": TimeFrame.Hour,
        "hour": TimeFrame.Hour,
        "1h": TimeFrame.Hour,
        "1min": TimeFrame.Minute,
        "1minute": TimeFrame.Minute,
        "minute": TimeFrame.Minute,
        "1m": TimeFrame.Minute,
    }
    if normalized in aliases:
        return aliases[normalized]

    match = re.fullmatch(r"(\d+)\s*(min|m|minute|minutes|h|hour|hours|d|day|days)", normalized)
    if not match:
        raise SystemExit(f"Unsupported timeframe: {value}")
    amount = int(match.group(1))
    unit_text = match.group(2)
    if unit_text in {"min", "m", "minute", "minutes"}:
        return TimeFrame(amount, TimeFrameUnit.Minute)
    if unit_text in {"h", "hour", "hours"}:
        return TimeFrame(amount, TimeFrameUnit.Hour)
    if unit_text in {"d", "day", "days"}:
        return TimeFrame(amount, TimeFrameUnit.Day)
    raise SystemExit(f"Unsupported timeframe: {value}")


def dataframe_to_canonical_csv(df, output_path: Path) -> None:
    if df.empty:
        raise SystemExit("Alpaca returned no bars for this request.")

    frame = df.reset_index()
    rename = {
        "timestamp": "timestamp",
        "symbol": "symbol",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
        "trade_count": "trade_count",
        "vwap": "vwap",
    }
    frame = frame.rename(columns={key: value for key, value in rename.items() if key in frame.columns})
    ordered = [col for col in ["timestamp", "symbol", "open", "high", "low", "close", "volume", "trade_count", "vwap"] if col in frame.columns]
    extras = [col for col in frame.columns if col not in ordered]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame[ordered + extras].to_csv(output_path, index=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Alpaca bars into a canonical CSV.")
    parser.add_argument("--asset", choices=["stock", "crypto"], default="stock")
    parser.add_argument("--symbols", nargs="+", required=True)
    parser.add_argument("--timeframe", default="1Day")
    parser.add_argument("--start", required=True, help="ISO date/datetime, UTC assumed if timezone omitted")
    parser.add_argument("--end", required=True, help="ISO date/datetime, UTC assumed if timezone omitted")
    parser.add_argument("--feed", choices=["iex", "sip"], default="iex", help="Stock feed. Free/default accounts generally use iex.")
    parser.add_argument("--output-dir", type=Path, default=Path("data/alpaca"))
    parser.add_argument("--output-name", default="")
    args = parser.parse_args()

    mods = load_alpaca_modules()
    timeframe = parse_timeframe(args.timeframe, mods["TimeFrame"], mods["TimeFrameUnit"])
    start = parse_datetime(args.start)
    end = parse_datetime(args.end)

    api_key = os.environ.get("ALPACA_API_KEY") or os.environ.get("APCA_API_KEY_ID")
    api_secret = os.environ.get("ALPACA_SECRET_KEY") or os.environ.get("APCA_API_SECRET_KEY")

    if args.asset == "stock":
        if not api_key or not api_secret:
            raise SystemExit("Stock data requires ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables.")
        client = mods["StockHistoricalDataClient"](api_key, api_secret)
        feed = getattr(mods["DataFeed"], args.feed.upper())
        request = mods["StockBarsRequest"](
            symbol_or_symbols=args.symbols,
            timeframe=timeframe,
            start=start,
            end=end,
            feed=feed,
        )
        bars = client.get_stock_bars(request)
    else:
        client_kwargs = {}
        if api_key and api_secret:
            client_kwargs = {"api_key": api_key, "secret_key": api_secret}
        client = mods["CryptoHistoricalDataClient"](**client_kwargs)
        request = mods["CryptoBarsRequest"](
            symbol_or_symbols=args.symbols,
            timeframe=timeframe,
            start=start,
            end=end,
        )
        bars = client.get_crypto_bars(request)

    safe_symbols = "-".join(symbol.replace("/", "") for symbol in args.symbols)
    output_name = args.output_name or f"{args.asset}_{safe_symbols}_{args.timeframe}_{args.start}_{args.end}.csv"
    output_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", output_name)
    output_path = args.output_dir / output_name
    dataframe_to_canonical_csv(bars.df, output_path)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

