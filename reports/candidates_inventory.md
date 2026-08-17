# Candidate Inventory

Scores are static first-pass signals. They should decide what to run deeply, not settle the final ranking.

| Rank | Candidate | Score | Micro | Tests | Data fit | Paper/live fit | Commands |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- |
| 1 | [nautilus_trader](../candidates/nautilus_trader) | 65.0 | 21.0 | 317 | tick/L2/L3 or generated order flow | paper/sandbox support | `cargo test` |
| 2 | [freqtrade](../candidates/freqtrade) | 58.0 | 14.0 | 142 | tick/L2/L3 or generated order flow | paper/sandbox support | `python -m pytest tests` |
| 3 | [backtrader](../candidates/backtrader) | 56.0 | 14.0 | 83 | tick/L2/L3 or generated order flow | live path, paper unclear | `python -m pytest tests` |
| 4 | [Lean](../candidates/Lean) | 56.0 | 14.0 | 820 | tick/L2/L3 or generated order flow | paper/sandbox support | `dotnet test QuantConnect.Lean.sln` |
| 5 | [jesse](../candidates/jesse) | 53.85 | 14.0 | 51 | tick/L2/L3 or generated order flow | paper/sandbox support | `python -m pytest tests` |
| 6 | [basana](../candidates/basana) | 53.36 | 14.0 | 60 | tick/L2/L3 or generated order flow | paper/sandbox support | `python -m pytest tests` |
| 7 | [zipline-reloaded](../candidates/zipline-reloaded) | 51.0 | 9.0 | 95 | tick/L2/L3 or generated order flow | paper/sandbox support | `python -m pytest tests` |
| 8 | [tensortrade](../candidates/tensortrade) | 50.5 | 12.0 | 76 | tick/L2/L3 or generated order flow | backtest/local only or unknown | `python -m pytest tests` |
| 9 | [blankly](../candidates/blankly) | 47.61 | 15.0 | 18 | tick/L2/L3 or generated order flow | direct Alpaca/paper references | `python -m pytest tests` |
| 10 | [rqalpha](../candidates/rqalpha) | 47.5 | 9.0 | 67 | tick/L2/L3 or generated order flow | paper/sandbox support | `python -m pytest tests` |
| 11 | [pybroker](../candidates/pybroker) | 43.5 | 9.0 | 16 | tick/L2/L3 or generated order flow | direct Alpaca/paper references | `python -m pytest tests` |
| 12 | [quantreplay](../candidates/quantreplay) | 42.61 | 15.0 | 18 | tick/L2/L3 or generated order flow | live path, paper unclear | `cmake -S . -B build/tests -DCMAKE_BUILD_TYPE=Debug && ctest --test-dir build/tests --output-on-failure` |
| 13 | [hftbacktest](../candidates/hftbacktest) | 42.0 | 21.0 | 1 | tick/L2/L3 or generated order flow | paper/sandbox support | `cargo test` |
| 14 | [vectorbt](../candidates/vectorbt) | 41.5 | 9.0 | 16 | tick/L2/L3 or generated order flow | backtest/local only or unknown | `python -m pytest tests` |
| 15 | [abides-jpmc-public](../candidates/abides-jpmc-public) | 39.9 | 16.0 | 19 | tick/L2/L3 or generated order flow | backtest/local only or unknown | `inspect test docs manually` |
| 16 | [qlib](../candidates/qlib) | 39.31 | 9.0 | 40 | tick/L2/L3 or generated order flow | backtest/local only or unknown | `python -m pytest tests` |
| 17 | [vnpy](../candidates/vnpy) | 37.54 | 11.0 | 2 | tick/L2/L3 or generated order flow | paper/sandbox support | `python -m pytest tests` |
| 18 | [tradingenv](../candidates/tradingenv) | 37.36 | 9.0 | 33 | tick/L2/L3 or generated order flow | backtest/local only or unknown | `python -m pytest tests` |
| 19 | [pyalgotrade](../candidates/pyalgotrade) | 35.0 | 11.0 | 0 | tick/L2/L3 or generated order flow | paper/sandbox support |  |
| 20 | [qstrader](../candidates/qstrader) | 33.19 | 4.0 | 30 | Alpaca bars via CSV/DataFrame | paper/sandbox support | `python -m pytest tests` |
| 21 | [FinRL](../candidates/FinRL) | 29.5 | 9.0 | 0 | tick/L2/L3 or generated order flow | direct Alpaca/paper references |  |
| 22 | [abides](../candidates/abides) | 28.5 | 16.0 | 0 | tick/L2/L3 or generated order flow | backtest/local only or unknown |  |
| 23 | [bt](../candidates/bt) | 28.09 | 6.0 | 5 | tick/L2/L3 or generated order flow | paper/sandbox support | `python -m pytest tests` |
| 24 | [gym-trading-env](../candidates/gym-trading-env) | 15.5 | 6.0 | 0 | tick/L2/L3 or generated order flow | backtest/local only or unknown |  |
| 25 | [gym-anytrading](../candidates/gym-anytrading) | 6.0 | 0 | 0 | Alpaca bars via CSV/DataFrame | backtest/local only or unknown |  |
