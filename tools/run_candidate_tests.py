#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import inventory_candidates


def run_command(command: str, cwd: Path, timeout: int) -> dict:
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return {
        "command": command,
        "cwd": str(cwd),
        "started_at": started,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-8000:],
        "stderr_tail": result.stderr[-8000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan or run native candidate test suites.")
    parser.add_argument("--candidates-dir", default="candidates", type=Path)
    parser.add_argument("--reports-dir", default="reports", type=Path)
    parser.add_argument("--candidate", action="append", help="Candidate name to include. Repeatable.")
    parser.add_argument("--execute", action="store_true", help="Actually execute detected test commands.")
    parser.add_argument("--dry-run", action="store_true", help="Only write the test plan. This is the default.")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    args = parser.parse_args()

    records = inventory_candidates.collect_all(args.candidates_dir)
    if args.candidate:
        wanted = {name.lower() for name in args.candidate}
        records = [record for record in records if record["name"].lower() in wanted]

    args.reports_dir.mkdir(parents=True, exist_ok=True)
    plan_path = args.reports_dir / "native_test_plan.md"
    result_path = args.reports_dir / "native_test_results.json"

    lines = [
        "# Native Test Plan",
        "",
        "Default mode only plans commands. Use `--execute` after installing each repo's dependencies.",
        "",
        "| Candidate | Test files | Commands |",
        "| --- | ---: | --- |",
    ]
    for record in records:
        commands = "<br>".join(f"`{cmd}`" for cmd in record["suggested_test_commands"]) or ""
        lines.append(f"| [{record['name']}](../candidates/{record['name']}) | {record['test_files']} | {commands} |")
    plan_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if not args.execute:
        print(f"Wrote {plan_path}")
        return 0

    results = []
    for record in records:
        cwd = Path(record["path"])
        for command in record["suggested_test_commands"]:
            if command == "inspect test docs manually":
                continue
            print(f"RUN {record['name']}: {command}")
            try:
                result = run_command(command, cwd, args.timeout_seconds)
            except subprocess.TimeoutExpired as exc:
                result = {
                    "command": command,
                    "cwd": str(cwd),
                    "returncode": "timeout",
                    "stdout_tail": (exc.stdout or "")[-8000:] if isinstance(exc.stdout, str) else "",
                    "stderr_tail": (exc.stderr or "")[-8000:] if isinstance(exc.stderr, str) else "",
                }
            result["candidate"] = record["name"]
            results.append(result)
            if result["returncode"] not in (0, "timeout"):
                print(f"FAIL {record['name']}: {command}", file=sys.stderr)

    result_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

