# Experiment Summary

This batch uses these adapters: `reference_bar`, `backtrader`, `muni`, `pybroker`, `vectorbt`.

## Adapter Agreement

| Adapter | Baseline | Match | Policy diff | Diff | Unavailable |
| --- | ---: | ---: | ---: | ---: | ---: |
| `backtrader` | 0 | 15 | 0 | 0 | 0 |
| `muni` | 0 | 15 | 0 | 0 | 0 |
| `pybroker` | 0 | 15 | 0 | 0 | 0 |
| `reference_bar` | 15 | 0 | 0 | 0 | 0 |
| `vectorbt` | 0 | 15 | 0 | 0 | 0 |

## Runs

| Run | reference_bar return % | backtrader return % | muni return % | pybroker return % | vectorbt return % |
| --- | ---: | ---: | ---: | ---: | ---: |
| `chop_1m_mr_20` | -0.1459 | -0.1459 | -0.1459 | -0.1459 | -0.1459 |
| `chop_1m_sma_5_20` | 0.2421 | 0.2421 | 0.2421 | 0.2421 | 0.2421 |
| `liquidity_1m_buy_hold` | -0.2204 | -0.2204 | -0.2204 | -0.2204 | -0.2204 |
| `liquidity_1m_sma_5_20` | 0.1457 | 0.1457 | 0.1457 | 0.1457 | 0.1457 |
| `regime_1m_breakout_30` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `regime_1m_sma_5_20` | 0.2129 | 0.2129 | 0.2129 | 0.2129 | 0.2129 |
| `trend_1h_breakout_30` | 0.7519 | 0.7519 | 0.7519 | 0.7519 | 0.7519 |
| `trend_1h_sma_5_20` | 0.7293 | 0.7293 | 0.7293 | 0.7293 | 0.7293 |
| `trend_1m_breakout_30` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `trend_1m_buy_hold` | 0.4567 | 0.4567 | 0.4567 | 0.4567 | 0.4567 |
| `trend_1m_sma_5_20` | 0.3122 | 0.3122 | 0.3122 | 0.3122 | 0.3122 |
| `trend_30m_breakout_30` | 0.6670 | 0.6670 | 0.6670 | 0.6670 | 0.6670 |
| `trend_30m_sma_5_20` | 0.6405 | 0.6405 | 0.6405 | 0.6405 | 0.6405 |
| `trend_4h_breakout_30` | 1.0164 | 1.0164 | 1.0164 | 1.0164 | 1.0164 |
| `trend_4h_sma_5_20` | 1.0308 | 1.0308 | 1.0308 | 1.0308 | 1.0308 |
