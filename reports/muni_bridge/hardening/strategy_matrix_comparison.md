# Strategy Matrix Comparison

| Run | Adapter | Status | Cash diff | Position diff | Equity diff | Fills diff | Signals diff | Mismatches | Notes |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `bad_data_1m_quality_notes` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | duplicate timestamp for SIM at 2024-01-02T14:40:00+00:00 | out-of-order timestamp for SIM at 2024-01-02T14:40:00+00:00 | invalid OHLC range for SIM at 2024-01-02T14:40:00+00:00 |
| `bad_data_1m_quality_notes` | `muni` | `policy_diff` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | duplicate timestamp for SIM at 2024-01-02T14:40:00+00:00 | out-of-order timestamp for SIM at 2024-01-02T14:40:00+00:00 | invalid OHLC range for SIM at 2024-01-02T14:40:00+00:00 |
| `churn_noise_1m_flip_5_high_cost` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `churn_noise_1m_flip_5_high_cost` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `gap_open_1m_scheduled_entry_exit` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `gap_open_1m_scheduled_entry_exit` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `last_bar_signal_no_next_fill` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `last_bar_signal_no_next_fill` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `liquidity_zero_volume_defer` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `liquidity_zero_volume_defer` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | zero-volume bar for SIM at 2024-01-02T15:07:00+00:00 | irregular timestamp gap for SIM before 2024-01-02T15:24:00+00:00: expected 0:01:00, got 0:02:00 | zero-volume bar for SIM at 2024-01-02T15:44:00+00:00 |
| `partial_volume_1m_scheduled_100` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | partial volume-limited fill at 2024-01-02T14:31:00+00:00: requested 100.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:32:00+00:00: requested 75.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:33:00+00:00: requested 50.00000000, filled 25.00000000 |
| `partial_volume_1m_scheduled_100` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  | partial volume-limited fill at 2024-01-02T14:31:00+00:00: requested 100.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:32:00+00:00: requested 75.00000000, filled 25.00000000 | partial volume-limited fill at 2024-01-02T14:33:00+00:00: requested 50.00000000, filled 25.00000000 |
| `short_round_trip_scheduled` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
| `short_round_trip_scheduled` | `muni` | `match` | 0.000000 | 0.000000 | 0.000000 | 0 | 0 |  |  |
