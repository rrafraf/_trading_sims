# Strategy Matrix Comparison

| Run | Adapter | Status | Equity diff | Return diff % | Fill count diff | Notes |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `alpaca_crypto_btc_sma_cross_4_12` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0 | partial volume-limited fill at 2024-01-01T12:00:00+00:00: requested 0.01000000, filled 0.00042350 | partial volume-limited fill at 2024-01-01T13:00:00+00:00: requested 0.00957650, filled 0.00013733 |
| `alpaca_crypto_btc_sma_cross_4_12` | `backtrader` | `match` | -0.000000 | -0.000000 | 0 | Backtrader volume filler enabled with FixedSize(size=None) |
| `alpaca_crypto_btc_sma_cross_4_12` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0 | partial volume-limited fill at 2024-01-01T12:00:00+00:00: requested 0.01000000, filled 0.00042350 | partial volume-limited fill at 2024-01-01T13:00:00+00:00: requested 0.00957650, filled 0.00013733 |
| `alpaca_crypto_btc_sma_cross_4_12` | `pybroker` | `match` | 0.000000 | 0.000000 | 0 | partial volume-limited fill at 2024-01-01T12:00:00+00:00: requested 0.01000000, filled 0.00042350 | partial volume-limited fill at 2024-01-01T13:00:00+00:00: requested 0.00957650, filled 0.00013733 |
| `alpaca_crypto_btc_sma_cross_4_12` | `lean` | `unavailable` | -25.615276 | -0.025615 | -4 | UNAVAILABLE: LEAN adapter slot is present, but v1 has not generated a LEAN algorithm project/config from AdapterContext yet | LEAN is still a first-wave target because it has the strongest all-around broker/order model surface. | Next implementation step: generate a minimal C#/Python LEAN algorithm that reads canonical CSV bars and emits normalized fills. |
| `sim_daily_breakout_6` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0 |  |
| `sim_daily_breakout_6` | `backtrader` | `match` | 0.000000 | 0.000000 | 0 | Backtrader volume filler enabled with FixedSize(size=None) |
| `sim_daily_breakout_6` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0 |  |
| `sim_daily_breakout_6` | `pybroker` | `match` | 0.000000 | 0.000000 | 0 |  |
| `sim_daily_breakout_6` | `lean` | `unavailable` | 0.000000 | 0.000000 | 0 | UNAVAILABLE: LEAN adapter slot is present, but v1 has not generated a LEAN algorithm project/config from AdapterContext yet | LEAN is still a first-wave target because it has the strongest all-around broker/order model surface. | Next implementation step: generate a minimal C#/Python LEAN algorithm that reads canonical CSV bars and emits normalized fills. |
| `sim_daily_buy_hold` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0 |  |
| `sim_daily_buy_hold` | `backtrader` | `match` | 0.000000 | 0.000000 | 0 | Backtrader volume filler enabled with FixedSize(size=None) |
| `sim_daily_buy_hold` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0 |  |
| `sim_daily_buy_hold` | `pybroker` | `match` | 0.000000 | 0.000000 | 0 |  |
| `sim_daily_buy_hold` | `lean` | `unavailable` | 181.431199 | 0.181431 | -1 | UNAVAILABLE: LEAN adapter slot is present, but v1 has not generated a LEAN algorithm project/config from AdapterContext yet | LEAN is still a first-wave target because it has the strongest all-around broker/order model surface. | Next implementation step: generate a minimal C#/Python LEAN algorithm that reads canonical CSV bars and emits normalized fills. |
| `sim_daily_sma_cross_3_8` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0 |  |
| `sim_daily_sma_cross_3_8` | `backtrader` | `match` | 0.000000 | 0.000000 | 0 | Backtrader volume filler enabled with FixedSize(size=None) |
| `sim_daily_sma_cross_3_8` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0 |  |
| `sim_daily_sma_cross_3_8` | `pybroker` | `match` | 0.000000 | 0.000000 | 0 |  |
| `sim_daily_sma_cross_3_8` | `lean` | `unavailable` | 0.000000 | 0.000000 | 0 | UNAVAILABLE: LEAN adapter slot is present, but v1 has not generated a LEAN algorithm project/config from AdapterContext yet | LEAN is still a first-wave target because it has the strongest all-around broker/order model surface. | Next implementation step: generate a minimal C#/Python LEAN algorithm that reads canonical CSV bars and emits normalized fills. |
| `sim_edge_buy_hold` | `reference_bar` | `baseline` | 0.000000 | 0.000000 | 0 | zero-volume bar for SIM at 2024-01-03T14:31:00+00:00 | deferred fill on zero-volume bar at 2024-01-03T14:31:00+00:00 |
| `sim_edge_buy_hold` | `backtrader` | `match` | -0.000000 | -0.000000 | 0 | zero-volume bar for SIM at 2024-01-03T14:31:00+00:00 | Backtrader volume filler enabled with FixedSize(size=None) |
| `sim_edge_buy_hold` | `vectorbt` | `match` | 0.000000 | 0.000000 | 0 | zero-volume bar for SIM at 2024-01-03T14:31:00+00:00 | deferred fill on zero-volume bar at 2024-01-03T14:31:00+00:00 |
| `sim_edge_buy_hold` | `pybroker` | `match` | 0.000000 | 0.000000 | 0 | zero-volume bar for SIM at 2024-01-03T14:31:00+00:00 | deferred fill on zero-volume bar at 2024-01-03T14:31:00+00:00 |
| `sim_edge_buy_hold` | `lean` | `unavailable` | 5058.001700 | 5.058002 | -1 | zero-volume bar for SIM at 2024-01-03T14:31:00+00:00 | UNAVAILABLE: LEAN adapter slot is present, but v1 has not generated a LEAN algorithm project/config from AdapterContext yet | LEAN is still a first-wave target because it has the strongest all-around broker/order model surface. |
