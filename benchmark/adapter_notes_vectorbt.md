# VectorBT Adapter Notes

- File: `benchmark_runner/adapters/vectorbt_adapter.py`
- Status: implemented as a real thin adapter when `vectorbt` and its dependencies are importable.
- Import path: tries installed `vectorbt` first, then `candidates/vectorbt`.
- Scope: single-symbol OHLCV bars, precomputed `TargetSignal` inputs, market orders at next bar open, percent fees, percent price slippage.
- Current local status: dependencies are installed from the cloned candidate package and the adapter matches the reference baseline on the current strategy matrix.
- Registered in `benchmark_runner.adapters.ADAPTERS`.
