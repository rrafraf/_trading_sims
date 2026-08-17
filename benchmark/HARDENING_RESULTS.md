# Hardening Suite Results

Generated from `benchmark/hardening_suite.json`.

## Summary

The harder target-position suite ran against the active adapters:

- `reference_bar`
- `backtrader`
- `vectorbt`
- `pybroker`

Result:

- Backtrader matched the reference on all 7 runs.
- VectorBT matched the reference on all 7 runs.
- PyBroker matched the reference on 6 of 7 runs.
- PyBroker diverged only on the deliberately bad data fixture.

## What Passed

The working adapters agreed on valid target-position stress cases:

- gap-open entry and exit
- volume-limited partial fills
- zero-volume deferral
- last-bar signal with no next bar available
- high-cost churn
- simple short round trip

This is stronger than the first smoke test, but it is still bar-level testing.

## Useful Failure

`bad_data_1m_quality_notes` produced a PyBroker equity difference of about
`2.9645`.

That fixture intentionally includes:

- duplicate timestamp
- out-of-order timestamp
- invalid OHLC range

Interpretation:

This should not be treated as "PyBroker is bad." It means the harness should
reject or quarantine bad market data before comparing simulator quality.

Recommended classification:

- `P0` if the harness lets known-invalid data enter a normal comparison.
- `P3` only if a suite is explicitly testing engine policy around bad data.

## Next Harness Change

Add a strict data validation mode:

```text
normal suites: reject duplicate/out-of-order/invalid OHLC data
data-quality suites: allow bad data only when the test is about bad-data policy
```

This prevents a simulator from looking different just because the input was
already corrupted.
