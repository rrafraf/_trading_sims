# Strategy Matrix Results

| Run | Adapter | Strategy | Symbol | Final equity | Return % | Fills | Signals | Notes |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `trend_1m_buy_hold` | `reference_bar` | `buy_hold` | `SIM` | 100456.66 | 0.4567 | 1 | 1 |  |
| `trend_1m_buy_hold` | `muni` | `buy_hold` | `SIM` | 100456.66 | 0.4567 | 1 | 1 |  |
| `trend_1m_sma_5_20` | `reference_bar` | `sma_cross` | `SIM` | 100312.17 | 0.3122 | 11 | 11 |  |
| `trend_1m_sma_5_20` | `muni` | `sma_cross` | `SIM` | 100312.17 | 0.3122 | 11 | 11 |  |
| `trend_1m_breakout_30` | `reference_bar` | `breakout_channel` | `SIM` | 100000.00 | 0.0000 | 0 | 0 |  |
| `trend_1m_breakout_30` | `muni` | `breakout_channel` | `SIM` | 100000.00 | 0.0000 | 0 | 0 |  |
| `chop_1m_sma_5_20` | `reference_bar` | `sma_cross` | `SIM` | 100242.08 | 0.2421 | 11 | 11 |  |
| `chop_1m_sma_5_20` | `muni` | `sma_cross` | `SIM` | 100242.08 | 0.2421 | 11 | 11 |  |
| `chop_1m_mr_20` | `reference_bar` | `mean_reversion_zscore` | `SIM` | 99854.07 | -0.1459 | 9 | 9 |  |
| `chop_1m_mr_20` | `muni` | `mean_reversion_zscore` | `SIM` | 99854.07 | -0.1459 | 9 | 9 |  |
| `regime_1m_sma_5_20` | `reference_bar` | `sma_cross` | `SIM` | 100212.87 | 0.2129 | 11 | 11 |  |
| `regime_1m_sma_5_20` | `muni` | `sma_cross` | `SIM` | 100212.87 | 0.2129 | 11 | 11 |  |
| `regime_1m_breakout_30` | `reference_bar` | `breakout_channel` | `SIM` | 100000.00 | 0.0000 | 0 | 0 |  |
| `regime_1m_breakout_30` | `muni` | `breakout_channel` | `SIM` | 100000.00 | 0.0000 | 0 | 0 |  |
| `liquidity_1m_buy_hold` | `reference_bar` | `buy_hold` | `SIM` | 99779.56 | -0.2204 | 1 | 1 | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00<br>irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00<br>zero-volume bar for SIM at 2024-01-02T15:44:00+00:00<br>irregular timestamp gap for SIM before 2024-01-02T16:17:00+00:00: expected 0:01:00, got 0:02:00<br>... 6 more |
| `liquidity_1m_buy_hold` | `muni` | `buy_hold` | `SIM` | 99779.56 | -0.2204 | 1 | 1 | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00<br>irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00<br>zero-volume bar for SIM at 2024-01-02T15:44:00+00:00<br>irregular timestamp gap for SIM before 2024-01-02T16:17:00+00:00: expected 0:01:00, got 0:02:00<br>... 6 more |
| `liquidity_1m_sma_5_20` | `reference_bar` | `sma_cross` | `SIM` | 100145.70 | 0.1457 | 11 | 11 | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00<br>irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00<br>zero-volume bar for SIM at 2024-01-02T15:44:00+00:00<br>irregular timestamp gap for SIM before 2024-01-02T16:17:00+00:00: expected 0:01:00, got 0:02:00<br>... 6 more |
| `liquidity_1m_sma_5_20` | `muni` | `sma_cross` | `SIM` | 100145.70 | 0.1457 | 11 | 11 | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00<br>irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00<br>zero-volume bar for SIM at 2024-01-02T15:44:00+00:00<br>irregular timestamp gap for SIM before 2024-01-02T16:17:00+00:00: expected 0:01:00, got 0:02:00<br>... 6 more |
| `trend_1h_sma_5_20` | `reference_bar` | `sma_cross` | `SIM` | 100729.27 | 0.7293 | 7 | 7 |  |
| `trend_1h_sma_5_20` | `muni` | `sma_cross` | `SIM` | 100729.27 | 0.7293 | 7 | 7 |  |
| `trend_1h_breakout_30` | `reference_bar` | `breakout_channel` | `SIM` | 100751.87 | 0.7519 | 1 | 1 |  |
| `trend_1h_breakout_30` | `muni` | `breakout_channel` | `SIM` | 100751.87 | 0.7519 | 1 | 1 |  |
