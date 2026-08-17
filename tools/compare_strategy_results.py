#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


FINAL_NUMERIC_FIELDS = [
    "final_cash",
    "final_position",
    "final_price",
    "final_equity",
    "return_pct",
]
COUNT_FIELDS = ["fill_count", "signal_count"]
FILL_TEXT_FIELDS = ["timestamp", "symbol", "side", "source_signal_timestamp"]
FILL_NUMERIC_FIELDS = ["quantity", "price", "fee"]


def load_results(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def compare(results: list[dict], baseline_adapter: str, numeric_tolerance: float) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in results:
        grouped[row["run_id"]].append(row)

    comparisons: list[dict] = []
    for run_id, rows in sorted(grouped.items()):
        baseline = next((row for row in rows if row["adapter"] == baseline_adapter), None)
        if baseline is None:
            comparisons.append(
                {
                    "run_id": run_id,
                    "adapter": "",
                    "baseline_adapter": baseline_adapter,
                    "status": "missing_baseline",
                    "final_equity": "",
                    "baseline_equity": "",
                    "final_cash_diff": "",
                    "final_position_diff": "",
                    "final_price_diff": "",
                    "equity_diff": "",
                    "return_diff_pct": "",
                    "fill_count_diff": "",
                    "signal_count_diff": "",
                    "mismatches": "No baseline result for this run.",
                    "notes": "No baseline result for this run.",
                }
            )
            continue
        for row in rows:
            notes_text = " | ".join(row.get("notes", []))
            diffs = final_diffs(row, baseline)
            fill_count_diff = int(row.get("fill_count", 0)) - int(baseline.get("fill_count", 0))
            signal_count_diff = int(row.get("signal_count", 0)) - int(baseline.get("signal_count", 0))
            mismatches = result_mismatches(row, baseline, numeric_tolerance)
            policy_notes = policy_difference_notes(row)
            status = "match" if not mismatches else "diff"
            if row["adapter"] == baseline_adapter:
                status = "baseline"
            elif "unavailable" in notes_text.lower():
                status = "unavailable"
            elif policy_notes and not mismatches:
                status = "policy_diff"
            comparisons.append(
                {
                    "run_id": run_id,
                    "adapter": row["adapter"],
                    "baseline_adapter": baseline_adapter,
                    "status": status,
                    "final_equity": row["final_equity"],
                    "baseline_equity": baseline["final_equity"],
                    "final_cash_diff": diffs["final_cash"],
                    "final_position_diff": diffs["final_position"],
                    "final_price_diff": diffs["final_price"],
                    "equity_diff": diffs["final_equity"],
                    "return_diff_pct": diffs["return_pct"],
                    "fill_count_diff": fill_count_diff,
                    "signal_count_diff": signal_count_diff,
                    "mismatches": " | ".join(mismatches[:6]),
                    "notes": " | ".join(row.get("notes", [])[:3]),
                }
            )
    return comparisons


def final_diffs(row: dict, baseline: dict) -> dict[str, float]:
    return {
        field: float(row.get(field, 0.0)) - float(baseline.get(field, 0.0))
        for field in FINAL_NUMERIC_FIELDS
    }


def result_mismatches(row: dict, baseline: dict, numeric_tolerance: float) -> list[str]:
    mismatches: list[str] = []

    for field in FINAL_NUMERIC_FIELDS:
        if not close_enough(row.get(field), baseline.get(field), numeric_tolerance):
            mismatches.append(
                f"{field}: candidate={row.get(field)} baseline={baseline.get(field)}"
            )

    for field in COUNT_FIELDS:
        if int(row.get(field, 0)) != int(baseline.get(field, 0)):
            mismatches.append(
                f"{field}: candidate={row.get(field)} baseline={baseline.get(field)}"
            )

    baseline_fills = baseline.get("fills", [])
    candidate_fills = row.get("fills", [])
    if len(candidate_fills) != len(baseline_fills):
        mismatches.append(
            f"fills length: candidate={len(candidate_fills)} baseline={len(baseline_fills)}"
        )

    for index, (candidate, expected) in enumerate(zip(candidate_fills, baseline_fills)):
        for field in FILL_TEXT_FIELDS:
            if candidate.get(field) != expected.get(field):
                mismatches.append(
                    f"fill[{index}].{field}: candidate={candidate.get(field)} baseline={expected.get(field)}"
                )
        for field in FILL_NUMERIC_FIELDS:
            if not close_enough(candidate.get(field), expected.get(field), numeric_tolerance):
                mismatches.append(
                    f"fill[{index}].{field}: candidate={candidate.get(field)} baseline={expected.get(field)}"
                )

    return mismatches


def close_enough(candidate, baseline, tolerance: float) -> bool:
    try:
        return abs(float(candidate) - float(baseline)) <= tolerance
    except (TypeError, ValueError):
        return candidate == baseline


def policy_difference_notes(row: dict) -> list[str]:
    return [
        str(note)
        for note in row.get("notes", [])
        if "policy_difference" in str(note).lower()
    ]


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Strategy Matrix Comparison",
        "",
        "| Run | Adapter | Status | Cash diff | Position diff | Equity diff | Fills diff | Signals diff | Mismatches | Notes |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        cash_diff = row["final_cash_diff"]
        position_diff = row["final_position_diff"]
        equity_diff = row["equity_diff"]
        fill_diff = row["fill_count_diff"]
        signal_diff = row["signal_count_diff"]
        cash_text = "" if cash_diff == "" else f"{cash_diff:.6f}"
        position_text = "" if position_diff == "" else f"{position_diff:.6f}"
        equity_text = "" if equity_diff == "" else f"{equity_diff:.6f}"
        fill_text = "" if fill_diff == "" else str(fill_diff)
        signal_text = "" if signal_diff == "" else str(signal_diff)
        lines.append(
            f"| `{row['run_id']}` | `{row['adapter']}` | `{row['status']}` | "
            f"{cash_text} | {position_text} | {equity_text} | {fill_text} | "
            f"{signal_text} | {row['mismatches']} | {row['notes']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare strategy matrix results against a baseline adapter.")
    parser.add_argument("--results", type=Path, default=Path("reports/strategy_matrix_results.json"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    parser.add_argument("--baseline-adapter", default="reference_bar")
    parser.add_argument("--equity-tolerance", type=float, default=1e-6, help="Backward-compatible alias for numeric tolerance.")
    parser.add_argument("--numeric-tolerance", type=float, default=None)
    args = parser.parse_args()

    tolerance = args.numeric_tolerance if args.numeric_tolerance is not None else args.equity_tolerance
    rows = compare(load_results(args.results), args.baseline_adapter, tolerance)
    write_csv(rows, args.reports_dir / "strategy_matrix_comparison.csv")
    write_markdown(rows, args.reports_dir / "strategy_matrix_comparison.md")
    print(f"Wrote {args.reports_dir / 'strategy_matrix_comparison.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
