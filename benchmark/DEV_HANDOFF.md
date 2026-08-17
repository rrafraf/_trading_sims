# Trading Simulator Evaluation: Dev Handoff

## Why This Exists

We want to test strategies on 1-minute bars first, then longer timeframes, and
compare simulators under the same assumptions. The concern is valid: if a
strategy only works because a simulator gives unrealistic fills, it is not a
real strategy.

The harness is built to catch that by separating:

- shared strategy intent
- simulator-specific execution
- normalized results and fill records
- explicit policy differences

## Current Shortlist

These are the first engines worth comparing for 1m+ bar strategies:

- LEAN: strongest all-around serious engine and broker model coverage.
- Backtrader: practical, pure-Python, fast to iterate on bar strategies.
- PyBroker: Alpaca-friendly and ML/walk-forward oriented.
- VectorBT: fast grid/parameter sweeps, intentionally less execution-realistic.

Microstructure engines are kept for later:

- NautilusTrader
- HftBacktest
- QuantReplay
- ABIDES-JPMC

Those are only needed when the strategy depends on order-book behavior, passive
limit-order queue position, latency, matching, or market-making assumptions.

## What The Harness Does

The shared strategy code emits neutral target-position signals:

```text
timestamp T, symbol SIM, target position 100
timestamp U, symbol SIM, target position 0
```

Each adapter translates those signals into the simulator's native API, runs the
engine, and returns normalized results:

- final equity
- cash
- final position
- fills
- fees
- notes / caveats

If engines disagree on a simple market-next-bar baseline, that is a bug,
adapter issue, configuration mismatch, or simulator limitation. If they disagree
on ambiguous execution behavior, the report should classify it as a policy
difference.

## Existing Files

- `benchmark_runner/strategies.py` - shared strategy definitions.
- `benchmark_runner/adapters/reference_bar.py` - deterministic baseline adapter.
- `benchmark_runner/adapters/own_engine_template.py` - copy this for the in-house engine.
- `benchmark/MUNI_BRIDGE_CONTRACT.md` - Vega/M55 agreement for connecting the
  in-house `muni` engine to this harness.
- `tools/run_strategy_matrix.py` - runs the strategy suite.
- `tools/compare_strategy_results.py` - compares adapters against a baseline.
- `benchmark/strategy_suite.json` - common run matrix.
- `benchmark/FAILURE_CLASSIFICATION.md` - how to interpret mismatches.
- `reports/strategy_matrix_results.md` - saved results.
- `reports/strategy_matrix_comparison.md` - saved comparisons.
- `reports/index.html` - local report index.

## Current First Run

The current suite registers:

- `reference_bar`
- `backtrader`
- `vectorbt`
- `pybroker`
- `lean`

Current result:

- `backtrader` matches `reference_bar` on the existing deterministic baseline
  runs, including the synthetic zero-volume fixture and the Alpaca crypto sample.
- `vectorbt` now runs from the cloned candidate package and matches
  `reference_bar` on the existing deterministic baseline runs.
- `pybroker` now runs from the cloned candidate package and matches
  `reference_bar` on the existing deterministic baseline runs.
- `lean` adapter is registered as a first-wave slot, but still needs a generated
  LEAN algorithm/project/config runner.

Open the local report index at `reports/index.html` for links to the generated
reports and decision docs.

## How To Plug In The In-House Engine

1. Copy `benchmark_runner/adapters/own_engine_template.py` to
   `benchmark_runner/adapters/own_engine_adapter.py`.
2. Implement the adapter's `run(context)` method.
3. Register it in `benchmark_runner/adapters/__init__.py`.
4. Add config under `adapters` in `benchmark/strategy_suite.json`.
5. Run:

```powershell
.venv\Scripts\python.exe tools\run_strategy_matrix.py
.venv\Scripts\python.exe tools\compare_strategy_results.py
```

## What We Should Decide Together

- Does the in-house engine fill market orders at next open, current close, VWAP,
  or model price?
- How does it handle zero-volume 1m bars?
- How does it handle missing candles?
- How does it handle stop and target touched inside one 1m candle?
- Are fees/slippage modeled as simple bps, schedule-based fees, or broker-specific?
- Is shorting/margin required for the strategies under test?
- Do we need quote/trade/order-book data now, or are bars enough for v1?

## Repo Integration Recommendation

Do not merge repos immediately. First add the in-house engine as an adapter from
its current repo path. Once the adapter proves stable and the interface is clear,
then decide whether to:

- keep separate repos and pin a path/package dependency,
- make a mono-repo,
- or vendor only a narrow simulation core.

The first adapter gives us a record of the contract before we make repo-layout
decisions.
