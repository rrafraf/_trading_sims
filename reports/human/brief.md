# Trading Simulator Experiment: Plain-English Brief

## One-Sentence Version

We built a small test bench that runs the same strategy idea through multiple
trading simulators and checks whether they give the same result under the same
rules.

## What We Have Working

Four adapters are active:

- `reference_bar`: our simple truth model for bar-based tests.
- `backtrader`: running and matching.
- `vectorbt`: running and matching.
- `pybroker`: running and matching.

`LEAN` is not running yet. That does not mean it failed. It means it is a
different kind of system: a full .NET trading engine that needs a generated
LEAN project/config/algorithm runner before it can be compared in the same way.

## What We Tested

We used synthetic data made to represent:

- 1-minute trend
- 1-minute sideways/choppy market
- 1-minute regime shift
- 1-minute liquidity gap with zero-volume and skipped bars
- 1-hour trend

Strategies tested:

- buy and hold
- SMA cross
- breakout
- mean-reversion z-score

## What We Found

Backtrader, VectorBT, and PyBroker all matched the reference model on the current
experiment suite.

That means the adapter layer is working for simple bar-based strategy tests.

We also added a harder target-position suite. Backtrader and VectorBT matched
all 7 hardening runs. PyBroker matched 6 of 7 and only differed on deliberately
bad market data with duplicate/out-of-order timestamps and invalid OHLC.

That is a useful warning: normal comparisons should reject corrupted data before
judging a simulator.

## What This Does Not Prove Yet

This does not prove the engines are realistic for every kind of trading.

Not tested yet:

- limit order behavior
- stop orders
- same-candle stop/target ambiguity
- broker-specific paper fills
- latency
- order-book queue position
- market impact

## Which Tool Is Good For What?

- Backtrader: best for quick practical 1-minute and daily bar strategy work.
- VectorBT: best for fast parameter sweeps and grid tests.
- PyBroker: best for Alpaca-style data, ML experiments, and walk-forward tests.
- LEAN: likely best serious all-around engine later, but deferred because it
  needs its own project/config/runner and the current three engines are enough
  for the next learning loop.
- NautilusTrader / HftBacktest / QuantReplay / ABIDES: later tools for true
  order-book or market-making questions.

## Recommendation

Do not merge the in-house engine repo yet.

First plug it into this harness as another adapter. Then we can compare it
against the same baseline and see where it matches, differs by policy, or finds
problems the simpler simulators do not model.
