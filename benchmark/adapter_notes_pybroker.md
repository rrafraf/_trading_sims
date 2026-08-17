# PyBroker Adapter Notes

- File: `benchmark_runner/adapters/pybroker_adapter.py`
- Status: implemented as a thin PyBroker event-loop wrapper when `pybroker` and its dependencies are importable.
- Import path: tries installed `pybroker` first, then `candidates/pybroker/src`.
- Scope: single-symbol OHLCV bars, precomputed `TargetSignal` inputs, market orders scheduled to fill at next bar open, percent fees, percent price slippage.
- Implementation note: the adapter precomputes order emission timestamps so PyBroker's `buy_delay=1` and `sell_delay=1` fill on the same next-bar timestamp as the reference adapter.
- Current local status: dependencies are installed from the cloned candidate package and the adapter matches the reference baseline on the current strategy matrix.
- Registered in `benchmark_runner.adapters.ADAPTERS`.
