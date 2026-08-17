# Common Scenario Spec

The common benchmark scenarios live in `benchmark/scenarios.json`.

These are intentionally small and deterministic. They are not intended to prove
profitability. They expose execution assumptions:

- market order on zero-volume bar
- both stop and target touched inside one candle
- missing candle followed by a gap-through-stop
- split-like discontinuity
- duplicate and out-of-order timestamps

For each candidate engine, the adapter should emit a result record with:

- scenario id
- candidate name and version/commit
- accepted/rejected orders
- fills with timestamp, price, quantity, and fee
- final cash, position, and equity
- explicit notes for behavior that is not supported or not applicable

The important result is not always pass/fail. For many engines, the useful
finding is the documented policy: for example, whether a stop fills at the stop
price, next open, next low, or a configured slippage model when price gaps
through it.

