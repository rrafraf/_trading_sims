# Decision Log

## 2026-08-14: Use Adapters Instead Of Rewriting Simulators

Decision: keep strategy logic shared and write thin simulator adapters.

Reason:

- prevents each simulator from getting a subtly different strategy
- lets us compare engines under the same data/config
- lets the in-house engine plug in without repo merge

## 2026-08-14: First-Wave Engines

Decision: prioritize LEAN, Backtrader, PyBroker, and VectorBT for 1m+ bar tests.

Reason:

- these are most relevant to the user's near-term strategy-testing goal
- true microstructure engines are valuable but premature unless the strategy
  depends on order book, queue position, latency, or market-making assumptions

## 2026-08-14: Compare Before Choosing A Winner

Decision: do not crown a single "best" engine until adapters run the same
strategy suite and comparison reports show where they agree or diverge.

Reason:

- simple baseline mismatches expose serious adapter/config/simulator problems
- ambiguous fill cases require policy classification, not naive pass/fail

