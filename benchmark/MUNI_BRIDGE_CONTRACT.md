# Muni Bridge Contract

This records the Vega/M55 agreement for connecting `_trading_sims` with the
`muni` in-house engine.

## Decision

Do not merge the repos yet.

Use `_trading_sims` as the benchmark harness and simulator comparison surface.
Use `muni` as the in-house execution model, trace/evidence engine, and anomaly
UI.

The first connection should be a subprocess/file bridge, not a deep import.

```text
_trading_sims strategy signals
        -> muni CLI seam
        -> muni execution model
        -> RunResult-compatible JSON
        -> _trading_sims comparison reports
```

## Responsibilities

`_trading_sims` owns:

- canonical bars, scenarios, and benchmark suites
- shared target-position strategies
- simulator adapters
- normalized result comparison
- human-readable reports

`muni` owns:

- execution semantics
- trace/evidence output
- anomaly classification
- stricter order behavior
- UI for inspecting decisions and fills

## Phase 1: Target Position Bridge

The first bridge mode is `target-position-v1`.

It is intentionally narrow. Its job is to prove that `muni` can run the same
simple bar-level policy as the current reference adapter.

Expected CLI shape:

```powershell
node training_ground/run-experiment.js `
  --mode target-signals `
  --bars path\to\bars.csv `
  --signals path\to\signals.json `
  --policy path\to\policy.json `
  --out path\to\run-result.json
```

The cleaner internal implementation is likely:

```text
training_ground/signal-runner.js
training_ground/run-experiment.js dispatches --mode target-signals to it
```

### Input

Bars:

- canonical OHLCV CSV
- sorted timestamps
- one symbol for v1 unless explicitly extended

Signals:

- timestamp
- symbol
- target position

Policy:

- `initial_cash`
- `fee_bps`
- `slippage_bps`
- fill timing: signal at bar timestamp T fills target delta at next eligible bar open
- volume policy: `ignore`, `defer`, or `partial`
- long-only for v1 unless the fixture explicitly tests short exposure

### Output

The `muni` command should write RunResult-compatible JSON:

```json
{
  "run_id": "string",
  "adapter_policy_version": "target-position-v1",
  "final_cash": 100000.0,
  "final_position": 0.0,
  "final_equity": 100000.0,
  "fills": [],
  "notes": [],
  "policy_differences": [],
  "artifacts": {
    "events": "path/to/events.csv",
    "decisions": "path/to/decisions.csv",
    "anomalies": "path/to/anomalies.csv"
  }
}
```

## First Acceptance Test

After the CLI seam exists, add a real `_trading_sims` `muni_adapter.py` that
calls it.

Then run the existing experiment suite:

```powershell
.venv\Scripts\python.exe tools\run_strategy_matrix.py --suite benchmark\experiment_suite.json
.venv\Scripts\python.exe tools\compare_strategy_results.py
```

Requirement:

- `muni` must match `reference_bar` on simple market-next-open cases, or
  classify the mismatch using `benchmark/FAILURE_CLASSIFICATION.md`.

## Phase 2: Order Intent Bridge

Do not force stop, limit, gap, and same-candle behavior into
`target-position-v1`.

After parity works, add `order-intent-v1` for the hard execution cases:

- same-candle stop and target both touched
- gap-through-stop behavior
- limit order touched by high/low behavior
- zero-volume fill, defer, or partial behavior
- missing candle handling
- duplicate timestamp rejection
- latency and missed-fill stress

This keeps the simple parity bridge honest while exposing the hard execution
semantics in a separate mode.

## M55 Warning Accepted By Vega

The current green adapter results are a smoke test, not proof of simulator
realism.

They show that `reference_bar`, `backtrader`, `vectorbt`, and `pybroker` agree
on the existing simple target-position bar matrix. They do not yet prove the
engines are realistic enough for broker-specific or microstructure-sensitive
strategies.
