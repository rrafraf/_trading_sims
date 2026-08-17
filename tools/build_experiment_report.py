#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import html
import json
from collections import defaultdict
from pathlib import Path


def load_json(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize_comparison(rows: list[dict]) -> dict[str, dict]:
    summary: dict[str, dict] = defaultdict(lambda: {"baseline": 0, "match": 0, "diff": 0, "unavailable": 0})
    for row in rows:
        adapter = row["adapter"]
        status = row["status"]
        summary[adapter][status] = summary[adapter].get(status, 0) + 1
    return dict(summary)


def group_results(results: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in results:
        grouped[row["run_id"]].append(row)
    return dict(grouped)


def adapter_names(results: list[dict]) -> list[str]:
    names = sorted({row["adapter"] for row in results})
    if "reference_bar" in names:
        names.remove("reference_bar")
        return ["reference_bar", *names]
    return names


def write_markdown(results: list[dict], comparisons: list[dict], path: Path) -> None:
    summary = summarize_comparison(comparisons)
    grouped = group_results(results)
    adapters = adapter_names(results)
    adapter_text = ", ".join(f"`{adapter}`" for adapter in adapters)
    lines = [
        "# Experiment Summary",
        "",
        f"This batch uses these adapters: {adapter_text}.",
        "",
        "## Adapter Agreement",
        "",
        "| Adapter | Baseline | Match | Policy diff | Diff | Unavailable |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for adapter, row in sorted(summary.items()):
        lines.append(
            f"| `{adapter}` | {row.get('baseline', 0)} | {row.get('match', 0)} | "
            f"{row.get('policy_diff', 0)} | "
            f"{row.get('diff', 0)} | {row.get('unavailable', 0)} |"
        )

    lines.extend(
        [
            "",
            "## Runs",
            "",
            "| Run | " + " | ".join(f"{adapter} return %" for adapter in adapters) + " |",
            "| --- | " + " | ".join("---:" for _adapter in adapters) + " |",
        ]
    )
    for run_id, rows in sorted(grouped.items()):
        by_adapter = {row["adapter"]: row for row in rows}
        lines.append(
            f"| `{run_id}` | "
            + " | ".join(_return_text(by_adapter.get(adapter)) for adapter in adapters)
            + " |"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_html(results: list[dict], comparisons: list[dict], path: Path) -> None:
    summary = summarize_comparison(comparisons)
    grouped = group_results(results)
    adapters = adapter_names(results)

    max_abs_return = max(abs(float(row["return_pct"])) for row in results) if results else 1.0
    max_abs_return = max(max_abs_return, 0.01)

    summary_rows = []
    for adapter in adapters:
        row = summary.get(adapter, {})
        summary_rows.append(
            "<tr>"
            f"<td><code>{html.escape(adapter)}</code></td>"
            f"<td>{row.get('baseline', 0)}</td>"
            f"<td>{row.get('match', 0)}</td>"
            f"<td>{row.get('policy_diff', 0)}</td>"
            f"<td>{row.get('diff', 0)}</td>"
            f"<td>{row.get('unavailable', 0)}</td>"
            "</tr>"
        )

    run_cards = []
    for run_id, rows in sorted(grouped.items()):
        by_adapter = {row["adapter"]: row for row in rows}
        bars = []
        for adapter in adapters:
            row = by_adapter.get(adapter)
            if not row:
                continue
            ret = float(row["return_pct"])
            width = max(2.0, abs(ret) / max_abs_return * 100.0)
            css_class = "positive" if ret >= 0 else "negative"
            bars.append(
                "<div class=\"bar-row\">"
                f"<span class=\"adapter\"><code>{html.escape(adapter)}</code></span>"
                "<div class=\"bar-track\">"
                f"<div class=\"bar {css_class}\" style=\"width:{width:.2f}%\"></div>"
                "</div>"
                f"<span class=\"ret\">{ret:.4f}%</span>"
                "</div>"
            )
        notes = []
        for row in rows:
            for note in row.get("notes", [])[:2]:
                if note and note not in notes:
                    notes.append(note)
        notes_html = "".join(f"<li>{html.escape(note)}</li>" for note in notes[:4])
        run_cards.append(
            "<section class=\"card\">"
            f"<h3>{html.escape(run_id)}</h3>"
            f"{''.join(bars)}"
            f"<ul>{notes_html}</ul>"
            "</section>"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Experiment Report</title>
  <style>
    :root {{
      --bg: #f4f6f7;
      --panel: #ffffff;
      --text: #182026;
      --muted: #5f6b75;
      --line: #d8dee3;
      --accent: #0f766e;
      --pos: #15803d;
      --neg: #b42318;
      --track: #e7ecef;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Arial, Helvetica, sans-serif;
    }}
    header {{
      padding: 24px 28px;
      background: var(--panel);
      border-bottom: 1px solid var(--line);
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 24px;
    }}
    h1, h2, h3 {{ margin: 0; letter-spacing: 0; }}
    h1 {{ font-size: 26px; }}
    h2 {{ font-size: 19px; margin-bottom: 12px; }}
    h3 {{ font-size: 16px; margin-bottom: 12px; }}
    p {{ margin: 8px 0 0; color: var(--muted); line-height: 1.45; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
      margin-top: 18px;
    }}
    .panel, .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      text-align: left;
      padding: 9px 10px;
      border-bottom: 1px solid var(--line);
    }}
    th {{ background: #eef3f2; }}
    code {{
      background: #edf2f4;
      padding: 2px 5px;
      border-radius: 4px;
      font-size: 13px;
    }}
    .bar-row {{
      display: grid;
      grid-template-columns: 116px 1fr 82px;
      gap: 10px;
      align-items: center;
      margin: 8px 0;
    }}
    .adapter {{ color: var(--muted); }}
    .bar-track {{
      height: 12px;
      background: var(--track);
      border-radius: 999px;
      overflow: hidden;
    }}
    .bar {{
      height: 100%;
      min-width: 2px;
      border-radius: 999px;
    }}
    .positive {{ background: var(--pos); }}
    .negative {{ background: var(--neg); }}
    .ret {{
      text-align: right;
      font-variant-numeric: tabular-nums;
      color: var(--muted);
    }}
    ul {{
      margin: 12px 0 0;
      padding-left: 18px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <header>
    <h1>Experiment Report</h1>
    <p>Working adapter comparison across deterministic 1-minute and longer synthetic datasets.</p>
  </header>
  <main>
    <section class="panel">
      <h2>Adapter Agreement</h2>
      <table>
        <thead>
          <tr>
            <th>Adapter</th>
            <th>Baseline</th>
            <th>Match</th>
            <th>Policy diff</th>
            <th>Diff</th>
            <th>Unavailable</th>
          </tr>
        </thead>
        <tbody>
          {''.join(summary_rows)}
        </tbody>
      </table>
      <p>Matching here means the adapter agrees with <code>reference_bar</code> on cash, position, equity, signal count, and fill details under the configured policy.</p>
    </section>
    <section class="grid">
      {''.join(run_cards)}
    </section>
    <p><a href="strategy_matrix_results.md">Raw matrix results</a> · <a href="strategy_matrix_comparison.md">Raw comparison</a></p>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )


def _return_text(row: dict | None) -> str:
    if not row:
        return ""
    return f"{float(row['return_pct']):.4f}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build human-readable experiment summaries.")
    parser.add_argument("--reports-dir", type=Path, default=Path("reports/experiments"))
    args = parser.parse_args()

    results = load_json(args.reports_dir / "strategy_matrix_results.json")
    comparisons = load_csv(args.reports_dir / "strategy_matrix_comparison.csv")
    write_markdown(results, comparisons, args.reports_dir / "summary.md")
    write_html(results, comparisons, args.reports_dir / "index.html")
    print(f"Wrote {args.reports_dir / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
