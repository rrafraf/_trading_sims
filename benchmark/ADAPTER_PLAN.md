# Adapter Plan

The harness should keep strategy logic shared and simulator-specific code thin.

## Contract

1. Load canonical bars from CSV.
2. Run shared signal strategy code to produce target-position signals.
3. Let each adapter translate target changes into simulator-native orders.
4. Save normalized fills, final equity, notes, and simulator policy differences.

This prevents each simulator from getting its own subtly different strategy.

## Adapter Priority

| Adapter | Status | Purpose |
| --- | --- | --- |
| `reference_bar` | implemented | Internal deterministic baseline for target-to-market-on-next-bar behavior. |
| `backtrader` | implemented and running | Fast practical 1m/daily bar testing and simple strategy iteration. |
| `vectorbt` | implemented and running | Parameter sweeps and grid tests; execution realism intentionally limited. |
| `pybroker` | implemented and running | Alpaca-native data and ML/walk-forward workflows. |
| `lean` | registered slot, runner-pending | Serious engine with broad brokerage/order model coverage and Alpaca support. |
| `own_engine_template` | implemented template | Starting point for the in-house engine adapter. |
| `freqtrade` | later | Crypto bot workflow, dry-run/backtest, lookahead and recursive analysis. |
| `nautilus_trader` | later | Low-level tick/order-book simulation when strategy needs microstructure. |
| `hftbacktest` | later | Queue/latency/fill probability tests for market making. |
| `quantreplay` | later | Matching engine/FIX/venue simulation. |

## Equality Rules

Simple target-market tests should match across engines when all assumptions are
identical:

- same bars
- same timestamp convention
- orders generated at bar close
- market-to-target fills at next bar open
- same fees and slippage
- no volume constraint unless configured

If those runs do not match, the adapter or engine configuration needs inspection.

Stress scenarios do not always have one correct answer. For zero-volume bars,
same-bar stop/target ambiguity, and gap-through-stop behavior, the first goal is
to record the engine policy explicitly.
