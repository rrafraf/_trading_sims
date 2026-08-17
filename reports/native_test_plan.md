# Native Test Plan

Default mode only plans commands. Use `--execute` after installing each repo's dependencies.

| Candidate | Test files | Commands |
| --- | ---: | --- |
| [nautilus_trader](../candidates/nautilus_trader) | 317 | `cargo test` |
| [freqtrade](../candidates/freqtrade) | 142 | `python -m pytest tests` |
| [backtrader](../candidates/backtrader) | 83 | `python -m pytest tests` |
| [Lean](../candidates/Lean) | 820 | `dotnet test QuantConnect.Lean.sln` |
| [jesse](../candidates/jesse) | 51 | `python -m pytest tests` |
| [basana](../candidates/basana) | 60 | `python -m pytest tests` |
| [zipline-reloaded](../candidates/zipline-reloaded) | 95 | `python -m pytest tests` |
| [tensortrade](../candidates/tensortrade) | 76 | `python -m pytest tests` |
| [blankly](../candidates/blankly) | 18 | `python -m pytest tests` |
| [rqalpha](../candidates/rqalpha) | 67 | `python -m pytest tests` |
| [pybroker](../candidates/pybroker) | 16 | `python -m pytest tests` |
| [quantreplay](../candidates/quantreplay) | 18 | `cmake -S . -B build/tests -DCMAKE_BUILD_TYPE=Debug && ctest --test-dir build/tests --output-on-failure` |
| [hftbacktest](../candidates/hftbacktest) | 1 | `cargo test` |
| [vectorbt](../candidates/vectorbt) | 16 | `python -m pytest tests` |
| [abides-jpmc-public](../candidates/abides-jpmc-public) | 19 | `inspect test docs manually` |
| [qlib](../candidates/qlib) | 40 | `python -m pytest tests` |
| [vnpy](../candidates/vnpy) | 2 | `python -m pytest tests` |
| [tradingenv](../candidates/tradingenv) | 33 | `python -m pytest tests` |
| [pyalgotrade](../candidates/pyalgotrade) | 0 |  |
| [qstrader](../candidates/qstrader) | 30 | `python -m pytest tests` |
| [FinRL](../candidates/FinRL) | 0 |  |
| [abides](../candidates/abides) | 0 |  |
| [bt](../candidates/bt) | 5 | `python -m pytest tests` |
| [gym-trading-env](../candidates/gym-trading-env) | 0 |  |
| [gym-anytrading](../candidates/gym-anytrading) | 0 |  |
