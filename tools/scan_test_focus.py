#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path


SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "target",
}

TEST_SUFFIXES = {".py", ".cs", ".rs", ".cpp", ".cc", ".c", ".h", ".hpp", ".md", ".rst"}

TOPICS = {
    "order_lifecycle": ["order", "submitted", "accepted", "cancel", "rejected", "expired", "modify", "replace"],
    "fills": ["fill", "filled", "partial", "execution", "executed", "matched", "matching"],
    "limit_market_stop": ["limit", "market order", "stop", "stop-limit", "stop_limit"],
    "time_in_force": ["time in force", "time-in-force", "gtc", "ioc", "fok", "day order", "post-only"],
    "slippage_impact": ["slippage", "impact", "volume share", "liquidity", "spread"],
    "fees_costs": ["fee", "fees", "commission", "cost", "rebate"],
    "latency_time": ["latency", "delay", "clock", "timestamp", "nanosecond", "event time", "simulated time"],
    "queue_orderbook": ["queue", "order book", "orderbook", "depth", "level 2", "level-2", "l2", "level 3", "level-3", "l3"],
    "broker_rules": ["buying power", "margin", "cash", "settlement", "short", "borrow", "leverage"],
    "calendar_sessions": ["calendar", "session", "holiday", "trading hours", "market open", "market close"],
    "data_quality": ["missing", "nan", "duplicate", "out of order", "gap", "resample", "split", "dividend"],
    "agent_rl": ["agent", "reward", "gym", "environment", "observation", "action"],
}


def iter_test_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        current = Path(dirpath)
        rel_parts = [part.lower() for part in current.relative_to(root).parts] if current != root else []
        in_test_dir = any(part in {"test", "tests"} for part in rel_parts)
        for filename in filenames:
            path = current / filename
            lower_name = filename.lower()
            if path.suffix.lower() not in TEST_SUFFIXES:
                continue
            looks_like_test = (
                in_test_dir
                or lower_name.startswith("test_")
                or lower_name.endswith("_test.py")
                or lower_name.endswith("tests.cs")
                or lower_name.endswith("test.cs")
                or lower_name.endswith("_test.rs")
            )
            if looks_like_test:
                yield path


def scan_candidate(root: Path) -> dict:
    topic_files = {topic: set() for topic in TOPICS}
    test_files = list(iter_test_files(root))
    for path in test_files:
        try:
            if path.stat().st_size > 800_000:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        for topic, terms in TOPICS.items():
            if any(term in text for term in terms):
                topic_files[topic].add(str(path.relative_to(root)))

    row = {
        "name": root.name,
        "test_files": len(test_files),
        "focused_topic_count": sum(1 for files in topic_files.values() if files),
    }
    for topic, files in topic_files.items():
        row[topic] = len(files)
    row["sample_files"] = {
        topic: sorted(files)[:8]
        for topic, files in topic_files.items()
        if files
    }
    row["test_focus_score"] = row["focused_topic_count"] * 3 + sum(min(count, 10) for topic, count in row.items() if topic in TOPICS)
    return row


def write_markdown(rows: list[dict], path: Path) -> None:
    lines = [
        "# Native Test Focus",
        "",
        "This report scans test files for terms associated with execution edge cases. It is a triage signal, not proof of correctness.",
        "",
        "| Rank | Candidate | Score | Test files | Topics | Fill/order | Book/queue | Latency/time | Data quality | Fees/costs |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for index, row in enumerate(rows, start=1):
        lines.append(
            f"| {index} | [{row['name']}](../candidates/{row['name']}) | {row['test_focus_score']} | {row['test_files']} | "
            f"{row['focused_topic_count']} | {row['fills'] + row['order_lifecycle'] + row['limit_market_stop']} | "
            f"{row['queue_orderbook']} | {row['latency_time']} | {row['data_quality']} | {row['fees_costs']} |"
        )

    lines.append("")
    lines.append("## Sample Matching Test Files")
    lines.append("")
    for row in rows:
        lines.append(f"### {row['name']}")
        samples = row["sample_files"]
        if not samples:
            lines.append("")
            lines.append("No matching test files found.")
            lines.append("")
            continue
        for topic in ["fills", "order_lifecycle", "queue_orderbook", "latency_time", "slippage_impact", "fees_costs", "data_quality", "agent_rl"]:
            files = samples.get(topic)
            if files:
                joined = ", ".join(f"`{file}`" for file in files[:5])
                lines.append(f"- `{topic}`: {joined}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan native tests for hard simulation topics.")
    parser.add_argument("--candidates-dir", default="candidates", type=Path)
    parser.add_argument("--reports-dir", default="reports", type=Path)
    args = parser.parse_args()

    rows = [scan_candidate(path) for path in sorted(args.candidates_dir.iterdir(), key=lambda p: p.name.lower()) if path.is_dir()]
    rows.sort(key=lambda row: row["test_focus_score"], reverse=True)

    args.reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.reports_dir / "native_test_focus.json"
    csv_path = args.reports_dir / "native_test_focus.csv"
    md_path = args.reports_dir / "native_test_focus.md"

    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [key for key in rows[0].keys() if key != "sample_files"] if rows else []
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: value for key, value in row.items() if key != "sample_files"})
    write_markdown(rows, md_path)

    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

