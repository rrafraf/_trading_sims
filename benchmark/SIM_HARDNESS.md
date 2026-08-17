# Simulator Hardness Model

This benchmark treats "best" as simulation depth plus testability, not just speed
or popularity.

## Dimensions

1. Native tests
   - Does the repo ship tests?
   - Are there tests for order edge cases rather than only indicators or examples?
   - Can the tests run locally without paid services?

2. Data model
   - Daily/minute OHLCV bars
   - Quotes and trades
   - L2 market-by-price order book
   - L3 market-by-order order book
   - Synthetic/generated market flow

3. Fill model
   - Market, limit, stop, stop-limit orders
   - Partial fills
   - Volume participation constraints
   - Time-in-force such as GTC, IOC, FOK, DAY
   - Same-bar ambiguity handling
   - Gap-through-stop handling

4. Microstructure
   - Price/time priority matching engine
   - Queue position
   - Latency model
   - Multi-venue routing
   - Auctions or open/close special sessions

5. Costs and constraints
   - Commission/fees
   - Slippage
   - Borrow/short/margin
   - Cash, buying power, settlement, corporate actions
   - Calendar/session behavior

6. Agent fit
   - Clean callback API for strategies
   - Gym/Gymnasium environment for RL
   - Batch parameter search
   - Deterministic replay for repeated agent evaluation

7. Paper/live path
   - Direct paper trading integration
   - Same strategy code between backtest and paper/live
   - Broker-specific order rules

## Alpaca Data Fit

Alpaca stock and crypto bars are enough for first-pass tests of bar-based engines:

- Backtrader
- Zipline Reloaded
- QSTrader
- VectorBT
- PyBroker
- bt
- LEAN
- Basana, with an adapter
- Gym-style RL environments

Alpaca bars are not enough for microstructure claims. These engines need tick,
quote, L2/L3, FIX, or generated order-flow data to test their strongest features:

- NautilusTrader
- HftBacktest
- QuantReplay
- ABIDES and ABIDES-JPMC
- LEAN, when testing order-book/fill-model details

Freqtrade and Jesse are primarily crypto-trading frameworks. They can be compared
with Alpaca crypto bars only if we add a conversion layer to their expected candle
formats, but exchange-native crypto data is usually a better fit.

## Edge-Case Dataset

`tools/make_synthetic_data.py` creates data designed to expose weak assumptions:

- missing minute inside a trading session
- zero-volume bar
- wide same-bar high/low where both stop and target could be touched
- gap-through-stop open
- split-like discontinuity
- duplicate timestamp file for loader validation

These files are not realistic market data. They are fixtures for finding how a
simulator chooses fills, validates data, and handles ambiguity.

