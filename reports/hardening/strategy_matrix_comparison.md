# Strategy Matrix Comparison

| Run | Adapter | Status | Cash diff | Position diff | Equity diff | Fills diff | Signals diff | Mismatches | Notes |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `bad_data_1m_quality_notes` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | duplicate timestamp for SIM at 2024-01-02T14:40:00+00:00 | out-of-order timestamp for SIM at 2024-01-02T14:40:00+00:00 | invalid OHLC range for SIM at 2024-01-02T14:40:00+00:00 |
| `bad_data_1m_quality_notes` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | duplicate timestamp for SIM at 2024-01-02T14:40:00+00:00 | out-of-order timestamp for SIM at 2024-01-02T14:40:00+00:00 | invalid OHLC range for SIM at 2024-01-02T14:40:00+00:00 |
| `bad_data_1m_quality_notes` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | duplicate timestamp for SIM at 2024-01-02T14:40:00+00:00 | out-of-order timestamp for SIM at 2024-01-02T14:40:00+00:00 | invalid OHLC range for SIM at 2024-01-02T14:40:00+00:00 |
| `bad_data_1m_quality_notes` | `pybroker` | `diff` | 0.000000 | 0.000000 | 2.964500 | 0 | 0 | final_equity: candidate=100011.32804975 baseline=100008.36354975 | return_pct: candidate=0.011328049749992353 baseline=0.008363549750001198 | duplicate timestamp for SIM at 2024-01-02T14:40:00+00:00 | out-of-order timestamp for SIM at 2024-01-02T14:40:00+00:00 | invalid OHLC range for SIM at 2024-01-02T14:40:00+00:00 |
| `bad_data_1m_quality_notes` | `muni` | `policy_diff` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | duplicate timestamp for SIM at 2024-01-02T14:40:00+00:00 | out-of-order timestamp for SIM at 2024-01-02T14:40:00+00:00 | invalid OHLC range for SIM at 2024-01-02T14:40:00+00:00 |
| `churn_noise_1m_flip_5_high_cost` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `churn_noise_1m_flip_5_high_cost` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `churn_noise_1m_flip_5_high_cost` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `churn_noise_1m_flip_5_high_cost` | `pybroker` | `match` | -0.000000 | 0.000000 | -0.000000 | 0 | 0 |  |  |
| `churn_noise_1m_flip_5_high_cost` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `gap_open_1m_scheduled_entry_exit` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `gap_open_1m_scheduled_entry_exit` | `backtrader` | `match` | -0.000000 | 0.000000 | -0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `gap_open_1m_scheduled_entry_exit` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `gap_open_1m_scheduled_entry_exit` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `gap_open_1m_scheduled_entry_exit` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `last_bar_signal_no_next_fill` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `last_bar_signal_no_next_fill` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `last_bar_signal_no_next_fill` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `last_bar_signal_no_next_fill` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `last_bar_signal_no_next_fill` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `liquidity_zero_volume_defer` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_zero_volume_defer` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_zero_volume_defer` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_zero_volume_defer` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_zero_volume_defer` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `partial_volume_1m_scheduled_100` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | partial volume-limited fill at 2024-01-02T14:31:00+00:00: requested 100.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:32:00+00:00: requested 75.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:33:00+00:00: requested 50.00000000, filled 25.00000000 |
| `partial_volume_1m_scheduled_100` | `backtrader` | `match` | -0.000000 | 0.000000 | -0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `partial_volume_1m_scheduled_100` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | partial volume-limited fill at 2024-01-02T14:31:00+00:00: requested 100.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:32:00+00:00: requested 75.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:33:00+00:00: requested 50.00000000, filled 25.00000000 |
| `partial_volume_1m_scheduled_100` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | partial volume-limited fill at 2024-01-02T14:31:00+00:00: requested 100.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:32:00+00:00: requested 75.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:33:00+00:00: requested 50.00000000, filled 25.00000000 |
| `partial_volume_1m_scheduled_100` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | partial volume-limited fill at 2024-01-02T14:31:00+00:00: requested 100.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:32:00+00:00: requested 75.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:33:00+00:00: requested 50.00000000, filled 25.00000000 |
| `short_round_trip_scheduled` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `short_round_trip_scheduled` | `backtrader` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | Backtrader volume filler enabled with FixedSize(size=None) |
| `short_round_trip_scheduled` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `short_round_trip_scheduled` | `pybroker` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `short_round_trip_scheduled` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
