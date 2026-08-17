# Project Status

Last updated: 2026-08-16

> **FROZEN FOR MIGRATION.** Read
> `reports/human/TEAM_FREEZE_2026-08-16.md` first. It contains the team map,
> consensus, restart prompts, current proof boundaries, and preservation risks.
> This status file is partly stale: the slower-timeframe ladder is recorded as
> complete in `reports/human/backlog.html`.

This is the central restart note for `_trading_sims`.

## Short Version

The simulator bench works.

`muni` is now connected as one of the engines under test. The current saved
reports say `muni` and `reference_bar` match on the normal and hardening suites
using the stricter comparator.

The next big work should not be "add more clever strategies" yet. The next work
should either make results easier to see, or run slower timeframes like 30m, 1h,
and 4h.

## What Works

- Candidate simulator repos are downloaded under `candidates/`.
- Working adapters:
  - `reference_bar`
  - `backtrader`
  - `vectorbt`
  - `pybroker`
  - `muni`
- `muni` is connected by a file/CLI bridge, not by merging repos.
- The comparator now checks more than final equity:
  - final cash
  - final position
  - final price
  - final equity
  - return
  - signal count
  - fill count
  - fill timestamp
  - fill side
  - fill quantity
  - fill price
  - fill fee
  - source signal timestamp
- Dirty market data is rejected by default before strategy generation.
- A dirty-data test can still be allowed on purpose with `data_quality: warn`.
- The truth-gate tests pass:

```powershell
.venv\Scripts\python.exe -m pytest tests -q
```

Latest result seen: `4 passed`.

## Can Rafa Play With The Simulators?

Yes, with one important warning.

Good for playing now:

- `backtrader`: practical bar strategy experiments.
- `vectorbt`: fast sweeps and parameter grids.
- `pybroker`: Alpaca-style and ML/walk-forward direction.
- `muni`: in-house engine comparison against the same benchmark rules.

Do not treat green results as trading proof. They only prove that the engines
agree under the current bar-level rules.

Not ready as "truth":

- broker-specific fills
- stop orders
- limit orders
- same-candle stop-vs-target cases
- latency
- queue position
- market impact
- LEAN parity

## What The "Judge" Means

The judge is `tools/compare_strategy_results.py`.

Before OG's review, it could say `match` when two runs had the same final money
and same number of fills, even if the actual fills were different.

Now it compares the actual final state and every normalized fill. That makes
the reports much harder to fool.

## What The Strict Data Gate Means

The strict data gate is in `tools/run_strategy_matrix.py`.

It stops normal runs before strategy generation if the bars contain fatal data
errors:

- duplicate timestamp
- out-of-order timestamp
- invalid OHLC range
- non-positive OHLC price
- negative volume

Why this matters: if bad bars get into a simulator, different engines may handle
the bad data differently. Then the report may blame the simulator when the real
problem was corrupted input.

## Where To See The Trace

The stable trace today is inside the saved result JSON files. Each fill records:

- fill time
- symbol
- buy or sell
- quantity
- price
- fee
- source signal time

Useful files:

- `reports/muni_bridge/experiment/strategy_matrix_results.json`
- `reports/muni_bridge/hardening/strategy_matrix_results.json`
- `reports/muni_bridge/experiment/strategy_matrix_comparison.md`
- `reports/muni_bridge/hardening/strategy_matrix_comparison.md`

The separate `muni` event/decision/anomaly CSV artifacts are a good next trace
target, but they are not yet the main stable report surface in this repo.

## Best Next Choices

Pick one:

1. Build a simple replay page so Rafa can see bars, signals, and fills.
2. Add 30m, 1h, and 4h strategy passes.
3. Add order-intent tests later: stops, limits, gaps, same-candle ambiguity.

My recommendation: do either replay UI or timeframe ladder next. Do not add
another strategy agent before the reports are easy to inspect.

## Model And Credit Use

This repo does not track OpenAI credit usage or model cost by itself.

Practical split:

- Use cheaper/faster models for rerunning reports, small code edits, and docs.
- Use the stronger model for architecture decisions, suspicious bugs, and review
  work like OG's comparator finding.

If model/credit stats become available from the app, add them to this status
file or a small `reports/human/model-usage.md` note.

## Start Here

- `reports/human/backlog.html`
- `reports/human/index.html`
- `reports/human/og-review-2026-08-15.md`
- `benchmark/MUNI_BRIDGE_CONTRACT.md`
- `benchmark/FAILURE_CLASSIFICATION.md`
