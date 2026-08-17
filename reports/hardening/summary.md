# Experiment Summary

This batch uses these adapters: `reference_bar`, `backtrader`, `muni`, `pybroker`, `vectorbt`.

## Adapter Agreement

| Adapter | Baseline | Match | Policy diff | Diff | Unavailable |
| --- | ---: | ---: | ---: | ---: | ---: |
| `backtrader` | 0 | 7 | 0 | 0 | 0 |
| `muni` | 0 | 6 | 1 | 0 | 0 |
| `pybroker` | 0 | 6 | 0 | 1 | 0 |
| `reference_bar` | 7 | 0 | 0 | 0 | 0 |
| `vectorbt` | 0 | 7 | 0 | 0 | 0 |

## Runs

| Run | reference_bar return % | backtrader return % | muni return % | pybroker return % | vectorbt return % |
| --- | ---: | ---: | ---: | ---: | ---: |
| `bad_data_1m_quality_notes` | 0.0084 | 0.0084 | 0.0084 | 0.0113 | 0.0084 |
| `churn_noise_1m_flip_5_high_cost` | -0.5001 | -0.5001 | -0.5001 | -0.5001 | -0.5001 |
| `gap_open_1m_scheduled_entry_exit` | 0.0178 | 0.0178 | 0.0178 | 0.0178 | 0.0178 |
| `last_bar_signal_no_next_fill` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `liquidity_zero_volume_defer` | 0.0105 | 0.0105 | 0.0105 | 0.0105 | 0.0105 |
| `partial_volume_1m_scheduled_100` | -0.0287 | -0.0287 | -0.0287 | -0.0287 | -0.0287 |
| `short_round_trip_scheduled` | -0.0455 | -0.0455 | -0.0455 | -0.0455 | -0.0455 |
