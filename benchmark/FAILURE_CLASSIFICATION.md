# Failure Classification

When a simulator result differs, do not collapse everything into "failed".
Classify it.

## P0: Harness Or Adapter Error

The adapter did not feed the same data, timestamps, fees, slippage, or target
signals into the engine. Fix the harness before judging the simulator.

Examples:

- shifted timestamps
- order submitted one bar earlier/later
- different cash, fees, slippage, or sizing
- data sorted differently

## P1: Simple Baseline Mismatch

The engine disagrees on a case that should be deterministic:

- market-to-target generated at bar close
- fill at next bar open
- no volume constraint
- same fees and slippage
- same initial cash

This is a serious issue for comparison. Either the engine cannot express the
policy, the adapter is wrong, or the engine is unsuitable for that baseline.

## P2: Unsupported Required Feature

The strategy or benchmark needs behavior the engine cannot represent:

- stop orders
- partial fills
- shorting/margin
- order volume limits
- intraday calendar/session behavior

This does not make the engine bad globally. It removes it from that category.

## P3: Policy Difference

The engine has a different but documented execution policy:

- zero-volume bar fills vs defers
- same-bar stop/target ordering
- gap-through-stop fills at stop, open, or model price
- limit order touched by high/low fills immediately vs requires bid/ask data

These are expected. The report should record the policy and let us choose which
policy matches our intended trading style.

## P4: Operational Failure

The simulator or broker paper API has live-system behavior that differs from a
local backtest:

- order rejection
- rate limit
- disconnect/retry
- account protection rule
- trading halt/session rule

These are exactly why paper trading and small live tests exist after local
simulation.

