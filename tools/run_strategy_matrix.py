#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from benchmark_runner.adapters import ADAPTERS
from benchmark_runner.adapters.common import unavailable_result
from benchmark_runner.adapters.types import AdapterContext
from benchmark_runner.data import load_bars, validate_bars
from benchmark_runner.reporting import write_csv, write_json, write_markdown
from benchmark_runner.strategies import build_strategy


FATAL_DATA_NOTE_PREFIXES = (
    "duplicate timestamp",
    "out-of-order timestamp",
    "invalid OHLC range",
    "non-positive OHLC value",
    "negative volume",
)


def load_suite(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fatal_data_notes(notes: list[str]) -> list[str]:
    return [
        note
        for note in notes
        if note.startswith(FATAL_DATA_NOTE_PREFIXES)
    ]


def run_suite(suite: dict, adapter_names: list[str] | None = None):
    results = []
    adapters_config = suite.get("adapters", {})
    selected_adapters = adapter_names or list(adapters_config.keys())

    for run in suite.get("runs", []):
        dataset = Path(run["dataset"])
        symbol = run["symbol"]
        bars = load_bars(dataset, symbol=symbol)
        data_notes = validate_bars(bars)
        data_quality = str(run.get("data_quality", suite.get("data_quality", "reject"))).lower()
        if data_quality not in {"reject", "warn"}:
            raise ValueError(f"{run['id']}: data_quality must be 'reject' or 'warn'")
        fatal_notes = fatal_data_notes(data_notes)
        if fatal_notes and data_quality == "reject":
            raise ValueError(
                f"{run['id']}: rejected dirty bars before strategy generation: "
                + " | ".join(fatal_notes[:5])
            )

        strategy = build_strategy(
            name=run["strategy"],
            symbol=symbol,
            quantity=float(run["quantity"]),
            params=run.get("params", {}),
        )
        signals = strategy.generate(bars)

        for adapter_name in selected_adapters:
            adapter_type = ADAPTERS.get(adapter_name)
            if adapter_type is None:
                raise ValueError(f"Unknown or unimplemented adapter: {adapter_name}")
            adapter_config = adapters_config.get(adapter_name, {})
            context = AdapterContext(
                run_id=run["id"],
                strategy_name=run["strategy"],
                dataset=dataset,
                symbol=symbol,
                bars=bars,
                signals=signals,
                data_notes=data_notes,
            )
            try:
                adapter = adapter_type(**adapter_config)
                results.append(adapter.run(context))
            except Exception as exc:
                results.append(
                    unavailable_result(
                        context=context,
                        adapter_name=adapter_name,
                        initial_cash=float(adapter_config.get("initial_cash", 0.0)),
                        reason=f"adapter raised {type(exc).__name__}: {exc}",
                    )
                )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the shared strategy matrix through benchmark adapters.")
    parser.add_argument("--suite", type=Path, default=Path("benchmark/strategy_suite.json"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    parser.add_argument("--adapter", action="append", help="Adapter name. Repeatable. Defaults to suite adapters.")
    args = parser.parse_args()

    suite = load_suite(args.suite)
    results = run_suite(suite, adapter_names=args.adapter)

    args.reports_dir.mkdir(parents=True, exist_ok=True)
    write_json(results, args.reports_dir / "strategy_matrix_results.json")
    write_csv(results, args.reports_dir / "strategy_matrix_results.csv")
    write_markdown(results, args.reports_dir / "strategy_matrix_results.md")
    print(f"Wrote {args.reports_dir / 'strategy_matrix_results.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
