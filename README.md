# Trading Simulator Evaluation Workspace

Current human status: read `PROJECT_STATUS.md` first.

This workspace collects open-source trading simulators/backtesters in `candidates/`
and adds a thin benchmark layer around them.

The immediate goal is not to crown a winner from README text. It is to compare:

- native test coverage and whether those tests exercise hard simulation cases
- fill mechanics: market, limit, stop, partial fills, time-in-force, volume limits
- market microstructure: order book, queue position, matching engine, latency
- cost models: fees, slippage, borrow, margin, market impact assumptions
- data compatibility with Alpaca bars, trades, quotes, or external L2/L3 data
- agent ergonomics: Gym/RL APIs, batch research APIs, live/paper parity

## Layout

- `candidates/` - shallow clones of each candidate engine
- `tools/inventory_candidates.py` - scans repos for tests, claims, and hard-sim features
- `tools/scan_test_focus.py` - scans native tests for execution/microstructure topics
- `tools/run_candidate_tests.py` - produces or executes native test commands
- `tools/fetch_alpaca_bars.py` - downloads Alpaca bars into a canonical CSV format
- `tools/make_synthetic_data.py` - creates deterministic edge-case data
- `tools/run_strategy_matrix.py` - runs shared strategies through benchmark adapters
- `tools/compare_strategy_results.py` - compares adapter outputs against a baseline
- `benchmark/SIM_HARDNESS.md` - scoring model and data-fit notes
- `data/` - generated Alpaca or synthetic data
- `reports/` - generated inventory and run results
- `reports/index.html` - local report index for handoff/review

## First Commands

Create or refresh the local tool environment:

```powershell
python -m venv .venv
uv --cache-dir .uv-cache pip install -r requirements.txt
uv --cache-dir .uv-cache pip install -r requirements-adapters.txt
```

`uv` normally finds `.venv` automatically. The local `--cache-dir` keeps uv's
cache inside this workspace, which avoids Windows sandbox permission issues.

Inventory the cloned candidates:

```powershell
.venv\Scripts\python.exe tools\inventory_candidates.py
```

Create deterministic edge-case bar data:

```powershell
.venv\Scripts\python.exe tools\make_synthetic_data.py
```

Show native test commands without running heavyweight suites:

```powershell
.venv\Scripts\python.exe tools\run_candidate_tests.py --dry-run
```

Scan native tests for hard-simulation topics:

```powershell
.venv\Scripts\python.exe tools\scan_test_focus.py
```

Run the shared strategy matrix through implemented adapters:

```powershell
.venv\Scripts\python.exe tools\run_strategy_matrix.py
```

Run the larger experiment suite with the working adapters:

```powershell
.venv\Scripts\python.exe tools\make_experiment_data.py
.venv\Scripts\python.exe tools\run_strategy_matrix.py --suite benchmark\experiment_suite.json --reports-dir reports\experiments
.venv\Scripts\python.exe tools\compare_strategy_results.py --results reports\experiments\strategy_matrix_results.json --reports-dir reports\experiments
.venv\Scripts\python.exe tools\build_experiment_report.py
```

Run the harder target-position suite:

```powershell
.venv\Scripts\python.exe tools\make_experiment_data.py
.venv\Scripts\python.exe tools\run_strategy_matrix.py --suite benchmark\hardening_suite.json --reports-dir reports\hardening
.venv\Scripts\python.exe tools\compare_strategy_results.py --results reports\hardening\strategy_matrix_results.json --reports-dir reports\hardening
.venv\Scripts\python.exe tools\build_experiment_report.py --reports-dir reports\hardening
```

Compare matrix outputs against the reference adapter:

```powershell
.venv\Scripts\python.exe tools\compare_strategy_results.py
```

Fetch Alpaca stock bars once credentials are present:

```powershell
$env:ALPACA_API_KEY="..."
$env:ALPACA_SECRET_KEY="..."
.venv\Scripts\python.exe tools\fetch_alpaca_bars.py --asset stock --symbols SPY QQQ --timeframe 1Day --start 2024-01-01 --end 2024-03-01
```

Fetch Alpaca crypto bars; keys are optional for crypto but improve rate limits:

```powershell
.venv\Scripts\python.exe tools\fetch_alpaca_bars.py --asset crypto --symbols BTC/USD ETH/USD --timeframe 1Hour --start 2024-01-01 --end 2024-01-07
```

## Important Alpaca Distinction

Alpaca is useful here in two separate ways:

- Data source: export bars/trades/quotes into files, then feed those files into engines.
- Paper broker: submit simulated live orders to Alpaca's paper API.

Paper trading is useful for API integration and operational failures. It is not a
high-fidelity exchange simulator: queue position, market impact, and latency slippage
are exactly the kinds of things we still need local simulators to test.
