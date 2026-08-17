# Strategy Matrix Comparison

| Run | Adapter | Status | Cash diff | Position diff | Equity diff | Fills diff | Signals diff | Mismatches | Notes |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `chop_1m_mr_20` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `chop_1m_mr_20` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `chop_1m_mr_20` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `chop_1m_mr_20` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `chop_1m_mr_20` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `chop_1m_sma_5_20` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `chop_1m_sma_5_20` | `backtrader` | `match` | -0.000000 | 0.000000 | -0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `chop_1m_sma_5_20` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `chop_1m_sma_5_20` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `chop_1m_sma_5_20` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `liquidity_1m_buy_hold` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_1m_buy_hold` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_1m_buy_hold` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_1m_buy_hold` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_1m_buy_hold` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_1m_sma_5_20` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_1m_sma_5_20` | `backtrader` | `match` | -0.000000 | 0.000000 | -0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_1m_sma_5_20` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_1m_sma_5_20` | `pybroker` | `match` | -0.000000 | 0.000000 | -0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_1m_sma_5_20` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `regime_1m_breakout_30` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `regime_1m_breakout_30` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `regime_1m_breakout_30` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `regime_1m_breakout_30` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `regime_1m_breakout_30` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `regime_1m_sma_5_20` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `regime_1m_sma_5_20` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `regime_1m_sma_5_20` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `regime_1m_sma_5_20` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `regime_1m_sma_5_20` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1h_breakout_30` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1h_breakout_30` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `trend_1h_breakout_30` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1h_breakout_30` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1h_breakout_30` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1h_sma_5_20` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1h_sma_5_20` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `trend_1h_sma_5_20` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1h_sma_5_20` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1h_sma_5_20` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_breakout_30` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_breakout_30` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `trend_1m_breakout_30` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_breakout_30` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_breakout_30` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_buy_hold` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_buy_hold` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `trend_1m_buy_hold` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_buy_hold` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_buy_hold` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_sma_5_20` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_sma_5_20` | `backtrader` | `match` | -0.000000 | 0.000000 | -0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `trend_1m_sma_5_20` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_sma_5_20` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_1m_sma_5_20` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_30m_breakout_30` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_30m_breakout_30` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `trend_30m_breakout_30` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_30m_breakout_30` | `pybroker` | `match` | -0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_30m_breakout_30` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_30m_sma_5_20` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_30m_sma_5_20` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `trend_30m_sma_5_20` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_30m_sma_5_20` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_30m_sma_5_20` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_4h_breakout_30` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_4h_breakout_30` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `trend_4h_breakout_30` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_4h_breakout_30` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_4h_breakout_30` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_4h_sma_5_20` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_4h_sma_5_20` | `backtrader` | `match` | -0.000000 | 0.000000 | -0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `trend_4h_sma_5_20` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_4h_sma_5_20` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `trend_4h_sma_5_20` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
