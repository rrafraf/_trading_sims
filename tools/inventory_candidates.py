#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import subprocess
from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
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
    ".idea",
    ".vscode",
}

TEXT_SUFFIXES = {
    ".md",
    ".rst",
    ".txt",
    ".py",
    ".cs",
    ".rs",
    ".toml",
    ".cfg",
    ".ini",
    ".json",
    ".yaml",
    ".yml",
}

LANG_EXTENSIONS = {
    ".py": "Python",
    ".cs": "C#",
    ".fs": "F#",
    ".rs": "Rust",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C/C++",
    ".h": "C/C++",
    ".hpp": "C++",
    ".java": "Java",
    ".go": "Go",
    ".js": "JavaScript",
    ".ts": "TypeScript",
}

FEATURES: dict[str, dict[str, Any]] = {
    "alpaca": {"weight": 4.0, "terms": ["alpaca"]},
    "paper_trading": {"weight": 2.0, "terms": ["paper trading", "paper_trade", "dry-run", "dry run", "sandbox"]},
    "live_trading": {"weight": 1.5, "terms": ["live trading", "livetrade", "live trade"]},
    "backtesting": {"weight": 1.0, "terms": ["backtest", "backtesting"]},
    "csv_data": {"weight": 1.0, "terms": ["csv", "dataframe", "pandas"]},
    "bar_data": {"weight": 1.0, "terms": ["ohlcv", "bar data", "bars", "candles", "k-line", "kline"]},
    "tick_data": {"weight": 2.0, "terms": ["tick data", "trade tick", "quote tick", "tick-by-tick"]},
    "order_book": {"weight": 4.0, "terms": ["order book", "orderbook", "level-2", "level 2", "l2", "level-3", "level 3", "l3", "market depth"]},
    "matching_engine": {"weight": 4.0, "terms": ["matching engine", "price/time priority", "price-time priority", "exchange agent"]},
    "latency": {"weight": 3.0, "terms": ["latency", "latencies", "delayed", "network delay"]},
    "queue_position": {"weight": 3.0, "terms": ["queue position", "match queue", "order queue"]},
    "partial_fills": {"weight": 3.0, "terms": ["partial fill", "partialfill", "partially filled"]},
    "market_orders": {"weight": 1.0, "terms": ["market order", "market orders"]},
    "limit_orders": {"weight": 1.5, "terms": ["limit order", "limit orders"]},
    "stop_orders": {"weight": 1.5, "terms": ["stop order", "stop orders", "stop-limit", "stop limit"]},
    "time_in_force": {"weight": 2.0, "terms": ["time in force", "time-in-force", "gtc", "ioc", "fok", "post-only"]},
    "slippage": {"weight": 2.0, "terms": ["slippage"]},
    "fees": {"weight": 1.5, "terms": ["fee", "fees", "commission", "commissions", "transaction cost"]},
    "margin_short": {"weight": 1.5, "terms": ["margin", "short", "borrow", "lending"]},
    "calendar": {"weight": 1.0, "terms": ["calendar", "session", "trading hours", "market hours"]},
    "multi_asset": {"weight": 1.5, "terms": ["multi-asset", "multi asset", "multiple assets", "multi symbol", "portfolio"]},
    "multi_venue": {"weight": 2.0, "terms": ["multi-venue", "multi venue", "multiple venues", "routing", "router"]},
    "rl_agent": {"weight": 2.0, "terms": ["reinforcement learning", "gym", "gymnasium", "agent", "rllib", "stable-baselines"]},
    "fix": {"weight": 2.0, "terms": ["fix", "itch", "ouch"]},
}


def run_git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception:
        return ""
    return result.stdout.strip()


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                rel = path.relative_to(root)
            except ValueError:
                rel = path
            yield path, rel


def read_search_text(root: Path, max_bytes: int = 8_000_000) -> str:
    chunks: list[str] = []
    used = 0
    for path, _rel in iter_files(root):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > 600_000 or used + size > max_bytes:
            continue
        try:
            chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
            used += size
        except OSError:
            continue
    return "\n".join(chunks).lower()


def count_tests(root: Path) -> tuple[int, int]:
    test_dirs: set[str] = set()
    test_files = 0
    for path, rel in iter_files(root):
        lowered_parts = [part.lower() for part in rel.parts]
        filename = rel.name.lower()
        in_test_dir = any(part in {"test", "tests"} for part in lowered_parts)
        looks_like_test = (
            filename.startswith("test_")
            or filename.endswith("_test.py")
            or filename.endswith("tests.cs")
            or filename.endswith("test.cs")
            or filename.endswith("_test.rs")
        )
        if in_test_dir:
            idx = next(i for i, part in enumerate(lowered_parts) if part in {"test", "tests"})
            test_dirs.add(str(Path(*rel.parts[: idx + 1])))
        if in_test_dir and path.is_file() and (looks_like_test or path.suffix.lower() in {".py", ".cs", ".rs"}):
            test_files += 1
    return len(test_dirs), test_files


def language_summary(root: Path) -> str:
    counts: dict[str, int] = {}
    for path, _rel in iter_files(root):
        lang = LANG_EXTENSIONS.get(path.suffix.lower())
        if lang:
            counts[lang] = counts.get(lang, 0) + 1
    if not counts:
        return ""
    return ", ".join(f"{name}:{count}" for name, count in sorted(counts.items(), key=lambda item: item[1], reverse=True)[:3])


def package_markers(root: Path) -> list[str]:
    markers = []
    for name in [
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "requirements.txt",
        "environment.yml",
        "package.json",
        "Cargo.toml",
        "CMakeLists.txt",
        "Makefile",
    ]:
        if (root / name).exists():
            markers.append(name)
    if any(root.glob("*.sln")):
        markers.append("*.sln")
    if (root / "Dockerfile").exists():
        markers.append("Dockerfile")
    return markers


def license_name(root: Path) -> str:
    for path, rel in iter_files(root):
        lower = rel.name.lower()
        if lower.startswith("license") or lower in {"copying", "copyright"}:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")[:400].lower()
            except OSError:
                return rel.name
            if "apache license" in text:
                return "Apache"
            if "mit license" in text or "permission is hereby granted" in text:
                return "MIT"
            if "gnu lesser general public license" in text or "lgpl" in text:
                return "LGPL"
            if "gnu general public license" in text or "gpl" in text:
                return "GPL"
            return rel.name
    return ""


def detect_features(text: str) -> dict[str, bool]:
    detected = {}
    for name, info in FEATURES.items():
        detected[name] = any(term in text for term in info["terms"])
    return detected


def suggested_test_commands(root: Path, test_files: int) -> list[str]:
    commands: list[str] = []
    sln_files = list(root.glob("*.sln"))
    if sln_files:
        commands.append(f"dotnet test {sln_files[0].name}")
    if (root / "Cargo.toml").exists():
        commands.append("cargo test")
    if (root / "CMakeLists.txt").exists():
        commands.append("cmake -S . -B build/tests -DCMAKE_BUILD_TYPE=Debug && ctest --test-dir build/tests --output-on-failure")
    if test_files and ((root / "pyproject.toml").exists() or (root / "setup.py").exists() or (root / "setup.cfg").exists()):
        commands.append("python -m pytest tests")
    if (root / "package.json").exists():
        commands.append("npm test")
    if not commands and test_files:
        commands.append("inspect test docs manually")
    return commands


def data_fit(features: dict[str, bool]) -> str:
    if features["order_book"] or features["matching_engine"] or features["queue_position"]:
        return "tick/L2/L3 or generated order flow"
    if features["tick_data"]:
        return "trades/quotes/ticks"
    if features["bar_data"] or features["csv_data"]:
        return "Alpaca bars via CSV/DataFrame"
    return "unknown/custom"


def paper_fit(features: dict[str, bool]) -> str:
    if features["alpaca"] and features["paper_trading"]:
        return "direct Alpaca/paper references"
    if features["paper_trading"]:
        return "paper/sandbox support"
    if features["live_trading"]:
        return "live path, paper unclear"
    return "backtest/local only or unknown"


def score(features: dict[str, bool], test_files: int) -> dict[str, float]:
    depth = sum(FEATURES[name]["weight"] for name, present in features.items() if present)
    test_depth = min(20.0, math.sqrt(test_files) * 2.5)
    micro = sum(
        FEATURES[name]["weight"]
        for name in ["order_book", "matching_engine", "latency", "queue_position", "partial_fills", "time_in_force", "fix"]
        if features[name]
    )
    agent = sum(FEATURES[name]["weight"] for name in ["rl_agent", "multi_asset", "multi_venue", "alpaca"] if features[name])
    total = round(depth + test_depth, 2)
    return {
        "feature_score": round(depth, 2),
        "native_test_score": round(test_depth, 2),
        "microstructure_score": round(micro, 2),
        "agent_data_score": round(agent, 2),
        "hardness_score": total,
    }


def collect_candidate(root: Path) -> dict[str, Any]:
    text = read_search_text(root)
    features = detect_features(text)
    test_dir_count, test_file_count = count_tests(root)
    scores = score(features, test_file_count)
    record: dict[str, Any] = {
        "name": root.name,
        "path": str(root),
        "remote": run_git(root, "remote", "get-url", "origin"),
        "commit": run_git(root, "rev-parse", "--short", "HEAD"),
        "license": license_name(root),
        "languages": language_summary(root),
        "package_markers": ", ".join(package_markers(root)),
        "test_dirs": test_dir_count,
        "test_files": test_file_count,
        "data_fit": data_fit(features),
        "paper_fit": paper_fit(features),
        "suggested_test_commands": suggested_test_commands(root, test_file_count),
        **scores,
    }
    for name, present in features.items():
        record[f"has_{name}"] = present
    return record


def collect_all(candidates_dir: Path) -> list[dict[str, Any]]:
    records = []
    for child in sorted(candidates_dir.iterdir(), key=lambda p: p.name.lower()):
        if child.is_dir():
            records.append(collect_candidate(child))
    return sorted(records, key=lambda row: row["hardness_score"], reverse=True)


def write_json(records: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, indent=2), encoding="utf-8")


def write_csv(records: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        return
    fieldnames = list(records[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in records:
            clean = dict(row)
            clean["suggested_test_commands"] = " | ".join(clean["suggested_test_commands"])
            writer.writerow(clean)


def write_markdown(records: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Candidate Inventory",
        "",
        "Scores are static first-pass signals. They should decide what to run deeply, not settle the final ranking.",
        "",
        "| Rank | Candidate | Score | Micro | Tests | Data fit | Paper/live fit | Commands |",
        "| ---: | --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for idx, row in enumerate(records, start=1):
        commands = "<br>".join(f"`{cmd}`" for cmd in row["suggested_test_commands"]) or ""
        lines.append(
            "| {rank} | [{name}](../candidates/{name}) | {score} | {micro} | {tests} | {data} | {paper} | {commands} |".format(
                rank=idx,
                name=row["name"],
                score=row["hardness_score"],
                micro=row["microstructure_score"],
                tests=row["test_files"],
                data=row["data_fit"],
                paper=row["paper_fit"],
                commands=commands,
            )
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory cloned trading simulator candidates.")
    parser.add_argument("--candidates-dir", default="candidates", type=Path)
    parser.add_argument("--reports-dir", default="reports", type=Path)
    args = parser.parse_args()

    records = collect_all(args.candidates_dir)
    write_json(records, args.reports_dir / "candidates_inventory.json")
    write_csv(records, args.reports_dir / "candidates_inventory.csv")
    write_markdown(records, args.reports_dir / "candidates_inventory.md")

    print(f"Inventoried {len(records)} candidates")
    print(f"Wrote {args.reports_dir / 'candidates_inventory.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

