from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from .models import Fill, RunResult


def fill_to_dict(fill: Fill) -> dict:
    row = asdict(fill)
    row["timestamp"] = fill.timestamp.isoformat()
    row["source_signal_timestamp"] = fill.source_signal_timestamp.isoformat()
    return row


def result_to_dict(result: RunResult, include_fills: bool = True) -> dict:
    row = asdict(result)
    if include_fills:
        row["fills"] = [fill_to_dict(fill) for fill in result.fills]
    else:
        row.pop("fills", None)
    return row


def write_json(results: list[RunResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [result_to_dict(result) for result in results]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_csv(results: list[RunResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "run_id",
        "adapter",
        "strategy",
        "dataset",
        "symbol",
        "initial_cash",
        "final_cash",
        "final_position",
        "final_price",
        "final_equity",
        "return_pct",
        "fill_count",
        "signal_count",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            row = result_to_dict(result, include_fills=False)
            row["notes"] = " | ".join(result.notes)
            writer.writerow(row)


def write_markdown(results: list[RunResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Strategy Matrix Results",
        "",
        "| Run | Adapter | Strategy | Symbol | Final equity | Return % | Fills | Signals | Notes |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for result in results:
        notes = "<br>".join(result.notes[:4])
        if len(result.notes) > 4:
            notes += f"<br>... {len(result.notes) - 4} more"
        lines.append(
            f"| `{result.run_id}` | `{result.adapter}` | `{result.strategy}` | `{result.symbol}` | "
            f"{result.final_equity:.2f} | {result.return_pct:.4f} | {result.fill_count} | "
            f"{result.signal_count} | {notes} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

