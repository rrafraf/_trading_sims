# Strategy Matrix Results

| Run | Adapter | Strategy | Symbol | Final equity | Return % | Fills | Signals | Notes |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `sim_daily_buy_hold` | `reference_bar` | `buy_hold` | `SIM` | 99818.57 | -0.1814 | 1 | 1 |  |
| `sim_daily_buy_hold` | `backtrader` | `buy_hold` | `SIM` | 99818.57 | -0.1814 | 1 | 1 | Backtrader volume filler enabled with FixedSize(size=None) |
| `sim_daily_buy_hold` | `vectorbt` | `buy_hold` | `SIM` | 99818.57 | -0.1814 | 1 | 1 |  |
| `sim_daily_buy_hold` | `pybroker` | `buy_hold` | `SIM` | 99818.57 | -0.1814 | 1 | 1 |  |
| `sim_daily_buy_hold` | `lean` | `buy_hold` | `SIM` | 100000.00 | 0.0000 | 0 | 1 | UNAVAILABLE: LEAN adapter slot is present, but v1 has not generated a LEAN algorithm project/config from AdapterContext yet<br>LEAN is still a first-wave target because it has the strongest all-around broker/order model surface.<br>Next implementation step: generate a minimal C#/Python LEAN algorithm that reads canonical CSV bars and emits normalized fills. |
| `sim_daily_sma_cross_3_8` | `reference_bar` | `sma_cross` | `SIM` | 100000.00 | 0.0000 | 0 | 1 |  |
| `sim_daily_sma_cross_3_8` | `backtrader` | `sma_cross` | `SIM` | 100000.00 | 0.0000 | 0 | 1 | Backtrader volume filler enabled with FixedSize(size=None) |
| `sim_daily_sma_cross_3_8` | `vectorbt` | `sma_cross` | `SIM` | 100000.00 | 0.0000 | 0 | 1 |  |
| `sim_daily_sma_cross_3_8` | `pybroker` | `sma_cross` | `SIM` | 100000.00 | 0.0000 | 0 | 1 |  |
| `sim_daily_sma_cross_3_8` | `lean` | `sma_cross` | `SIM` | 100000.00 | 0.0000 | 0 | 1 | UNAVAILABLE: LEAN adapter slot is present, but v1 has not generated a LEAN algorithm project/config from AdapterContext yet<br>LEAN is still a first-wave target because it has the strongest all-around broker/order model surface.<br>Next implementation step: generate a minimal C#/Python LEAN algorithm that reads canonical CSV bars and emits normalized fills. |
| `sim_daily_breakout_6` | `reference_bar` | `breakout_channel` | `SIM` | 100000.00 | 0.0000 | 0 | 0 |  |
| `sim_daily_breakout_6` | `backtrader` | `breakout_channel` | `SIM` | 100000.00 | 0.0000 | 0 | 0 | Backtrader volume filler enabled with FixedSize(size=None) |
| `sim_daily_breakout_6` | `vectorbt` | `breakout_channel` | `SIM` | 100000.00 | 0.0000 | 0 | 0 |  |
| `sim_daily_breakout_6` | `pybroker` | `breakout_channel` | `SIM` | 100000.00 | 0.0000 | 0 | 0 |  |
| `sim_daily_breakout_6` | `lean` | `breakout_channel` | `SIM` | 100000.00 | 0.0000 | 0 | 0 | UNAVAILABLE: LEAN adapter slot is present, but v1 has not generated a LEAN algorithm project/config from AdapterContext yet<br>LEAN is still a first-wave target because it has the strongest all-around broker/order model surface.<br>Next implementation step: generate a minimal C#/Python LEAN algorithm that reads canonical CSV bars and emits normalized fills. |
| `sim_edge_buy_hold` | `reference_bar` | `buy_hold` | `SIM` | 94942.00 | -5.0580 | 1 | 1 | zero-volume bar for SIM at 2024-01-03T14:31:00+00:00<br>deferred fill on zero-volume bar at 2024-01-03T14:31:00+00:00 |
| `sim_edge_buy_hold` | `backtrader` | `buy_hold` | `SIM` | 94942.00 | -5.0580 | 1 | 1 | zero-volume bar for SIM at 2024-01-03T14:31:00+00:00<br>Backtrader volume filler enabled with FixedSize(size=None) |
| `sim_edge_buy_hold` | `vectorbt` | `buy_hold` | `SIM` | 94942.00 | -5.0580 | 1 | 1 | zero-volume bar for SIM at 2024-01-03T14:31:00+00:00<br>deferred fill on zero-volume bar at 2024-01-03T14:31:00+00:00 |
| `sim_edge_buy_hold` | `pybroker` | `buy_hold` | `SIM` | 94942.00 | -5.0580 | 1 | 1 | zero-volume bar for SIM at 2024-01-03T14:31:00+00:00<br>deferred fill on zero-volume bar at 2024-01-03T14:31:00+00:00 |
| `sim_edge_buy_hold` | `lean` | `buy_hold` | `SIM` | 100000.00 | 0.0000 | 0 | 1 | zero-volume bar for SIM at 2024-01-03T14:31:00+00:00<br>UNAVAILABLE: LEAN adapter slot is present, but v1 has not generated a LEAN algorithm project/config from AdapterContext yet<br>LEAN is still a first-wave target because it has the strongest all-around broker/order model surface.<br>Next implementation step: generate a minimal C#/Python LEAN algorithm that reads canonical CSV bars and emits normalized fills. |
| `alpaca_crypto_btc_sma_cross_4_12` | `reference_bar` | `sma_cross` | `BTC/USD` | 100025.62 | 0.0256 | 4 | 2 | partial volume-limited fill at 2024-01-01T12:00:00+00:00: requested 0.01000000, filled 0.00042350<br>partial volume-limited fill at 2024-01-01T13:00:00+00:00: requested 0.00957650, filled 0.00013733 |
| `alpaca_crypto_btc_sma_cross_4_12` | `backtrader` | `sma_cross` | `BTC/USD` | 100025.62 | 0.0256 | 4 | 2 | Backtrader volume filler enabled with FixedSize(size=None) |
| `alpaca_crypto_btc_sma_cross_4_12` | `vectorbt` | `sma_cross` | `BTC/USD` | 100025.62 | 0.0256 | 4 | 2 | partial volume-limited fill at 2024-01-01T12:00:00+00:00: requested 0.01000000, filled 0.00042350<br>partial volume-limited fill at 2024-01-01T13:00:00+00:00: requested 0.00957650, filled 0.00013733 |
| `alpaca_crypto_btc_sma_cross_4_12` | `pybroker` | `sma_cross` | `BTC/USD` | 100025.62 | 0.0256 | 4 | 2 | partial volume-limited fill at 2024-01-01T12:00:00+00:00: requested 0.01000000, filled 0.00042350<br>partial volume-limited fill at 2024-01-01T13:00:00+00:00: requested 0.00957650, filled 0.00013733 |
| `alpaca_crypto_btc_sma_cross_4_12` | `lean` | `sma_cross` | `BTC/USD` | 100000.00 | 0.0000 | 0 | 2 | UNAVAILABLE: LEAN adapter slot is present, but v1 has not generated a LEAN algorithm project/config from AdapterContext yet<br>LEAN is still a first-wave target because it has the strongest all-around broker/order model surface.<br>Next implementation step: generate a minimal C#/Python LEAN algorithm that reads canonical CSV bars and emits normalized fills. |
