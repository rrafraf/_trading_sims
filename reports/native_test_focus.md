# Native Test Focus

This report scans test files for terms associated with execution edge cases. It is a triage signal, not proof of correctness.

| Rank | Candidate | Score | Test files | Topics | Fill/order | Book/queue | Latency/time | Data quality | Fees/costs |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | [Lean](../candidates/Lean) | 156 | 818 | 12 | 1221 | 78 | 51 | 814 | 269 |
| 2 | [nautilus_trader](../candidates/nautilus_trader) | 156 | 327 | 12 | 693 | 105 | 162 | 174 | 92 |
| 3 | [freqtrade](../candidates/freqtrade) | 150 | 139 | 12 | 197 | 13 | 49 | 80 | 45 |
| 4 | [quantreplay](../candidates/quantreplay) | 148 | 380 | 12 | 377 | 79 | 54 | 45 | 2 |
| 5 | [basana](../candidates/basana) | 136 | 60 | 12 | 107 | 16 | 11 | 21 | 11 |
| 6 | [zipline-reloaded](../candidates/zipline-reloaded) | 133 | 97 | 11 | 121 | 5 | 57 | 65 | 6 |
| 7 | [pyalgotrade](../candidates/pyalgotrade) | 126 | 55 | 12 | 92 | 2 | 1 | 21 | 31 |
| 8 | [jesse](../candidates/jesse) | 117 | 53 | 10 | 55 | 2 | 15 | 25 | 17 |
| 9 | [rqalpha](../candidates/rqalpha) | 114 | 52 | 11 | 73 | 1 | 3 | 12 | 10 |
| 10 | [qlib](../candidates/qlib) | 104 | 43 | 11 | 34 | 4 | 5 | 18 | 6 |
| 11 | [tensortrade](../candidates/tensortrade) | 97 | 76 | 9 | 43 | 0 | 8 | 6 | 27 |
| 12 | [tradingenv](../candidates/tradingenv) | 97 | 33 | 11 | 9 | 2 | 6 | 12 | 6 |
| 13 | [vectorbt](../candidates/vectorbt) | 86 | 16 | 10 | 24 | 1 | 8 | 14 | 4 |
| 14 | [qstrader](../candidates/qstrader) | 81 | 30 | 10 | 15 | 1 | 24 | 1 | 8 |
| 15 | [blankly](../candidates/blankly) | 77 | 19 | 11 | 26 | 1 | 4 | 6 | 3 |
| 16 | [pybroker](../candidates/pybroker) | 77 | 16 | 10 | 19 | 0 | 5 | 6 | 4 |
| 17 | [abides-jpmc-public](../candidates/abides-jpmc-public) | 70 | 22 | 7 | 31 | 12 | 1 | 4 | 0 |
| 18 | [backtrader](../candidates/backtrader) | 62 | 83 | 7 | 92 | 0 | 4 | 3 | 8 |
| 19 | [bt](../candidates/bt) | 44 | 6 | 9 | 2 | 2 | 1 | 2 | 3 |
| 20 | [FinRL](../candidates/FinRL) | 27 | 6 | 6 | 1 | 0 | 1 | 0 | 1 |
| 21 | [hftbacktest](../candidates/hftbacktest) | 16 | 1 | 4 | 2 | 1 | 1 | 0 | 0 |
| 22 | [vnpy](../candidates/vnpy) | 16 | 4 | 4 | 0 | 1 | 1 | 1 | 0 |
| 23 | [abides](../candidates/abides) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 24 | [gym-anytrading](../candidates/gym-anytrading) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 25 | [gym-trading-env](../candidates/gym-trading-env) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Sample Matching Test Files

### Lean
- `fills`: `Tests\AlgorithmRunnerResults.cs`, `Tests\Algorithm\AlgorithmAddDataTests.cs`, `Tests\Algorithm\AlgorithmAddSecurityTests.cs`, `Tests\Algorithm\AlgorithmChainsTests.cs`, `Tests\Algorithm\AlgorithmHistoryTests.cs`
- `order_lifecycle`: `Algorithm.CSharp\UniverseSelectionSymbolCacheRemovalRegressionTest.cs`, `Common\Api\OptimizationBacktest.cs`, `Optimizer\Analysis\OptimizationFailedBacktests.cs`, `Tests\AlgorithmRunner.cs`, `Tests\Algorithm\AlgorithmAddDataTests.cs`
- `queue_orderbook`: `Tests\AlgorithmRunner.cs`, `Tests\Algorithm\AlgorithmAddDataTests.cs`, `Tests\Algorithm\AlgorithmAddUniverseTests.cs`, `Tests\Algorithm\AlgorithmHistoryTests.cs`, `Tests\Algorithm\AlgorithmIndicatorsTests.cs`
- `latency_time`: `Tests\Algorithm\AlgorithmIndicatorsTests.cs`, `Tests\Algorithm\Framework\Alphas\Serialization\InsightJsonConverterTests.cs`, `Tests\Algorithm\Framework\Portfolio\ReturnsSymbolDataTests.cs`, `Tests\Api\ObjectStoreTests.cs`, `Tests\Api\ProjectTests.cs`
- `slippage_impact`: `Tests\Algorithm\AlgorithmAddSecurityTests.cs`, `Tests\Algorithm\AlgorithmSetBrokerageTests.cs`, `Tests\Algorithm\Framework\Execution\SpreadExecutionModelTests.cs`, `Tests\Algorithm\Framework\Portfolio\PortfolioTargetCollectionTests.cs`, `Tests\Brokerages\ComboLimitOrderTestParameters.cs`
- `fees_costs`: `Algorithm.CSharp\UniverseSelectionSymbolCacheRemovalRegressionTest.cs`, `Tests\AlgorithmRunner.cs`, `Tests\Algorithm\AlgorithmAddDataTests.cs`, `Tests\Algorithm\AlgorithmAddSecurityTests.cs`, `Tests\Algorithm\AlgorithmAddUniverseTests.cs`
- `data_quality`: `Algorithm.CSharp\UniverseSelectionSymbolCacheRemovalRegressionTest.cs`, `Common\Api\Backtest.cs`, `Common\Api\OptimizationBacktest.cs`, `Optimizer\Analysis\OptimizationFailedBacktests.cs`, `Tests\AlgorithmFactory\LoaderTests.cs`
- `agent_rl`: `Tests\AlgorithmRunner.cs`, `Tests\Algorithm\AlgorithmAddSecurityTests.cs`, `Tests\Algorithm\AlgorithmHistoryTests.cs`, `Tests\Algorithm\AlgorithmLiveTradingTests.cs`, `Tests\Algorithm\AlgorithmNamingTests.cs`

### nautilus_trader
- `fills`: `crates\adapters\architect_ax\tests\common\server.rs`, `crates\adapters\architect_ax\tests\exec_client.rs`, `crates\adapters\architect_ax\tests\http.rs`, `crates\adapters\betfair\tests\README.md`, `crates\adapters\betfair\tests\exec_client.rs`
- `order_lifecycle`: `crates\adapters\architect_ax\tests\common\server.rs`, `crates\adapters\architect_ax\tests\data_client.rs`, `crates\adapters\architect_ax\tests\exec_client.rs`, `crates\adapters\architect_ax\tests\http.rs`, `crates\adapters\architect_ax\tests\websocket.rs`
- `queue_orderbook`: `crates\adapters\architect_ax\tests\common\server.rs`, `crates\adapters\architect_ax\tests\data_client.rs`, `crates\adapters\architect_ax\tests\websocket.rs`, `crates\adapters\betfair\tests\README.md`, `crates\adapters\betfair\tests\data_client.rs`
- `latency_time`: `crates\adapters\architect_ax\tests\common\server.rs`, `crates\adapters\architect_ax\tests\data_client.rs`, `crates\adapters\architect_ax\tests\exec_client.rs`, `crates\adapters\architect_ax\tests\http.rs`, `crates\adapters\architect_ax\tests\websocket.rs`
- `slippage_impact`: `crates\adapters\architect_ax\tests\exec_client.rs`, `crates\adapters\bybit\tests\exec_client.rs`, `crates\adapters\coinbase\tests\exec_client.rs`, `crates\adapters\derive\tests\data_client.rs`, `crates\adapters\derive\tests\exec_client.rs`
- `fees_costs`: `crates\adapters\architect_ax\tests\exec_client.rs`, `crates\adapters\architect_ax\tests\http.rs`, `crates\adapters\betfair\tests\README.md`, `crates\adapters\betfair\tests\harness\mod.rs`, `crates\adapters\betfair\tests\live.rs`
- `data_quality`: `crates\adapters\architect_ax\tests\common\server.rs`, `crates\adapters\architect_ax\tests\data_client.rs`, `crates\adapters\architect_ax\tests\exec_client.rs`, `crates\adapters\architect_ax\tests\http.rs`, `crates\adapters\architect_ax\tests\websocket.rs`
- `agent_rl`: `crates\adapters\architect_ax\tests\exec_client.rs`, `crates\adapters\betfair\tests\data_client.rs`, `crates\adapters\betfair\tests\node.rs`, `crates\adapters\binance\tests\futures\data_client.rs`, `crates\adapters\binance\tests\futures\http.rs`

### freqtrade
- `fills`: `tests\conftest.py`, `tests\conftest_trades.py`, `tests\conftest_trades_usdt.py`, `tests\data\test_converter.py`, `tests\data\test_dataprovider.py`
- `order_lifecycle`: `ft_client\test_client\test_rest_client.py`, `tests\conftest.py`, `tests\conftest_trades.py`, `tests\conftest_trades_usdt.py`, `tests\data\test_converter.py`
- `queue_orderbook`: `tests\conftest.py`, `tests\data\test_dataprovider.py`, `tests\exchange\test_binance.py`, `tests\exchange\test_exchange.py`, `tests\exchange\test_gate.py`
- `latency_time`: `tests\commands\test_commands.py`, `tests\conftest.py`, `tests\data\test_btanalysis.py`, `tests\data\test_converter.py`, `tests\data\test_converter_orderflow.py`
- `slippage_impact`: `tests\exchange\test_exchange.py`, `tests\freqtradebot\test_freqtradebot.py`, `tests\optimize\test_backtesting.py`, `tests\plugins\test_pairlist.py`
- `fees_costs`: `tests\commands\test_commands.py`, `tests\conftest.py`, `tests\conftest_trades.py`, `tests\conftest_trades_usdt.py`, `tests\data\test_btanalysis.py`
- `data_quality`: `ft_client\test_client\test_rest_client.py`, `tests\commands\test_build_config.py`, `tests\commands\test_commands.py`, `tests\conftest.py`, `tests\conftest_hyperopt.py`
- `agent_rl`: `tests\conftest.py`, `tests\exchange\test_kraken.py`, `tests\freqai\conftest.py`, `tests\freqai\test_freqai_datadrawer.py`, `tests\freqai\test_models\ReinforcementLearner_test_3ac.py`

### quantreplay
- `fills`: `project\core\tests\unit_tests\common\attributes_tests.cpp`, `project\core\tests\unit_tests\common\json\attributes_tests.cpp`, `project\core\tests\unit_tests\domain\enumerators_tests.cpp`, `project\data_layer\tests\unit_tests\converters\column_mapping_tests.cpp`, `project\data_layer\tests\unit_tests\inspectors\datasource_inspectors_tests.cpp`
- `order_lifecycle`: `project\core\tests\unit_tests\common\attributes_tests.cpp`, `project\core\tests\unit_tests\common\json\attributes_tests.cpp`, `project\core\tests\unit_tests\domain\enumerators_tests.cpp`, `project\data_layer\tests\unit_tests\converters\column_mapping_tests.cpp`, `project\data_layer\tests\unit_tests\inspectors\datasource_inspectors_tests.cpp`
- `queue_orderbook`: `project\data_layer\tests\unit_tests\converters\column_mapping_tests.cpp`, `project\data_layer\tests\unit_tests\inspectors\datasource_inspectors_tests.cpp`, `project\data_layer\tests\unit_tests\inspectors\listing_inspectors_tests.cpp`, `project\data_layer\tests\unit_tests\models\datasource_tests.cpp`, `project\data_layer\tests\unit_tests\models\listing_tests.cpp`
- `latency_time`: `project\core\tests\test_definitions\test_attributes.hpp`, `project\core\tests\unit_tests\common\attributes_tests.cpp`, `project\core\tests\unit_tests\common\json\attribute_tests.cpp`, `project\core\tests\unit_tests\common\json\attributes_tests.cpp`, `project\core\tests\unit_tests\tools\time_tests.cpp`
- `slippage_impact`: `project\core\tests\unit_tests\domain\enumerators_tests.cpp`, `project\data_layer\tests\unit_tests\inspectors\listing_inspectors_tests.cpp`, `project\data_layer\tests\unit_tests\models\listing_tests.cpp`, `project\data_layer\tests\unit_tests\pqxx\common\column_resolver_tests.cpp`, `project\fix\common\tests\unit_tests\mapping\from_fix_conversion_tests.cpp`
- `fees_costs`: `project\http\tests\test_utils\processors.hpp`, `project\trading_system\components\matching_engine\tests\unit_tests\orders\order_system_facade_tests.cpp`
- `data_quality`: `project\core\tests\unit_tests\common\json\type_tests.cpp`, `project\core\tests\unit_tests\domain\enumerators_tests.cpp`, `project\core\tests\unit_tests\tools\numeric_round_to_tick_tests.cpp`, `project\core\tests\unit_tests\tools\numeric_tests.cpp`, `project\data_layer\tests\unit_tests\models\datasource_tests.cpp`
- `agent_rl`: `project\core\tests\unit_tests\domain\enumerators_tests.cpp`, `project\data_layer\tests\unit_tests\common\database\ping_agent_tests.cpp`, `project\data_layer\tests\unit_tests\common\queries\data_extractor_tests.cpp`, `project\data_layer\tests\unit_tests\pqxx\database\connection_abort_timer_tests.cpp`, `project\data_layer\tests\unit_tests\pqxx\database\transaction_tests.cpp`

### basana
- `fills`: `tests\backtesting_exchange_orders_test_data.py`, `tests\fixtures\binance.py`, `tests\fixtures\ccxt.py`, `tests\test_backtesting_account_balances.py`, `tests\test_backtesting_exchange_orders.py`
- `order_lifecycle`: `tests\backtesting_exchange_orders_test_data.py`, `tests\fixtures\ccxt.py`, `tests\test_backtesting_account_balances.py`, `tests\test_backtesting_charts.py`, `tests\test_backtesting_dispatcher.py`
- `queue_orderbook`: `tests\fixtures\ccxt.py`, `tests\test_backtesting_account_balances.py`, `tests\test_backtesting_dispatcher.py`, `tests\test_backtesting_exchange.py`, `tests\test_backtesting_exchange_auto_lending.py`
- `latency_time`: `tests\test_backtesting_exchange_loans.py`, `tests\test_binance_bars.py`, `tests\test_binance_user_data.py`, `tests\test_bitstamp_bars.py`, `tests\test_bitstamp_client.py`
- `slippage_impact`: `tests\test_backtesting_account_balances.py`, `tests\test_backtesting_exchange_orders.py`, `tests\test_backtesting_liquidity.py`, `tests\test_backtesting_margin.py`, `tests\test_backtesting_orders.py`
- `fees_costs`: `tests\backtesting_exchange_orders_test_data.py`, `tests\fixtures\ccxt.py`, `tests\test_backtesting_exchange.py`, `tests\test_backtesting_exchange_auto_lending.py`, `tests\test_backtesting_exchange_orders.py`
- `data_quality`: `tests\conftest.py`, `tests\fixtures\binance.py`, `tests\fixtures\ccxt.py`, `tests\helpers.py`, `tests\test_backtesting_dispatcher.py`
- `agent_rl`: `tests\test_backtesting_exchange_auto_lending.py`, `tests\test_binance_exchange_cross_margin.py`, `tests\test_binance_exchange_spot.py`, `tests\test_bitstamp_exchange.py`

### zipline-reloaded
- `fills`: `src\zipline\test_algorithms.py`, `tests\data\bundles\test_csvdir.py`, `tests\data\bundles\test_quandl.py`, `tests\data\test_fx.py`, `tests\data\test_resample.py`
- `order_lifecycle`: `src\zipline\sources\test_source.py`, `src\zipline\test_algorithms.py`, `tests\conftest.py`, `tests\data\test_fx.py`, `tests\data\test_minute_bars.py`
- `queue_orderbook`: `tests\pipeline\test_domain.py`, `tests\pipeline\test_engine.py`, `tests\pipeline\test_hooks.py`, `tests\test_algorithm.py`, `tests\test_bar_data.py`
- `latency_time`: `src\zipline\sources\test_source.py`, `tests\conftest.py`, `tests\data\bundles\test_core.py`, `tests\data\bundles\test_csvdir.py`, `tests\data\bundles\test_quandl.py`
- `slippage_impact`: `src\zipline\test_algorithms.py`, `tests\finance\test_commissions.py`, `tests\finance\test_slippage.py`, `tests\metrics\test_metrics.py`, `tests\test_algorithm.py`
- `fees_costs`: `src\zipline\test_algorithms.py`, `tests\finance\test_commissions.py`, `tests\metrics\test_metrics.py`, `tests\test_algorithm.py`, `tests\test_blotter.py`
- `data_quality`: `src\zipline\test_algorithms.py`, `tests\conftest.py`, `tests\data\bundles\test_core.py`, `tests\data\bundles\test_csvdir.py`, `tests\data\bundles\test_quandl.py`
- `agent_rl`: `src\zipline\test_algorithms.py`, `tests\conftest.py`, `tests\data\bundles\test_core.py`, `tests\data\bundles\test_csvdir.py`, `tests\data\bundles\test_quandl.py`

### pyalgotrade
- `fills`: `testcases\bitstamp_test.py`, `testcases\broker_backtesting_test.py`, `testcases\broker_test.py`, `testcases\dataseries_test.py`, `testcases\dbfeed_test.py`
- `order_lifecycle`: `testcases\barfeed_test.py`, `testcases\bitstamp_test.py`, `testcases\broker_backtesting_test.py`, `testcases\broker_test.py`, `testcases\doc_test.py`
- `queue_orderbook`: `testcases\bitstamp_test.py`, `testcases\doc_test.py`
- `latency_time`: `testcases\utils_test.py`
- `slippage_impact`: `testcases\returns_analyzer_test.py`, `testcases\slippage_model_test.py`
- `fees_costs`: `testcases\barfeed_test.py`, `testcases\bitstamp_test.py`, `testcases\broker_backtesting_test.py`, `testcases\btcharts_test.py`, `testcases\csvfeed_test.py`
- `data_quality`: `testcases\broker_backtesting_test.py`, `testcases\csvfeed_test.py`, `testcases\dbfeed_test.py`, `testcases\doc_test.py`, `testcases\eventprofiler_test.py`
- `agent_rl`: `testcases\bitstamp_test.py`, `testcases\broker_backtesting_test.py`, `testcases\broker_test.py`, `testcases\drawdown_analyzer_test.py`, `testcases\fill_strategy_test.py`

### jesse
- `fills`: `tests\test_broker.py`, `tests\test_config_safety.py`, `tests\test_helpers.py`, `tests\test_import_candles.py`, `tests\test_import_candles_workflow.py`
- `order_lifecycle`: `jesse\mcp\tools\services\significance_test.py`, `jesse\mcp\tools\significance_test.py`, `tests\data\test_candles_indicators.py`, `tests\test_backtest_session_chart_data.py`, `tests\test_broker.py`
- `queue_orderbook`: `tests\test_helpers.py`, `tests\test_state_orderbook.py`
- `latency_time`: `tests\test_backtest.py`, `tests\test_candle_service.py`, `tests\test_candle_timeframe_filter.py`, `tests\test_e2e_database.py`, `tests\test_helpers.py`
- `fees_costs`: `jesse\mcp\tools\services\significance_test.py`, `tests\test_broker.py`, `tests\test_completed_trade.py`, `tests\test_config_safety.py`, `tests\test_exchange.py`
- `data_quality`: `jesse\mcp\tools\services\significance_test.py`, `jesse\mcp\tools\significance_test.py`, `tests\data\test_candles_indicators.py`, `tests\test_backtest_session_chart_data.py`, `tests\test_candle_service.py`
- `agent_rl`: `jesse\mcp\tools\services\significance_test.py`, `jesse\mcp\tools\significance_test.py`, `tests\test_e2e_database.py`, `tests\test_mcp_resources.py`, `tests\test_rule_significance_testing.py`

### rqalpha
- `fills`: `rqalpha\examples\extend_api\test_extend_api.py`, `tests\integration_tests\test_api\mod\sys_analyser\test_negative_benchmark.py`, `tests\integration_tests\test_api\mod\sys_simulation\test_simulation_broker.py`, `tests\integration_tests\test_api\test_api_base.py`, `tests\integration_tests\test_api\test_api_future.py`
- `order_lifecycle`: `rqalpha\examples\test_pt.py`, `tests\integration_tests\conftest.py`, `tests\integration_tests\test_api\mod\sys_accounts\test_account_model.py`, `tests\integration_tests\test_api\mod\sys_accounts\test_margin_stocks.py`, `tests\integration_tests\test_api\mod\sys_accounts\test_position_models.py`
- `queue_orderbook`: `tests\integration_tests\test_api\test_position_queue.py`
- `latency_time`: `tests\test_bundle\test_daybar.py`, `tests\test_bundle\test_daybar_checker.py`, `tests\unittest\test_mod\test_sys_accounts\test_api\test_order_target_portfolio_smart_api_unittest.py`
- `slippage_impact`: `tests\integration_tests\test_backtest_results\test_f_mean_reverting.py`, `tests\integration_tests\test_backtest_results\test_f_tick_size.py`, `tests\integration_tests\test_backtest_results\test_s_tick_size.py`, `tests\unittest\test_mod\test_sys_simulation\test_matcher.py`
- `fees_costs`: `tests\integration_tests\test_api\mod\sys_accounts\test_futures_settlement_price_type.py`, `tests\integration_tests\test_api\mod\sys_accounts\test_position_models.py`, `tests\integration_tests\test_api\mod\sys_simulation\test_management_fee.py`, `tests\integration_tests\test_api\mod\sys_transaction_cost\test_commission_multiplier.py`, `tests\integration_tests\test_api\test_config.py`
- `data_quality`: `tests\integration_tests\conftest.py`, `tests\integration_tests\test_api\mod\sys_accounts\test_account_model.py`, `tests\integration_tests\test_api\mod\sys_accounts\test_futures_settlement_price_type.py`, `tests\integration_tests\test_api\mod\sys_accounts\test_margin_stocks.py`, `tests\integration_tests\test_api\mod\sys_accounts\test_position_models.py`
- `agent_rl`: `tests\integration_tests\test_api\mod\sys_accounts\test_futures_settlement_price_type.py`, `tests\integration_tests\test_api\mod\sys_accounts\test_position_models.py`, `tests\integration_tests\test_api\mod\sys_analyser\test_negative_benchmark.py`, `tests\integration_tests\test_api\mod\sys_simulation\test_signal_broker.py`, `tests\integration_tests\test_api\mod\sys_transaction_cost\test_commission_multiplier.py`

### qlib
- `fills`: `tests\backtest\test_high_freq_trading.py`, `tests\backtest\test_soft_topk_strategy.py`, `tests\backtest\test_soft_topk_strategy_cold_start.py`, `tests\data_mid_layer_tests\test_dataloader.py`, `tests\data_mid_layer_tests\test_dataset.py`
- `order_lifecycle`: `tests\backtest\test_file_strategy.py`, `tests\backtest\test_high_freq_trading.py`, `tests\misc\test_index_data.py`, `tests\misc\test_utils.py`, `tests\rl\test_logger.py`
- `queue_orderbook`: `qlib\tests\config.py`, `tests\backtest\test_high_freq_trading.py`, `tests\rl\test_data_queue.py`, `tests\rl\test_logger.py`
- `latency_time`: `tests\misc\test_index_data.py`, `tests\misc\test_utils.py`, `tests\rl\test_qlib_simulator.py`, `tests\rl\test_saoe_simple.py`, `tests\test_dump_data.py`
- `slippage_impact`: `tests\backtest\test_soft_topk_strategy.py`, `tests\backtest\test_soft_topk_strategy_cold_start.py`
- `fees_costs`: `tests\backtest\test_file_strategy.py`, `tests\backtest\test_high_freq_trading.py`, `tests\backtest\test_soft_topk_strategy.py`, `tests\backtest\test_soft_topk_strategy_cold_start.py`, `tests\rl\test_qlib_simulator.py`
- `data_quality`: `qlib\tests\data.py`, `qlib\tests\test_config_validation.py`, `tests\backtest\test_file_strategy.py`, `tests\data_mid_layer_tests\test_dataloader.py`, `tests\data_mid_layer_tests\test_dataset.py`
- `agent_rl`: `tests\rl\test_finite_env.py`, `tests\rl\test_logger.py`, `tests\rl\test_qlib_simulator.py`, `tests\rl\test_saoe_simple.py`, `tests\rl\test_trainer.py`

### tensortrade
- `fills`: `tests\tensortrade\integration\rllib\test_checkpoint.py`, `tests\tensortrade\integration\rllib\test_env_creation.py`, `tests\tensortrade\integration\rllib\test_ray_training.py`, `tests\tensortrade\integration\test_end_to_end.py`, `tests\tensortrade\unit\feed\api\float\test_imputations.py`
- `order_lifecycle`: `tests\tensortrade\integration\rllib\test_checkpoint.py`, `tests\tensortrade\integration\rllib\test_env_creation.py`, `tests\tensortrade\integration\rllib\test_ray_training.py`, `tests\tensortrade\integration\test_end_to_end.py`, `tests\tensortrade\unit\base\test_registry.py`
- `latency_time`: `tests\tensortrade\unit\base\test_clock.py`, `tests\tensortrade\unit\oms\orders\criteria\test_compound.py`, `tests\tensortrade\unit\oms\orders\criteria\test_timed.py`, `tests\tensortrade\unit\oms\orders\test_order.py`, `tests\tensortrade\unit\oms\orders\test_order_listener.py`
- `fees_costs`: `tests\tensortrade\integration\rllib\test_checkpoint.py`, `tests\tensortrade\integration\rllib\test_env_creation.py`, `tests\tensortrade\integration\rllib\test_ray_training.py`, `tests\tensortrade\integration\test_end_to_end.py`, `tests\tensortrade\unit\feed\api\float\test_accumulators.py`
- `data_quality`: `tests\tensortrade\unit\feed\api\float\test_accumulators.py`, `tests\tensortrade\unit\feed\api\float\test_imputations.py`, `tests\tensortrade\unit\feed\api\float\test_utils.py`, `tests\tensortrade\unit\feed\api\float\window\test_ewm.py`, `tests\tensortrade\unit\feed\api\float\window\test_expanding.py`
- `agent_rl`: `tests\tensortrade\integration\rllib\conftest.py`, `tests\tensortrade\integration\rllib\test_checkpoint.py`, `tests\tensortrade\integration\rllib\test_env_creation.py`, `tests\tensortrade\integration\rllib\test_ray_training.py`, `tests\tensortrade\integration\test_end_to_end.py`

### tradingenv
- `fills`: `tests\integration\test_transmitter.py`, `tests\notebooks\test_notebooks.py`
- `order_lifecycle`: `tests\integration\test_transmitter.py`, `tests\notebooks\test_notebooks.py`, `tests\unit\test_exchange.py`, `tests\unit\test_transmitter.py`
- `queue_orderbook`: `tests\integration\test_transmitter.py`, `tests\unit\test_exchange.py`
- `latency_time`: `tests\examples\test_readme.py`, `tests\integration\test_env.py`, `tests\integration\test_track_record.py`, `tests\integration\test_transmitter.py`, `tests\unit\test_library.py`
- `slippage_impact`: `tests\examples\test_readme.py`, `tests\integration\test_broker.py`, `tests\integration\test_env.py`, `tests\integration\test_transmitter.py`, `tests\regression\test_env.py`
- `fees_costs`: `tests\examples\test_readme.py`, `tests\integration\test_broker.py`, `tests\integration\test_env.py`, `tests\regression\test_env.py`, `tests\unit\test_fees.py`
- `data_quality`: `tests\examples\test_readme.py`, `tests\integration\test_broker.py`, `tests\integration\test_env.py`, `tests\integration\test_rebalancing.py`, `tests\integration\test_track_record.py`
- `agent_rl`: `tests\examples\test_readme.py`, `tests\integration\test_broker.py`, `tests\integration\test_env.py`, `tests\integration\test_features.py`, `tests\integration\test_rebalancing.py`

### vectorbt
- `fills`: `tests\test_base.py`, `tests\test_engine.py`, `tests\test_generic.py`, `tests\test_plotting.py`, `tests\test_portfolio.py`
- `order_lifecycle`: `tests\conftest.py`, `tests\test_base.py`, `tests\test_data.py`, `tests\test_engine.py`, `tests\test_generic.py`
- `queue_orderbook`: `tests\test_plotting.py`
- `latency_time`: `tests\test_data.py`, `tests\test_generic.py`, `tests\test_indicators.py`, `tests\test_portfolio.py`, `tests\test_records.py`
- `slippage_impact`: `tests\test_engine.py`, `tests\test_portfolio.py`, `tests\test_records.py`
- `fees_costs`: `tests\test_engine.py`, `tests\test_plotting.py`, `tests\test_portfolio.py`, `tests\test_records.py`
- `data_quality`: `tests\conftest.py`, `tests\test_base.py`, `tests\test_data.py`, `tests\test_engine.py`, `tests\test_generic.py`
- `agent_rl`: `tests\test_plotting.py`

### qstrader
- `fills`: `tests\integration\portcon\test_pcm_e2e.py`, `tests\integration\trading\test_backtest_e2e.py`, `tests\unit\broker\portfolio\test_position.py`, `tests\unit\portcon\test_pcm.py`
- `order_lifecycle`: `tests\conftest.py`, `tests\integration\portcon\test_pcm_e2e.py`, `tests\integration\trading\test_backtest_e2e.py`, `tests\unit\broker\portfolio\test_portfolio.py`, `tests\unit\broker\portfolio\test_position.py`
- `queue_orderbook`: `tests\unit\broker\test_simulated_broker.py`
- `latency_time`: `tests\integration\portcon\test_pcm_e2e.py`, `tests\integration\trading\test_backtest_e2e.py`, `tests\unit\alpha_model\test_fixed_signals.py`, `tests\unit\alpha_model\test_single_signal.py`, `tests\unit\asset\universe\test_dynamic_universe.py`
- `fees_costs`: `tests\unit\broker\fee_model\test_percent_fee_model.py`, `tests\unit\broker\fee_model\test_zero_fee_model.py`, `tests\unit\broker\portfolio\test_portfolio.py`, `tests\unit\broker\portfolio\test_position.py`, `tests\unit\broker\portfolio\test_position_handler.py`
- `data_quality`: `tests\unit\broker\test_simulated_broker.py`
- `agent_rl`: `tests\unit\broker\portfolio\test_portfolio.py`, `tests\unit\broker\portfolio\test_position.py`, `tests\unit\broker\portfolio\test_position_handler.py`, `tests\unit\broker\test_simulated_broker.py`, `tests\unit\broker\transaction\test_transaction.py`

### blankly
- `fills`: `tests\exchanges\interfaces\alpaca\test_alpaca_interface.py`, `tests\exchanges\interfaces\alpaca\test_alpaca_interface_functional.py`, `tests\exchanges\interfaces\binance\test_binance_interface.py`, `tests\exchanges\interfaces\ftx\test_ftx_interface.py`, `tests\exchanges\test_interface_homogeneity.py`
- `order_lifecycle`: `tests\exchanges\interfaces\alpaca\test_alpaca_interface.py`, `tests\exchanges\interfaces\alpaca\test_alpaca_interface_functional.py`, `tests\exchanges\interfaces\binance\test_binance_interface.py`, `tests\exchanges\interfaces\coinbase_pro\test_coinbase_pro_interface.py`, `tests\exchanges\interfaces\ftx\test_ftx_interface.py`
- `queue_orderbook`: `tests\websockets\test_crypto_websockets.py`
- `latency_time`: `tests\exchanges\interfaces\alpaca\test_alpaca_interface_functional.py`, `tests\exchanges\interfaces\coinbase_pro\test_coinbase_pro_interface.py`, `tests\exchanges\interfaces\oanda\test_oanda_interface.py`, `tests\exchanges\test_interface_homogeneity.py`
- `fees_costs`: `tests\exchanges\interfaces\alpaca\test_alpaca_interface.py`, `tests\exchanges\interfaces\ftx\test_ftx_interface.py`, `tests\exchanges\test_interface_homogeneity.py`
- `data_quality`: `tests\exchanges\interfaces\alpaca\test_alpaca_interface.py`, `tests\exchanges\interfaces\binance\test_binance_interface.py`, `tests\exchanges\test_interface_homogeneity.py`, `tests\strategy\test_strategy.py`, `tests\testing_utils.py`
- `agent_rl`: `tests\exchanges\interfaces\alpaca\test_alpaca_interface.py`, `tests\exchanges\interfaces\alpaca\test_alpaca_interface_functional.py`, `tests\exchanges\test_interface_homogeneity.py`

### pybroker
- `fills`: `tests\fixtures.py`, `tests\test_context.py`, `tests\test_data.py`, `tests\test_exit_on_last_bar_perf.py`, `tests\test_indicator.py`
- `order_lifecycle`: `tests\fixtures.py`, `tests\test_context.py`, `tests\test_portfolio.py`, `tests\test_scope.py`, `tests\test_slippage.py`
- `latency_time`: `tests\test_common.py`, `tests\test_data.py`, `tests\test_eval.py`, `tests\test_indicator.py`, `tests\test_strategy.py`
- `slippage_impact`: `tests\test_slippage.py`, `tests\test_strategy.py`
- `fees_costs`: `tests\test_context.py`, `tests\test_eval.py`, `tests\test_portfolio.py`, `tests\test_strategy.py`
- `data_quality`: `tests\test_common.py`, `tests\test_data.py`, `tests\test_indicator.py`, `tests\test_scope.py`, `tests\test_strategy.py`
- `agent_rl`: `tests\test_context.py`, `tests\test_portfolio.py`, `tests\test_strategy.py`

### abides-jpmc-public
- `fills`: `abides-markets\tests\orderbook\test_limit_orders.py`, `abides-markets\tests\orderbook\test_market_orders.py`, `abides-markets\tests\orderbook\test_price_to_comply.py`, `abides-markets\tests\test_gym_runner.py`
- `order_lifecycle`: `abides-markets\tests\__init__.py`, `abides-markets\tests\orderbook\__init__.py`, `abides-markets\tests\orderbook\test_cancel_order.py`, `abides-markets\tests\orderbook\test_data_methods.py`, `abides-markets\tests\orderbook\test_limit_orders.py`
- `queue_orderbook`: `abides-markets\tests\orderbook\__init__.py`, `abides-markets\tests\orderbook\test_cancel_order.py`, `abides-markets\tests\orderbook\test_data_methods.py`, `abides-markets\tests\orderbook\test_limit_orders.py`, `abides-markets\tests\orderbook\test_market_orders.py`
- `latency_time`: `abides-markets\tests\test_sim.py`
- `data_quality`: `abides-markets\tests\test_orders.py`, `version_testing\test_config.py`, `version_testing\test_current_vs_pastcommit.py`, `version_testing\test_original_vs_functionalized.py`
- `agent_rl`: `abides-markets\tests\orderbook\__init__.py`, `abides-markets\tests\orderbook\test_cancel_order.py`, `abides-markets\tests\orderbook\test_data_methods.py`, `abides-markets\tests\orderbook\test_limit_orders.py`, `abides-markets\tests\orderbook\test_market_orders.py`

### backtrader
- `fills`: `tests\test_analyzer-sqn.py`, `tests\test_analyzer-timereturn.py`, `tests\test_order.py`, `tests\test_strategy_unoptimized.py`
- `order_lifecycle`: `tests\test_analyzer-sqn.py`, `tests\test_analyzer-timereturn.py`, `tests\test_comminfo.py`, `tests\test_data_multiframe.py`, `tests\test_data_replay.py`
- `latency_time`: `tests\test_analyzer-sqn.py`, `tests\test_analyzer-timereturn.py`, `tests\test_strategy_optimized.py`, `tests\test_strategy_unoptimized.py`
- `fees_costs`: `tests\test_analyzer-sqn.py`, `tests\test_analyzer-timereturn.py`, `tests\test_comminfo.py`, `tests\test_order.py`, `tests\test_strategy_optimized.py`
- `data_quality`: `tests\test_data_resample.py`, `tests\test_ind_ichimoku.py`, `tests\test_study_fractal.py`

### bt
- `order_lifecycle`: `tests\test_core.py`
- `queue_orderbook`: `tests\test_backtest.py`, `tests\test_core.py`
- `latency_time`: `tests\test_algos.py`
- `slippage_impact`: `tests\test_backtest.py`, `tests\test_core.py`
- `fees_costs`: `tests\test_algos.py`, `tests\test_backtest.py`, `tests\test_core.py`
- `data_quality`: `tests\test_algos.py`, `tests\test_core.py`
- `agent_rl`: `tests\test_algos.py`, `tests\test_backtest.py`, `tests\test_core.py`

### FinRL
- `order_lifecycle`: `unit_tests\preprocessors\test_yahoodownloader.py`
- `latency_time`: `unit_tests\downloaders\test_alpaca_downloader.py`
- `fees_costs`: `unit_tests\environments\test_cash_penalty.py`
- `agent_rl`: `unit_tests\environments\test_cash_penalty.py`

### hftbacktest
- `fills`: `py-hftbacktest\tests\test_hftbacktest.py`
- `order_lifecycle`: `py-hftbacktest\tests\test_hftbacktest.py`
- `queue_orderbook`: `py-hftbacktest\tests\test_hftbacktest.py`
- `latency_time`: `py-hftbacktest\tests\test_hftbacktest.py`

### vnpy
- `queue_orderbook`: `tests\test_alpha101.py`
- `latency_time`: `tests\test_alpha101.py`
- `data_quality`: `tests\test_alpha101.py`

### abides

No matching test files found.

### gym-anytrading

No matching test files found.

### gym-trading-env

No matching test files found.
