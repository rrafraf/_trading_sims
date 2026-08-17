# Why Simulate If The Brokerage Behaves Differently?

Backtests, microstructure simulators, and broker paper accounts answer different
questions.

## Bar Backtest

Question: does the signal and portfolio logic make sense over history?

Input: daily/minute OHLCV bars, such as Alpaca bars.

Useful for:

- strategy logic
- position sizing
- portfolio accounting
- fees and simple slippage
- missing candles, bad timestamps, split-like discontinuities
- same-bar ambiguity, if the engine exposes its policy

Not enough for:

- whether a passive limit order really filled
- queue position
- latency
- market impact
- exact intrabar path

## Microstructure Simulator

Question: does the strategy still work when execution is modeled with more
realistic market mechanics?

Input: trades/quotes/L2/L3 order book data, FIX replay data, or generated agent
order flow.

Useful for:

- market making
- passive limit orders
- fill probability
- order queue position
- feed latency and order latency
- partial fills
- order book depth and price/time priority

It still will not exactly predict one broker's paper fill. Its value is
stress-testing the assumptions. If a strategy only works when every touched
limit order fills at the best possible price, the simulator should expose that.

## Broker Paper Trading

Question: does the trading system operate correctly against a broker API in
real time?

Input: live/paper API, real-time data feed, broker order lifecycle events.

Useful for:

- authentication and account state
- order submission/cancel/replace logic
- clock/session handling
- reconnects, retries, rate limits
- broker-specific order rules
- operational safety before real money

Paper trading is not a complete exchange model. Alpaca's own docs say paper
trading is a simulation and does not account for market impact, information
leakage, latency slippage, or queue position. That is why a good local
simulator is still useful.

## Practical Evaluation Flow

1. Use Alpaca historical bars for a common, cheap baseline across bar engines.
2. Run synthetic edge-case fixtures to expose hidden fill/data assumptions.
3. Use native engine tests to see which projects already test low-level order
   mechanics.
4. For microstructure engines, use their native tick/L2/L3 or generated order
   flow fixtures rather than forcing Alpaca bars into the wrong shape.
5. After a strategy survives those, paper-trade it with Alpaca to test the
   integration path.

