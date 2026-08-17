# Candidate Matrix

There are 25 folders in `candidates/`, but they are not 25 equivalent
full-fidelity simulators. This is the practical grouping for evaluation.

## Best Fit For Hardcore Simulation

| Candidate | Runs on | Strongest data shape | Paper/live path | Why it matters |
| --- | --- | --- | --- | --- |
| NautilusTrader | Python control plane plus Rust core | bars, ticks, quotes, order books, Parquet catalog | sandbox/live adapters, not Alpaca-first | Production-style event engine with deterministic backtests and rich execution semantics. |
| HftBacktest | Python/Rust | full tick, L2/L3, latency data | crypto live bot path, not Alpaca-first | Focused on queue position, feed/order latency, and market-making fills. |
| QuantReplay | native/C++-style project with FIX components | replay/generator/FIX/order book data | FIX gateway style, not Alpaca-first | Matching engine, generated order flow, venues, latency, and FIX-oriented simulation. |
| LEAN | .NET/C#/Python algorithms | bars, ticks, quotes, option/future data | direct Alpaca brokerage model plus paper/live modes | Broad asset-class engine with serious brokerage/order model coverage. |
| ABIDES-JPMC | Python packages | agent-generated order flow and exchange messages | local simulation/gym, not Alpaca-first | Multi-agent market simulator with latency-aware message passing and exchange agents. |
| ABIDES | Python | agent-generated order flow and exchange messages | local simulation, not Alpaca-first | Older reference implementation for agent-based market simulation. |

## Strong General Backtesters

| Candidate | Runs on | Alpaca bars? | Paper/live path | Notes |
| --- | --- | --- | --- | --- |
| Backtrader | Python | yes, via CSV/DataFrame adapter | live brokers exist, Alpaca not native here | Mature event-driven bar backtester with orders, slippage, commission, analyzers. |
| Zipline Reloaded | Python | yes, via custom bundle/ingest | mostly research/backtest | Good for equities/factor-style research with calendars, slippage, commissions. |
| QSTrader | Python | yes, via CSV | local backtest | Modular long/short equities and ETF backtesting. |
| PyBroker | Python | yes, native Alpaca data source | backtest/research | ML-oriented bar backtester with walk-forward and bootstrap metrics. |
| VectorBT | Python | yes, DataFrame | research/backtest | Very fast vectorized sweeps; not a realistic order-book simulator. |
| bt | Python | yes, DataFrame | local backtest | Portfolio allocation/backtesting library, less execution-microstructure oriented. |
| RQAlpha | Python | possible with adapted data bundle | simulation/live ecosystem mostly RiceQuant/China-market oriented | Good event-driven framework, but data integration is not Alpaca-native. |
| Basana | Python async | yes, with CSV bar source adapter | Binance/Bitstamp/CCXT integrations | Nice event-driven exchange abstraction with fees, liquidity, lending. |

## Crypto Bot / Strategy Frameworks

| Candidate | Runs on | Alpaca bars? | Paper/free mode | Notes |
| --- | --- | --- | --- | --- |
| Freqtrade | Python | possible after converting candles, but exchange-native crypto data fits better | free dry-run mode | Strong crypto bot with backtesting, hyperopt, lookahead/recursive analysis. |
| Jesse | Python | possible after candle conversion | backtesting free; live plugin is paid | Crypto strategy framework with backtesting, optimization, benchmark, Monte Carlo claims. |
| Blankly | Python | direct Alpaca interface | paper-trade interface and broker integrations | Useful for broker/paper parity experiments, but project maturity must be checked. |

## RL / Agent Environments

| Candidate | Runs on | Alpaca bars? | Paper/live path | Notes |
| --- | --- | --- | --- | --- |
| TensorTrade | Python | yes, via data feed | local RL training/eval | Agent/RL-focused composable environment and OMS. |
| FinRL | Python | yes, through data processors | paper/live examples may exist | Research-heavy DRL framework; less a fill simulator. |
| Qlib | Python | possible after dataset conversion | research/backtest/serving | AI quant platform with forecasting, portfolio, and RL components. |
| tradingenv | Python | yes, DataFrame | local Gym-compatible env | Event-driven Gym-style market simulator. |
| gym-anytrading | Python | yes, DataFrame | local Gym env | Simple RL baseline environment. |
| gym-trading-env | Python | yes, DataFrame | local Gymnasium env | Fast customizable RL trading environment with short/margin position action space. |

## Older / Reference

| Candidate | Runs on | Alpaca bars? | Paper/live path | Notes |
| --- | --- | --- | --- | --- |
| PyAlgoTrade | Python legacy | yes, CSV | old paper/live support | Historically important, but likely not where we should invest time first. |
| vn.py / VeighNa | Python plus external apps | possible through database/datafeed adapters | simulation/live platform modules | Powerful platform, but many backtesting pieces are separate plugin packages. |

## Suggested Funnel

First wave to run deeply:

1. LEAN, PyBroker, Backtrader, Basana, QSTrader with Alpaca-exported bars.
2. Freqtrade and Jesse with converted crypto candle data.
3. NautilusTrader, HftBacktest, QuantReplay, ABIDES-JPMC with their own native low-level fixtures.

Second wave:

VectorBT, Zipline Reloaded, bt, TensorTrade, tradingenv, gym-anytrading, gym-trading-env, Qlib.

Hold mostly for reference:

PyAlgoTrade, original ABIDES if ABIDES-JPMC works better, and vn.py unless we install its backtester plugin stack.

