# Chunk Index and Stable Source Anchors

Index version 1.0.1. Anchor format: [[F:path#line-range#hash8]]. Hash8 covers the complete working-tree file at index time; regenerate after a source edit. Line ranges are one-based and inclusive. Oversized declarations are partitioned into 38-line slices labelled with their enclosing function/class. Read adjacent slices where a statement crosses a boundary. This is a navigation index, not a claim that all listed lines have been fully analyzed.

## src/api/main.py

SHA8 fa29d125; total lines 3948.

- _validate_operator (function, lines 176-179): CHUNK_ID = src/api/main.py#176-179#fa29d125 — [[F:src/api/main.py#176-179#fa29d125]].
- _terminal_job_reporter (function, lines 182-195): CHUNK_ID = src/api/main.py#182-195#fa29d125 — [[F:src/api/main.py#182-195#fa29d125]].
- _job_error (function, lines 201-203): CHUNK_ID = src/api/main.py#201-203#fa29d125 — [[F:src/api/main.py#201-203#fa29d125]].
- AppState (class, lines 217-254, slice 1): CHUNK_ID = src/api/main.py#217-254#fa29d125 — [[F:src/api/main.py#217-254#fa29d125]].
- AppState (class, lines 255-292, slice 2): CHUNK_ID = src/api/main.py#255-292#fa29d125 — [[F:src/api/main.py#255-292#fa29d125]].
- AppState (class, lines 293-330, slice 3): CHUNK_ID = src/api/main.py#293-330#fa29d125 — [[F:src/api/main.py#293-330#fa29d125]].
- AppState (class, lines 331-368, slice 4): CHUNK_ID = src/api/main.py#331-368#fa29d125 — [[F:src/api/main.py#331-368#fa29d125]].
- AppState (class, lines 369-406, slice 5): CHUNK_ID = src/api/main.py#369-406#fa29d125 — [[F:src/api/main.py#369-406#fa29d125]].
- AppState (class, lines 407-443, slice 6): CHUNK_ID = src/api/main.py#407-443#fa29d125 — [[F:src/api/main.py#407-443#fa29d125]].
- AppState.__init__ (method, lines 235-279): CHUNK_ID = src/api/main.py#235-279#fa29d125 — [[F:src/api/main.py#235-279#fa29d125]].
- AppState.ws_clients (method, lines 282-284): CHUNK_ID = src/api/main.py#282-284#fa29d125 — [[F:src/api/main.py#282-284#fa29d125]].
- AppState.add_ws_client (method, lines 286-298): CHUNK_ID = src/api/main.py#286-298#fa29d125 — [[F:src/api/main.py#286-298#fa29d125]].
- AppState.remove_ws_client (method, lines 300-305): CHUNK_ID = src/api/main.py#300-305#fa29d125 — [[F:src/api/main.py#300-305#fa29d125]].
- AppState.set_ws_topics (method, lines 307-310): CHUNK_ID = src/api/main.py#307-310#fa29d125 — [[F:src/api/main.py#307-310#fa29d125]].
- AppState.permitted_topics (method, lines 312-324): CHUNK_ID = src/api/main.py#312-324#fa29d125 — [[F:src/api/main.py#312-324#fa29d125]].
- AppState.broadcast (method, lines 326-363, slice 1): CHUNK_ID = src/api/main.py#326-363#fa29d125 — [[F:src/api/main.py#326-363#fa29d125]].
- AppState.broadcast (method, lines 364-394, slice 2): CHUNK_ID = src/api/main.py#364-394#fa29d125 — [[F:src/api/main.py#364-394#fa29d125]].
- AppState.check_endpoint_rate_limit (method, lines 396-424): CHUNK_ID = src/api/main.py#396-424#fa29d125 — [[F:src/api/main.py#396-424#fa29d125]].
- AppState.check_mode_change_rate_limit (method, lines 426-443): CHUNK_ID = src/api/main.py#426-443#fa29d125 — [[F:src/api/main.py#426-443#fa29d125]].
- _release_after_failed_startup (function, lines 453-471): CHUNK_ID = src/api/main.py#453-471#fa29d125 — [[F:src/api/main.py#453-471#fa29d125]].
- _StartupGuard (class, lines 474-511, slice 1): CHUNK_ID = src/api/main.py#474-511#fa29d125 — [[F:src/api/main.py#474-511#fa29d125]].
- _StartupGuard (class, lines 512-549, slice 2): CHUNK_ID = src/api/main.py#512-549#fa29d125 — [[F:src/api/main.py#512-549#fa29d125]].
- _StartupGuard (class, lines 550-580, slice 3): CHUNK_ID = src/api/main.py#550-580#fa29d125 — [[F:src/api/main.py#550-580#fa29d125]].
- _StartupGuard.__init__ (method, lines 483-492): CHUNK_ID = src/api/main.py#483-492#fa29d125 — [[F:src/api/main.py#483-492#fa29d125]].
- _StartupGuard.__aenter__ (method, lines 494-495): CHUNK_ID = src/api/main.py#494-495#fa29d125 — [[F:src/api/main.py#494-495#fa29d125]].
- _StartupGuard.__aexit__ (method, lines 497-500): CHUNK_ID = src/api/main.py#497-500#fa29d125 — [[F:src/api/main.py#497-500#fa29d125]].
- _StartupGuard._cleanup (method, lines 502-539, slice 1): CHUNK_ID = src/api/main.py#502-539#fa29d125 — [[F:src/api/main.py#502-539#fa29d125]].
- _StartupGuard._cleanup (method, lines 540-577, slice 2): CHUNK_ID = src/api/main.py#540-577#fa29d125 — [[F:src/api/main.py#540-577#fa29d125]].
- _StartupGuard._cleanup (method, lines 578-580, slice 3): CHUNK_ID = src/api/main.py#578-580#fa29d125 — [[F:src/api/main.py#578-580#fa29d125]].
- lifespan (function, lines 584-621, slice 1): CHUNK_ID = src/api/main.py#584-621#fa29d125 — [[F:src/api/main.py#584-621#fa29d125]].
- lifespan (function, lines 622-659, slice 2): CHUNK_ID = src/api/main.py#622-659#fa29d125 — [[F:src/api/main.py#622-659#fa29d125]].
- lifespan (function, lines 660-697, slice 3): CHUNK_ID = src/api/main.py#660-697#fa29d125 — [[F:src/api/main.py#660-697#fa29d125]].
- lifespan (function, lines 698-735, slice 4): CHUNK_ID = src/api/main.py#698-735#fa29d125 — [[F:src/api/main.py#698-735#fa29d125]].
- lifespan (function, lines 736-773, slice 5): CHUNK_ID = src/api/main.py#736-773#fa29d125 — [[F:src/api/main.py#736-773#fa29d125]].
- lifespan (function, lines 774-790, slice 6): CHUNK_ID = src/api/main.py#774-790#fa29d125 — [[F:src/api/main.py#774-790#fa29d125]].
- api_key_header (function, lines 830-832): CHUNK_ID = src/api/main.py#830-832#fa29d125 — [[F:src/api/main.py#830-832#fa29d125]].
- resolve_role (function, lines 835-844): CHUNK_ID = src/api/main.py#835-844#fa29d125 — [[F:src/api/main.py#835-844#fa29d125]].
- requires (function, lines 847-874): CHUNK_ID = src/api/main.py#847-874#fa29d125 — [[F:src/api/main.py#847-874#fa29d125]].
- require_healthy_security_controls (function, lines 877-889): CHUNK_ID = src/api/main.py#877-889#fa29d125 — [[F:src/api/main.py#877-889#fa29d125]].
- require_ready (function, lines 892-895): CHUNK_ID = src/api/main.py#892-895#fa29d125 — [[F:src/api/main.py#892-895#fa29d125]].
- require_orchestrator (function, lines 898-915): CHUNK_ID = src/api/main.py#898-915#fa29d125 — [[F:src/api/main.py#898-915#fa29d125]].
- ResolveApprovalRequest (class, lines 923-938): CHUNK_ID = src/api/main.py#923-938#fa29d125 — [[F:src/api/main.py#923-938#fa29d125]].
- ResolveApprovalRequest.validate_operator (method, lines 937-938): CHUNK_ID = src/api/main.py#937-938#fa29d125 — [[F:src/api/main.py#937-938#fa29d125]].
- SetExecutionModeRequest (class, lines 941-953): CHUNK_ID = src/api/main.py#941-953#fa29d125 — [[F:src/api/main.py#941-953#fa29d125]].
- SetExecutionModeRequest.validate_operator (method, lines 952-953): CHUNK_ID = src/api/main.py#952-953#fa29d125 — [[F:src/api/main.py#952-953#fa29d125]].
- SetRiskControlsRequest (class, lines 956-988): CHUNK_ID = src/api/main.py#956-988#fa29d125 — [[F:src/api/main.py#956-988#fa29d125]].
- SetRiskControlsRequest.validate_operator (method, lines 987-988): CHUNK_ID = src/api/main.py#987-988#fa29d125 — [[F:src/api/main.py#987-988#fa29d125]].
- SelfTuningPauseRequest (class, lines 991-1007): CHUNK_ID = src/api/main.py#991-1007#fa29d125 — [[F:src/api/main.py#991-1007#fa29d125]].
- SelfTuningPauseRequest.validate_operator (method, lines 1006-1007): CHUNK_ID = src/api/main.py#1006-1007#fa29d125 — [[F:src/api/main.py#1006-1007#fa29d125]].
- RetrainRequest (class, lines 1010-1025): CHUNK_ID = src/api/main.py#1010-1025#fa29d125 — [[F:src/api/main.py#1010-1025#fa29d125]].
- RetrainRequest.validate_operator (method, lines 1024-1025): CHUNK_ID = src/api/main.py#1024-1025#fa29d125 — [[F:src/api/main.py#1024-1025#fa29d125]].
- BackfillRequest (class, lines 1028-1038): CHUNK_ID = src/api/main.py#1028-1038#fa29d125 — [[F:src/api/main.py#1028-1038#fa29d125]].
- CapitalFloorReAuthorizeRequest (class, lines 1041-1059): CHUNK_ID = src/api/main.py#1041-1059#fa29d125 — [[F:src/api/main.py#1041-1059#fa29d125]].
- CapitalFloorReAuthorizeRequest.validate_operator (method, lines 1058-1059): CHUNK_ID = src/api/main.py#1058-1059#fa29d125 — [[F:src/api/main.py#1058-1059#fa29d125]].
- RecoveryAcknowledgeRequest (class, lines 1062-1081): CHUNK_ID = src/api/main.py#1062-1081#fa29d125 — [[F:src/api/main.py#1062-1081#fa29d125]].
- RecoveryAcknowledgeRequest.validate_operator (method, lines 1080-1081): CHUNK_ID = src/api/main.py#1080-1081#fa29d125 — [[F:src/api/main.py#1080-1081#fa29d125]].
- StrategyReEnableRequest (class, lines 1084-1105): CHUNK_ID = src/api/main.py#1084-1105#fa29d125 — [[F:src/api/main.py#1084-1105#fa29d125]].
- StrategyReEnableRequest.validate_operator (method, lines 1104-1105): CHUNK_ID = src/api/main.py#1104-1105#fa29d125 — [[F:src/api/main.py#1104-1105#fa29d125]].
- SelfTuningRollbackRequest (class, lines 1108-1124): CHUNK_ID = src/api/main.py#1108-1124#fa29d125 — [[F:src/api/main.py#1108-1124#fa29d125]].
- SelfTuningRollbackRequest.validate_operator (method, lines 1123-1124): CHUNK_ID = src/api/main.py#1123-1124#fa29d125 — [[F:src/api/main.py#1123-1124#fa29d125]].
- _verify_operator_secret (function, lines 1127-1136): CHUNK_ID = src/api/main.py#1127-1136#fa29d125 — [[F:src/api/main.py#1127-1136#fa29d125]].
- livez (function, lines 1145-1151): CHUNK_ID = src/api/main.py#1145-1151#fa29d125 — [[F:src/api/main.py#1145-1151#fa29d125]].
- readyz (function, lines 1155-1171): CHUNK_ID = src/api/main.py#1155-1171#fa29d125 — [[F:src/api/main.py#1155-1171#fa29d125]].
- health (function, lines 1175-1184): CHUNK_ID = src/api/main.py#1175-1184#fa29d125 — [[F:src/api/main.py#1175-1184#fa29d125]].
- prometheus_metrics (function, lines 1188-1193): CHUNK_ID = src/api/main.py#1188-1193#fa29d125 — [[F:src/api/main.py#1188-1193#fa29d125]].
- status (function, lines 1197-1234, slice 1): CHUNK_ID = src/api/main.py#1197-1234#fa29d125 — [[F:src/api/main.py#1197-1234#fa29d125]].
- status (function, lines 1235-1260, slice 2): CHUNK_ID = src/api/main.py#1235-1260#fa29d125 — [[F:src/api/main.py#1235-1260#fa29d125]].
- trades (function, lines 1264-1301, slice 1): CHUNK_ID = src/api/main.py#1264-1301#fa29d125 — [[F:src/api/main.py#1264-1301#fa29d125]].
- trades (function, lines 1302-1312, slice 2): CHUNK_ID = src/api/main.py#1302-1312#fa29d125 — [[F:src/api/main.py#1302-1312#fa29d125]].
- missed_trades (function, lines 1316-1349): CHUNK_ID = src/api/main.py#1316-1349#fa29d125 — [[F:src/api/main.py#1316-1349#fa29d125]].
- equity_curve (function, lines 1353-1375): CHUNK_ID = src/api/main.py#1353-1375#fa29d125 — [[F:src/api/main.py#1353-1375#fa29d125]].
- regime (function, lines 1386-1410): CHUNK_ID = src/api/main.py#1386-1410#fa29d125 — [[F:src/api/main.py#1386-1410#fa29d125]].
- _get_crypto_box_adapter (function, lines 1414-1426): CHUNK_ID = src/api/main.py#1414-1426#fa29d125 — [[F:src/api/main.py#1414-1426#fa29d125]].
- crypto_box_status (function, lines 1430-1448): CHUNK_ID = src/api/main.py#1430-1448#fa29d125 — [[F:src/api/main.py#1430-1448#fa29d125]].
- approvals (function, lines 1452-1458): CHUNK_ID = src/api/main.py#1452-1458#fa29d125 — [[F:src/api/main.py#1452-1458#fa29d125]].
- resolve_approval (function, lines 1473-1517): CHUNK_ID = src/api/main.py#1473-1517#fa29d125 — [[F:src/api/main.py#1473-1517#fa29d125]].
- set_execution_mode (function, lines 1532-1569, slice 1): CHUNK_ID = src/api/main.py#1532-1569#fa29d125 — [[F:src/api/main.py#1532-1569#fa29d125]].
- set_execution_mode (function, lines 1570-1589, slice 2): CHUNK_ID = src/api/main.py#1570-1589#fa29d125 — [[F:src/api/main.py#1570-1589#fa29d125]].
- get_risk_controls (function, lines 1593-1602): CHUNK_ID = src/api/main.py#1593-1602#fa29d125 — [[F:src/api/main.py#1593-1602#fa29d125]].
- set_risk_controls (function, lines 1618-1655, slice 1): CHUNK_ID = src/api/main.py#1618-1655#fa29d125 — [[F:src/api/main.py#1618-1655#fa29d125]].
- set_risk_controls (function, lines 1656-1674, slice 2): CHUNK_ID = src/api/main.py#1656-1674#fa29d125 — [[F:src/api/main.py#1656-1674#fa29d125]].
- model_metrics (function, lines 1682-1718): CHUNK_ID = src/api/main.py#1682-1718#fa29d125 — [[F:src/api/main.py#1682-1718#fa29d125]].
- self_tuning_status (function, lines 1732-1774): CHUNK_ID = src/api/main.py#1732-1774#fa29d125 — [[F:src/api/main.py#1732-1774#fa29d125]].
- self_tuning_pause (function, lines 1788-1803): CHUNK_ID = src/api/main.py#1788-1803#fa29d125 — [[F:src/api/main.py#1788-1803#fa29d125]].
- self_tuning_resume (function, lines 1817-1828): CHUNK_ID = src/api/main.py#1817-1828#fa29d125 — [[F:src/api/main.py#1817-1828#fa29d125]].
- self_tuning_rollback (function, lines 1843-1868): CHUNK_ID = src/api/main.py#1843-1868#fa29d125 — [[F:src/api/main.py#1843-1868#fa29d125]].
- _build_tick_snapshot (function, lines 1876-1913, slice 1): CHUNK_ID = src/api/main.py#1876-1913#fa29d125 — [[F:src/api/main.py#1876-1913#fa29d125]].
- _build_tick_snapshot (function, lines 1914-1925, slice 2): CHUNK_ID = src/api/main.py#1914-1925#fa29d125 — [[F:src/api/main.py#1914-1925#fa29d125]].
- _heartbeat_loop (function, lines 1928-1953): CHUNK_ID = src/api/main.py#1928-1953#fa29d125 — [[F:src/api/main.py#1928-1953#fa29d125]].
- _event_fanout_loop (function, lines 1956-1996): CHUNK_ID = src/api/main.py#1956-1996#fa29d125 — [[F:src/api/main.py#1956-1996#fa29d125]].
- websocket_endpoint (function, lines 2000-2037, slice 1): CHUNK_ID = src/api/main.py#2000-2037#fa29d125 — [[F:src/api/main.py#2000-2037#fa29d125]].
- websocket_endpoint (function, lines 2038-2069, slice 2): CHUNK_ID = src/api/main.py#2038-2069#fa29d125 — [[F:src/api/main.py#2038-2069#fa29d125]].
- _handle_ws_command (function, lines 2072-2109, slice 1): CHUNK_ID = src/api/main.py#2072-2109#fa29d125 — [[F:src/api/main.py#2072-2109#fa29d125]].
- _handle_ws_command (function, lines 2110-2121, slice 2): CHUNK_ID = src/api/main.py#2110-2121#fa29d125 — [[F:src/api/main.py#2110-2121#fa29d125]].
- _send_ws_error (function, lines 2124-2135): CHUNK_ID = src/api/main.py#2124-2135#fa29d125 — [[F:src/api/main.py#2124-2135#fa29d125]].
- _guarded_ws_reader (function, lines 2138-2167): CHUNK_ID = src/api/main.py#2138-2167#fa29d125 — [[F:src/api/main.py#2138-2167#fa29d125]].
- debug_health (function, lines 2176-2183): CHUNK_ID = src/api/main.py#2176-2183#fa29d125 — [[F:src/api/main.py#2176-2183#fa29d125]].
- debug_audit (function, lines 2187-2198): CHUNK_ID = src/api/main.py#2187-2198#fa29d125 — [[F:src/api/main.py#2187-2198#fa29d125]].
- audit_chain_integrity (function, lines 2202-2239, slice 1): CHUNK_ID = src/api/main.py#2202-2239#fa29d125 — [[F:src/api/main.py#2202-2239#fa29d125]].
- audit_chain_integrity (function, lines 2240-2261, slice 2): CHUNK_ID = src/api/main.py#2240-2261#fa29d125 — [[F:src/api/main.py#2240-2261#fa29d125]].
- debug_drift (function, lines 2265-2287): CHUNK_ID = src/api/main.py#2265-2287#fa29d125 — [[F:src/api/main.py#2265-2287#fa29d125]].
- _fetch_all_open_trades (function, lines 2294-2316): CHUNK_ID = src/api/main.py#2294-2316#fa29d125 — [[F:src/api/main.py#2294-2316#fa29d125]].
- _net_by_symbol (function, lines 2319-2324): CHUNK_ID = src/api/main.py#2319-2324#fa29d125 — [[F:src/api/main.py#2319-2324#fa29d125]].
- debug_reconcile (function, lines 2331-2368, slice 1): CHUNK_ID = src/api/main.py#2331-2368#fa29d125 — [[F:src/api/main.py#2331-2368#fa29d125]].
- debug_reconcile (function, lines 2369-2395, slice 2): CHUNK_ID = src/api/main.py#2369-2395#fa29d125 — [[F:src/api/main.py#2369-2395#fa29d125]].
- debug_selftest (function, lines 2403-2427): CHUNK_ID = src/api/main.py#2403-2427#fa29d125 — [[F:src/api/main.py#2403-2427#fa29d125]].
- get_order_status (function, lines 2431-2468, slice 1): CHUNK_ID = src/api/main.py#2431-2468#fa29d125 — [[F:src/api/main.py#2431-2468#fa29d125]].
- get_order_status (function, lines 2469-2497, slice 2): CHUNK_ID = src/api/main.py#2469-2497#fa29d125 — [[F:src/api/main.py#2469-2497#fa29d125]].
- get_unified_ledger_snapshot (function, lines 2501-2540): CHUNK_ID = src/api/main.py#2501-2540#fa29d125 — [[F:src/api/main.py#2501-2540#fa29d125]].
- _live_executor_or_none (function, lines 2543-2551): CHUNK_ID = src/api/main.py#2543-2551#fa29d125 — [[F:src/api/main.py#2543-2551#fa29d125]].
- recovery_status (function, lines 2555-2583): CHUNK_ID = src/api/main.py#2555-2583#fa29d125 — [[F:src/api/main.py#2555-2583#fa29d125]].
- recovery_acknowledge (function, lines 2599-2636): CHUNK_ID = src/api/main.py#2599-2636#fa29d125 — [[F:src/api/main.py#2599-2636#fa29d125]].
- _parse_timeframe_or_400 (function, lines 2639-2648): CHUNK_ID = src/api/main.py#2639-2648#fa29d125 — [[F:src/api/main.py#2639-2648#fa29d125]].
- models_status (function, lines 2656-2677): CHUNK_ID = src/api/main.py#2656-2677#fa29d125 — [[F:src/api/main.py#2656-2677#fa29d125]].
- trigger_retrain (function, lines 2694-2718): CHUNK_ID = src/api/main.py#2694-2718#fa29d125 — [[F:src/api/main.py#2694-2718#fa29d125]].
- _report_retrain (function, lines 2721-2737): CHUNK_ID = src/api/main.py#2721-2737#fa29d125 — [[F:src/api/main.py#2721-2737#fa29d125]].
- trigger_backfill (function, lines 2752-2779): CHUNK_ID = src/api/main.py#2752-2779#fa29d125 — [[F:src/api/main.py#2752-2779#fa29d125]].
- horizons (function, lines 2783-2824): CHUNK_ID = src/api/main.py#2783-2824#fa29d125 — [[F:src/api/main.py#2783-2824#fa29d125]].
- capital_floor (function, lines 2832-2835): CHUNK_ID = src/api/main.py#2832-2835#fa29d125 — [[F:src/api/main.py#2832-2835#fa29d125]].
- capital_floor_re_authorize (function, lines 2852-2893): CHUNK_ID = src/api/main.py#2852-2893#fa29d125 — [[F:src/api/main.py#2852-2893#fa29d125]].
- get_strategy_attribution (function, lines 2897-2919): CHUNK_ID = src/api/main.py#2897-2919#fa29d125 — [[F:src/api/main.py#2897-2919#fa29d125]].
- get_strategy_gauntlet (function, lines 2927-2964, slice 1): CHUNK_ID = src/api/main.py#2927-2964#fa29d125 — [[F:src/api/main.py#2927-2964#fa29d125]].
- get_strategy_gauntlet (function, lines 2965-2980, slice 2): CHUNK_ID = src/api/main.py#2965-2980#fa29d125 — [[F:src/api/main.py#2965-2980#fa29d125]].
- get_strategy_allocation (function, lines 2984-3021, slice 1): CHUNK_ID = src/api/main.py#2984-3021#fa29d125 — [[F:src/api/main.py#2984-3021#fa29d125]].
- get_strategy_allocation (function, lines 3022-3035, slice 2): CHUNK_ID = src/api/main.py#3022-3035#fa29d125 — [[F:src/api/main.py#3022-3035#fa29d125]].
- re_enable_strategy (function, lines 3053-3090, slice 1): CHUNK_ID = src/api/main.py#3053-3090#fa29d125 — [[F:src/api/main.py#3053-3090#fa29d125]].
- re_enable_strategy (function, lines 3091-3118, slice 2): CHUNK_ID = src/api/main.py#3091-3118#fa29d125 — [[F:src/api/main.py#3091-3118#fa29d125]].
- get_strategy_portfolio (function, lines 3122-3159, slice 1): CHUNK_ID = src/api/main.py#3122-3159#fa29d125 — [[F:src/api/main.py#3122-3159#fa29d125]].
- get_strategy_portfolio (function, lines 3160-3181, slice 2): CHUNK_ID = src/api/main.py#3160-3181#fa29d125 — [[F:src/api/main.py#3160-3181#fa29d125]].
- get_allocation_stress_test (function, lines 3185-3222, slice 1): CHUNK_ID = src/api/main.py#3185-3222#fa29d125 — [[F:src/api/main.py#3185-3222#fa29d125]].
- get_allocation_stress_test (function, lines 3223-3260, slice 2): CHUNK_ID = src/api/main.py#3223-3260#fa29d125 — [[F:src/api/main.py#3223-3260#fa29d125]].
- get_allocation_stress_test (function, lines 3261-3271, slice 3): CHUNK_ID = src/api/main.py#3261-3271#fa29d125 — [[F:src/api/main.py#3261-3271#fa29d125]].
- get_performance_drift (function, lines 3275-3311): CHUNK_ID = src/api/main.py#3275-3311#fa29d125 — [[F:src/api/main.py#3275-3311#fa29d125]].
- get_intelligence_coverage (function, lines 3315-3348): CHUNK_ID = src/api/main.py#3315-3348#fa29d125 — [[F:src/api/main.py#3315-3348#fa29d125]].
- get_intelligence_providers (function, lines 3352-3389, slice 1): CHUNK_ID = src/api/main.py#3352-3389#fa29d125 — [[F:src/api/main.py#3352-3389#fa29d125]].
- get_intelligence_providers (function, lines 3390-3400, slice 2): CHUNK_ID = src/api/main.py#3390-3400#fa29d125 — [[F:src/api/main.py#3390-3400#fa29d125]].
- SizeCheckRequest (class, lines 3408-3425): CHUNK_ID = src/api/main.py#3408-3425#fa29d125 — [[F:src/api/main.py#3408-3425#fa29d125]].
- risk_size_check (function, lines 3429-3466, slice 1): CHUNK_ID = src/api/main.py#3429-3466#fa29d125 — [[F:src/api/main.py#3429-3466#fa29d125]].
- risk_size_check (function, lines 3467-3496, slice 2): CHUNK_ID = src/api/main.py#3467-3496#fa29d125 — [[F:src/api/main.py#3467-3496#fa29d125]].
- VenueReconnectRequest (class, lines 3508-3517): CHUNK_ID = src/api/main.py#3508-3517#fa29d125 — [[F:src/api/main.py#3508-3517#fa29d125]].
- VenueReconnectRequest.validate_operator (method, lines 3516-3517): CHUNK_ID = src/api/main.py#3516-3517#fa29d125 — [[F:src/api/main.py#3516-3517#fa29d125]].
- _known_venue_or_404 (function, lines 3528-3531): CHUNK_ID = src/api/main.py#3528-3531#fa29d125 — [[F:src/api/main.py#3528-3531#fa29d125]].
- _venue_action_recorded (function, lines 3534-3554): CHUNK_ID = src/api/main.py#3534-3554#fa29d125 — [[F:src/api/main.py#3534-3554#fa29d125]].
- venues_status (function, lines 3558-3574): CHUNK_ID = src/api/main.py#3558-3574#fa29d125 — [[F:src/api/main.py#3558-3574#fa29d125]].
- reconnect_venue (function, lines 3578-3598): CHUNK_ID = src/api/main.py#3578-3598#fa29d125 — [[F:src/api/main.py#3578-3598#fa29d125]].
- connect_venue (function, lines 3602-3622): CHUNK_ID = src/api/main.py#3602-3622#fa29d125 — [[F:src/api/main.py#3602-3622#fa29d125]].
- disconnect_venue (function, lines 3626-3648): CHUNK_ID = src/api/main.py#3626-3648#fa29d125 — [[F:src/api/main.py#3626-3648#fa29d125]].
- verify_venue_account (function, lines 3652-3664): CHUNK_ID = src/api/main.py#3652-3664#fa29d125 — [[F:src/api/main.py#3652-3664#fa29d125]].
- control_surface (function, lines 3668-3678): CHUNK_ID = src/api/main.py#3668-3678#fa29d125 — [[F:src/api/main.py#3668-3678#fa29d125]].
- SetControlRequest (class, lines 3681-3686): CHUNK_ID = src/api/main.py#3681-3686#fa29d125 — [[F:src/api/main.py#3681-3686#fa29d125]].
- set_control (function, lines 3690-3724): CHUNK_ID = src/api/main.py#3690-3724#fa29d125 — [[F:src/api/main.py#3690-3724#fa29d125]].
- start_runtime_platform (function, lines 3737-3775): CHUNK_ID = src/api/main.py#3737-3775#fa29d125 — [[F:src/api/main.py#3737-3775#fa29d125]].
- runtime_sources (function, lines 3778-3800): CHUNK_ID = src/api/main.py#3778-3800#fa29d125 — [[F:src/api/main.py#3778-3800#fa29d125]].
- _note_runtime_intent (function, lines 3806-3820): CHUNK_ID = src/api/main.py#3806-3820#fa29d125 — [[F:src/api/main.py#3806-3820#fa29d125]].
- require_runtime (function, lines 3823-3826): CHUNK_ID = src/api/main.py#3823-3826#fa29d125 — [[F:src/api/main.py#3823-3826#fa29d125]].
- _runtime_call (function, lines 3829-3833): CHUNK_ID = src/api/main.py#3829-3833#fa29d125 — [[F:src/api/main.py#3829-3833#fa29d125]].
- runtime_overview (function, lines 3844-3846): CHUNK_ID = src/api/main.py#3844-3846#fa29d125 — [[F:src/api/main.py#3844-3846#fa29d125]].
- runtime_components (function, lines 3850-3859): CHUNK_ID = src/api/main.py#3850-3859#fa29d125 — [[F:src/api/main.py#3850-3859#fa29d125]].
- runtime_component (function, lines 3863-3866): CHUNK_ID = src/api/main.py#3863-3866#fa29d125 — [[F:src/api/main.py#3863-3866#fa29d125]].
- runtime_dependencies (function, lines 3870-3871): CHUNK_ID = src/api/main.py#3870-3871#fa29d125 — [[F:src/api/main.py#3870-3871#fa29d125]].
- runtime_changes (function, lines 3875-3876): CHUNK_ID = src/api/main.py#3875-3876#fa29d125 — [[F:src/api/main.py#3875-3876#fa29d125]].
- runtime_change (function, lines 3880-3882): CHUNK_ID = src/api/main.py#3880-3882#fa29d125 — [[F:src/api/main.py#3880-3882#fa29d125]].
- runtime_traces (function, lines 3886-3887): CHUNK_ID = src/api/main.py#3886-3887#fa29d125 — [[F:src/api/main.py#3886-3887#fa29d125]].
- runtime_trace (function, lines 3891-3893): CHUNK_ID = src/api/main.py#3891-3893#fa29d125 — [[F:src/api/main.py#3891-3893#fa29d125]].
- runtime_agent_ledgers (function, lines 3897-3899): CHUNK_ID = src/api/main.py#3897-3899#fa29d125 — [[F:src/api/main.py#3897-3899#fa29d125]].
- runtime_submit_change (function, lines 3903-3908): CHUNK_ID = src/api/main.py#3903-3908#fa29d125 — [[F:src/api/main.py#3903-3908#fa29d125]].
- runtime_decide (function, lines 3912-3919): CHUNK_ID = src/api/main.py#3912-3919#fa29d125 — [[F:src/api/main.py#3912-3919#fa29d125]].
- runtime_component_action (function, lines 3923-3930): CHUNK_ID = src/api/main.py#3923-3930#fa29d125 — [[F:src/api/main.py#3923-3930#fa29d125]].
- runtime_set_desired (function, lines 3934-3939): CHUNK_ID = src/api/main.py#3934-3939#fa29d125 — [[F:src/api/main.py#3934-3939#fa29d125]].
- runtime_reconcile (function, lines 3943-3948): CHUNK_ID = src/api/main.py#3943-3948#fa29d125 — [[F:src/api/main.py#3943-3948#fa29d125]].

## src/api/auth.py

SHA8 c9a226cf; total lines 179.

- _get_configured_key (function, lines 42-64): CHUNK_ID = src/api/auth.py#42-64#c9a226cf — [[F:src/api/auth.py#42-64#c9a226cf]].
- _get_readonly_key (function, lines 67-91): CHUNK_ID = src/api/auth.py#67-91#c9a226cf — [[F:src/api/auth.py#67-91#c9a226cf]].
- verify_api_key (function, lines 94-133): CHUNK_ID = src/api/auth.py#94-133#c9a226cf — [[F:src/api/auth.py#94-133#c9a226cf]].
- verify_ws_key (function, lines 136-179): CHUNK_ID = src/api/auth.py#136-179#c9a226cf — [[F:src/api/auth.py#136-179#c9a226cf]].

## src/config.py

SHA8 f4b591a7; total lines 1486.

- TradingMode (class, lines 30-34): CHUNK_ID = src/config.py#30-34#f4b591a7 — [[F:src/config.py#30-34#f4b591a7]].
- ExecutionMode (class, lines 37-49): CHUNK_ID = src/config.py#37-49#f4b591a7 — [[F:src/config.py#37-49#f4b591a7]].
- Timeframe (class, lines 52-57): CHUNK_ID = src/config.py#52-57#f4b591a7 — [[F:src/config.py#52-57#f4b591a7]].
- BinanceSettings (class, lines 65-104): CHUNK_ID = src/config.py#65-104#f4b591a7 — [[F:src/config.py#65-104#f4b591a7]].
- BinanceSettings.resolve_urls (method, lines 94-104): CHUNK_ID = src/config.py#94-104#f4b591a7 — [[F:src/config.py#94-104#f4b591a7]].
- OKXSettings (class, lines 107-120): CHUNK_ID = src/config.py#107-120#f4b591a7 — [[F:src/config.py#107-120#f4b591a7]].
- RiskSettings (class, lines 128-165, slice 1): CHUNK_ID = src/config.py#128-165#f4b591a7 — [[F:src/config.py#128-165#f4b591a7]].
- RiskSettings (class, lines 166-203, slice 2): CHUNK_ID = src/config.py#166-203#f4b591a7 — [[F:src/config.py#166-203#f4b591a7]].
- RiskSettings (class, lines 204-241, slice 3): CHUNK_ID = src/config.py#204-241#f4b591a7 — [[F:src/config.py#204-241#f4b591a7]].
- RiskSettings (class, lines 242-279, slice 4): CHUNK_ID = src/config.py#242-279#f4b591a7 — [[F:src/config.py#242-279#f4b591a7]].
- RiskSettings (class, lines 280-317, slice 5): CHUNK_ID = src/config.py#280-317#f4b591a7 — [[F:src/config.py#280-317#f4b591a7]].
- RiskSettings (class, lines 318-320, slice 6): CHUNK_ID = src/config.py#318-320#f4b591a7 — [[F:src/config.py#318-320#f4b591a7]].
- HMMSettings (class, lines 341-372): CHUNK_ID = src/config.py#341-372#f4b591a7 — [[F:src/config.py#341-372#f4b591a7]].
- HMMSettings.validate_cov_type (method, lines 368-372): CHUNK_ID = src/config.py#368-372#f4b591a7 — [[F:src/config.py#368-372#f4b591a7]].
- XGBoostSettings (class, lines 375-412, slice 1): CHUNK_ID = src/config.py#375-412#f4b591a7 — [[F:src/config.py#375-412#f4b591a7]].
- XGBoostSettings (class, lines 413-429, slice 2): CHUNK_ID = src/config.py#413-429#f4b591a7 — [[F:src/config.py#413-429#f4b591a7]].
- XGBoostSettings.validate_shadow_window (method, lines 422-429): CHUNK_ID = src/config.py#422-429#f4b591a7 — [[F:src/config.py#422-429#f4b591a7]].
- FeatureSettings (class, lines 437-474, slice 1): CHUNK_ID = src/config.py#437-474#f4b591a7 — [[F:src/config.py#437-474#f4b591a7]].
- FeatureSettings (class, lines 475-512, slice 2): CHUNK_ID = src/config.py#475-512#f4b591a7 — [[F:src/config.py#475-512#f4b591a7]].
- FeatureSettings (class, lines 513-513, slice 3): CHUNK_ID = src/config.py#513-513#f4b591a7 — [[F:src/config.py#513-513#f4b591a7]].
- FeatureSettings.validate_purge_gap_covers_label_horizon (method, lines 505-513): CHUNK_ID = src/config.py#505-513#f4b591a7 — [[F:src/config.py#505-513#f4b591a7]].
- StorageSettings (class, lines 521-549): CHUNK_ID = src/config.py#521-549#f4b591a7 — [[F:src/config.py#521-549#f4b591a7]].
- APISettings (class, lines 564-595): CHUNK_ID = src/config.py#564-595#f4b591a7 — [[F:src/config.py#564-595#f4b591a7]].
- APISettings.validate_cors_origins (method, lines 588-595): CHUNK_ID = src/config.py#588-595#f4b591a7 — [[F:src/config.py#588-595#f4b591a7]].
- IntelligenceSettings (class, lines 603-640, slice 1): CHUNK_ID = src/config.py#603-640#f4b591a7 — [[F:src/config.py#603-640#f4b591a7]].
- IntelligenceSettings (class, lines 641-652, slice 2): CHUNK_ID = src/config.py#641-652#f4b591a7 — [[F:src/config.py#641-652#f4b591a7]].
- SelfTuningSettings (class, lines 655-692, slice 1): CHUNK_ID = src/config.py#655-692#f4b591a7 — [[F:src/config.py#655-692#f4b591a7]].
- SelfTuningSettings (class, lines 693-730, slice 2): CHUNK_ID = src/config.py#693-730#f4b591a7 — [[F:src/config.py#693-730#f4b591a7]].
- SelfTuningSettings (class, lines 731-745, slice 3): CHUNK_ID = src/config.py#731-745#f4b591a7 — [[F:src/config.py#731-745#f4b591a7]].
- SelfTuningSettings._blank_path_disables (method, lines 741-745): CHUNK_ID = src/config.py#741-745#f4b591a7 — [[F:src/config.py#741-745#f4b591a7]].
- StrategyPortfolioSettings (class, lines 748-785, slice 1): CHUNK_ID = src/config.py#748-785#f4b591a7 — [[F:src/config.py#748-785#f4b591a7]].
- StrategyPortfolioSettings (class, lines 786-823, slice 2): CHUNK_ID = src/config.py#786-823#f4b591a7 — [[F:src/config.py#786-823#f4b591a7]].
- StrategyPortfolioSettings (class, lines 824-861, slice 3): CHUNK_ID = src/config.py#824-861#f4b591a7 — [[F:src/config.py#824-861#f4b591a7]].
- StrategyPortfolioSettings (class, lines 862-899, slice 4): CHUNK_ID = src/config.py#862-899#f4b591a7 — [[F:src/config.py#862-899#f4b591a7]].
- StrategyPortfolioSettings (class, lines 900-913, slice 5): CHUNK_ID = src/config.py#900-913#f4b591a7 — [[F:src/config.py#900-913#f4b591a7]].
- StrategyPortfolioSettings._validate_pair (method, lines 795-800): CHUNK_ID = src/config.py#795-800#f4b591a7 — [[F:src/config.py#795-800#f4b591a7]].
- StrategyPortfolioSettings._greeks_caps_are_all_or_nothing (method, lines 886-895): CHUNK_ID = src/config.py#886-895#f4b591a7 — [[F:src/config.py#886-895#f4b591a7]].
- OrderThrottleSettings (class, lines 916-952): CHUNK_ID = src/config.py#916-952#f4b591a7 — [[F:src/config.py#916-952#f4b591a7]].
- StrategySettings (class, lines 955-992, slice 1): CHUNK_ID = src/config.py#955-992#f4b591a7 — [[F:src/config.py#955-992#f4b591a7]].
- StrategySettings (class, lines 993-1023, slice 2): CHUNK_ID = src/config.py#993-1023#f4b591a7 — [[F:src/config.py#993-1023#f4b591a7]].
- StrategySettings._check_cross_field_invariants (method, lines 1013-1023): CHUNK_ID = src/config.py#1013-1023#f4b591a7 — [[F:src/config.py#1013-1023#f4b591a7]].
- Settings (class, lines 1026-1063, slice 1): CHUNK_ID = src/config.py#1026-1063#f4b591a7 — [[F:src/config.py#1026-1063#f4b591a7]].
- Settings (class, lines 1064-1101, slice 2): CHUNK_ID = src/config.py#1064-1101#f4b591a7 — [[F:src/config.py#1064-1101#f4b591a7]].
- Settings (class, lines 1102-1125, slice 3): CHUNK_ID = src/config.py#1102-1125#f4b591a7 — [[F:src/config.py#1102-1125#f4b591a7]].
- Settings.validate_log_level (method, lines 1095-1100): CHUNK_ID = src/config.py#1095-1100#f4b591a7 — [[F:src/config.py#1095-1100#f4b591a7]].
- Settings.enforce_live_gate (method, lines 1103-1117): CHUNK_ID = src/config.py#1103-1117#f4b591a7 — [[F:src/config.py#1103-1117#f4b591a7]].
- Settings.validate_primary_timeframe_in_active (method, lines 1120-1125): CHUNK_ID = src/config.py#1120-1125#f4b591a7 — [[F:src/config.py#1120-1125#f4b591a7]].
- _base_settings (function, lines 1165-1173): CHUNK_ID = src/config.py#1165-1173#f4b591a7 — [[F:src/config.py#1165-1173#f4b591a7]].
- _LiveSettings (class, lines 1194-1231, slice 1): CHUNK_ID = src/config.py#1194-1231#f4b591a7 — [[F:src/config.py#1194-1231#f4b591a7]].
- _LiveSettings (class, lines 1232-1269, slice 2): CHUNK_ID = src/config.py#1232-1269#f4b591a7 — [[F:src/config.py#1232-1269#f4b591a7]].
- _LiveSettings.__init__ (method, lines 1212-1215): CHUNK_ID = src/config.py#1212-1215#f4b591a7 — [[F:src/config.py#1212-1215#f4b591a7]].
- _LiveSettings.current (method, lines 1217-1219): CHUNK_ID = src/config.py#1217-1219#f4b591a7 — [[F:src/config.py#1217-1219#f4b591a7]].
- _LiveSettings.names (method, lines 1221-1222): CHUNK_ID = src/config.py#1221-1222#f4b591a7 — [[F:src/config.py#1221-1222#f4b591a7]].
- _LiveSettings._rebuild (method, lines 1224-1240): CHUNK_ID = src/config.py#1224-1240#f4b591a7 — [[F:src/config.py#1224-1240#f4b591a7]].
- _LiveSettings.set (method, lines 1242-1258): CHUNK_ID = src/config.py#1242-1258#f4b591a7 — [[F:src/config.py#1242-1258#f4b591a7]].
- _LiveSettings.clear (method, lines 1260-1264): CHUNK_ID = src/config.py#1260-1264#f4b591a7 — [[F:src/config.py#1260-1264#f4b591a7]].
- _LiveSettings.reset (method, lines 1266-1269): CHUNK_ID = src/config.py#1266-1269#f4b591a7 — [[F:src/config.py#1266-1269#f4b591a7]].
- get_settings (function, lines 1275-1282): CHUNK_ID = src/config.py#1275-1282#f4b591a7 — [[F:src/config.py#1275-1282#f4b591a7]].
- settings_override_names (function, lines 1285-1287): CHUNK_ID = src/config.py#1285-1287#f4b591a7 — [[F:src/config.py#1285-1287#f4b591a7]].
- resolve_setting_path (function, lines 1290-1315): CHUNK_ID = src/config.py#1290-1315#f4b591a7 — [[F:src/config.py#1290-1315#f4b591a7]].
- set_setting_override (function, lines 1318-1326): CHUNK_ID = src/config.py#1318-1326#f4b591a7 — [[F:src/config.py#1318-1326#f4b591a7]].
- clear_setting_override (function, lines 1329-1331): CHUNK_ID = src/config.py#1329-1331#f4b591a7 — [[F:src/config.py#1329-1331#f4b591a7]].
- invalidate_settings_cache (function, lines 1334-1337): CHUNK_ID = src/config.py#1334-1337#f4b591a7 — [[F:src/config.py#1334-1337#f4b591a7]].
- RuntimeConfig (class, lines 1362-1399, slice 1): CHUNK_ID = src/config.py#1362-1399#f4b591a7 — [[F:src/config.py#1362-1399#f4b591a7]].
- RuntimeConfig (class, lines 1400-1437, slice 2): CHUNK_ID = src/config.py#1400-1437#f4b591a7 — [[F:src/config.py#1400-1437#f4b591a7]].
- RuntimeConfig (class, lines 1438-1475, slice 3): CHUNK_ID = src/config.py#1438-1475#f4b591a7 — [[F:src/config.py#1438-1475#f4b591a7]].
- RuntimeConfig (class, lines 1476-1482, slice 4): CHUNK_ID = src/config.py#1476-1482#f4b591a7 — [[F:src/config.py#1476-1482#f4b591a7]].
- RuntimeConfig.__init__ (method, lines 1371-1393): CHUNK_ID = src/config.py#1371-1393#f4b591a7 — [[F:src/config.py#1371-1393#f4b591a7]].
- RuntimeConfig._get_lock (method, lines 1395-1406): CHUNK_ID = src/config.py#1395-1406#f4b591a7 — [[F:src/config.py#1395-1406#f4b591a7]].
- RuntimeConfig.get_execution_mode (method, lines 1408-1410): CHUNK_ID = src/config.py#1408-1410#f4b591a7 — [[F:src/config.py#1408-1410#f4b591a7]].
- RuntimeConfig.set_execution_mode (method, lines 1412-1414): CHUNK_ID = src/config.py#1412-1414#f4b591a7 — [[F:src/config.py#1412-1414#f4b591a7]].
- RuntimeConfig.get_risk_controls (method, lines 1420-1431): CHUNK_ID = src/config.py#1420-1431#f4b591a7 — [[F:src/config.py#1420-1431#f4b591a7]].
- RuntimeConfig.set_risk_controls (method, lines 1433-1472): CHUNK_ID = src/config.py#1433-1472#f4b591a7 — [[F:src/config.py#1433-1472#f4b591a7]].
- RuntimeConfig.execution_mode (method, lines 1480-1482): CHUNK_ID = src/config.py#1480-1482#f4b591a7 — [[F:src/config.py#1480-1482#f4b591a7]].

## src/engine/orchestrator.py

SHA8 10c49738; total lines 3483.

- _blend_audit (function, lines 103-122): CHUNK_ID = src/engine/orchestrator.py#103-122#10c49738 — [[F:src/engine/orchestrator.py#103-122#10c49738]].
- _metrics_payload (function, lines 125-149): CHUNK_ID = src/engine/orchestrator.py#125-149#10c49738 — [[F:src/engine/orchestrator.py#125-149#10c49738]].
- _aggregate_venue_positions (function, lines 203-240, slice 1): CHUNK_ID = src/engine/orchestrator.py#203-240#10c49738 — [[F:src/engine/orchestrator.py#203-240#10c49738]].
- _aggregate_venue_positions (function, lines 241-251, slice 2): CHUNK_ID = src/engine/orchestrator.py#241-251#10c49738 — [[F:src/engine/orchestrator.py#241-251#10c49738]].
- Orchestrator (class, lines 254-291, slice 1): CHUNK_ID = src/engine/orchestrator.py#254-291#10c49738 — [[F:src/engine/orchestrator.py#254-291#10c49738]].
- Orchestrator (class, lines 292-329, slice 2): CHUNK_ID = src/engine/orchestrator.py#292-329#10c49738 — [[F:src/engine/orchestrator.py#292-329#10c49738]].
- Orchestrator (class, lines 330-367, slice 3): CHUNK_ID = src/engine/orchestrator.py#330-367#10c49738 — [[F:src/engine/orchestrator.py#330-367#10c49738]].
- Orchestrator (class, lines 368-405, slice 4): CHUNK_ID = src/engine/orchestrator.py#368-405#10c49738 — [[F:src/engine/orchestrator.py#368-405#10c49738]].
- Orchestrator (class, lines 406-443, slice 5): CHUNK_ID = src/engine/orchestrator.py#406-443#10c49738 — [[F:src/engine/orchestrator.py#406-443#10c49738]].
- Orchestrator (class, lines 444-481, slice 6): CHUNK_ID = src/engine/orchestrator.py#444-481#10c49738 — [[F:src/engine/orchestrator.py#444-481#10c49738]].
- Orchestrator (class, lines 482-519, slice 7): CHUNK_ID = src/engine/orchestrator.py#482-519#10c49738 — [[F:src/engine/orchestrator.py#482-519#10c49738]].
- Orchestrator (class, lines 520-557, slice 8): CHUNK_ID = src/engine/orchestrator.py#520-557#10c49738 — [[F:src/engine/orchestrator.py#520-557#10c49738]].
- Orchestrator (class, lines 558-595, slice 9): CHUNK_ID = src/engine/orchestrator.py#558-595#10c49738 — [[F:src/engine/orchestrator.py#558-595#10c49738]].
- Orchestrator (class, lines 596-633, slice 10): CHUNK_ID = src/engine/orchestrator.py#596-633#10c49738 — [[F:src/engine/orchestrator.py#596-633#10c49738]].
- Orchestrator (class, lines 634-671, slice 11): CHUNK_ID = src/engine/orchestrator.py#634-671#10c49738 — [[F:src/engine/orchestrator.py#634-671#10c49738]].
- Orchestrator (class, lines 672-709, slice 12): CHUNK_ID = src/engine/orchestrator.py#672-709#10c49738 — [[F:src/engine/orchestrator.py#672-709#10c49738]].
- Orchestrator (class, lines 710-747, slice 13): CHUNK_ID = src/engine/orchestrator.py#710-747#10c49738 — [[F:src/engine/orchestrator.py#710-747#10c49738]].
- Orchestrator (class, lines 748-785, slice 14): CHUNK_ID = src/engine/orchestrator.py#748-785#10c49738 — [[F:src/engine/orchestrator.py#748-785#10c49738]].
- Orchestrator (class, lines 786-823, slice 15): CHUNK_ID = src/engine/orchestrator.py#786-823#10c49738 — [[F:src/engine/orchestrator.py#786-823#10c49738]].
- Orchestrator (class, lines 824-861, slice 16): CHUNK_ID = src/engine/orchestrator.py#824-861#10c49738 — [[F:src/engine/orchestrator.py#824-861#10c49738]].
- Orchestrator (class, lines 862-899, slice 17): CHUNK_ID = src/engine/orchestrator.py#862-899#10c49738 — [[F:src/engine/orchestrator.py#862-899#10c49738]].
- Orchestrator (class, lines 900-937, slice 18): CHUNK_ID = src/engine/orchestrator.py#900-937#10c49738 — [[F:src/engine/orchestrator.py#900-937#10c49738]].
- Orchestrator (class, lines 938-975, slice 19): CHUNK_ID = src/engine/orchestrator.py#938-975#10c49738 — [[F:src/engine/orchestrator.py#938-975#10c49738]].
- Orchestrator (class, lines 976-1013, slice 20): CHUNK_ID = src/engine/orchestrator.py#976-1013#10c49738 — [[F:src/engine/orchestrator.py#976-1013#10c49738]].
- Orchestrator (class, lines 1014-1051, slice 21): CHUNK_ID = src/engine/orchestrator.py#1014-1051#10c49738 — [[F:src/engine/orchestrator.py#1014-1051#10c49738]].
- Orchestrator (class, lines 1052-1089, slice 22): CHUNK_ID = src/engine/orchestrator.py#1052-1089#10c49738 — [[F:src/engine/orchestrator.py#1052-1089#10c49738]].
- Orchestrator (class, lines 1090-1127, slice 23): CHUNK_ID = src/engine/orchestrator.py#1090-1127#10c49738 — [[F:src/engine/orchestrator.py#1090-1127#10c49738]].
- Orchestrator (class, lines 1128-1165, slice 24): CHUNK_ID = src/engine/orchestrator.py#1128-1165#10c49738 — [[F:src/engine/orchestrator.py#1128-1165#10c49738]].
- Orchestrator (class, lines 1166-1203, slice 25): CHUNK_ID = src/engine/orchestrator.py#1166-1203#10c49738 — [[F:src/engine/orchestrator.py#1166-1203#10c49738]].
- Orchestrator (class, lines 1204-1241, slice 26): CHUNK_ID = src/engine/orchestrator.py#1204-1241#10c49738 — [[F:src/engine/orchestrator.py#1204-1241#10c49738]].
- Orchestrator (class, lines 1242-1279, slice 27): CHUNK_ID = src/engine/orchestrator.py#1242-1279#10c49738 — [[F:src/engine/orchestrator.py#1242-1279#10c49738]].
- Orchestrator (class, lines 1280-1317, slice 28): CHUNK_ID = src/engine/orchestrator.py#1280-1317#10c49738 — [[F:src/engine/orchestrator.py#1280-1317#10c49738]].
- Orchestrator (class, lines 1318-1355, slice 29): CHUNK_ID = src/engine/orchestrator.py#1318-1355#10c49738 — [[F:src/engine/orchestrator.py#1318-1355#10c49738]].
- Orchestrator (class, lines 1356-1393, slice 30): CHUNK_ID = src/engine/orchestrator.py#1356-1393#10c49738 — [[F:src/engine/orchestrator.py#1356-1393#10c49738]].
- Orchestrator (class, lines 1394-1431, slice 31): CHUNK_ID = src/engine/orchestrator.py#1394-1431#10c49738 — [[F:src/engine/orchestrator.py#1394-1431#10c49738]].
- Orchestrator (class, lines 1432-1469, slice 32): CHUNK_ID = src/engine/orchestrator.py#1432-1469#10c49738 — [[F:src/engine/orchestrator.py#1432-1469#10c49738]].
- Orchestrator (class, lines 1470-1507, slice 33): CHUNK_ID = src/engine/orchestrator.py#1470-1507#10c49738 — [[F:src/engine/orchestrator.py#1470-1507#10c49738]].
- Orchestrator (class, lines 1508-1545, slice 34): CHUNK_ID = src/engine/orchestrator.py#1508-1545#10c49738 — [[F:src/engine/orchestrator.py#1508-1545#10c49738]].
- Orchestrator (class, lines 1546-1583, slice 35): CHUNK_ID = src/engine/orchestrator.py#1546-1583#10c49738 — [[F:src/engine/orchestrator.py#1546-1583#10c49738]].
- Orchestrator (class, lines 1584-1621, slice 36): CHUNK_ID = src/engine/orchestrator.py#1584-1621#10c49738 — [[F:src/engine/orchestrator.py#1584-1621#10c49738]].
- Orchestrator (class, lines 1622-1659, slice 37): CHUNK_ID = src/engine/orchestrator.py#1622-1659#10c49738 — [[F:src/engine/orchestrator.py#1622-1659#10c49738]].
- Orchestrator (class, lines 1660-1697, slice 38): CHUNK_ID = src/engine/orchestrator.py#1660-1697#10c49738 — [[F:src/engine/orchestrator.py#1660-1697#10c49738]].
- Orchestrator (class, lines 1698-1735, slice 39): CHUNK_ID = src/engine/orchestrator.py#1698-1735#10c49738 — [[F:src/engine/orchestrator.py#1698-1735#10c49738]].
- Orchestrator (class, lines 1736-1773, slice 40): CHUNK_ID = src/engine/orchestrator.py#1736-1773#10c49738 — [[F:src/engine/orchestrator.py#1736-1773#10c49738]].
- Orchestrator (class, lines 1774-1811, slice 41): CHUNK_ID = src/engine/orchestrator.py#1774-1811#10c49738 — [[F:src/engine/orchestrator.py#1774-1811#10c49738]].
- Orchestrator (class, lines 1812-1849, slice 42): CHUNK_ID = src/engine/orchestrator.py#1812-1849#10c49738 — [[F:src/engine/orchestrator.py#1812-1849#10c49738]].
- Orchestrator (class, lines 1850-1887, slice 43): CHUNK_ID = src/engine/orchestrator.py#1850-1887#10c49738 — [[F:src/engine/orchestrator.py#1850-1887#10c49738]].
- Orchestrator (class, lines 1888-1925, slice 44): CHUNK_ID = src/engine/orchestrator.py#1888-1925#10c49738 — [[F:src/engine/orchestrator.py#1888-1925#10c49738]].
- Orchestrator (class, lines 1926-1963, slice 45): CHUNK_ID = src/engine/orchestrator.py#1926-1963#10c49738 — [[F:src/engine/orchestrator.py#1926-1963#10c49738]].
- Orchestrator (class, lines 1964-2001, slice 46): CHUNK_ID = src/engine/orchestrator.py#1964-2001#10c49738 — [[F:src/engine/orchestrator.py#1964-2001#10c49738]].
- Orchestrator (class, lines 2002-2039, slice 47): CHUNK_ID = src/engine/orchestrator.py#2002-2039#10c49738 — [[F:src/engine/orchestrator.py#2002-2039#10c49738]].
- Orchestrator (class, lines 2040-2077, slice 48): CHUNK_ID = src/engine/orchestrator.py#2040-2077#10c49738 — [[F:src/engine/orchestrator.py#2040-2077#10c49738]].
- Orchestrator (class, lines 2078-2115, slice 49): CHUNK_ID = src/engine/orchestrator.py#2078-2115#10c49738 — [[F:src/engine/orchestrator.py#2078-2115#10c49738]].
- Orchestrator (class, lines 2116-2153, slice 50): CHUNK_ID = src/engine/orchestrator.py#2116-2153#10c49738 — [[F:src/engine/orchestrator.py#2116-2153#10c49738]].
- Orchestrator (class, lines 2154-2191, slice 51): CHUNK_ID = src/engine/orchestrator.py#2154-2191#10c49738 — [[F:src/engine/orchestrator.py#2154-2191#10c49738]].
- Orchestrator (class, lines 2192-2229, slice 52): CHUNK_ID = src/engine/orchestrator.py#2192-2229#10c49738 — [[F:src/engine/orchestrator.py#2192-2229#10c49738]].
- Orchestrator (class, lines 2230-2267, slice 53): CHUNK_ID = src/engine/orchestrator.py#2230-2267#10c49738 — [[F:src/engine/orchestrator.py#2230-2267#10c49738]].
- Orchestrator (class, lines 2268-2305, slice 54): CHUNK_ID = src/engine/orchestrator.py#2268-2305#10c49738 — [[F:src/engine/orchestrator.py#2268-2305#10c49738]].
- Orchestrator (class, lines 2306-2343, slice 55): CHUNK_ID = src/engine/orchestrator.py#2306-2343#10c49738 — [[F:src/engine/orchestrator.py#2306-2343#10c49738]].
- Orchestrator (class, lines 2344-2381, slice 56): CHUNK_ID = src/engine/orchestrator.py#2344-2381#10c49738 — [[F:src/engine/orchestrator.py#2344-2381#10c49738]].
- Orchestrator (class, lines 2382-2419, slice 57): CHUNK_ID = src/engine/orchestrator.py#2382-2419#10c49738 — [[F:src/engine/orchestrator.py#2382-2419#10c49738]].
- Orchestrator (class, lines 2420-2457, slice 58): CHUNK_ID = src/engine/orchestrator.py#2420-2457#10c49738 — [[F:src/engine/orchestrator.py#2420-2457#10c49738]].
- Orchestrator (class, lines 2458-2495, slice 59): CHUNK_ID = src/engine/orchestrator.py#2458-2495#10c49738 — [[F:src/engine/orchestrator.py#2458-2495#10c49738]].
- Orchestrator (class, lines 2496-2533, slice 60): CHUNK_ID = src/engine/orchestrator.py#2496-2533#10c49738 — [[F:src/engine/orchestrator.py#2496-2533#10c49738]].
- Orchestrator (class, lines 2534-2571, slice 61): CHUNK_ID = src/engine/orchestrator.py#2534-2571#10c49738 — [[F:src/engine/orchestrator.py#2534-2571#10c49738]].
- Orchestrator (class, lines 2572-2609, slice 62): CHUNK_ID = src/engine/orchestrator.py#2572-2609#10c49738 — [[F:src/engine/orchestrator.py#2572-2609#10c49738]].
- Orchestrator (class, lines 2610-2647, slice 63): CHUNK_ID = src/engine/orchestrator.py#2610-2647#10c49738 — [[F:src/engine/orchestrator.py#2610-2647#10c49738]].
- Orchestrator (class, lines 2648-2685, slice 64): CHUNK_ID = src/engine/orchestrator.py#2648-2685#10c49738 — [[F:src/engine/orchestrator.py#2648-2685#10c49738]].
- Orchestrator (class, lines 2686-2723, slice 65): CHUNK_ID = src/engine/orchestrator.py#2686-2723#10c49738 — [[F:src/engine/orchestrator.py#2686-2723#10c49738]].
- Orchestrator (class, lines 2724-2761, slice 66): CHUNK_ID = src/engine/orchestrator.py#2724-2761#10c49738 — [[F:src/engine/orchestrator.py#2724-2761#10c49738]].
- Orchestrator (class, lines 2762-2799, slice 67): CHUNK_ID = src/engine/orchestrator.py#2762-2799#10c49738 — [[F:src/engine/orchestrator.py#2762-2799#10c49738]].
- Orchestrator (class, lines 2800-2837, slice 68): CHUNK_ID = src/engine/orchestrator.py#2800-2837#10c49738 — [[F:src/engine/orchestrator.py#2800-2837#10c49738]].
- Orchestrator (class, lines 2838-2875, slice 69): CHUNK_ID = src/engine/orchestrator.py#2838-2875#10c49738 — [[F:src/engine/orchestrator.py#2838-2875#10c49738]].
- Orchestrator (class, lines 2876-2913, slice 70): CHUNK_ID = src/engine/orchestrator.py#2876-2913#10c49738 — [[F:src/engine/orchestrator.py#2876-2913#10c49738]].
- Orchestrator (class, lines 2914-2951, slice 71): CHUNK_ID = src/engine/orchestrator.py#2914-2951#10c49738 — [[F:src/engine/orchestrator.py#2914-2951#10c49738]].
- Orchestrator (class, lines 2952-2989, slice 72): CHUNK_ID = src/engine/orchestrator.py#2952-2989#10c49738 — [[F:src/engine/orchestrator.py#2952-2989#10c49738]].
- Orchestrator (class, lines 2990-3027, slice 73): CHUNK_ID = src/engine/orchestrator.py#2990-3027#10c49738 — [[F:src/engine/orchestrator.py#2990-3027#10c49738]].
- Orchestrator (class, lines 3028-3065, slice 74): CHUNK_ID = src/engine/orchestrator.py#3028-3065#10c49738 — [[F:src/engine/orchestrator.py#3028-3065#10c49738]].
- Orchestrator (class, lines 3066-3103, slice 75): CHUNK_ID = src/engine/orchestrator.py#3066-3103#10c49738 — [[F:src/engine/orchestrator.py#3066-3103#10c49738]].
- Orchestrator (class, lines 3104-3141, slice 76): CHUNK_ID = src/engine/orchestrator.py#3104-3141#10c49738 — [[F:src/engine/orchestrator.py#3104-3141#10c49738]].
- Orchestrator (class, lines 3142-3179, slice 77): CHUNK_ID = src/engine/orchestrator.py#3142-3179#10c49738 — [[F:src/engine/orchestrator.py#3142-3179#10c49738]].
- Orchestrator (class, lines 3180-3217, slice 78): CHUNK_ID = src/engine/orchestrator.py#3180-3217#10c49738 — [[F:src/engine/orchestrator.py#3180-3217#10c49738]].
- Orchestrator (class, lines 3218-3255, slice 79): CHUNK_ID = src/engine/orchestrator.py#3218-3255#10c49738 — [[F:src/engine/orchestrator.py#3218-3255#10c49738]].
- Orchestrator (class, lines 3256-3293, slice 80): CHUNK_ID = src/engine/orchestrator.py#3256-3293#10c49738 — [[F:src/engine/orchestrator.py#3256-3293#10c49738]].
- Orchestrator (class, lines 3294-3331, slice 81): CHUNK_ID = src/engine/orchestrator.py#3294-3331#10c49738 — [[F:src/engine/orchestrator.py#3294-3331#10c49738]].
- Orchestrator (class, lines 3332-3369, slice 82): CHUNK_ID = src/engine/orchestrator.py#3332-3369#10c49738 — [[F:src/engine/orchestrator.py#3332-3369#10c49738]].
- Orchestrator (class, lines 3370-3407, slice 83): CHUNK_ID = src/engine/orchestrator.py#3370-3407#10c49738 — [[F:src/engine/orchestrator.py#3370-3407#10c49738]].
- Orchestrator (class, lines 3408-3445, slice 84): CHUNK_ID = src/engine/orchestrator.py#3408-3445#10c49738 — [[F:src/engine/orchestrator.py#3408-3445#10c49738]].
- Orchestrator (class, lines 3446-3483, slice 85): CHUNK_ID = src/engine/orchestrator.py#3446-3483#10c49738 — [[F:src/engine/orchestrator.py#3446-3483#10c49738]].
- Orchestrator.__init__ (method, lines 268-305, slice 1): CHUNK_ID = src/engine/orchestrator.py#268-305#10c49738 — [[F:src/engine/orchestrator.py#268-305#10c49738]].
- Orchestrator.__init__ (method, lines 306-343, slice 2): CHUNK_ID = src/engine/orchestrator.py#306-343#10c49738 — [[F:src/engine/orchestrator.py#306-343#10c49738]].
- Orchestrator.__init__ (method, lines 344-381, slice 3): CHUNK_ID = src/engine/orchestrator.py#344-381#10c49738 — [[F:src/engine/orchestrator.py#344-381#10c49738]].
- Orchestrator.__init__ (method, lines 382-390, slice 4): CHUNK_ID = src/engine/orchestrator.py#382-390#10c49738 — [[F:src/engine/orchestrator.py#382-390#10c49738]].
- Orchestrator._cfg (method, lines 408-418): CHUNK_ID = src/engine/orchestrator.py#408-418#10c49738 — [[F:src/engine/orchestrator.py#408-418#10c49738]].
- Orchestrator._cfg (method, lines 421-431): CHUNK_ID = src/engine/orchestrator.py#421-431#10c49738 — [[F:src/engine/orchestrator.py#421-431#10c49738]].
- Orchestrator.startup (method, lines 433-470, slice 1): CHUNK_ID = src/engine/orchestrator.py#433-470#10c49738 — [[F:src/engine/orchestrator.py#433-470#10c49738]].
- Orchestrator.startup (method, lines 471-500, slice 2): CHUNK_ID = src/engine/orchestrator.py#471-500#10c49738 — [[F:src/engine/orchestrator.py#471-500#10c49738]].
- Orchestrator._run_pipeline_selftest (method, lines 502-510): CHUNK_ID = src/engine/orchestrator.py#502-510#10c49738 — [[F:src/engine/orchestrator.py#502-510#10c49738]].
- Orchestrator.warm_up (method, lines 512-532): CHUNK_ID = src/engine/orchestrator.py#512-532#10c49738 — [[F:src/engine/orchestrator.py#512-532#10c49738]].
- Orchestrator._warm_up_models (method, lines 534-571, slice 1): CHUNK_ID = src/engine/orchestrator.py#534-571#10c49738 — [[F:src/engine/orchestrator.py#534-571#10c49738]].
- Orchestrator._warm_up_models (method, lines 572-609, slice 2): CHUNK_ID = src/engine/orchestrator.py#572-609#10c49738 — [[F:src/engine/orchestrator.py#572-609#10c49738]].
- Orchestrator._warm_up_models (method, lines 610-647, slice 3): CHUNK_ID = src/engine/orchestrator.py#610-647#10c49738 — [[F:src/engine/orchestrator.py#610-647#10c49738]].
- Orchestrator._warm_up_models (method, lines 648-685, slice 4): CHUNK_ID = src/engine/orchestrator.py#648-685#10c49738 — [[F:src/engine/orchestrator.py#648-685#10c49738]].
- Orchestrator._warm_up_models (method, lines 686-708, slice 5): CHUNK_ID = src/engine/orchestrator.py#686-708#10c49738 — [[F:src/engine/orchestrator.py#686-708#10c49738]].
- Orchestrator._prepare_history (method, lines 710-747, slice 1): CHUNK_ID = src/engine/orchestrator.py#710-747#10c49738 — [[F:src/engine/orchestrator.py#710-747#10c49738]].
- Orchestrator._prepare_history (method, lines 748-785, slice 2): CHUNK_ID = src/engine/orchestrator.py#748-785#10c49738 — [[F:src/engine/orchestrator.py#748-785#10c49738]].
- Orchestrator._prepare_history (method, lines 786-787, slice 3): CHUNK_ID = src/engine/orchestrator.py#786-787#10c49738 — [[F:src/engine/orchestrator.py#786-787#10c49738]].
- Orchestrator.readiness (method, lines 789-814): CHUNK_ID = src/engine/orchestrator.py#789-814#10c49738 — [[F:src/engine/orchestrator.py#789-814#10c49738]].
- Orchestrator.run (method, lines 820-857, slice 1): CHUNK_ID = src/engine/orchestrator.py#820-857#10c49738 — [[F:src/engine/orchestrator.py#820-857#10c49738]].
- Orchestrator.run (method, lines 858-879, slice 2): CHUNK_ID = src/engine/orchestrator.py#858-879#10c49738 — [[F:src/engine/orchestrator.py#858-879#10c49738]].
- Orchestrator._warm_up_unless_stopped (method, lines 881-918, slice 1): CHUNK_ID = src/engine/orchestrator.py#881-918#10c49738 — [[F:src/engine/orchestrator.py#881-918#10c49738]].
- Orchestrator._warm_up_unless_stopped (method, lines 919-948, slice 2): CHUNK_ID = src/engine/orchestrator.py#919-948#10c49738 — [[F:src/engine/orchestrator.py#919-948#10c49738]].
- Orchestrator.stop (method, lines 950-952): CHUNK_ID = src/engine/orchestrator.py#950-952#10c49738 — [[F:src/engine/orchestrator.py#950-952#10c49738]].
- Orchestrator._executor_for (method, lines 958-988): CHUNK_ID = src/engine/orchestrator.py#958-988#10c49738 — [[F:src/engine/orchestrator.py#958-988#10c49738]].
- Orchestrator._all_executors (method, lines 990-997): CHUNK_ID = src/engine/orchestrator.py#990-997#10c49738 — [[F:src/engine/orchestrator.py#990-997#10c49738]].
- Orchestrator._crypto_box_provider_tasks (method, lines 999-1033): CHUNK_ID = src/engine/orchestrator.py#999-1033#10c49738 — [[F:src/engine/orchestrator.py#999-1033#10c49738]].
- Orchestrator.crypto_box (method, lines 1040-1041): CHUNK_ID = src/engine/orchestrator.py#1040-1041#10c49738 — [[F:src/engine/orchestrator.py#1040-1041#10c49738]].
- Orchestrator.signal_engines (method, lines 1043-1045): CHUNK_ID = src/engine/orchestrator.py#1043-1045#10c49738 — [[F:src/engine/orchestrator.py#1043-1045#10c49738]].
- Orchestrator.background_tasks (method, lines 1047-1052): CHUNK_ID = src/engine/orchestrator.py#1047-1052#10c49738 — [[F:src/engine/orchestrator.py#1047-1052#10c49738]].
- Orchestrator.provider_tasks (method, lines 1054-1056): CHUNK_ID = src/engine/orchestrator.py#1054-1056#10c49738 — [[F:src/engine/orchestrator.py#1054-1056#10c49738]].
- Orchestrator.worker_pools (method, lines 1058-1075): CHUNK_ID = src/engine/orchestrator.py#1058-1075#10c49738 — [[F:src/engine/orchestrator.py#1058-1075#10c49738]].
- Orchestrator.shutdown (method, lines 1077-1096): CHUNK_ID = src/engine/orchestrator.py#1077-1096#10c49738 — [[F:src/engine/orchestrator.py#1077-1096#10c49738]].
- Orchestrator._persist_online_trainers (method, lines 1098-1119): CHUNK_ID = src/engine/orchestrator.py#1098-1119#10c49738 — [[F:src/engine/orchestrator.py#1098-1119#10c49738]].
- Orchestrator._timeframe_loop (method, lines 1125-1156): CHUNK_ID = src/engine/orchestrator.py#1125-1156#10c49738 — [[F:src/engine/orchestrator.py#1125-1156#10c49738]].
- Orchestrator._sleep_until_next_bar (method, lines 1158-1163): CHUNK_ID = src/engine/orchestrator.py#1158-1163#10c49738 — [[F:src/engine/orchestrator.py#1158-1163#10c49738]].
- Orchestrator._tick (method, lines 1169-1193): CHUNK_ID = src/engine/orchestrator.py#1169-1193#10c49738 — [[F:src/engine/orchestrator.py#1169-1193#10c49738]].
- Orchestrator._tick_traced (method, lines 1195-1232, slice 1): CHUNK_ID = src/engine/orchestrator.py#1195-1232#10c49738 — [[F:src/engine/orchestrator.py#1195-1232#10c49738]].
- Orchestrator._tick_traced (method, lines 1233-1270, slice 2): CHUNK_ID = src/engine/orchestrator.py#1233-1270#10c49738 — [[F:src/engine/orchestrator.py#1233-1270#10c49738]].
- Orchestrator._tick_traced (method, lines 1271-1308, slice 3): CHUNK_ID = src/engine/orchestrator.py#1271-1308#10c49738 — [[F:src/engine/orchestrator.py#1271-1308#10c49738]].
- Orchestrator._tick_traced (method, lines 1309-1346, slice 4): CHUNK_ID = src/engine/orchestrator.py#1309-1346#10c49738 — [[F:src/engine/orchestrator.py#1309-1346#10c49738]].
- Orchestrator._tick_traced (method, lines 1347-1384, slice 5): CHUNK_ID = src/engine/orchestrator.py#1347-1384#10c49738 — [[F:src/engine/orchestrator.py#1347-1384#10c49738]].
- Orchestrator._tick_traced (method, lines 1385-1422, slice 6): CHUNK_ID = src/engine/orchestrator.py#1385-1422#10c49738 — [[F:src/engine/orchestrator.py#1385-1422#10c49738]].
- Orchestrator._tick_traced (method, lines 1423-1460, slice 7): CHUNK_ID = src/engine/orchestrator.py#1423-1460#10c49738 — [[F:src/engine/orchestrator.py#1423-1460#10c49738]].
- Orchestrator._tick_traced (method, lines 1461-1498, slice 8): CHUNK_ID = src/engine/orchestrator.py#1461-1498#10c49738 — [[F:src/engine/orchestrator.py#1461-1498#10c49738]].
- Orchestrator._tick_traced (method, lines 1499-1536, slice 9): CHUNK_ID = src/engine/orchestrator.py#1499-1536#10c49738 — [[F:src/engine/orchestrator.py#1499-1536#10c49738]].
- Orchestrator._tick_traced (method, lines 1537-1574, slice 10): CHUNK_ID = src/engine/orchestrator.py#1537-1574#10c49738 — [[F:src/engine/orchestrator.py#1537-1574#10c49738]].
- Orchestrator._tick_traced (method, lines 1575-1612, slice 11): CHUNK_ID = src/engine/orchestrator.py#1575-1612#10c49738 — [[F:src/engine/orchestrator.py#1575-1612#10c49738]].
- Orchestrator._tick_traced (method, lines 1613-1650, slice 12): CHUNK_ID = src/engine/orchestrator.py#1613-1650#10c49738 — [[F:src/engine/orchestrator.py#1613-1650#10c49738]].
- Orchestrator._tick_traced (method, lines 1651-1688, slice 13): CHUNK_ID = src/engine/orchestrator.py#1651-1688#10c49738 — [[F:src/engine/orchestrator.py#1651-1688#10c49738]].
- Orchestrator._tick_traced (method, lines 1689-1726, slice 14): CHUNK_ID = src/engine/orchestrator.py#1689-1726#10c49738 — [[F:src/engine/orchestrator.py#1689-1726#10c49738]].
- Orchestrator._tick_traced (method, lines 1727-1751, slice 15): CHUNK_ID = src/engine/orchestrator.py#1727-1751#10c49738 — [[F:src/engine/orchestrator.py#1727-1751#10c49738]].
- Orchestrator.request_retrain (method, lines 1757-1790): CHUNK_ID = src/engine/orchestrator.py#1757-1790#10c49738 — [[F:src/engine/orchestrator.py#1757-1790#10c49738]].
- Orchestrator.retrain_task (method, lines 1792-1801): CHUNK_ID = src/engine/orchestrator.py#1792-1801#10c49738 — [[F:src/engine/orchestrator.py#1792-1801#10c49738]].
- Orchestrator.retrain_status (method, lines 1803-1813): CHUNK_ID = src/engine/orchestrator.py#1803-1813#10c49738 — [[F:src/engine/orchestrator.py#1803-1813#10c49738]].
- Orchestrator.request_backfill (method, lines 1815-1838): CHUNK_ID = src/engine/orchestrator.py#1815-1838#10c49738 — [[F:src/engine/orchestrator.py#1815-1838#10c49738]].
- Orchestrator.capital_floor_status (method, lines 1840-1866): CHUNK_ID = src/engine/orchestrator.py#1840-1866#10c49738 — [[F:src/engine/orchestrator.py#1840-1866#10c49738]].
- Orchestrator.re_authorize_capital_floor (method, lines 1868-1891): CHUNK_ID = src/engine/orchestrator.py#1868-1891#10c49738 — [[F:src/engine/orchestrator.py#1868-1891#10c49738]].
- Orchestrator._route_retrained_bundle (method, lines 1897-1934, slice 1): CHUNK_ID = src/engine/orchestrator.py#1897-1934#10c49738 — [[F:src/engine/orchestrator.py#1897-1934#10c49738]].
- Orchestrator._route_retrained_bundle (method, lines 1935-1961, slice 2): CHUNK_ID = src/engine/orchestrator.py#1935-1961#10c49738 — [[F:src/engine/orchestrator.py#1935-1961#10c49738]].
- Orchestrator._train_models (method, lines 1963-2000, slice 1): CHUNK_ID = src/engine/orchestrator.py#1963-2000#10c49738 — [[F:src/engine/orchestrator.py#1963-2000#10c49738]].
- Orchestrator._train_models (method, lines 2001-2038, slice 2): CHUNK_ID = src/engine/orchestrator.py#2001-2038#10c49738 — [[F:src/engine/orchestrator.py#2001-2038#10c49738]].
- Orchestrator._train_models (method, lines 2039-2076, slice 3): CHUNK_ID = src/engine/orchestrator.py#2039-2076#10c49738 — [[F:src/engine/orchestrator.py#2039-2076#10c49738]].
- Orchestrator._train_models (method, lines 2077-2114, slice 4): CHUNK_ID = src/engine/orchestrator.py#2077-2114#10c49738 — [[F:src/engine/orchestrator.py#2077-2114#10c49738]].
- Orchestrator._train_models (method, lines 2115-2152, slice 5): CHUNK_ID = src/engine/orchestrator.py#2115-2152#10c49738 — [[F:src/engine/orchestrator.py#2115-2152#10c49738]].
- Orchestrator._train_models (method, lines 2153-2158, slice 6): CHUNK_ID = src/engine/orchestrator.py#2153-2158#10c49738 — [[F:src/engine/orchestrator.py#2153-2158#10c49738]].
- Orchestrator._midnight_reset_loop (method, lines 2164-2187): CHUNK_ID = src/engine/orchestrator.py#2164-2187#10c49738 — [[F:src/engine/orchestrator.py#2164-2187#10c49738]].
- Orchestrator._allocation_rebalance_loop (method, lines 2193-2237): CHUNK_ID = src/engine/orchestrator.py#2193-2237#10c49738 — [[F:src/engine/orchestrator.py#2193-2237#10c49738]].
- Orchestrator._position_monitor_loop (method, lines 2243-2280, slice 1): CHUNK_ID = src/engine/orchestrator.py#2243-2280#10c49738 — [[F:src/engine/orchestrator.py#2243-2280#10c49738]].
- Orchestrator._position_monitor_loop (method, lines 2281-2318, slice 2): CHUNK_ID = src/engine/orchestrator.py#2281-2318#10c49738 — [[F:src/engine/orchestrator.py#2281-2318#10c49738]].
- Orchestrator._position_monitor_loop (method, lines 2319-2321, slice 3): CHUNK_ID = src/engine/orchestrator.py#2319-2321#10c49738 — [[F:src/engine/orchestrator.py#2319-2321#10c49738]].
- Orchestrator._orderbook_stream_loop (method, lines 2323-2352): CHUNK_ID = src/engine/orchestrator.py#2323-2352#10c49738 — [[F:src/engine/orchestrator.py#2323-2352#10c49738]].
- Orchestrator._price_preview_loop (method, lines 2354-2389): CHUNK_ID = src/engine/orchestrator.py#2354-2389#10c49738 — [[F:src/engine/orchestrator.py#2354-2389#10c49738]].
- Orchestrator._register_kill_switches (method, lines 2391-2423): CHUNK_ID = src/engine/orchestrator.py#2391-2423#10c49738 — [[F:src/engine/orchestrator.py#2391-2423#10c49738]].
- Orchestrator.set_intelligence_adapter (method, lines 2425-2427): CHUNK_ID = src/engine/orchestrator.py#2425-2427#10c49738 — [[F:src/engine/orchestrator.py#2425-2427#10c49738]].
- Orchestrator._apply_intelligence_order_gate (method, lines 2429-2466, slice 1): CHUNK_ID = src/engine/orchestrator.py#2429-2466#10c49738 — [[F:src/engine/orchestrator.py#2429-2466#10c49738]].
- Orchestrator._apply_intelligence_order_gate (method, lines 2467-2492, slice 2): CHUNK_ID = src/engine/orchestrator.py#2467-2492#10c49738 — [[F:src/engine/orchestrator.py#2467-2492#10c49738]].
- Orchestrator._process_intelligence_bar (method, lines 2494-2531, slice 1): CHUNK_ID = src/engine/orchestrator.py#2494-2531#10c49738 — [[F:src/engine/orchestrator.py#2494-2531#10c49738]].
- Orchestrator._process_intelligence_bar (method, lines 2532-2547, slice 2): CHUNK_ID = src/engine/orchestrator.py#2532-2547#10c49738 — [[F:src/engine/orchestrator.py#2532-2547#10c49738]].
- Orchestrator._macro_exposure_budget (method, lines 2549-2585): CHUNK_ID = src/engine/orchestrator.py#2549-2585#10c49738 — [[F:src/engine/orchestrator.py#2549-2585#10c49738]].
- Orchestrator._prune_old_bars (method, lines 2587-2619): CHUNK_ID = src/engine/orchestrator.py#2587-2619#10c49738 — [[F:src/engine/orchestrator.py#2587-2619#10c49738]].
- Orchestrator._attach_intelligence_features (method, lines 2621-2658, slice 1): CHUNK_ID = src/engine/orchestrator.py#2621-2658#10c49738 — [[F:src/engine/orchestrator.py#2621-2658#10c49738]].
- Orchestrator._attach_intelligence_features (method, lines 2659-2679, slice 2): CHUNK_ID = src/engine/orchestrator.py#2659-2679#10c49738 — [[F:src/engine/orchestrator.py#2659-2679#10c49738]].
- Orchestrator._venue_for (method, lines 2681-2690): CHUNK_ID = src/engine/orchestrator.py#2681-2690#10c49738 — [[F:src/engine/orchestrator.py#2681-2690#10c49738]].
- Orchestrator._sync_and_read_ledger (method, lines 2692-2729, slice 1): CHUNK_ID = src/engine/orchestrator.py#2692-2729#10c49738 — [[F:src/engine/orchestrator.py#2692-2729#10c49738]].
- Orchestrator._sync_and_read_ledger (method, lines 2730-2741, slice 2): CHUNK_ID = src/engine/orchestrator.py#2730-2741#10c49738 — [[F:src/engine/orchestrator.py#2730-2741#10c49738]].
- Orchestrator._strategy_correlation_scalar (method, lines 2743-2765): CHUNK_ID = src/engine/orchestrator.py#2743-2765#10c49738 — [[F:src/engine/orchestrator.py#2743-2765#10c49738]].
- Orchestrator._push_strategy_returns (method, lines 2767-2804, slice 1): CHUNK_ID = src/engine/orchestrator.py#2767-2804#10c49738 — [[F:src/engine/orchestrator.py#2767-2804#10c49738]].
- Orchestrator._push_strategy_returns (method, lines 2805-2828, slice 2): CHUNK_ID = src/engine/orchestrator.py#2805-2828#10c49738 — [[F:src/engine/orchestrator.py#2805-2828#10c49738]].
- Orchestrator._record_kill_switch_outcome (method, lines 2830-2867, slice 1): CHUNK_ID = src/engine/orchestrator.py#2830-2867#10c49738 — [[F:src/engine/orchestrator.py#2830-2867#10c49738]].
- Orchestrator._record_kill_switch_outcome (method, lines 2868-2886, slice 2): CHUNK_ID = src/engine/orchestrator.py#2868-2886#10c49738 — [[F:src/engine/orchestrator.py#2868-2886#10c49738]].
- Orchestrator._publish_signal_to_registry (method, lines 2888-2908): CHUNK_ID = src/engine/orchestrator.py#2888-2908#10c49738 — [[F:src/engine/orchestrator.py#2888-2908#10c49738]].
- Orchestrator._build_portfolio_inputs (method, lines 2910-2947, slice 1): CHUNK_ID = src/engine/orchestrator.py#2910-2947#10c49738 — [[F:src/engine/orchestrator.py#2910-2947#10c49738]].
- Orchestrator._build_portfolio_inputs (method, lines 2948-2985, slice 2): CHUNK_ID = src/engine/orchestrator.py#2948-2985#10c49738 — [[F:src/engine/orchestrator.py#2948-2985#10c49738]].
- Orchestrator._build_portfolio_inputs (method, lines 2986-3023, slice 3): CHUNK_ID = src/engine/orchestrator.py#2986-3023#10c49738 — [[F:src/engine/orchestrator.py#2986-3023#10c49738]].
- Orchestrator._build_portfolio_inputs (method, lines 3024-3056, slice 4): CHUNK_ID = src/engine/orchestrator.py#3024-3056#10c49738 — [[F:src/engine/orchestrator.py#3024-3056#10c49738]].
- Orchestrator._load_symbol_precision (method, lines 3058-3098): CHUNK_ID = src/engine/orchestrator.py#3058-3098#10c49738 — [[F:src/engine/orchestrator.py#3058-3098#10c49738]].
- Orchestrator._pair_series (method, lines 3100-3137, slice 1): CHUNK_ID = src/engine/orchestrator.py#3100-3137#10c49738 — [[F:src/engine/orchestrator.py#3100-3137#10c49738]].
- Orchestrator._pair_series (method, lines 3138-3175, slice 2): CHUNK_ID = src/engine/orchestrator.py#3138-3175#10c49738 — [[F:src/engine/orchestrator.py#3138-3175#10c49738]].
- Orchestrator._pair_series (method, lines 3176-3185, slice 3): CHUNK_ID = src/engine/orchestrator.py#3176-3185#10c49738 — [[F:src/engine/orchestrator.py#3176-3185#10c49738]].
- Orchestrator._quote (method, lines 3187-3228): CHUNK_ID = src/engine/orchestrator.py#3187-3228#10c49738 — [[F:src/engine/orchestrator.py#3187-3228#10c49738]].
- Orchestrator._fetch_basis_legs (method, lines 3230-3255): CHUNK_ID = src/engine/orchestrator.py#3230-3255#10c49738 — [[F:src/engine/orchestrator.py#3230-3255#10c49738]].
- Orchestrator._fetch_venue_prices (method, lines 3257-3289): CHUNK_ID = src/engine/orchestrator.py#3257-3289#10c49738 — [[F:src/engine/orchestrator.py#3257-3289#10c49738]].
- Orchestrator._evaluate_strategy_portfolio (method, lines 3291-3328, slice 1): CHUNK_ID = src/engine/orchestrator.py#3291-3328#10c49738 — [[F:src/engine/orchestrator.py#3291-3328#10c49738]].
- Orchestrator._evaluate_strategy_portfolio (method, lines 3329-3366, slice 2): CHUNK_ID = src/engine/orchestrator.py#3329-3366#10c49738 — [[F:src/engine/orchestrator.py#3329-3366#10c49738]].
- Orchestrator._evaluate_strategy_portfolio (method, lines 3367-3368, slice 3): CHUNK_ID = src/engine/orchestrator.py#3367-3368#10c49738 — [[F:src/engine/orchestrator.py#3367-3368#10c49738]].
- Orchestrator.portfolio_evaluation (method, lines 3370-3386): CHUNK_ID = src/engine/orchestrator.py#3370-3386#10c49738 — [[F:src/engine/orchestrator.py#3370-3386#10c49738]].
- Orchestrator._monitor_positions_for (method, lines 3388-3425, slice 1): CHUNK_ID = src/engine/orchestrator.py#3388-3425#10c49738 — [[F:src/engine/orchestrator.py#3388-3425#10c49738]].
- Orchestrator._monitor_positions_for (method, lines 3426-3463, slice 2): CHUNK_ID = src/engine/orchestrator.py#3426-3463#10c49738 — [[F:src/engine/orchestrator.py#3426-3463#10c49738]].
- Orchestrator._monitor_positions_for (method, lines 3464-3483, slice 3): CHUNK_ID = src/engine/orchestrator.py#3464-3483#10c49738 — [[F:src/engine/orchestrator.py#3464-3483#10c49738]].

## src/engine/signal_engine.py

SHA8 c4c078db; total lines 1898.

- ShadowBundle (class, lines 124-142): CHUNK_ID = src/engine/signal_engine.py#124-142#c4c078db — [[F:src/engine/signal_engine.py#124-142#c4c078db]].
- _PendingShadowObservation (class, lines 146-157): CHUNK_ID = src/engine/signal_engine.py#146-157#c4c078db — [[F:src/engine/signal_engine.py#146-157#c4c078db]].
- _append_decision_log (function, lines 160-167): CHUNK_ID = src/engine/signal_engine.py#160-167#c4c078db — [[F:src/engine/signal_engine.py#160-167#c4c078db]].
- SignalResult (class, lines 176-213, slice 1): CHUNK_ID = src/engine/signal_engine.py#176-213#c4c078db — [[F:src/engine/signal_engine.py#176-213#c4c078db]].
- SignalResult (class, lines 214-223, slice 2): CHUNK_ID = src/engine/signal_engine.py#214-223#c4c078db — [[F:src/engine/signal_engine.py#214-223#c4c078db]].
- SignalEngine (class, lines 231-268, slice 1): CHUNK_ID = src/engine/signal_engine.py#231-268#c4c078db — [[F:src/engine/signal_engine.py#231-268#c4c078db]].
- SignalEngine (class, lines 269-306, slice 2): CHUNK_ID = src/engine/signal_engine.py#269-306#c4c078db — [[F:src/engine/signal_engine.py#269-306#c4c078db]].
- SignalEngine (class, lines 307-344, slice 3): CHUNK_ID = src/engine/signal_engine.py#307-344#c4c078db — [[F:src/engine/signal_engine.py#307-344#c4c078db]].
- SignalEngine (class, lines 345-382, slice 4): CHUNK_ID = src/engine/signal_engine.py#345-382#c4c078db — [[F:src/engine/signal_engine.py#345-382#c4c078db]].
- SignalEngine (class, lines 383-420, slice 5): CHUNK_ID = src/engine/signal_engine.py#383-420#c4c078db — [[F:src/engine/signal_engine.py#383-420#c4c078db]].
- SignalEngine (class, lines 421-458, slice 6): CHUNK_ID = src/engine/signal_engine.py#421-458#c4c078db — [[F:src/engine/signal_engine.py#421-458#c4c078db]].
- SignalEngine (class, lines 459-496, slice 7): CHUNK_ID = src/engine/signal_engine.py#459-496#c4c078db — [[F:src/engine/signal_engine.py#459-496#c4c078db]].
- SignalEngine (class, lines 497-534, slice 8): CHUNK_ID = src/engine/signal_engine.py#497-534#c4c078db — [[F:src/engine/signal_engine.py#497-534#c4c078db]].
- SignalEngine (class, lines 535-572, slice 9): CHUNK_ID = src/engine/signal_engine.py#535-572#c4c078db — [[F:src/engine/signal_engine.py#535-572#c4c078db]].
- SignalEngine (class, lines 573-610, slice 10): CHUNK_ID = src/engine/signal_engine.py#573-610#c4c078db — [[F:src/engine/signal_engine.py#573-610#c4c078db]].
- SignalEngine (class, lines 611-648, slice 11): CHUNK_ID = src/engine/signal_engine.py#611-648#c4c078db — [[F:src/engine/signal_engine.py#611-648#c4c078db]].
- SignalEngine (class, lines 649-686, slice 12): CHUNK_ID = src/engine/signal_engine.py#649-686#c4c078db — [[F:src/engine/signal_engine.py#649-686#c4c078db]].
- SignalEngine (class, lines 687-724, slice 13): CHUNK_ID = src/engine/signal_engine.py#687-724#c4c078db — [[F:src/engine/signal_engine.py#687-724#c4c078db]].
- SignalEngine (class, lines 725-762, slice 14): CHUNK_ID = src/engine/signal_engine.py#725-762#c4c078db — [[F:src/engine/signal_engine.py#725-762#c4c078db]].
- SignalEngine (class, lines 763-800, slice 15): CHUNK_ID = src/engine/signal_engine.py#763-800#c4c078db — [[F:src/engine/signal_engine.py#763-800#c4c078db]].
- SignalEngine (class, lines 801-838, slice 16): CHUNK_ID = src/engine/signal_engine.py#801-838#c4c078db — [[F:src/engine/signal_engine.py#801-838#c4c078db]].
- SignalEngine (class, lines 839-876, slice 17): CHUNK_ID = src/engine/signal_engine.py#839-876#c4c078db — [[F:src/engine/signal_engine.py#839-876#c4c078db]].
- SignalEngine (class, lines 877-914, slice 18): CHUNK_ID = src/engine/signal_engine.py#877-914#c4c078db — [[F:src/engine/signal_engine.py#877-914#c4c078db]].
- SignalEngine (class, lines 915-952, slice 19): CHUNK_ID = src/engine/signal_engine.py#915-952#c4c078db — [[F:src/engine/signal_engine.py#915-952#c4c078db]].
- SignalEngine (class, lines 953-990, slice 20): CHUNK_ID = src/engine/signal_engine.py#953-990#c4c078db — [[F:src/engine/signal_engine.py#953-990#c4c078db]].
- SignalEngine (class, lines 991-1028, slice 21): CHUNK_ID = src/engine/signal_engine.py#991-1028#c4c078db — [[F:src/engine/signal_engine.py#991-1028#c4c078db]].
- SignalEngine (class, lines 1029-1066, slice 22): CHUNK_ID = src/engine/signal_engine.py#1029-1066#c4c078db — [[F:src/engine/signal_engine.py#1029-1066#c4c078db]].
- SignalEngine (class, lines 1067-1104, slice 23): CHUNK_ID = src/engine/signal_engine.py#1067-1104#c4c078db — [[F:src/engine/signal_engine.py#1067-1104#c4c078db]].
- SignalEngine (class, lines 1105-1142, slice 24): CHUNK_ID = src/engine/signal_engine.py#1105-1142#c4c078db — [[F:src/engine/signal_engine.py#1105-1142#c4c078db]].
- SignalEngine (class, lines 1143-1180, slice 25): CHUNK_ID = src/engine/signal_engine.py#1143-1180#c4c078db — [[F:src/engine/signal_engine.py#1143-1180#c4c078db]].
- SignalEngine (class, lines 1181-1218, slice 26): CHUNK_ID = src/engine/signal_engine.py#1181-1218#c4c078db — [[F:src/engine/signal_engine.py#1181-1218#c4c078db]].
- SignalEngine (class, lines 1219-1256, slice 27): CHUNK_ID = src/engine/signal_engine.py#1219-1256#c4c078db — [[F:src/engine/signal_engine.py#1219-1256#c4c078db]].
- SignalEngine (class, lines 1257-1294, slice 28): CHUNK_ID = src/engine/signal_engine.py#1257-1294#c4c078db — [[F:src/engine/signal_engine.py#1257-1294#c4c078db]].
- SignalEngine (class, lines 1295-1332, slice 29): CHUNK_ID = src/engine/signal_engine.py#1295-1332#c4c078db — [[F:src/engine/signal_engine.py#1295-1332#c4c078db]].
- SignalEngine (class, lines 1333-1370, slice 30): CHUNK_ID = src/engine/signal_engine.py#1333-1370#c4c078db — [[F:src/engine/signal_engine.py#1333-1370#c4c078db]].
- SignalEngine (class, lines 1371-1408, slice 31): CHUNK_ID = src/engine/signal_engine.py#1371-1408#c4c078db — [[F:src/engine/signal_engine.py#1371-1408#c4c078db]].
- SignalEngine (class, lines 1409-1446, slice 32): CHUNK_ID = src/engine/signal_engine.py#1409-1446#c4c078db — [[F:src/engine/signal_engine.py#1409-1446#c4c078db]].
- SignalEngine (class, lines 1447-1484, slice 33): CHUNK_ID = src/engine/signal_engine.py#1447-1484#c4c078db — [[F:src/engine/signal_engine.py#1447-1484#c4c078db]].
- SignalEngine (class, lines 1485-1522, slice 34): CHUNK_ID = src/engine/signal_engine.py#1485-1522#c4c078db — [[F:src/engine/signal_engine.py#1485-1522#c4c078db]].
- SignalEngine (class, lines 1523-1560, slice 35): CHUNK_ID = src/engine/signal_engine.py#1523-1560#c4c078db — [[F:src/engine/signal_engine.py#1523-1560#c4c078db]].
- SignalEngine (class, lines 1561-1598, slice 36): CHUNK_ID = src/engine/signal_engine.py#1561-1598#c4c078db — [[F:src/engine/signal_engine.py#1561-1598#c4c078db]].
- SignalEngine (class, lines 1599-1636, slice 37): CHUNK_ID = src/engine/signal_engine.py#1599-1636#c4c078db — [[F:src/engine/signal_engine.py#1599-1636#c4c078db]].
- SignalEngine (class, lines 1637-1674, slice 38): CHUNK_ID = src/engine/signal_engine.py#1637-1674#c4c078db — [[F:src/engine/signal_engine.py#1637-1674#c4c078db]].
- SignalEngine (class, lines 1675-1712, slice 39): CHUNK_ID = src/engine/signal_engine.py#1675-1712#c4c078db — [[F:src/engine/signal_engine.py#1675-1712#c4c078db]].
- SignalEngine (class, lines 1713-1750, slice 40): CHUNK_ID = src/engine/signal_engine.py#1713-1750#c4c078db — [[F:src/engine/signal_engine.py#1713-1750#c4c078db]].
- SignalEngine (class, lines 1751-1788, slice 41): CHUNK_ID = src/engine/signal_engine.py#1751-1788#c4c078db — [[F:src/engine/signal_engine.py#1751-1788#c4c078db]].
- SignalEngine (class, lines 1789-1826, slice 42): CHUNK_ID = src/engine/signal_engine.py#1789-1826#c4c078db — [[F:src/engine/signal_engine.py#1789-1826#c4c078db]].
- SignalEngine (class, lines 1827-1864, slice 43): CHUNK_ID = src/engine/signal_engine.py#1827-1864#c4c078db — [[F:src/engine/signal_engine.py#1827-1864#c4c078db]].
- SignalEngine (class, lines 1865-1898, slice 44): CHUNK_ID = src/engine/signal_engine.py#1865-1898#c4c078db — [[F:src/engine/signal_engine.py#1865-1898#c4c078db]].
- SignalEngine.__init__ (method, lines 260-297, slice 1): CHUNK_ID = src/engine/signal_engine.py#260-297#c4c078db — [[F:src/engine/signal_engine.py#260-297#c4c078db]].
- SignalEngine.__init__ (method, lines 298-335, slice 2): CHUNK_ID = src/engine/signal_engine.py#298-335#c4c078db — [[F:src/engine/signal_engine.py#298-335#c4c078db]].
- SignalEngine.__init__ (method, lines 336-344, slice 3): CHUNK_ID = src/engine/signal_engine.py#336-344#c4c078db — [[F:src/engine/signal_engine.py#336-344#c4c078db]].
- SignalEngine._cfg (method, lines 356-366): CHUNK_ID = src/engine/signal_engine.py#356-366#c4c078db — [[F:src/engine/signal_engine.py#356-366#c4c078db]].
- SignalEngine._cfg (method, lines 369-379): CHUNK_ID = src/engine/signal_engine.py#369-379#c4c078db — [[F:src/engine/signal_engine.py#369-379#c4c078db]].
- SignalEngine.swap_models (method, lines 381-414): CHUNK_ID = src/engine/signal_engine.py#381-414#c4c078db — [[F:src/engine/signal_engine.py#381-414#c4c078db]].
- SignalEngine.set_shadow_bundle (method, lines 420-435): CHUNK_ID = src/engine/signal_engine.py#420-435#c4c078db — [[F:src/engine/signal_engine.py#420-435#c4c078db]].
- SignalEngine.live_model_id (method, lines 438-440): CHUNK_ID = src/engine/signal_engine.py#438-440#c4c078db — [[F:src/engine/signal_engine.py#438-440#c4c078db]].
- SignalEngine.shadow_model_id (method, lines 443-445): CHUNK_ID = src/engine/signal_engine.py#443-445#c4c078db — [[F:src/engine/signal_engine.py#443-445#c4c078db]].
- SignalEngine.shadow_evaluations (method, lines 447-452): CHUNK_ID = src/engine/signal_engine.py#447-452#c4c078db — [[F:src/engine/signal_engine.py#447-452#c4c078db]].
- SignalEngine.discard_shadow_now (method, lines 454-471): CHUNK_ID = src/engine/signal_engine.py#454-471#c4c078db — [[F:src/engine/signal_engine.py#454-471#c4c078db]].
- SignalEngine._discard_shadow_locked (method, lines 473-482): CHUNK_ID = src/engine/signal_engine.py#473-482#c4c078db — [[F:src/engine/signal_engine.py#473-482#c4c078db]].
- SignalEngine._evaluate_shadow_tick (method, lines 484-521, slice 1): CHUNK_ID = src/engine/signal_engine.py#484-521#c4c078db — [[F:src/engine/signal_engine.py#484-521#c4c078db]].
- SignalEngine._evaluate_shadow_tick (method, lines 522-559, slice 2): CHUNK_ID = src/engine/signal_engine.py#522-559#c4c078db — [[F:src/engine/signal_engine.py#522-559#c4c078db]].
- SignalEngine._evaluate_shadow_tick (method, lines 560-595, slice 3): CHUNK_ID = src/engine/signal_engine.py#560-595#c4c078db — [[F:src/engine/signal_engine.py#560-595#c4c078db]].
- SignalEngine._record_promotion (method, lines 597-638): CHUNK_ID = src/engine/signal_engine.py#597-638#c4c078db — [[F:src/engine/signal_engine.py#597-638#c4c078db]].
- SignalEngine.shadow_status (method, lines 640-657): CHUNK_ID = src/engine/signal_engine.py#640-657#c4c078db — [[F:src/engine/signal_engine.py#640-657#c4c078db]].
- SignalEngine.tick (method, lines 663-700, slice 1): CHUNK_ID = src/engine/signal_engine.py#663-700#c4c078db — [[F:src/engine/signal_engine.py#663-700#c4c078db]].
- SignalEngine.tick (method, lines 701-738, slice 2): CHUNK_ID = src/engine/signal_engine.py#701-738#c4c078db — [[F:src/engine/signal_engine.py#701-738#c4c078db]].
- SignalEngine.tick (method, lines 739-776, slice 3): CHUNK_ID = src/engine/signal_engine.py#739-776#c4c078db — [[F:src/engine/signal_engine.py#739-776#c4c078db]].
- SignalEngine.tick (method, lines 777-814, slice 4): CHUNK_ID = src/engine/signal_engine.py#777-814#c4c078db — [[F:src/engine/signal_engine.py#777-814#c4c078db]].
- SignalEngine.tick (method, lines 815-852, slice 5): CHUNK_ID = src/engine/signal_engine.py#815-852#c4c078db — [[F:src/engine/signal_engine.py#815-852#c4c078db]].
- SignalEngine.tick (method, lines 853-890, slice 6): CHUNK_ID = src/engine/signal_engine.py#853-890#c4c078db — [[F:src/engine/signal_engine.py#853-890#c4c078db]].
- SignalEngine.tick (method, lines 891-928, slice 7): CHUNK_ID = src/engine/signal_engine.py#891-928#c4c078db — [[F:src/engine/signal_engine.py#891-928#c4c078db]].
- SignalEngine.tick (method, lines 929-966, slice 8): CHUNK_ID = src/engine/signal_engine.py#929-966#c4c078db — [[F:src/engine/signal_engine.py#929-966#c4c078db]].
- SignalEngine.tick (method, lines 967-1004, slice 9): CHUNK_ID = src/engine/signal_engine.py#967-1004#c4c078db — [[F:src/engine/signal_engine.py#967-1004#c4c078db]].
- SignalEngine.tick (method, lines 1005-1042, slice 10): CHUNK_ID = src/engine/signal_engine.py#1005-1042#c4c078db — [[F:src/engine/signal_engine.py#1005-1042#c4c078db]].
- SignalEngine.tick (method, lines 1043-1080, slice 11): CHUNK_ID = src/engine/signal_engine.py#1043-1080#c4c078db — [[F:src/engine/signal_engine.py#1043-1080#c4c078db]].
- SignalEngine.tick (method, lines 1081-1118, slice 12): CHUNK_ID = src/engine/signal_engine.py#1081-1118#c4c078db — [[F:src/engine/signal_engine.py#1081-1118#c4c078db]].
- SignalEngine.tick (method, lines 1119-1156, slice 13): CHUNK_ID = src/engine/signal_engine.py#1119-1156#c4c078db — [[F:src/engine/signal_engine.py#1119-1156#c4c078db]].
- SignalEngine.tick (method, lines 1157-1194, slice 14): CHUNK_ID = src/engine/signal_engine.py#1157-1194#c4c078db — [[F:src/engine/signal_engine.py#1157-1194#c4c078db]].
- SignalEngine.tick (method, lines 1195-1232, slice 15): CHUNK_ID = src/engine/signal_engine.py#1195-1232#c4c078db — [[F:src/engine/signal_engine.py#1195-1232#c4c078db]].
- SignalEngine.tick (method, lines 1233-1270, slice 16): CHUNK_ID = src/engine/signal_engine.py#1233-1270#c4c078db — [[F:src/engine/signal_engine.py#1233-1270#c4c078db]].
- SignalEngine.tick (method, lines 1271-1308, slice 17): CHUNK_ID = src/engine/signal_engine.py#1271-1308#c4c078db — [[F:src/engine/signal_engine.py#1271-1308#c4c078db]].
- SignalEngine.tick (method, lines 1309-1346, slice 18): CHUNK_ID = src/engine/signal_engine.py#1309-1346#c4c078db — [[F:src/engine/signal_engine.py#1309-1346#c4c078db]].
- SignalEngine.tick (method, lines 1347-1384, slice 19): CHUNK_ID = src/engine/signal_engine.py#1347-1384#c4c078db — [[F:src/engine/signal_engine.py#1347-1384#c4c078db]].
- SignalEngine.tick (method, lines 1385-1422, slice 20): CHUNK_ID = src/engine/signal_engine.py#1385-1422#c4c078db — [[F:src/engine/signal_engine.py#1385-1422#c4c078db]].
- SignalEngine.tick (method, lines 1423-1460, slice 21): CHUNK_ID = src/engine/signal_engine.py#1423-1460#c4c078db — [[F:src/engine/signal_engine.py#1423-1460#c4c078db]].
- SignalEngine.tick (method, lines 1461-1498, slice 22): CHUNK_ID = src/engine/signal_engine.py#1461-1498#c4c078db — [[F:src/engine/signal_engine.py#1461-1498#c4c078db]].
- SignalEngine.tick (method, lines 1499-1536, slice 23): CHUNK_ID = src/engine/signal_engine.py#1499-1536#c4c078db — [[F:src/engine/signal_engine.py#1499-1536#c4c078db]].
- SignalEngine.tick (method, lines 1537-1574, slice 24): CHUNK_ID = src/engine/signal_engine.py#1537-1574#c4c078db — [[F:src/engine/signal_engine.py#1537-1574#c4c078db]].
- SignalEngine.tick (method, lines 1575-1612, slice 25): CHUNK_ID = src/engine/signal_engine.py#1575-1612#c4c078db — [[F:src/engine/signal_engine.py#1575-1612#c4c078db]].
- SignalEngine.tick (method, lines 1613-1624, slice 26): CHUNK_ID = src/engine/signal_engine.py#1613-1624#c4c078db — [[F:src/engine/signal_engine.py#1613-1624#c4c078db]].
- SignalEngine._load_bars (method, lines 1630-1665): CHUNK_ID = src/engine/signal_engine.py#1630-1665#c4c078db — [[F:src/engine/signal_engine.py#1630-1665#c4c078db]].
- SignalEngine._record_p_long_for_bar (method, lines 1667-1690): CHUNK_ID = src/engine/signal_engine.py#1667-1690#c4c078db — [[F:src/engine/signal_engine.py#1667-1690#c4c078db]].
- SignalEngine._learn_online (method, lines 1692-1729, slice 1): CHUNK_ID = src/engine/signal_engine.py#1692-1729#c4c078db — [[F:src/engine/signal_engine.py#1692-1729#c4c078db]].
- SignalEngine._learn_online (method, lines 1730-1767, slice 2): CHUNK_ID = src/engine/signal_engine.py#1730-1767#c4c078db — [[F:src/engine/signal_engine.py#1730-1767#c4c078db]].
- SignalEngine._learn_online (method, lines 1768-1770, slice 3): CHUNK_ID = src/engine/signal_engine.py#1768-1770#c4c078db — [[F:src/engine/signal_engine.py#1768-1770#c4c078db]].
- SignalEngine._blend_online (method, lines 1772-1796): CHUNK_ID = src/engine/signal_engine.py#1772-1796#c4c078db — [[F:src/engine/signal_engine.py#1772-1796#c4c078db]].
- SignalEngine._cvar_notional_cap (method, lines 1798-1840): CHUNK_ID = src/engine/signal_engine.py#1798-1840#c4c078db — [[F:src/engine/signal_engine.py#1798-1840#c4c078db]].
- SignalEngine._persist_intelligence_features (method, lines 1842-1885): CHUNK_ID = src/engine/signal_engine.py#1842-1885#c4c078db — [[F:src/engine/signal_engine.py#1842-1885#c4c078db]].
- SignalEngine._skip (method, lines 1887-1898): CHUNK_ID = src/engine/signal_engine.py#1887-1898#c4c078db — [[F:src/engine/signal_engine.py#1887-1898#c4c078db]].

## src/features/pipeline.py

SHA8 32403b07; total lines 1204.

- get_active_feature_columns (function, lines 84-121, slice 1): CHUNK_ID = src/features/pipeline.py#84-121#32403b07 — [[F:src/features/pipeline.py#84-121#32403b07]].
- get_active_feature_columns (function, lines 122-146, slice 2): CHUNK_ID = src/features/pipeline.py#122-146#32403b07 — [[F:src/features/pipeline.py#122-146#32403b07]].
- _frac_diff_weights (function, lines 172-198): CHUNK_ID = src/features/pipeline.py#172-198#32403b07 — [[F:src/features/pipeline.py#172-198#32403b07]].
- fractional_differentiation (function, lines 201-241): CHUNK_ID = src/features/pipeline.py#201-241#32403b07 — [[F:src/features/pipeline.py#201-241#32403b07]].
- vwap_deviation_zscore (function, lines 249-277): CHUNK_ID = src/features/pipeline.py#249-277#32403b07 — [[F:src/features/pipeline.py#249-277#32403b07]].
- order_flow_imbalance (function, lines 285-306): CHUNK_ID = src/features/pipeline.py#285-306#32403b07 — [[F:src/features/pipeline.py#285-306#32403b07]].
- realized_vol_ratio (function, lines 314-339): CHUNK_ID = src/features/pipeline.py#314-339#32403b07 — [[F:src/features/pipeline.py#314-339#32403b07]].
- atr_momentum (function, lines 347-375): CHUNK_ID = src/features/pipeline.py#347-375#32403b07 — [[F:src/features/pipeline.py#347-375#32403b07]].
- rolling_sharpe (function, lines 383-401): CHUNK_ID = src/features/pipeline.py#383-401#32403b07 — [[F:src/features/pipeline.py#383-401#32403b07]].
- volume_zscore (function, lines 409-424): CHUNK_ID = src/features/pipeline.py#409-424#32403b07 — [[F:src/features/pipeline.py#409-424#32403b07]].
- TripleBarrierResult (class, lines 433-444): CHUNK_ID = src/features/pipeline.py#433-444#32403b07 — [[F:src/features/pipeline.py#433-444#32403b07]].
- TripleBarrierComposition (class, lines 448-487): CHUNK_ID = src/features/pipeline.py#448-487#32403b07 — [[F:src/features/pipeline.py#448-487#32403b07]].
- TripleBarrierComposition.total (method, lines 471-472): CHUNK_ID = src/features/pipeline.py#471-472#32403b07 — [[F:src/features/pipeline.py#471-472#32403b07]].
- TripleBarrierComposition.time_exit_fraction (method, lines 475-477): CHUNK_ID = src/features/pipeline.py#475-477#32403b07 — [[F:src/features/pipeline.py#475-477#32403b07]].
- TripleBarrierComposition.as_dict (method, lines 479-487): CHUNK_ID = src/features/pipeline.py#479-487#32403b07 — [[F:src/features/pipeline.py#479-487#32403b07]].
- _compute_daily_vol (function, lines 490-496): CHUNK_ID = src/features/pipeline.py#490-496#32403b07 — [[F:src/features/pipeline.py#490-496#32403b07]].
- triple_barrier_labels_with_offsets (function, lines 499-536, slice 1): CHUNK_ID = src/features/pipeline.py#499-536#32403b07 — [[F:src/features/pipeline.py#499-536#32403b07]].
- triple_barrier_labels_with_offsets (function, lines 537-574, slice 2): CHUNK_ID = src/features/pipeline.py#537-574#32403b07 — [[F:src/features/pipeline.py#537-574#32403b07]].
- triple_barrier_labels_with_offsets (function, lines 575-595, slice 3): CHUNK_ID = src/features/pipeline.py#575-595#32403b07 — [[F:src/features/pipeline.py#575-595#32403b07]].
- triple_barrier_labels (function, lines 598-615): CHUNK_ID = src/features/pipeline.py#598-615#32403b07 — [[F:src/features/pipeline.py#598-615#32403b07]].
- summarize_triple_barrier (function, lines 618-636): CHUNK_ID = src/features/pipeline.py#618-636#32403b07 — [[F:src/features/pipeline.py#618-636#32403b07]].
- meta_labels (function, lines 644-675): CHUNK_ID = src/features/pipeline.py#644-675#32403b07 — [[F:src/features/pipeline.py#644-675#32403b07]].
- FeatureMatrix (class, lines 684-702): CHUNK_ID = src/features/pipeline.py#684-702#32403b07 — [[F:src/features/pipeline.py#684-702#32403b07]].
- bar_gap_report (function, lines 710-747, slice 1): CHUNK_ID = src/features/pipeline.py#710-747#32403b07 — [[F:src/features/pipeline.py#710-747#32403b07]].
- bar_gap_report (function, lines 748-755, slice 2): CHUNK_ID = src/features/pipeline.py#748-755#32403b07 — [[F:src/features/pipeline.py#748-755#32403b07]].
- _warn_on_bar_gaps (function, lines 758-768): CHUNK_ID = src/features/pipeline.py#758-768#32403b07 — [[F:src/features/pipeline.py#758-768#32403b07]].
- build_feature_matrix (function, lines 771-808, slice 1): CHUNK_ID = src/features/pipeline.py#771-808#32403b07 — [[F:src/features/pipeline.py#771-808#32403b07]].
- build_feature_matrix (function, lines 809-846, slice 2): CHUNK_ID = src/features/pipeline.py#809-846#32403b07 — [[F:src/features/pipeline.py#809-846#32403b07]].
- build_feature_matrix (function, lines 847-884, slice 3): CHUNK_ID = src/features/pipeline.py#847-884#32403b07 — [[F:src/features/pipeline.py#847-884#32403b07]].
- build_feature_matrix (function, lines 885-922, slice 4): CHUNK_ID = src/features/pipeline.py#885-922#32403b07 — [[F:src/features/pipeline.py#885-922#32403b07]].
- build_feature_matrix (function, lines 923-960, slice 5): CHUNK_ID = src/features/pipeline.py#923-960#32403b07 — [[F:src/features/pipeline.py#923-960#32403b07]].
- build_feature_matrix (function, lines 961-985, slice 6): CHUNK_ID = src/features/pipeline.py#961-985#32403b07 — [[F:src/features/pipeline.py#961-985#32403b07]].
- build_inference_features (function, lines 993-1030, slice 1): CHUNK_ID = src/features/pipeline.py#993-1030#32403b07 — [[F:src/features/pipeline.py#993-1030#32403b07]].
- build_inference_features (function, lines 1031-1068, slice 2): CHUNK_ID = src/features/pipeline.py#1031-1068#32403b07 — [[F:src/features/pipeline.py#1031-1068#32403b07]].
- build_inference_features (function, lines 1069-1106, slice 3): CHUNK_ID = src/features/pipeline.py#1069-1106#32403b07 — [[F:src/features/pipeline.py#1069-1106#32403b07]].
- build_inference_features (function, lines 1107-1131, slice 4): CHUNK_ID = src/features/pipeline.py#1107-1131#32403b07 — [[F:src/features/pipeline.py#1107-1131#32403b07]].
- _inject_intelligence_features (function, lines 1139-1176, slice 1): CHUNK_ID = src/features/pipeline.py#1139-1176#32403b07 — [[F:src/features/pipeline.py#1139-1176#32403b07]].
- _inject_intelligence_features (function, lines 1177-1204, slice 2): CHUNK_ID = src/features/pipeline.py#1177-1204#32403b07 — [[F:src/features/pipeline.py#1177-1204#32403b07]].

## src/risk/gates.py

SHA8 36a7f38f; total lines 1281.

- GateStatus (class, lines 62-76): CHUNK_ID = src/risk/gates.py#62-76#36a7f38f — [[F:src/risk/gates.py#62-76#36a7f38f]].
- _non_finite (function, lines 79-94): CHUNK_ID = src/risk/gates.py#79-94#36a7f38f — [[F:src/risk/gates.py#79-94#36a7f38f]].
- GateResult (class, lines 98-135, slice 1): CHUNK_ID = src/risk/gates.py#98-135#36a7f38f — [[F:src/risk/gates.py#98-135#36a7f38f]].
- GateResult (class, lines 136-169, slice 2): CHUNK_ID = src/risk/gates.py#136-169#36a7f38f — [[F:src/risk/gates.py#136-169#36a7f38f]].
- GateResult.pass_gate (method, lines 124-130): CHUNK_ID = src/risk/gates.py#124-130#36a7f38f — [[F:src/risk/gates.py#124-130#36a7f38f]].
- GateResult.fail (method, lines 133-144): CHUNK_ID = src/risk/gates.py#133-144#36a7f38f — [[F:src/risk/gates.py#133-144#36a7f38f]].
- GateResult.reduce (method, lines 147-169): CHUNK_ID = src/risk/gates.py#147-169#36a7f38f — [[F:src/risk/gates.py#147-169#36a7f38f]].
- check_slippage_veto (function, lines 177-214, slice 1): CHUNK_ID = src/risk/gates.py#177-214#36a7f38f — [[F:src/risk/gates.py#177-214#36a7f38f]].
- check_slippage_veto (function, lines 215-252, slice 2): CHUNK_ID = src/risk/gates.py#215-252#36a7f38f — [[F:src/risk/gates.py#215-252#36a7f38f]].
- check_slippage_veto (function, lines 253-263, slice 3): CHUNK_ID = src/risk/gates.py#253-263#36a7f38f — [[F:src/risk/gates.py#253-263#36a7f38f]].
- check_capital_preservation_floor (function, lines 266-295): CHUNK_ID = src/risk/gates.py#266-295#36a7f38f — [[F:src/risk/gates.py#266-295#36a7f38f]].
- check_daily_drawdown (function, lines 298-335, slice 1): CHUNK_ID = src/risk/gates.py#298-335#36a7f38f — [[F:src/risk/gates.py#298-335#36a7f38f]].
- check_daily_drawdown (function, lines 336-366, slice 2): CHUNK_ID = src/risk/gates.py#336-366#36a7f38f — [[F:src/risk/gates.py#336-366#36a7f38f]].
- check_consecutive_losses (function, lines 369-408): CHUNK_ID = src/risk/gates.py#369-408#36a7f38f — [[F:src/risk/gates.py#369-408#36a7f38f]].
- check_regime_gate (function, lines 411-441): CHUNK_ID = src/risk/gates.py#411-441#36a7f38f — [[F:src/risk/gates.py#411-441#36a7f38f]].
- check_position_size (function, lines 444-481, slice 1): CHUNK_ID = src/risk/gates.py#444-481#36a7f38f — [[F:src/risk/gates.py#444-481#36a7f38f]].
- check_position_size (function, lines 482-509, slice 2): CHUNK_ID = src/risk/gates.py#482-509#36a7f38f — [[F:src/risk/gates.py#482-509#36a7f38f]].
- check_live_gate (function, lines 512-549, slice 1): CHUNK_ID = src/risk/gates.py#512-549#36a7f38f — [[F:src/risk/gates.py#512-549#36a7f38f]].
- check_live_gate (function, lines 550-562, slice 2): CHUNK_ID = src/risk/gates.py#550-562#36a7f38f — [[F:src/risk/gates.py#550-562#36a7f38f]].
- check_paper_minimum_days (function, lines 565-605): CHUNK_ID = src/risk/gates.py#565-605#36a7f38f — [[F:src/risk/gates.py#565-605#36a7f38f]].
- RiskGateContext (class, lines 614-651, slice 1): CHUNK_ID = src/risk/gates.py#614-651#36a7f38f — [[F:src/risk/gates.py#614-651#36a7f38f]].
- RiskGateContext (class, lines 652-666, slice 2): CHUNK_ID = src/risk/gates.py#652-666#36a7f38f — [[F:src/risk/gates.py#652-666#36a7f38f]].
- evaluate_all_gates (function, lines 669-706, slice 1): CHUNK_ID = src/risk/gates.py#669-706#36a7f38f — [[F:src/risk/gates.py#669-706#36a7f38f]].
- evaluate_all_gates (function, lines 707-744, slice 2): CHUNK_ID = src/risk/gates.py#707-744#36a7f38f — [[F:src/risk/gates.py#707-744#36a7f38f]].
- evaluate_all_gates (function, lines 745-782, slice 3): CHUNK_ID = src/risk/gates.py#745-782#36a7f38f — [[F:src/risk/gates.py#745-782#36a7f38f]].
- evaluate_all_gates (function, lines 783-805, slice 4): CHUNK_ID = src/risk/gates.py#783-805#36a7f38f — [[F:src/risk/gates.py#783-805#36a7f38f]].
- DrawdownTracker (class, lines 813-850, slice 1): CHUNK_ID = src/risk/gates.py#813-850#36a7f38f — [[F:src/risk/gates.py#813-850#36a7f38f]].
- DrawdownTracker (class, lines 851-888, slice 2): CHUNK_ID = src/risk/gates.py#851-888#36a7f38f — [[F:src/risk/gates.py#851-888#36a7f38f]].
- DrawdownTracker (class, lines 889-895, slice 3): CHUNK_ID = src/risk/gates.py#889-895#36a7f38f — [[F:src/risk/gates.py#889-895#36a7f38f]].
- DrawdownTracker.__init__ (method, lines 821-827): CHUNK_ID = src/risk/gates.py#821-827#36a7f38f — [[F:src/risk/gates.py#821-827#36a7f38f]].
- DrawdownTracker.update (method, lines 829-833): CHUNK_ID = src/risk/gates.py#829-833#36a7f38f — [[F:src/risk/gates.py#829-833#36a7f38f]].
- DrawdownTracker.reset_daily (method, lines 835-838): CHUNK_ID = src/risk/gates.py#835-838#36a7f38f — [[F:src/risk/gates.py#835-838#36a7f38f]].
- DrawdownTracker.daily_pnl_usd (method, lines 841-842): CHUNK_ID = src/risk/gates.py#841-842#36a7f38f — [[F:src/risk/gates.py#841-842#36a7f38f]].
- DrawdownTracker.daily_pnl_pct (method, lines 845-848): CHUNK_ID = src/risk/gates.py#845-848#36a7f38f — [[F:src/risk/gates.py#845-848#36a7f38f]].
- DrawdownTracker.drawdown_from_peak_pct (method, lines 851-862): CHUNK_ID = src/risk/gates.py#851-862#36a7f38f — [[F:src/risk/gates.py#851-862#36a7f38f]].
- DrawdownTracker.drawdown_from_alltime_peak_pct (method, lines 865-867): CHUNK_ID = src/risk/gates.py#865-867#36a7f38f — [[F:src/risk/gates.py#865-867#36a7f38f]].
- DrawdownTracker.drawdown_from_daily_start_pct (method, lines 870-879): CHUNK_ID = src/risk/gates.py#870-879#36a7f38f — [[F:src/risk/gates.py#870-879#36a7f38f]].
- DrawdownTracker.starting_equity (method, lines 882-883): CHUNK_ID = src/risk/gates.py#882-883#36a7f38f — [[F:src/risk/gates.py#882-883#36a7f38f]].
- DrawdownTracker.current_equity (method, lines 886-887): CHUNK_ID = src/risk/gates.py#886-887#36a7f38f — [[F:src/risk/gates.py#886-887#36a7f38f]].
- DrawdownTracker.peak_equity (method, lines 890-891): CHUNK_ID = src/risk/gates.py#890-891#36a7f38f — [[F:src/risk/gates.py#890-891#36a7f38f]].
- DrawdownTracker.daily_start_equity (method, lines 894-895): CHUNK_ID = src/risk/gates.py#894-895#36a7f38f — [[F:src/risk/gates.py#894-895#36a7f38f]].
- check_performance_drift (function, lines 903-940, slice 1): CHUNK_ID = src/risk/gates.py#903-940#36a7f38f — [[F:src/risk/gates.py#903-940#36a7f38f]].
- check_performance_drift (function, lines 941-972, slice 2): CHUNK_ID = src/risk/gates.py#941-972#36a7f38f — [[F:src/risk/gates.py#941-972#36a7f38f]].
- check_exchange_stress (function, lines 992-1029, slice 1): CHUNK_ID = src/risk/gates.py#992-1029#36a7f38f — [[F:src/risk/gates.py#992-1029#36a7f38f]].
- check_exchange_stress (function, lines 1030-1067, slice 2): CHUNK_ID = src/risk/gates.py#1030-1067#36a7f38f — [[F:src/risk/gates.py#1030-1067#36a7f38f]].
- check_exchange_stress (function, lines 1068-1074, slice 3): CHUNK_ID = src/risk/gates.py#1068-1074#36a7f38f — [[F:src/risk/gates.py#1068-1074#36a7f38f]].
- _whale_outcome (function, lines 1077-1106): CHUNK_ID = src/risk/gates.py#1077-1106#36a7f38f — [[F:src/risk/gates.py#1077-1106#36a7f38f]].
- check_whale_activity (function, lines 1109-1146, slice 1): CHUNK_ID = src/risk/gates.py#1109-1146#36a7f38f — [[F:src/risk/gates.py#1109-1146#36a7f38f]].
- check_whale_activity (function, lines 1147-1182, slice 2): CHUNK_ID = src/risk/gates.py#1147-1182#36a7f38f — [[F:src/risk/gates.py#1147-1182#36a7f38f]].
- check_position_exit (function, lines 1192-1229, slice 1): CHUNK_ID = src/risk/gates.py#1192-1229#36a7f38f — [[F:src/risk/gates.py#1192-1229#36a7f38f]].
- check_position_exit (function, lines 1230-1267, slice 2): CHUNK_ID = src/risk/gates.py#1230-1267#36a7f38f — [[F:src/risk/gates.py#1230-1267#36a7f38f]].
- check_position_exit (function, lines 1268-1281, slice 3): CHUNK_ID = src/risk/gates.py#1268-1281#36a7f38f — [[F:src/risk/gates.py#1268-1281#36a7f38f]].

## src/execution/order_fsm.py

SHA8 14f635a5; total lines 375.

- OrderStatus (class, lines 44-52): CHUNK_ID = src/execution/order_fsm.py#44-52#14f635a5 — [[F:src/execution/order_fsm.py#44-52#14f635a5]].
- OrderFSMError (class, lines 59-60): CHUNK_ID = src/execution/order_fsm.py#59-60#14f635a5 — [[F:src/execution/order_fsm.py#59-60#14f635a5]].
- OrderFSMState (class, lines 64-101, slice 1): CHUNK_ID = src/execution/order_fsm.py#64-101#14f635a5 — [[F:src/execution/order_fsm.py#64-101#14f635a5]].
- OrderFSMState (class, lines 102-139, slice 2): CHUNK_ID = src/execution/order_fsm.py#102-139#14f635a5 — [[F:src/execution/order_fsm.py#102-139#14f635a5]].
- OrderFSMState (class, lines 140-146, slice 3): CHUNK_ID = src/execution/order_fsm.py#140-146#14f635a5 — [[F:src/execution/order_fsm.py#140-146#14f635a5]].
- OrderFSMState.to_dict (method, lines 107-125): CHUNK_ID = src/execution/order_fsm.py#107-125#14f635a5 — [[F:src/execution/order_fsm.py#107-125#14f635a5]].
- OrderFSMState.is_terminal (method, lines 127-134): CHUNK_ID = src/execution/order_fsm.py#127-134#14f635a5 — [[F:src/execution/order_fsm.py#127-134#14f635a5]].
- OrderFSMState.is_active (method, lines 136-138): CHUNK_ID = src/execution/order_fsm.py#136-138#14f635a5 — [[F:src/execution/order_fsm.py#136-138#14f635a5]].
- OrderFSMState.fill_percentage (method, lines 140-142): CHUNK_ID = src/execution/order_fsm.py#140-142#14f635a5 — [[F:src/execution/order_fsm.py#140-142#14f635a5]].
- OrderFSMState.elapsed_ms (method, lines 144-146): CHUNK_ID = src/execution/order_fsm.py#144-146#14f635a5 — [[F:src/execution/order_fsm.py#144-146#14f635a5]].
- OrderFSM (class, lines 149-186, slice 1): CHUNK_ID = src/execution/order_fsm.py#149-186#14f635a5 — [[F:src/execution/order_fsm.py#149-186#14f635a5]].
- OrderFSM (class, lines 187-224, slice 2): CHUNK_ID = src/execution/order_fsm.py#187-224#14f635a5 — [[F:src/execution/order_fsm.py#187-224#14f635a5]].
- OrderFSM (class, lines 225-262, slice 3): CHUNK_ID = src/execution/order_fsm.py#225-262#14f635a5 — [[F:src/execution/order_fsm.py#225-262#14f635a5]].
- OrderFSM (class, lines 263-300, slice 4): CHUNK_ID = src/execution/order_fsm.py#263-300#14f635a5 — [[F:src/execution/order_fsm.py#263-300#14f635a5]].
- OrderFSM (class, lines 301-338, slice 5): CHUNK_ID = src/execution/order_fsm.py#301-338#14f635a5 — [[F:src/execution/order_fsm.py#301-338#14f635a5]].
- OrderFSM (class, lines 339-375, slice 6): CHUNK_ID = src/execution/order_fsm.py#339-375#14f635a5 — [[F:src/execution/order_fsm.py#339-375#14f635a5]].
- OrderFSM.__init__ (method, lines 194-197): CHUNK_ID = src/execution/order_fsm.py#194-197#14f635a5 — [[F:src/execution/order_fsm.py#194-197#14f635a5]].
- OrderFSM.state (method, lines 200-202): CHUNK_ID = src/execution/order_fsm.py#200-202#14f635a5 — [[F:src/execution/order_fsm.py#200-202#14f635a5]].
- OrderFSM.transition (method, lines 204-241, slice 1): CHUNK_ID = src/execution/order_fsm.py#204-241#14f635a5 — [[F:src/execution/order_fsm.py#204-241#14f635a5]].
- OrderFSM.transition (method, lines 242-269, slice 2): CHUNK_ID = src/execution/order_fsm.py#242-269#14f635a5 — [[F:src/execution/order_fsm.py#242-269#14f635a5]].
- OrderFSM.add_partial_fill (method, lines 271-308, slice 1): CHUNK_ID = src/execution/order_fsm.py#271-308#14f635a5 — [[F:src/execution/order_fsm.py#271-308#14f635a5]].
- OrderFSM.add_partial_fill (method, lines 309-323, slice 2): CHUNK_ID = src/execution/order_fsm.py#309-323#14f635a5 — [[F:src/execution/order_fsm.py#309-323#14f635a5]].
- OrderFSM._calculate_vwap (method, lines 325-333): CHUNK_ID = src/execution/order_fsm.py#325-333#14f635a5 — [[F:src/execution/order_fsm.py#325-333#14f635a5]].
- OrderFSM._transition_to_filling (method, lines 335-341): CHUNK_ID = src/execution/order_fsm.py#335-341#14f635a5 — [[F:src/execution/order_fsm.py#335-341#14f635a5]].
- OrderFSM._transition_to_filled (method, lines 343-355): CHUNK_ID = src/execution/order_fsm.py#343-355#14f635a5 — [[F:src/execution/order_fsm.py#343-355#14f635a5]].
- OrderFSM._transition_to_cancelled (method, lines 357-360): CHUNK_ID = src/execution/order_fsm.py#357-360#14f635a5 — [[F:src/execution/order_fsm.py#357-360#14f635a5]].
- OrderFSM._transition_to_timeout (method, lines 362-366): CHUNK_ID = src/execution/order_fsm.py#362-366#14f635a5 — [[F:src/execution/order_fsm.py#362-366#14f635a5]].
- OrderFSM._transition_to_failed (method, lines 368-371): CHUNK_ID = src/execution/order_fsm.py#368-371#14f635a5 — [[F:src/execution/order_fsm.py#368-371#14f635a5]].
- OrderFSM.increment_retry (method, lines 373-375): CHUNK_ID = src/execution/order_fsm.py#373-375#14f635a5 — [[F:src/execution/order_fsm.py#373-375#14f635a5]].

## src/execution/live.py

SHA8 3152d6df; total lines 1508.

- LivePosition (class, lines 92-126): CHUNK_ID = src/execution/live.py#92-126#3152d6df — [[F:src/execution/live.py#92-126#3152d6df]].
- LivePosition.mark (method, lines 116-126): CHUNK_ID = src/execution/live.py#116-126#3152d6df — [[F:src/execution/live.py#116-126#3152d6df]].
- ApprovalRequest (class, lines 135-167): CHUNK_ID = src/execution/live.py#135-167#3152d6df — [[F:src/execution/live.py#135-167#3152d6df]].
- ApprovalRequest.to_dict (method, lines 154-167): CHUNK_ID = src/execution/live.py#154-167#3152d6df — [[F:src/execution/live.py#154-167#3152d6df]].
- LiveExecutor (class, lines 175-212, slice 1): CHUNK_ID = src/execution/live.py#175-212#3152d6df — [[F:src/execution/live.py#175-212#3152d6df]].
- LiveExecutor (class, lines 213-250, slice 2): CHUNK_ID = src/execution/live.py#213-250#3152d6df — [[F:src/execution/live.py#213-250#3152d6df]].
- LiveExecutor (class, lines 251-288, slice 3): CHUNK_ID = src/execution/live.py#251-288#3152d6df — [[F:src/execution/live.py#251-288#3152d6df]].
- LiveExecutor (class, lines 289-326, slice 4): CHUNK_ID = src/execution/live.py#289-326#3152d6df — [[F:src/execution/live.py#289-326#3152d6df]].
- LiveExecutor (class, lines 327-364, slice 5): CHUNK_ID = src/execution/live.py#327-364#3152d6df — [[F:src/execution/live.py#327-364#3152d6df]].
- LiveExecutor (class, lines 365-402, slice 6): CHUNK_ID = src/execution/live.py#365-402#3152d6df — [[F:src/execution/live.py#365-402#3152d6df]].
- LiveExecutor (class, lines 403-440, slice 7): CHUNK_ID = src/execution/live.py#403-440#3152d6df — [[F:src/execution/live.py#403-440#3152d6df]].
- LiveExecutor (class, lines 441-478, slice 8): CHUNK_ID = src/execution/live.py#441-478#3152d6df — [[F:src/execution/live.py#441-478#3152d6df]].
- LiveExecutor (class, lines 479-516, slice 9): CHUNK_ID = src/execution/live.py#479-516#3152d6df — [[F:src/execution/live.py#479-516#3152d6df]].
- LiveExecutor (class, lines 517-554, slice 10): CHUNK_ID = src/execution/live.py#517-554#3152d6df — [[F:src/execution/live.py#517-554#3152d6df]].
- LiveExecutor (class, lines 555-592, slice 11): CHUNK_ID = src/execution/live.py#555-592#3152d6df — [[F:src/execution/live.py#555-592#3152d6df]].
- LiveExecutor (class, lines 593-630, slice 12): CHUNK_ID = src/execution/live.py#593-630#3152d6df — [[F:src/execution/live.py#593-630#3152d6df]].
- LiveExecutor (class, lines 631-668, slice 13): CHUNK_ID = src/execution/live.py#631-668#3152d6df — [[F:src/execution/live.py#631-668#3152d6df]].
- LiveExecutor (class, lines 669-706, slice 14): CHUNK_ID = src/execution/live.py#669-706#3152d6df — [[F:src/execution/live.py#669-706#3152d6df]].
- LiveExecutor (class, lines 707-744, slice 15): CHUNK_ID = src/execution/live.py#707-744#3152d6df — [[F:src/execution/live.py#707-744#3152d6df]].
- LiveExecutor (class, lines 745-782, slice 16): CHUNK_ID = src/execution/live.py#745-782#3152d6df — [[F:src/execution/live.py#745-782#3152d6df]].
- LiveExecutor (class, lines 783-820, slice 17): CHUNK_ID = src/execution/live.py#783-820#3152d6df — [[F:src/execution/live.py#783-820#3152d6df]].
- LiveExecutor (class, lines 821-858, slice 18): CHUNK_ID = src/execution/live.py#821-858#3152d6df — [[F:src/execution/live.py#821-858#3152d6df]].
- LiveExecutor (class, lines 859-896, slice 19): CHUNK_ID = src/execution/live.py#859-896#3152d6df — [[F:src/execution/live.py#859-896#3152d6df]].
- LiveExecutor (class, lines 897-934, slice 20): CHUNK_ID = src/execution/live.py#897-934#3152d6df — [[F:src/execution/live.py#897-934#3152d6df]].
- LiveExecutor (class, lines 935-972, slice 21): CHUNK_ID = src/execution/live.py#935-972#3152d6df — [[F:src/execution/live.py#935-972#3152d6df]].
- LiveExecutor (class, lines 973-1010, slice 22): CHUNK_ID = src/execution/live.py#973-1010#3152d6df — [[F:src/execution/live.py#973-1010#3152d6df]].
- LiveExecutor (class, lines 1011-1048, slice 23): CHUNK_ID = src/execution/live.py#1011-1048#3152d6df — [[F:src/execution/live.py#1011-1048#3152d6df]].
- LiveExecutor (class, lines 1049-1086, slice 24): CHUNK_ID = src/execution/live.py#1049-1086#3152d6df — [[F:src/execution/live.py#1049-1086#3152d6df]].
- LiveExecutor (class, lines 1087-1124, slice 25): CHUNK_ID = src/execution/live.py#1087-1124#3152d6df — [[F:src/execution/live.py#1087-1124#3152d6df]].
- LiveExecutor (class, lines 1125-1162, slice 26): CHUNK_ID = src/execution/live.py#1125-1162#3152d6df — [[F:src/execution/live.py#1125-1162#3152d6df]].
- LiveExecutor (class, lines 1163-1200, slice 27): CHUNK_ID = src/execution/live.py#1163-1200#3152d6df — [[F:src/execution/live.py#1163-1200#3152d6df]].
- LiveExecutor (class, lines 1201-1238, slice 28): CHUNK_ID = src/execution/live.py#1201-1238#3152d6df — [[F:src/execution/live.py#1201-1238#3152d6df]].
- LiveExecutor (class, lines 1239-1276, slice 29): CHUNK_ID = src/execution/live.py#1239-1276#3152d6df — [[F:src/execution/live.py#1239-1276#3152d6df]].
- LiveExecutor (class, lines 1277-1314, slice 30): CHUNK_ID = src/execution/live.py#1277-1314#3152d6df — [[F:src/execution/live.py#1277-1314#3152d6df]].
- LiveExecutor (class, lines 1315-1352, slice 31): CHUNK_ID = src/execution/live.py#1315-1352#3152d6df — [[F:src/execution/live.py#1315-1352#3152d6df]].
- LiveExecutor (class, lines 1353-1390, slice 32): CHUNK_ID = src/execution/live.py#1353-1390#3152d6df — [[F:src/execution/live.py#1353-1390#3152d6df]].
- LiveExecutor (class, lines 1391-1428, slice 33): CHUNK_ID = src/execution/live.py#1391-1428#3152d6df — [[F:src/execution/live.py#1391-1428#3152d6df]].
- LiveExecutor (class, lines 1429-1466, slice 34): CHUNK_ID = src/execution/live.py#1429-1466#3152d6df — [[F:src/execution/live.py#1429-1466#3152d6df]].
- LiveExecutor (class, lines 1467-1504, slice 35): CHUNK_ID = src/execution/live.py#1467-1504#3152d6df — [[F:src/execution/live.py#1467-1504#3152d6df]].
- LiveExecutor (class, lines 1505-1508, slice 36): CHUNK_ID = src/execution/live.py#1505-1508#3152d6df — [[F:src/execution/live.py#1505-1508#3152d6df]].
- LiveExecutor.__init__ (method, lines 191-228, slice 1): CHUNK_ID = src/execution/live.py#191-228#3152d6df — [[F:src/execution/live.py#191-228#3152d6df]].
- LiveExecutor.__init__ (method, lines 229-249, slice 2): CHUNK_ID = src/execution/live.py#229-249#3152d6df — [[F:src/execution/live.py#229-249#3152d6df]].
- LiveExecutor.initialize (method, lines 255-271): CHUNK_ID = src/execution/live.py#255-271#3152d6df — [[F:src/execution/live.py#255-271#3152d6df]].
- LiveExecutor._reconcile_with_exchange (method, lines 273-310, slice 1): CHUNK_ID = src/execution/live.py#273-310#3152d6df — [[F:src/execution/live.py#273-310#3152d6df]].
- LiveExecutor._reconcile_with_exchange (method, lines 311-348, slice 2): CHUNK_ID = src/execution/live.py#311-348#3152d6df — [[F:src/execution/live.py#311-348#3152d6df]].
- LiveExecutor._reconcile_with_exchange (method, lines 349-357, slice 3): CHUNK_ID = src/execution/live.py#349-357#3152d6df — [[F:src/execution/live.py#349-357#3152d6df]].
- LiveExecutor.recovery_discrepancies (method, lines 360-362): CHUNK_ID = src/execution/live.py#360-362#3152d6df — [[F:src/execution/live.py#360-362#3152d6df]].
- LiveExecutor.acknowledge_recovery (method, lines 364-377): CHUNK_ID = src/execution/live.py#364-377#3152d6df — [[F:src/execution/live.py#364-377#3152d6df]].
- LiveExecutor.shutdown (method, lines 379-388): CHUNK_ID = src/execution/live.py#379-388#3152d6df — [[F:src/execution/live.py#379-388#3152d6df]].
- LiveExecutor.submit_signal (method, lines 394-431, slice 1): CHUNK_ID = src/execution/live.py#394-431#3152d6df — [[F:src/execution/live.py#394-431#3152d6df]].
- LiveExecutor.submit_signal (method, lines 432-469, slice 2): CHUNK_ID = src/execution/live.py#432-469#3152d6df — [[F:src/execution/live.py#432-469#3152d6df]].
- LiveExecutor.submit_signal (method, lines 470-488, slice 3): CHUNK_ID = src/execution/live.py#470-488#3152d6df — [[F:src/execution/live.py#470-488#3152d6df]].
- LiveExecutor._submit_signal_auto (method, lines 490-515): CHUNK_ID = src/execution/live.py#490-515#3152d6df — [[F:src/execution/live.py#490-515#3152d6df]].
- LiveExecutor._submit_signal_with_approval (method, lines 517-554): CHUNK_ID = src/execution/live.py#517-554#3152d6df — [[F:src/execution/live.py#517-554#3152d6df]].
- LiveExecutor.close_position (method, lines 560-597, slice 1): CHUNK_ID = src/execution/live.py#560-597#3152d6df — [[F:src/execution/live.py#560-597#3152d6df]].
- LiveExecutor.close_position (method, lines 598-635, slice 2): CHUNK_ID = src/execution/live.py#598-635#3152d6df — [[F:src/execution/live.py#598-635#3152d6df]].
- LiveExecutor.close_position (method, lines 636-673, slice 3): CHUNK_ID = src/execution/live.py#636-673#3152d6df — [[F:src/execution/live.py#636-673#3152d6df]].
- LiveExecutor.close_position (method, lines 674-711, slice 4): CHUNK_ID = src/execution/live.py#674-711#3152d6df — [[F:src/execution/live.py#674-711#3152d6df]].
- LiveExecutor.close_position (method, lines 712-713, slice 5): CHUNK_ID = src/execution/live.py#712-713#3152d6df — [[F:src/execution/live.py#712-713#3152d6df]].
- LiveExecutor.mark_to_market (method, lines 715-745): CHUNK_ID = src/execution/live.py#715-745#3152d6df — [[F:src/execution/live.py#715-745#3152d6df]].
- LiveExecutor.resolve_approval (method, lines 751-775): CHUNK_ID = src/execution/live.py#751-775#3152d6df — [[F:src/execution/live.py#751-775#3152d6df]].
- LiveExecutor._pending_approvals_unsafe (method, lines 777-793): CHUNK_ID = src/execution/live.py#777-793#3152d6df — [[F:src/execution/live.py#777-793#3152d6df]].
- LiveExecutor.pending_approvals (method, lines 795-801): CHUNK_ID = src/execution/live.py#795-801#3152d6df — [[F:src/execution/live.py#795-801#3152d6df]].
- LiveExecutor.open_positions_safe (method, lines 803-806): CHUNK_ID = src/execution/live.py#803-806#3152d6df — [[F:src/execution/live.py#803-806#3152d6df]].
- LiveExecutor.pending_approvals_safe (method, lines 808-819): CHUNK_ID = src/execution/live.py#808-819#3152d6df — [[F:src/execution/live.py#808-819#3152d6df]].
- LiveExecutor._open_positions_snapshot (method, lines 821-844): CHUNK_ID = src/execution/live.py#821-844#3152d6df — [[F:src/execution/live.py#821-844#3152d6df]].
- LiveExecutor.open_positions (method, lines 850-852): CHUNK_ID = src/execution/live.py#850-852#3152d6df — [[F:src/execution/live.py#850-852#3152d6df]].
- LiveExecutor.cash_usd (method, lines 855-856): CHUNK_ID = src/execution/live.py#855-856#3152d6df — [[F:src/execution/live.py#855-856#3152d6df]].
- LiveExecutor.idempotency (method, lines 859-863): CHUNK_ID = src/execution/live.py#859-863#3152d6df — [[F:src/execution/live.py#859-863#3152d6df]].
- LiveExecutor.equity_usd (method, lines 866-867): CHUNK_ID = src/execution/live.py#866-867#3152d6df — [[F:src/execution/live.py#866-867#3152d6df]].
- LiveExecutor.starting_capital (method, lines 870-871): CHUNK_ID = src/execution/live.py#870-871#3152d6df — [[F:src/execution/live.py#870-871#3152d6df]].
- LiveExecutor.peak_equity (method, lines 874-875): CHUNK_ID = src/execution/live.py#874-875#3152d6df — [[F:src/execution/live.py#874-875#3152d6df]].
- LiveExecutor.drawdown_tracker (method, lines 878-879): CHUNK_ID = src/execution/live.py#878-879#3152d6df — [[F:src/execution/live.py#878-879#3152d6df]].
- LiveExecutor.starting_equity_usd (method, lines 882-884): CHUNK_ID = src/execution/live.py#882-884#3152d6df — [[F:src/execution/live.py#882-884#3152d6df]].
- LiveExecutor.reset_daily_equity (method, lines 886-897): CHUNK_ID = src/execution/live.py#886-897#3152d6df — [[F:src/execution/live.py#886-897#3152d6df]].
- LiveExecutor.get_risk_snapshot (method, lines 899-905): CHUNK_ID = src/execution/live.py#899-905#3152d6df — [[F:src/execution/live.py#899-905#3152d6df]].
- LiveExecutor.position_count (method, lines 907-908): CHUNK_ID = src/execution/live.py#907-908#3152d6df — [[F:src/execution/live.py#907-908#3152d6df]].
- LiveExecutor.get_consecutive_losses (method, lines 910-911): CHUNK_ID = src/execution/live.py#910-911#3152d6df — [[F:src/execution/live.py#910-911#3152d6df]].
- LiveExecutor.get_daily_pnl (method, lines 913-914): CHUNK_ID = src/execution/live.py#913-914#3152d6df — [[F:src/execution/live.py#913-914#3152d6df]].
- LiveExecutor._place_and_record (method, lines 920-957, slice 1): CHUNK_ID = src/execution/live.py#920-957#3152d6df — [[F:src/execution/live.py#920-957#3152d6df]].
- LiveExecutor._place_and_record (method, lines 958-995, slice 2): CHUNK_ID = src/execution/live.py#958-995#3152d6df — [[F:src/execution/live.py#958-995#3152d6df]].
- LiveExecutor._place_and_record (method, lines 996-1033, slice 3): CHUNK_ID = src/execution/live.py#996-1033#3152d6df — [[F:src/execution/live.py#996-1033#3152d6df]].
- LiveExecutor._place_and_record (method, lines 1034-1071, slice 4): CHUNK_ID = src/execution/live.py#1034-1071#3152d6df — [[F:src/execution/live.py#1034-1071#3152d6df]].
- LiveExecutor._place_and_record (method, lines 1072-1109, slice 5): CHUNK_ID = src/execution/live.py#1072-1109#3152d6df — [[F:src/execution/live.py#1072-1109#3152d6df]].
- LiveExecutor._place_and_record (method, lines 1110-1143, slice 6): CHUNK_ID = src/execution/live.py#1110-1143#3152d6df — [[F:src/execution/live.py#1110-1143#3152d6df]].
- LiveExecutor._await_throttle_token (method, lines 1145-1182, slice 1): CHUNK_ID = src/execution/live.py#1145-1182#3152d6df — [[F:src/execution/live.py#1145-1182#3152d6df]].
- LiveExecutor._await_throttle_token (method, lines 1183-1211, slice 2): CHUNK_ID = src/execution/live.py#1183-1211#3152d6df — [[F:src/execution/live.py#1183-1211#3152d6df]].
- LiveExecutor._place_market_order (method, lines 1213-1250, slice 1): CHUNK_ID = src/execution/live.py#1213-1250#3152d6df — [[F:src/execution/live.py#1213-1250#3152d6df]].
- LiveExecutor._place_market_order (method, lines 1251-1288, slice 2): CHUNK_ID = src/execution/live.py#1251-1288#3152d6df — [[F:src/execution/live.py#1251-1288#3152d6df]].
- LiveExecutor._place_market_order (method, lines 1289-1317, slice 3): CHUNK_ID = src/execution/live.py#1289-1317#3152d6df — [[F:src/execution/live.py#1289-1317#3152d6df]].
- LiveExecutor._enqueue_approval (method, lines 1319-1355): CHUNK_ID = src/execution/live.py#1319-1355#3152d6df — [[F:src/execution/live.py#1319-1355#3152d6df]].
- LiveExecutor._await_approval (method, lines 1357-1390): CHUNK_ID = src/execution/live.py#1357-1390#3152d6df — [[F:src/execution/live.py#1357-1390#3152d6df]].
- LiveExecutor._equity_usd (method, lines 1392-1393): CHUNK_ID = src/execution/live.py#1392-1393#3152d6df — [[F:src/execution/live.py#1392-1393#3152d6df]].
- LiveExecutor._snapshot_equity (method, lines 1395-1420): CHUNK_ID = src/execution/live.py#1395-1420#3152d6df — [[F:src/execution/live.py#1395-1420#3152d6df]].
- LiveExecutor._snapshot_equity_with_values (method, lines 1422-1449): CHUNK_ID = src/execution/live.py#1422-1449#3152d6df — [[F:src/execution/live.py#1422-1449#3152d6df]].
- LiveExecutor._register_order_fsm (method, lines 1451-1463): CHUNK_ID = src/execution/live.py#1451-1463#3152d6df — [[F:src/execution/live.py#1451-1463#3152d6df]].
- LiveExecutor.get_order_fsm_state (method, lines 1465-1474): CHUNK_ID = src/execution/live.py#1465-1474#3152d6df — [[F:src/execution/live.py#1465-1474#3152d6df]].
- LiveExecutor._extract_fee (method, lines 1476-1502): CHUNK_ID = src/execution/live.py#1476-1502#3152d6df — [[F:src/execution/live.py#1476-1502#3152d6df]].
- LiveExecutor._require_initialized (method, lines 1504-1508): CHUNK_ID = src/execution/live.py#1504-1508#3152d6df — [[F:src/execution/live.py#1504-1508#3152d6df]].

## src/execution/unified_ledger.py

SHA8 86392a2d; total lines 89.

- VenuePosition (class, lines 26-33): CHUNK_ID = src/execution/unified_ledger.py#26-33#86392a2d — [[F:src/execution/unified_ledger.py#26-33#86392a2d]].
- UnifiedLedger (class, lines 36-73, slice 1): CHUNK_ID = src/execution/unified_ledger.py#36-73#86392a2d — [[F:src/execution/unified_ledger.py#36-73#86392a2d]].
- UnifiedLedger (class, lines 74-81, slice 2): CHUNK_ID = src/execution/unified_ledger.py#74-81#86392a2d — [[F:src/execution/unified_ledger.py#74-81#86392a2d]].
- UnifiedLedger.__init__ (method, lines 48-49): CHUNK_ID = src/execution/unified_ledger.py#48-49#86392a2d — [[F:src/execution/unified_ledger.py#48-49#86392a2d]].
- UnifiedLedger.record_position (method, lines 51-53): CHUNK_ID = src/execution/unified_ledger.py#51-53#86392a2d — [[F:src/execution/unified_ledger.py#51-53#86392a2d]].
- UnifiedLedger.clear_position (method, lines 55-56): CHUNK_ID = src/execution/unified_ledger.py#55-56#86392a2d — [[F:src/execution/unified_ledger.py#55-56#86392a2d]].
- UnifiedLedger.positions_for_symbol (method, lines 58-59): CHUNK_ID = src/execution/unified_ledger.py#58-59#86392a2d — [[F:src/execution/unified_ledger.py#58-59#86392a2d]].
- UnifiedLedger.net_exposure (method, lines 61-63): CHUNK_ID = src/execution/unified_ledger.py#61-63#86392a2d — [[F:src/execution/unified_ledger.py#61-63#86392a2d]].
- UnifiedLedger.gross_exposure (method, lines 65-67): CHUNK_ID = src/execution/unified_ledger.py#65-67#86392a2d — [[F:src/execution/unified_ledger.py#65-67#86392a2d]].
- UnifiedLedger.total_margin_used_usd (method, lines 69-74): CHUNK_ID = src/execution/unified_ledger.py#69-74#86392a2d — [[F:src/execution/unified_ledger.py#69-74#86392a2d]].
- UnifiedLedger.venues_holding (method, lines 76-77): CHUNK_ID = src/execution/unified_ledger.py#76-77#86392a2d — [[F:src/execution/unified_ledger.py#76-77#86392a2d]].
- UnifiedLedger.all_positions (method, lines 80-81): CHUNK_ID = src/execution/unified_ledger.py#80-81#86392a2d — [[F:src/execution/unified_ledger.py#80-81#86392a2d]].
- get_unified_ledger (function, lines 87-89): CHUNK_ID = src/execution/unified_ledger.py#87-89#86392a2d — [[F:src/execution/unified_ledger.py#87-89#86392a2d]].

## src/data/fetcher.py

SHA8 26cf972e; total lines 1282.

- _as_float (function, lines 60-67): CHUNK_ID = src/data/fetcher.py#60-67#26cf972e — [[F:src/data/fetcher.py#60-67#26cf972e]].
- OrderBookSnapshot (class, lines 75-112, slice 1): CHUNK_ID = src/data/fetcher.py#75-112#26cf972e — [[F:src/data/fetcher.py#75-112#26cf972e]].
- OrderBookSnapshot (class, lines 113-132, slice 2): CHUNK_ID = src/data/fetcher.py#113-132#26cf972e — [[F:src/data/fetcher.py#113-132#26cf972e]].
- OrderBookSnapshot.__init__ (method, lines 84-94): CHUNK_ID = src/data/fetcher.py#84-94#26cf972e — [[F:src/data/fetcher.py#84-94#26cf972e]].
- OrderBookSnapshot.bid_price (method, lines 97-99): CHUNK_ID = src/data/fetcher.py#97-99#26cf972e — [[F:src/data/fetcher.py#97-99#26cf972e]].
- OrderBookSnapshot.ask_price (method, lines 102-104): CHUNK_ID = src/data/fetcher.py#102-104#26cf972e — [[F:src/data/fetcher.py#102-104#26cf972e]].
- OrderBookSnapshot.mid_price (method, lines 107-108): CHUNK_ID = src/data/fetcher.py#107-108#26cf972e — [[F:src/data/fetcher.py#107-108#26cf972e]].
- OrderBookSnapshot.spread (method, lines 111-112): CHUNK_ID = src/data/fetcher.py#111-112#26cf972e — [[F:src/data/fetcher.py#111-112#26cf972e]].
- OrderBookSnapshot.bid_volume (method, lines 114-116): CHUNK_ID = src/data/fetcher.py#114-116#26cf972e — [[F:src/data/fetcher.py#114-116#26cf972e]].
- OrderBookSnapshot.ask_volume (method, lines 118-120): CHUNK_ID = src/data/fetcher.py#118-120#26cf972e — [[F:src/data/fetcher.py#118-120#26cf972e]].
- OrderBookSnapshot.order_flow_imbalance (method, lines 122-132): CHUNK_ID = src/data/fetcher.py#122-132#26cf972e — [[F:src/data/fetcher.py#122-132#26cf972e]].
- _parse_book_side (function, lines 135-153): CHUNK_ID = src/data/fetcher.py#135-153#26cf972e — [[F:src/data/fetcher.py#135-153#26cf972e]].
- _build_binance (function, lines 161-178): CHUNK_ID = src/data/fetcher.py#161-178#26cf972e — [[F:src/data/fetcher.py#161-178#26cf972e]].
- _build_okx (function, lines 181-196): CHUNK_ID = src/data/fetcher.py#181-196#26cf972e — [[F:src/data/fetcher.py#181-196#26cf972e]].
- _jittered (function, lines 207-230): CHUNK_ID = src/data/fetcher.py#207-230#26cf972e — [[F:src/data/fetcher.py#207-230#26cf972e]].
- VenueDisconnectRefused (class, lines 272-273): CHUNK_ID = src/data/fetcher.py#272-273#26cf972e — [[F:src/data/fetcher.py#272-273#26cf972e]].
- _VenueState (class, lines 277-283): CHUNK_ID = src/data/fetcher.py#277-283#26cf972e — [[F:src/data/fetcher.py#277-283#26cf972e]].
- _describe_error (function, lines 286-297): CHUNK_ID = src/data/fetcher.py#286-297#26cf972e — [[F:src/data/fetcher.py#286-297#26cf972e]].
- _with_retry (function, lines 300-337, slice 1): CHUNK_ID = src/data/fetcher.py#300-337#26cf972e — [[F:src/data/fetcher.py#300-337#26cf972e]].
- _with_retry (function, lines 338-371, slice 2): CHUNK_ID = src/data/fetcher.py#338-371#26cf972e — [[F:src/data/fetcher.py#338-371#26cf972e]].
- MarketDataFetcher (class, lines 379-416, slice 1): CHUNK_ID = src/data/fetcher.py#379-416#26cf972e — [[F:src/data/fetcher.py#379-416#26cf972e]].
- MarketDataFetcher (class, lines 417-454, slice 2): CHUNK_ID = src/data/fetcher.py#417-454#26cf972e — [[F:src/data/fetcher.py#417-454#26cf972e]].
- MarketDataFetcher (class, lines 455-492, slice 3): CHUNK_ID = src/data/fetcher.py#455-492#26cf972e — [[F:src/data/fetcher.py#455-492#26cf972e]].
- MarketDataFetcher (class, lines 493-530, slice 4): CHUNK_ID = src/data/fetcher.py#493-530#26cf972e — [[F:src/data/fetcher.py#493-530#26cf972e]].
- MarketDataFetcher (class, lines 531-568, slice 5): CHUNK_ID = src/data/fetcher.py#531-568#26cf972e — [[F:src/data/fetcher.py#531-568#26cf972e]].
- MarketDataFetcher (class, lines 569-606, slice 6): CHUNK_ID = src/data/fetcher.py#569-606#26cf972e — [[F:src/data/fetcher.py#569-606#26cf972e]].
- MarketDataFetcher (class, lines 607-644, slice 7): CHUNK_ID = src/data/fetcher.py#607-644#26cf972e — [[F:src/data/fetcher.py#607-644#26cf972e]].
- MarketDataFetcher (class, lines 645-682, slice 8): CHUNK_ID = src/data/fetcher.py#645-682#26cf972e — [[F:src/data/fetcher.py#645-682#26cf972e]].
- MarketDataFetcher (class, lines 683-720, slice 9): CHUNK_ID = src/data/fetcher.py#683-720#26cf972e — [[F:src/data/fetcher.py#683-720#26cf972e]].
- MarketDataFetcher (class, lines 721-758, slice 10): CHUNK_ID = src/data/fetcher.py#721-758#26cf972e — [[F:src/data/fetcher.py#721-758#26cf972e]].
- MarketDataFetcher (class, lines 759-796, slice 11): CHUNK_ID = src/data/fetcher.py#759-796#26cf972e — [[F:src/data/fetcher.py#759-796#26cf972e]].
- MarketDataFetcher (class, lines 797-834, slice 12): CHUNK_ID = src/data/fetcher.py#797-834#26cf972e — [[F:src/data/fetcher.py#797-834#26cf972e]].
- MarketDataFetcher (class, lines 835-872, slice 13): CHUNK_ID = src/data/fetcher.py#835-872#26cf972e — [[F:src/data/fetcher.py#835-872#26cf972e]].
- MarketDataFetcher (class, lines 873-910, slice 14): CHUNK_ID = src/data/fetcher.py#873-910#26cf972e — [[F:src/data/fetcher.py#873-910#26cf972e]].
- MarketDataFetcher (class, lines 911-948, slice 15): CHUNK_ID = src/data/fetcher.py#911-948#26cf972e — [[F:src/data/fetcher.py#911-948#26cf972e]].
- MarketDataFetcher (class, lines 949-986, slice 16): CHUNK_ID = src/data/fetcher.py#949-986#26cf972e — [[F:src/data/fetcher.py#949-986#26cf972e]].
- MarketDataFetcher (class, lines 987-1024, slice 17): CHUNK_ID = src/data/fetcher.py#987-1024#26cf972e — [[F:src/data/fetcher.py#987-1024#26cf972e]].
- MarketDataFetcher (class, lines 1025-1062, slice 18): CHUNK_ID = src/data/fetcher.py#1025-1062#26cf972e — [[F:src/data/fetcher.py#1025-1062#26cf972e]].
- MarketDataFetcher (class, lines 1063-1100, slice 19): CHUNK_ID = src/data/fetcher.py#1063-1100#26cf972e — [[F:src/data/fetcher.py#1063-1100#26cf972e]].
- MarketDataFetcher (class, lines 1101-1138, slice 20): CHUNK_ID = src/data/fetcher.py#1101-1138#26cf972e — [[F:src/data/fetcher.py#1101-1138#26cf972e]].
- MarketDataFetcher (class, lines 1139-1176, slice 21): CHUNK_ID = src/data/fetcher.py#1139-1176#26cf972e — [[F:src/data/fetcher.py#1139-1176#26cf972e]].
- MarketDataFetcher (class, lines 1177-1202, slice 22): CHUNK_ID = src/data/fetcher.py#1177-1202#26cf972e — [[F:src/data/fetcher.py#1177-1202#26cf972e]].
- MarketDataFetcher.__init__ (method, lines 395-413): CHUNK_ID = src/data/fetcher.py#395-413#26cf972e — [[F:src/data/fetcher.py#395-413#26cf972e]].
- MarketDataFetcher._settings (method, lines 421-431): CHUNK_ID = src/data/fetcher.py#421-431#26cf972e — [[F:src/data/fetcher.py#421-431#26cf972e]].
- MarketDataFetcher._settings (method, lines 434-444): CHUNK_ID = src/data/fetcher.py#434-444#26cf972e — [[F:src/data/fetcher.py#434-444#26cf972e]].
- MarketDataFetcher._get_sem (method, lines 446-456): CHUNK_ID = src/data/fetcher.py#446-456#26cf972e — [[F:src/data/fetcher.py#446-456#26cf972e]].
- MarketDataFetcher.initialize (method, lines 458-488): CHUNK_ID = src/data/fetcher.py#458-488#26cf972e — [[F:src/data/fetcher.py#458-488#26cf972e]].
- MarketDataFetcher._open_venue (method, lines 490-527, slice 1): CHUNK_ID = src/data/fetcher.py#490-527#26cf972e — [[F:src/data/fetcher.py#490-527#26cf972e]].
- MarketDataFetcher._open_venue (method, lines 528-543, slice 2): CHUNK_ID = src/data/fetcher.py#528-543#26cf972e — [[F:src/data/fetcher.py#528-543#26cf972e]].
- MarketDataFetcher._set_phase (method, lines 545-548): CHUNK_ID = src/data/fetcher.py#545-548#26cf972e — [[F:src/data/fetcher.py#545-548#26cf972e]].
- MarketDataFetcher._lock (method, lines 550-554): CHUNK_ID = src/data/fetcher.py#550-554#26cf972e — [[F:src/data/fetcher.py#550-554#26cf972e]].
- MarketDataFetcher._check_venue (method, lines 557-559): CHUNK_ID = src/data/fetcher.py#557-559#26cf972e — [[F:src/data/fetcher.py#557-559#26cf972e]].
- MarketDataFetcher.credential_state (method, lines 561-572): CHUNK_ID = src/data/fetcher.py#561-572#26cf972e — [[F:src/data/fetcher.py#561-572#26cf972e]].
- MarketDataFetcher._set_venue (method, lines 574-578): CHUNK_ID = src/data/fetcher.py#574-578#26cf972e — [[F:src/data/fetcher.py#574-578#26cf972e]].
- MarketDataFetcher.available_venues (method, lines 580-587): CHUNK_ID = src/data/fetcher.py#580-587#26cf972e — [[F:src/data/fetcher.py#580-587#26cf972e]].
- MarketDataFetcher.venue_status (method, lines 589-628): CHUNK_ID = src/data/fetcher.py#589-628#26cf972e — [[F:src/data/fetcher.py#589-628#26cf972e]].
- MarketDataFetcher.reconnect (method, lines 630-648): CHUNK_ID = src/data/fetcher.py#630-648#26cf972e — [[F:src/data/fetcher.py#630-648#26cf972e]].
- MarketDataFetcher.disconnect (method, lines 650-678): CHUNK_ID = src/data/fetcher.py#650-678#26cf972e — [[F:src/data/fetcher.py#650-678#26cf972e]].
- MarketDataFetcher.verify_account (method, lines 680-717): CHUNK_ID = src/data/fetcher.py#680-717#26cf972e — [[F:src/data/fetcher.py#680-717#26cf972e]].
- MarketDataFetcher._close_client (method, lines 719-725): CHUNK_ID = src/data/fetcher.py#719-725#26cf972e — [[F:src/data/fetcher.py#719-725#26cf972e]].
- MarketDataFetcher.close (method, lines 727-733): CHUNK_ID = src/data/fetcher.py#727-733#26cf972e — [[F:src/data/fetcher.py#727-733#26cf972e]].
- MarketDataFetcher._unavailable_message (method, lines 735-755): CHUNK_ID = src/data/fetcher.py#735-755#26cf972e — [[F:src/data/fetcher.py#735-755#26cf972e]].
- MarketDataFetcher._require_binance (method, lines 757-760): CHUNK_ID = src/data/fetcher.py#757-760#26cf972e — [[F:src/data/fetcher.py#757-760#26cf972e]].
- MarketDataFetcher.get_order_exchange (method, lines 762-772): CHUNK_ID = src/data/fetcher.py#762-772#26cf972e — [[F:src/data/fetcher.py#762-772#26cf972e]].
- MarketDataFetcher._require_okx (method, lines 774-777): CHUNK_ID = src/data/fetcher.py#774-777#26cf972e — [[F:src/data/fetcher.py#774-777#26cf972e]].
- MarketDataFetcher.bootstrap_history (method, lines 783-820, slice 1): CHUNK_ID = src/data/fetcher.py#783-820#26cf972e — [[F:src/data/fetcher.py#783-820#26cf972e]].
- MarketDataFetcher.bootstrap_history (method, lines 821-854, slice 2): CHUNK_ID = src/data/fetcher.py#821-854#26cf972e — [[F:src/data/fetcher.py#821-854#26cf972e]].
- MarketDataFetcher.gap_fill (method, lines 860-897, slice 1): CHUNK_ID = src/data/fetcher.py#860-897#26cf972e — [[F:src/data/fetcher.py#860-897#26cf972e]].
- MarketDataFetcher.gap_fill (method, lines 898-909, slice 2): CHUNK_ID = src/data/fetcher.py#898-909#26cf972e — [[F:src/data/fetcher.py#898-909#26cf972e]].
- MarketDataFetcher.fetch_orderbook (method, lines 915-955): CHUNK_ID = src/data/fetcher.py#915-955#26cf972e — [[F:src/data/fetcher.py#915-955#26cf972e]].
- MarketDataFetcher.gap_fill_all_timeframes (method, lines 961-987): CHUNK_ID = src/data/fetcher.py#961-987#26cf972e — [[F:src/data/fetcher.py#961-987#26cf972e]].
- MarketDataFetcher.fetch_ohlcv_okx (method, lines 993-1012): CHUNK_ID = src/data/fetcher.py#993-1012#26cf972e — [[F:src/data/fetcher.py#993-1012#26cf972e]].
- MarketDataFetcher.fetch_ticker_price (method, lines 1018-1047): CHUNK_ID = src/data/fetcher.py#1018-1047#26cf972e — [[F:src/data/fetcher.py#1018-1047#26cf972e]].
- MarketDataFetcher.fetch_symbol_precision (method, lines 1053-1095): CHUNK_ID = src/data/fetcher.py#1053-1095#26cf972e — [[F:src/data/fetcher.py#1053-1095#26cf972e]].
- MarketDataFetcher.fetch_funding_rate (method, lines 1101-1141): CHUNK_ID = src/data/fetcher.py#1101-1141#26cf972e — [[F:src/data/fetcher.py#1101-1141#26cf972e]].
- MarketDataFetcher.fetch_exchange_holdings (method, lines 1147-1184, slice 1): CHUNK_ID = src/data/fetcher.py#1147-1184#26cf972e — [[F:src/data/fetcher.py#1147-1184#26cf972e]].
- MarketDataFetcher.fetch_exchange_holdings (method, lines 1185-1202, slice 2): CHUNK_ID = src/data/fetcher.py#1185-1202#26cf972e — [[F:src/data/fetcher.py#1185-1202#26cf972e]].
- _raw_to_bar_records (function, lines 1210-1240): CHUNK_ID = src/data/fetcher.py#1210-1240#26cf972e — [[F:src/data/fetcher.py#1210-1240#26cf972e]].
- _FetcherContextManager (class, lines 1248-1270): CHUNK_ID = src/data/fetcher.py#1248-1270#26cf972e — [[F:src/data/fetcher.py#1248-1270#26cf972e]].
- _FetcherContextManager.__init__ (method, lines 1249-1251): CHUNK_ID = src/data/fetcher.py#1249-1251#26cf972e — [[F:src/data/fetcher.py#1249-1251#26cf972e]].
- _FetcherContextManager.__aenter__ (method, lines 1253-1256): CHUNK_ID = src/data/fetcher.py#1253-1256#26cf972e — [[F:src/data/fetcher.py#1253-1256#26cf972e]].
- _FetcherContextManager.__aexit__ (method, lines 1258-1270): CHUNK_ID = src/data/fetcher.py#1258-1270#26cf972e — [[F:src/data/fetcher.py#1258-1270#26cf972e]].
- open_fetcher (function, lines 1273-1282): CHUNK_ID = src/data/fetcher.py#1273-1282#26cf972e — [[F:src/data/fetcher.py#1273-1282#26cf972e]].

## src/data/storage.py

SHA8 b1db7068; total lines 2183.

- BarRecord (class, lines 391-429): CHUNK_ID = src/data/storage.py#391-429#b1db7068 — [[F:src/data/storage.py#391-429#b1db7068]].
- BarRecord.__init__ (method, lines 407-429): CHUNK_ID = src/data/storage.py#407-429#b1db7068 — [[F:src/data/storage.py#407-429#b1db7068]].
- BlendAudit (class, lines 433-449): CHUNK_ID = src/data/storage.py#433-449#b1db7068 — [[F:src/data/storage.py#433-449#b1db7068]].
- TradeRecord (class, lines 452-489, slice 1): CHUNK_ID = src/data/storage.py#452-489#b1db7068 — [[F:src/data/storage.py#452-489#b1db7068]].
- TradeRecord (class, lines 490-527, slice 2): CHUNK_ID = src/data/storage.py#490-527#b1db7068 — [[F:src/data/storage.py#490-527#b1db7068]].
- TradeRecord (class, lines 528-535, slice 3): CHUNK_ID = src/data/storage.py#528-535#b1db7068 — [[F:src/data/storage.py#528-535#b1db7068]].
- TradeRecord.__init__ (method, lines 483-520, slice 1): CHUNK_ID = src/data/storage.py#483-520#b1db7068 — [[F:src/data/storage.py#483-520#b1db7068]].
- TradeRecord.__init__ (method, lines 521-535, slice 2): CHUNK_ID = src/data/storage.py#521-535#b1db7068 — [[F:src/data/storage.py#521-535#b1db7068]].
- MissedTradeRecord (class, lines 538-581): CHUNK_ID = src/data/storage.py#538-581#b1db7068 — [[F:src/data/storage.py#538-581#b1db7068]].
- MissedTradeRecord.__init__ (method, lines 557-581): CHUNK_ID = src/data/storage.py#557-581#b1db7068 — [[F:src/data/storage.py#557-581#b1db7068]].
- RegimeSnapshotRecord (class, lines 584-619): CHUNK_ID = src/data/storage.py#584-619#b1db7068 — [[F:src/data/storage.py#584-619#b1db7068]].
- RegimeSnapshotRecord.__init__ (method, lines 599-619): CHUNK_ID = src/data/storage.py#599-619#b1db7068 — [[F:src/data/storage.py#599-619#b1db7068]].
- ModelMetricsRecord (class, lines 622-663): CHUNK_ID = src/data/storage.py#622-663#b1db7068 — [[F:src/data/storage.py#622-663#b1db7068]].
- ModelMetricsRecord.__init__ (method, lines 639-663): CHUNK_ID = src/data/storage.py#639-663#b1db7068 — [[F:src/data/storage.py#639-663#b1db7068]].
- EquityRecord (class, lines 666-701): CHUNK_ID = src/data/storage.py#666-701#b1db7068 — [[F:src/data/storage.py#666-701#b1db7068]].
- EquityRecord.__init__ (method, lines 681-701): CHUNK_ID = src/data/storage.py#681-701#b1db7068 — [[F:src/data/storage.py#681-701#b1db7068]].
- StorageBackend (class, lines 709-746, slice 1): CHUNK_ID = src/data/storage.py#709-746#b1db7068 — [[F:src/data/storage.py#709-746#b1db7068]].
- StorageBackend (class, lines 747-784, slice 2): CHUNK_ID = src/data/storage.py#747-784#b1db7068 — [[F:src/data/storage.py#747-784#b1db7068]].
- StorageBackend (class, lines 785-822, slice 3): CHUNK_ID = src/data/storage.py#785-822#b1db7068 — [[F:src/data/storage.py#785-822#b1db7068]].
- StorageBackend (class, lines 823-860, slice 4): CHUNK_ID = src/data/storage.py#823-860#b1db7068 — [[F:src/data/storage.py#823-860#b1db7068]].
- StorageBackend (class, lines 861-898, slice 5): CHUNK_ID = src/data/storage.py#861-898#b1db7068 — [[F:src/data/storage.py#861-898#b1db7068]].
- StorageBackend (class, lines 899-936, slice 6): CHUNK_ID = src/data/storage.py#899-936#b1db7068 — [[F:src/data/storage.py#899-936#b1db7068]].
- StorageBackend (class, lines 937-974, slice 7): CHUNK_ID = src/data/storage.py#937-974#b1db7068 — [[F:src/data/storage.py#937-974#b1db7068]].
- StorageBackend (class, lines 975-1012, slice 8): CHUNK_ID = src/data/storage.py#975-1012#b1db7068 — [[F:src/data/storage.py#975-1012#b1db7068]].
- StorageBackend (class, lines 1013-1050, slice 9): CHUNK_ID = src/data/storage.py#1013-1050#b1db7068 — [[F:src/data/storage.py#1013-1050#b1db7068]].
- StorageBackend (class, lines 1051-1088, slice 10): CHUNK_ID = src/data/storage.py#1051-1088#b1db7068 — [[F:src/data/storage.py#1051-1088#b1db7068]].
- StorageBackend (class, lines 1089-1126, slice 11): CHUNK_ID = src/data/storage.py#1089-1126#b1db7068 — [[F:src/data/storage.py#1089-1126#b1db7068]].
- StorageBackend (class, lines 1127-1164, slice 12): CHUNK_ID = src/data/storage.py#1127-1164#b1db7068 — [[F:src/data/storage.py#1127-1164#b1db7068]].
- StorageBackend (class, lines 1165-1202, slice 13): CHUNK_ID = src/data/storage.py#1165-1202#b1db7068 — [[F:src/data/storage.py#1165-1202#b1db7068]].
- StorageBackend (class, lines 1203-1240, slice 14): CHUNK_ID = src/data/storage.py#1203-1240#b1db7068 — [[F:src/data/storage.py#1203-1240#b1db7068]].
- StorageBackend (class, lines 1241-1278, slice 15): CHUNK_ID = src/data/storage.py#1241-1278#b1db7068 — [[F:src/data/storage.py#1241-1278#b1db7068]].
- StorageBackend (class, lines 1279-1316, slice 16): CHUNK_ID = src/data/storage.py#1279-1316#b1db7068 — [[F:src/data/storage.py#1279-1316#b1db7068]].
- StorageBackend (class, lines 1317-1354, slice 17): CHUNK_ID = src/data/storage.py#1317-1354#b1db7068 — [[F:src/data/storage.py#1317-1354#b1db7068]].
- StorageBackend (class, lines 1355-1392, slice 18): CHUNK_ID = src/data/storage.py#1355-1392#b1db7068 — [[F:src/data/storage.py#1355-1392#b1db7068]].
- StorageBackend (class, lines 1393-1430, slice 19): CHUNK_ID = src/data/storage.py#1393-1430#b1db7068 — [[F:src/data/storage.py#1393-1430#b1db7068]].
- StorageBackend (class, lines 1431-1468, slice 20): CHUNK_ID = src/data/storage.py#1431-1468#b1db7068 — [[F:src/data/storage.py#1431-1468#b1db7068]].
- StorageBackend (class, lines 1469-1506, slice 21): CHUNK_ID = src/data/storage.py#1469-1506#b1db7068 — [[F:src/data/storage.py#1469-1506#b1db7068]].
- StorageBackend (class, lines 1507-1544, slice 22): CHUNK_ID = src/data/storage.py#1507-1544#b1db7068 — [[F:src/data/storage.py#1507-1544#b1db7068]].
- StorageBackend (class, lines 1545-1582, slice 23): CHUNK_ID = src/data/storage.py#1545-1582#b1db7068 — [[F:src/data/storage.py#1545-1582#b1db7068]].
- StorageBackend (class, lines 1583-1620, slice 24): CHUNK_ID = src/data/storage.py#1583-1620#b1db7068 — [[F:src/data/storage.py#1583-1620#b1db7068]].
- StorageBackend (class, lines 1621-1658, slice 25): CHUNK_ID = src/data/storage.py#1621-1658#b1db7068 — [[F:src/data/storage.py#1621-1658#b1db7068]].
- StorageBackend (class, lines 1659-1696, slice 26): CHUNK_ID = src/data/storage.py#1659-1696#b1db7068 — [[F:src/data/storage.py#1659-1696#b1db7068]].
- StorageBackend (class, lines 1697-1734, slice 27): CHUNK_ID = src/data/storage.py#1697-1734#b1db7068 — [[F:src/data/storage.py#1697-1734#b1db7068]].
- StorageBackend (class, lines 1735-1772, slice 28): CHUNK_ID = src/data/storage.py#1735-1772#b1db7068 — [[F:src/data/storage.py#1735-1772#b1db7068]].
- StorageBackend (class, lines 1773-1810, slice 29): CHUNK_ID = src/data/storage.py#1773-1810#b1db7068 — [[F:src/data/storage.py#1773-1810#b1db7068]].
- StorageBackend (class, lines 1811-1848, slice 30): CHUNK_ID = src/data/storage.py#1811-1848#b1db7068 — [[F:src/data/storage.py#1811-1848#b1db7068]].
- StorageBackend (class, lines 1849-1886, slice 31): CHUNK_ID = src/data/storage.py#1849-1886#b1db7068 — [[F:src/data/storage.py#1849-1886#b1db7068]].
- StorageBackend (class, lines 1887-1924, slice 32): CHUNK_ID = src/data/storage.py#1887-1924#b1db7068 — [[F:src/data/storage.py#1887-1924#b1db7068]].
- StorageBackend (class, lines 1925-1962, slice 33): CHUNK_ID = src/data/storage.py#1925-1962#b1db7068 — [[F:src/data/storage.py#1925-1962#b1db7068]].
- StorageBackend (class, lines 1963-2000, slice 34): CHUNK_ID = src/data/storage.py#1963-2000#b1db7068 — [[F:src/data/storage.py#1963-2000#b1db7068]].
- StorageBackend (class, lines 2001-2038, slice 35): CHUNK_ID = src/data/storage.py#2001-2038#b1db7068 — [[F:src/data/storage.py#2001-2038#b1db7068]].
- StorageBackend (class, lines 2039-2076, slice 36): CHUNK_ID = src/data/storage.py#2039-2076#b1db7068 — [[F:src/data/storage.py#2039-2076#b1db7068]].
- StorageBackend (class, lines 2077-2114, slice 37): CHUNK_ID = src/data/storage.py#2077-2114#b1db7068 — [[F:src/data/storage.py#2077-2114#b1db7068]].
- StorageBackend (class, lines 2115-2140, slice 38): CHUNK_ID = src/data/storage.py#2115-2140#b1db7068 — [[F:src/data/storage.py#2115-2140#b1db7068]].
- StorageBackend.__init__ (method, lines 722-731): CHUNK_ID = src/data/storage.py#722-731#b1db7068 — [[F:src/data/storage.py#722-731#b1db7068]].
- StorageBackend._get_lock (method, lines 733-743): CHUNK_ID = src/data/storage.py#733-743#b1db7068 — [[F:src/data/storage.py#733-743#b1db7068]].
- StorageBackend.initialize (method, lines 745-761): CHUNK_ID = src/data/storage.py#745-761#b1db7068 — [[F:src/data/storage.py#745-761#b1db7068]].
- StorageBackend._run_migrations (method, lines 763-800, slice 1): CHUNK_ID = src/data/storage.py#763-800#b1db7068 — [[F:src/data/storage.py#763-800#b1db7068]].
- StorageBackend._run_migrations (method, lines 801-814, slice 2): CHUNK_ID = src/data/storage.py#801-814#b1db7068 — [[F:src/data/storage.py#801-814#b1db7068]].
- StorageBackend.close (method, lines 816-824): CHUNK_ID = src/data/storage.py#816-824#b1db7068 — [[F:src/data/storage.py#816-824#b1db7068]].
- StorageBackend._require_conn (method, lines 826-835): CHUNK_ID = src/data/storage.py#826-835#b1db7068 — [[F:src/data/storage.py#826-835#b1db7068]].
- StorageBackend._bulk_write_ctx (method, lines 838-854): CHUNK_ID = src/data/storage.py#838-854#b1db7068 — [[F:src/data/storage.py#838-854#b1db7068]].
- StorageBackend._write_ctx (method, lines 857-878): CHUNK_ID = src/data/storage.py#857-878#b1db7068 — [[F:src/data/storage.py#857-878#b1db7068]].
- StorageBackend.upsert_bars (method, lines 884-921): CHUNK_ID = src/data/storage.py#884-921#b1db7068 — [[F:src/data/storage.py#884-921#b1db7068]].
- StorageBackend.fetch_bars (method, lines 923-964): CHUNK_ID = src/data/storage.py#923-964#b1db7068 — [[F:src/data/storage.py#923-964#b1db7068]].
- StorageBackend.store_intelligence_features (method, lines 970-1007, slice 1): CHUNK_ID = src/data/storage.py#970-1007#b1db7068 — [[F:src/data/storage.py#970-1007#b1db7068]].
- StorageBackend.store_intelligence_features (method, lines 1008-1045, slice 2): CHUNK_ID = src/data/storage.py#1008-1045#b1db7068 — [[F:src/data/storage.py#1008-1045#b1db7068]].
- StorageBackend.store_intelligence_features (method, lines 1046-1083, slice 3): CHUNK_ID = src/data/storage.py#1046-1083#b1db7068 — [[F:src/data/storage.py#1046-1083#b1db7068]].
- StorageBackend.store_intelligence_features (method, lines 1084-1121, slice 4): CHUNK_ID = src/data/storage.py#1084-1121#b1db7068 — [[F:src/data/storage.py#1084-1121#b1db7068]].
- StorageBackend.store_intelligence_features (method, lines 1122-1122, slice 5): CHUNK_ID = src/data/storage.py#1122-1122#b1db7068 — [[F:src/data/storage.py#1122-1122#b1db7068]].
- StorageBackend.fetch_intelligence_features (method, lines 1124-1161, slice 1): CHUNK_ID = src/data/storage.py#1124-1161#b1db7068 — [[F:src/data/storage.py#1124-1161#b1db7068]].
- StorageBackend.fetch_intelligence_features (method, lines 1162-1199, slice 2): CHUNK_ID = src/data/storage.py#1162-1199#b1db7068 — [[F:src/data/storage.py#1162-1199#b1db7068]].
- StorageBackend.fetch_intelligence_features (method, lines 1200-1228, slice 3): CHUNK_ID = src/data/storage.py#1200-1228#b1db7068 — [[F:src/data/storage.py#1200-1228#b1db7068]].
- StorageBackend.intelligence_feature_coverage (method, lines 1230-1267, slice 1): CHUNK_ID = src/data/storage.py#1230-1267#b1db7068 — [[F:src/data/storage.py#1230-1267#b1db7068]].
- StorageBackend.intelligence_feature_coverage (method, lines 1268-1288, slice 2): CHUNK_ID = src/data/storage.py#1268-1288#b1db7068 — [[F:src/data/storage.py#1268-1288#b1db7068]].
- StorageBackend.latest_bar_ts (method, lines 1290-1298): CHUNK_ID = src/data/storage.py#1290-1298#b1db7068 — [[F:src/data/storage.py#1290-1298#b1db7068]].
- StorageBackend.latest_close (method, lines 1300-1322): CHUNK_ID = src/data/storage.py#1300-1322#b1db7068 — [[F:src/data/storage.py#1300-1322#b1db7068]].
- StorageBackend.bar_count (method, lines 1324-1332): CHUNK_ID = src/data/storage.py#1324-1332#b1db7068 — [[F:src/data/storage.py#1324-1332#b1db7068]].
- StorageBackend.prune_old_bars (method, lines 1334-1355): CHUNK_ID = src/data/storage.py#1334-1355#b1db7068 — [[F:src/data/storage.py#1334-1355#b1db7068]].
- StorageBackend.insert_trade (method, lines 1361-1398, slice 1): CHUNK_ID = src/data/storage.py#1361-1398#b1db7068 — [[F:src/data/storage.py#1361-1398#b1db7068]].
- StorageBackend.insert_trade (method, lines 1399-1421, slice 2): CHUNK_ID = src/data/storage.py#1399-1421#b1db7068 — [[F:src/data/storage.py#1399-1421#b1db7068]].
- StorageBackend.update_trade_exit (method, lines 1423-1459): CHUNK_ID = src/data/storage.py#1423-1459#b1db7068 — [[F:src/data/storage.py#1423-1459#b1db7068]].
- StorageBackend.update_trade_ensemble_fields (method, lines 1461-1482): CHUNK_ID = src/data/storage.py#1461-1482#b1db7068 — [[F:src/data/storage.py#1461-1482#b1db7068]].
- StorageBackend.fetch_trades (method, lines 1484-1521, slice 1): CHUNK_ID = src/data/storage.py#1484-1521#b1db7068 — [[F:src/data/storage.py#1484-1521#b1db7068]].
- StorageBackend.fetch_trades (method, lines 1522-1559, slice 2): CHUNK_ID = src/data/storage.py#1522-1559#b1db7068 — [[F:src/data/storage.py#1522-1559#b1db7068]].
- StorageBackend.fetch_trades (method, lines 1560-1579, slice 3): CHUNK_ID = src/data/storage.py#1560-1579#b1db7068 — [[F:src/data/storage.py#1560-1579#b1db7068]].
- StorageBackend.count_consecutive_losses (method, lines 1581-1603): CHUNK_ID = src/data/storage.py#1581-1603#b1db7068 — [[F:src/data/storage.py#1581-1603#b1db7068]].
- StorageBackend.daily_pnl (method, lines 1605-1623): CHUNK_ID = src/data/storage.py#1605-1623#b1db7068 — [[F:src/data/storage.py#1605-1623#b1db7068]].
- StorageBackend.upsert_regime_snapshot (method, lines 1629-1653): CHUNK_ID = src/data/storage.py#1629-1653#b1db7068 — [[F:src/data/storage.py#1629-1653#b1db7068]].
- StorageBackend.latest_regime (method, lines 1655-1682): CHUNK_ID = src/data/storage.py#1655-1682#b1db7068 — [[F:src/data/storage.py#1655-1682#b1db7068]].
- StorageBackend.regime_snapshot_before (method, lines 1684-1716): CHUNK_ID = src/data/storage.py#1684-1716#b1db7068 — [[F:src/data/storage.py#1684-1716#b1db7068]].
- StorageBackend.bars_before (method, lines 1718-1756): CHUNK_ID = src/data/storage.py#1718-1756#b1db7068 — [[F:src/data/storage.py#1718-1756#b1db7068]].
- StorageBackend.insert_missed_trade (method, lines 1762-1791): CHUNK_ID = src/data/storage.py#1762-1791#b1db7068 — [[F:src/data/storage.py#1762-1791#b1db7068]].
- StorageBackend.fetch_missed_trades (method, lines 1793-1828): CHUNK_ID = src/data/storage.py#1793-1828#b1db7068 — [[F:src/data/storage.py#1793-1828#b1db7068]].
- StorageBackend.insert_model_metrics (method, lines 1834-1867): CHUNK_ID = src/data/storage.py#1834-1867#b1db7068 — [[F:src/data/storage.py#1834-1867#b1db7068]].
- StorageBackend.latest_model_metrics (method, lines 1869-1900): CHUNK_ID = src/data/storage.py#1869-1900#b1db7068 — [[F:src/data/storage.py#1869-1900#b1db7068]].
- StorageBackend.live_gate_passes (method, lines 1902-1911): CHUNK_ID = src/data/storage.py#1902-1911#b1db7068 — [[F:src/data/storage.py#1902-1911#b1db7068]].
- StorageBackend.insert_equity (method, lines 1917-1941): CHUNK_ID = src/data/storage.py#1917-1941#b1db7068 — [[F:src/data/storage.py#1917-1941#b1db7068]].
- StorageBackend.fetch_equity_curve (method, lines 1943-1980, slice 1): CHUNK_ID = src/data/storage.py#1943-1980#b1db7068 — [[F:src/data/storage.py#1943-1980#b1db7068]].
- StorageBackend.fetch_equity_curve (method, lines 1981-1991, slice 2): CHUNK_ID = src/data/storage.py#1981-1991#b1db7068 — [[F:src/data/storage.py#1981-1991#b1db7068]].
- StorageBackend.latest_equity (method, lines 1993-2019): CHUNK_ID = src/data/storage.py#1993-2019#b1db7068 — [[F:src/data/storage.py#1993-2019#b1db7068]].
- StorageBackend.earliest_equity_ts (method, lines 2021-2031): CHUNK_ID = src/data/storage.py#2021-2031#b1db7068 — [[F:src/data/storage.py#2021-2031#b1db7068]].
- StorageBackend.validate_symbol (method, lines 2033-2051): CHUNK_ID = src/data/storage.py#2033-2051#b1db7068 — [[F:src/data/storage.py#2033-2051#b1db7068]].
- StorageBackend.insert_audit_event (method, lines 2057-2080): CHUNK_ID = src/data/storage.py#2057-2080#b1db7068 — [[F:src/data/storage.py#2057-2080#b1db7068]].
- StorageBackend.upsert_runtime_desired_state (method, lines 2086-2106): CHUNK_ID = src/data/storage.py#2086-2106#b1db7068 — [[F:src/data/storage.py#2086-2106#b1db7068]].
- StorageBackend.fetch_runtime_desired_states (method, lines 2108-2115): CHUNK_ID = src/data/storage.py#2108-2115#b1db7068 — [[F:src/data/storage.py#2108-2115#b1db7068]].
- StorageBackend.health_check (method, lines 2121-2140): CHUNK_ID = src/data/storage.py#2121-2140#b1db7068 — [[F:src/data/storage.py#2121-2140#b1db7068]].
- create_storage_backend (function, lines 2148-2163): CHUNK_ID = src/data/storage.py#2148-2163#b1db7068 — [[F:src/data/storage.py#2148-2163#b1db7068]].
- open_storage (function, lines 2167-2183): CHUNK_ID = src/data/storage.py#2167-2183#b1db7068 — [[F:src/data/storage.py#2167-2183#b1db7068]].

## src/data/timescale_storage.py

SHA8 1aa58429; total lines 1594.

- _rows_from_status (function, lines 381-386): CHUNK_ID = src/data/timescale_storage.py#381-386#1aa58429 — [[F:src/data/timescale_storage.py#381-386#1aa58429]].
- TimescaleBackend (class, lines 394-431, slice 1): CHUNK_ID = src/data/timescale_storage.py#394-431#1aa58429 — [[F:src/data/timescale_storage.py#394-431#1aa58429]].
- TimescaleBackend (class, lines 432-469, slice 2): CHUNK_ID = src/data/timescale_storage.py#432-469#1aa58429 — [[F:src/data/timescale_storage.py#432-469#1aa58429]].
- TimescaleBackend (class, lines 470-507, slice 3): CHUNK_ID = src/data/timescale_storage.py#470-507#1aa58429 — [[F:src/data/timescale_storage.py#470-507#1aa58429]].
- TimescaleBackend (class, lines 508-545, slice 4): CHUNK_ID = src/data/timescale_storage.py#508-545#1aa58429 — [[F:src/data/timescale_storage.py#508-545#1aa58429]].
- TimescaleBackend (class, lines 546-583, slice 5): CHUNK_ID = src/data/timescale_storage.py#546-583#1aa58429 — [[F:src/data/timescale_storage.py#546-583#1aa58429]].
- TimescaleBackend (class, lines 584-621, slice 6): CHUNK_ID = src/data/timescale_storage.py#584-621#1aa58429 — [[F:src/data/timescale_storage.py#584-621#1aa58429]].
- TimescaleBackend (class, lines 622-659, slice 7): CHUNK_ID = src/data/timescale_storage.py#622-659#1aa58429 — [[F:src/data/timescale_storage.py#622-659#1aa58429]].
- TimescaleBackend (class, lines 660-697, slice 8): CHUNK_ID = src/data/timescale_storage.py#660-697#1aa58429 — [[F:src/data/timescale_storage.py#660-697#1aa58429]].
- TimescaleBackend (class, lines 698-735, slice 9): CHUNK_ID = src/data/timescale_storage.py#698-735#1aa58429 — [[F:src/data/timescale_storage.py#698-735#1aa58429]].
- TimescaleBackend (class, lines 736-773, slice 10): CHUNK_ID = src/data/timescale_storage.py#736-773#1aa58429 — [[F:src/data/timescale_storage.py#736-773#1aa58429]].
- TimescaleBackend (class, lines 774-811, slice 11): CHUNK_ID = src/data/timescale_storage.py#774-811#1aa58429 — [[F:src/data/timescale_storage.py#774-811#1aa58429]].
- TimescaleBackend (class, lines 812-849, slice 12): CHUNK_ID = src/data/timescale_storage.py#812-849#1aa58429 — [[F:src/data/timescale_storage.py#812-849#1aa58429]].
- TimescaleBackend (class, lines 850-887, slice 13): CHUNK_ID = src/data/timescale_storage.py#850-887#1aa58429 — [[F:src/data/timescale_storage.py#850-887#1aa58429]].
- TimescaleBackend (class, lines 888-925, slice 14): CHUNK_ID = src/data/timescale_storage.py#888-925#1aa58429 — [[F:src/data/timescale_storage.py#888-925#1aa58429]].
- TimescaleBackend (class, lines 926-963, slice 15): CHUNK_ID = src/data/timescale_storage.py#926-963#1aa58429 — [[F:src/data/timescale_storage.py#926-963#1aa58429]].
- TimescaleBackend (class, lines 964-1001, slice 16): CHUNK_ID = src/data/timescale_storage.py#964-1001#1aa58429 — [[F:src/data/timescale_storage.py#964-1001#1aa58429]].
- TimescaleBackend (class, lines 1002-1039, slice 17): CHUNK_ID = src/data/timescale_storage.py#1002-1039#1aa58429 — [[F:src/data/timescale_storage.py#1002-1039#1aa58429]].
- TimescaleBackend (class, lines 1040-1077, slice 18): CHUNK_ID = src/data/timescale_storage.py#1040-1077#1aa58429 — [[F:src/data/timescale_storage.py#1040-1077#1aa58429]].
- TimescaleBackend (class, lines 1078-1115, slice 19): CHUNK_ID = src/data/timescale_storage.py#1078-1115#1aa58429 — [[F:src/data/timescale_storage.py#1078-1115#1aa58429]].
- TimescaleBackend (class, lines 1116-1153, slice 20): CHUNK_ID = src/data/timescale_storage.py#1116-1153#1aa58429 — [[F:src/data/timescale_storage.py#1116-1153#1aa58429]].
- TimescaleBackend (class, lines 1154-1191, slice 21): CHUNK_ID = src/data/timescale_storage.py#1154-1191#1aa58429 — [[F:src/data/timescale_storage.py#1154-1191#1aa58429]].
- TimescaleBackend (class, lines 1192-1229, slice 22): CHUNK_ID = src/data/timescale_storage.py#1192-1229#1aa58429 — [[F:src/data/timescale_storage.py#1192-1229#1aa58429]].
- TimescaleBackend (class, lines 1230-1267, slice 23): CHUNK_ID = src/data/timescale_storage.py#1230-1267#1aa58429 — [[F:src/data/timescale_storage.py#1230-1267#1aa58429]].
- TimescaleBackend (class, lines 1268-1305, slice 24): CHUNK_ID = src/data/timescale_storage.py#1268-1305#1aa58429 — [[F:src/data/timescale_storage.py#1268-1305#1aa58429]].
- TimescaleBackend (class, lines 1306-1343, slice 25): CHUNK_ID = src/data/timescale_storage.py#1306-1343#1aa58429 — [[F:src/data/timescale_storage.py#1306-1343#1aa58429]].
- TimescaleBackend (class, lines 1344-1381, slice 26): CHUNK_ID = src/data/timescale_storage.py#1344-1381#1aa58429 — [[F:src/data/timescale_storage.py#1344-1381#1aa58429]].
- TimescaleBackend (class, lines 1382-1419, slice 27): CHUNK_ID = src/data/timescale_storage.py#1382-1419#1aa58429 — [[F:src/data/timescale_storage.py#1382-1419#1aa58429]].
- TimescaleBackend (class, lines 1420-1457, slice 28): CHUNK_ID = src/data/timescale_storage.py#1420-1457#1aa58429 — [[F:src/data/timescale_storage.py#1420-1457#1aa58429]].
- TimescaleBackend (class, lines 1458-1495, slice 29): CHUNK_ID = src/data/timescale_storage.py#1458-1495#1aa58429 — [[F:src/data/timescale_storage.py#1458-1495#1aa58429]].
- TimescaleBackend (class, lines 1496-1533, slice 30): CHUNK_ID = src/data/timescale_storage.py#1496-1533#1aa58429 — [[F:src/data/timescale_storage.py#1496-1533#1aa58429]].
- TimescaleBackend (class, lines 1534-1571, slice 31): CHUNK_ID = src/data/timescale_storage.py#1534-1571#1aa58429 — [[F:src/data/timescale_storage.py#1534-1571#1aa58429]].
- TimescaleBackend.__init__ (method, lines 407-419): CHUNK_ID = src/data/timescale_storage.py#407-419#1aa58429 — [[F:src/data/timescale_storage.py#407-419#1aa58429]].
- TimescaleBackend._get_lock (method, lines 421-431): CHUNK_ID = src/data/timescale_storage.py#421-431#1aa58429 — [[F:src/data/timescale_storage.py#421-431#1aa58429]].
- TimescaleBackend.initialize (method, lines 433-456): CHUNK_ID = src/data/timescale_storage.py#433-456#1aa58429 — [[F:src/data/timescale_storage.py#433-456#1aa58429]].
- TimescaleBackend._run_migrations (method, lines 458-492): CHUNK_ID = src/data/timescale_storage.py#458-492#1aa58429 — [[F:src/data/timescale_storage.py#458-492#1aa58429]].
- TimescaleBackend.close (method, lines 494-501): CHUNK_ID = src/data/timescale_storage.py#494-501#1aa58429 — [[F:src/data/timescale_storage.py#494-501#1aa58429]].
- TimescaleBackend._require_pool (method, lines 503-512): CHUNK_ID = src/data/timescale_storage.py#503-512#1aa58429 — [[F:src/data/timescale_storage.py#503-512#1aa58429]].
- TimescaleBackend.upsert_bars (method, lines 518-555, slice 1): CHUNK_ID = src/data/timescale_storage.py#518-555#1aa58429 — [[F:src/data/timescale_storage.py#518-555#1aa58429]].
- TimescaleBackend.upsert_bars (method, lines 556-565, slice 2): CHUNK_ID = src/data/timescale_storage.py#556-565#1aa58429 — [[F:src/data/timescale_storage.py#556-565#1aa58429]].
- TimescaleBackend.fetch_bars (method, lines 567-608): CHUNK_ID = src/data/timescale_storage.py#567-608#1aa58429 — [[F:src/data/timescale_storage.py#567-608#1aa58429]].
- TimescaleBackend.store_intelligence_features (method, lines 614-651, slice 1): CHUNK_ID = src/data/timescale_storage.py#614-651#1aa58429 — [[F:src/data/timescale_storage.py#614-651#1aa58429]].
- TimescaleBackend.store_intelligence_features (method, lines 652-663, slice 2): CHUNK_ID = src/data/timescale_storage.py#652-663#1aa58429 — [[F:src/data/timescale_storage.py#652-663#1aa58429]].
- TimescaleBackend.fetch_intelligence_features (method, lines 665-703): CHUNK_ID = src/data/timescale_storage.py#665-703#1aa58429 — [[F:src/data/timescale_storage.py#665-703#1aa58429]].
- TimescaleBackend.intelligence_feature_coverage (method, lines 705-738): CHUNK_ID = src/data/timescale_storage.py#705-738#1aa58429 — [[F:src/data/timescale_storage.py#705-738#1aa58429]].
- TimescaleBackend.latest_bar_ts (method, lines 740-749): CHUNK_ID = src/data/timescale_storage.py#740-749#1aa58429 — [[F:src/data/timescale_storage.py#740-749#1aa58429]].
- TimescaleBackend.latest_close (method, lines 751-772): CHUNK_ID = src/data/timescale_storage.py#751-772#1aa58429 — [[F:src/data/timescale_storage.py#751-772#1aa58429]].
- TimescaleBackend.bar_count (method, lines 774-783): CHUNK_ID = src/data/timescale_storage.py#774-783#1aa58429 — [[F:src/data/timescale_storage.py#774-783#1aa58429]].
- TimescaleBackend.prune_old_bars (method, lines 785-807): CHUNK_ID = src/data/timescale_storage.py#785-807#1aa58429 — [[F:src/data/timescale_storage.py#785-807#1aa58429]].
- TimescaleBackend.insert_trade (method, lines 813-850, slice 1): CHUNK_ID = src/data/timescale_storage.py#813-850#1aa58429 — [[F:src/data/timescale_storage.py#813-850#1aa58429]].
- TimescaleBackend.insert_trade (method, lines 851-867, slice 2): CHUNK_ID = src/data/timescale_storage.py#851-867#1aa58429 — [[F:src/data/timescale_storage.py#851-867#1aa58429]].
- TimescaleBackend.update_trade_exit (method, lines 869-908): CHUNK_ID = src/data/timescale_storage.py#869-908#1aa58429 — [[F:src/data/timescale_storage.py#869-908#1aa58429]].
- TimescaleBackend.update_trade_ensemble_fields (method, lines 910-926): CHUNK_ID = src/data/timescale_storage.py#910-926#1aa58429 — [[F:src/data/timescale_storage.py#910-926#1aa58429]].
- TimescaleBackend.fetch_trades (method, lines 928-965, slice 1): CHUNK_ID = src/data/timescale_storage.py#928-965#1aa58429 — [[F:src/data/timescale_storage.py#928-965#1aa58429]].
- TimescaleBackend.fetch_trades (method, lines 966-1003, slice 2): CHUNK_ID = src/data/timescale_storage.py#966-1003#1aa58429 — [[F:src/data/timescale_storage.py#966-1003#1aa58429]].
- TimescaleBackend.fetch_trades (method, lines 1004-1006, slice 3): CHUNK_ID = src/data/timescale_storage.py#1004-1006#1aa58429 — [[F:src/data/timescale_storage.py#1004-1006#1aa58429]].
- TimescaleBackend.count_consecutive_losses (method, lines 1008-1031): CHUNK_ID = src/data/timescale_storage.py#1008-1031#1aa58429 — [[F:src/data/timescale_storage.py#1008-1031#1aa58429]].
- TimescaleBackend.daily_pnl (method, lines 1033-1053): CHUNK_ID = src/data/timescale_storage.py#1033-1053#1aa58429 — [[F:src/data/timescale_storage.py#1033-1053#1aa58429]].
- TimescaleBackend.upsert_regime_snapshot (method, lines 1059-1087): CHUNK_ID = src/data/timescale_storage.py#1059-1087#1aa58429 — [[F:src/data/timescale_storage.py#1059-1087#1aa58429]].
- TimescaleBackend.latest_regime (method, lines 1089-1117): CHUNK_ID = src/data/timescale_storage.py#1089-1117#1aa58429 — [[F:src/data/timescale_storage.py#1089-1117#1aa58429]].
- TimescaleBackend.regime_snapshot_before (method, lines 1119-1152): CHUNK_ID = src/data/timescale_storage.py#1119-1152#1aa58429 — [[F:src/data/timescale_storage.py#1119-1152#1aa58429]].
- TimescaleBackend.bars_before (method, lines 1154-1195): CHUNK_ID = src/data/timescale_storage.py#1154-1195#1aa58429 — [[F:src/data/timescale_storage.py#1154-1195#1aa58429]].
- TimescaleBackend.insert_missed_trade (method, lines 1201-1225): CHUNK_ID = src/data/timescale_storage.py#1201-1225#1aa58429 — [[F:src/data/timescale_storage.py#1201-1225#1aa58429]].
- TimescaleBackend.fetch_missed_trades (method, lines 1227-1260): CHUNK_ID = src/data/timescale_storage.py#1227-1260#1aa58429 — [[F:src/data/timescale_storage.py#1227-1260#1aa58429]].
- TimescaleBackend.insert_model_metrics (method, lines 1266-1305): CHUNK_ID = src/data/timescale_storage.py#1266-1305#1aa58429 — [[F:src/data/timescale_storage.py#1266-1305#1aa58429]].
- TimescaleBackend.latest_model_metrics (method, lines 1307-1339): CHUNK_ID = src/data/timescale_storage.py#1307-1339#1aa58429 — [[F:src/data/timescale_storage.py#1307-1339#1aa58429]].
- TimescaleBackend.live_gate_passes (method, lines 1341-1350): CHUNK_ID = src/data/timescale_storage.py#1341-1350#1aa58429 — [[F:src/data/timescale_storage.py#1341-1350#1aa58429]].
- TimescaleBackend.insert_equity (method, lines 1356-1384): CHUNK_ID = src/data/timescale_storage.py#1356-1384#1aa58429 — [[F:src/data/timescale_storage.py#1356-1384#1aa58429]].
- TimescaleBackend.fetch_equity_curve (method, lines 1386-1427): CHUNK_ID = src/data/timescale_storage.py#1386-1427#1aa58429 — [[F:src/data/timescale_storage.py#1386-1427#1aa58429]].
- TimescaleBackend.latest_equity (method, lines 1429-1455): CHUNK_ID = src/data/timescale_storage.py#1429-1455#1aa58429 — [[F:src/data/timescale_storage.py#1429-1455#1aa58429]].
- TimescaleBackend.earliest_equity_ts (method, lines 1457-1465): CHUNK_ID = src/data/timescale_storage.py#1457-1465#1aa58429 — [[F:src/data/timescale_storage.py#1457-1465#1aa58429]].
- TimescaleBackend.validate_symbol (method, lines 1467-1485): CHUNK_ID = src/data/timescale_storage.py#1467-1485#1aa58429 — [[F:src/data/timescale_storage.py#1467-1485#1aa58429]].
- TimescaleBackend.upsert_runtime_desired_state (method, lines 1491-1512): CHUNK_ID = src/data/timescale_storage.py#1491-1512#1aa58429 — [[F:src/data/timescale_storage.py#1491-1512#1aa58429]].
- TimescaleBackend.fetch_runtime_desired_states (method, lines 1514-1522): CHUNK_ID = src/data/timescale_storage.py#1514-1522#1aa58429 — [[F:src/data/timescale_storage.py#1514-1522#1aa58429]].
- TimescaleBackend.insert_audit_event (method, lines 1528-1552): CHUNK_ID = src/data/timescale_storage.py#1528-1552#1aa58429 — [[F:src/data/timescale_storage.py#1528-1552#1aa58429]].
- TimescaleBackend.health_check (method, lines 1558-1571): CHUNK_ID = src/data/timescale_storage.py#1558-1571#1aa58429 — [[F:src/data/timescale_storage.py#1558-1571#1aa58429]].
- open_timescale_storage (function, lines 1580-1594): CHUNK_ID = src/data/timescale_storage.py#1580-1594#1aa58429 — [[F:src/data/timescale_storage.py#1580-1594#1aa58429]].

## src/models/trainer.py

SHA8 77a4dac0; total lines 1639.

- _validate_timeframe (function, lines 90-104): CHUNK_ID = src/models/trainer.py#90-104#77a4dac0 — [[F:src/models/trainer.py#90-104#77a4dac0]].
- _atomic_write_bytes (function, lines 107-121): CHUNK_ID = src/models/trainer.py#107-121#77a4dac0 — [[F:src/models/trainer.py#107-121#77a4dac0]].
- _write_manifest (function, lines 124-143): CHUNK_ID = src/models/trainer.py#124-143#77a4dac0 — [[F:src/models/trainer.py#124-143#77a4dac0]].
- _verify_manifest (function, lines 146-176): CHUNK_ID = src/models/trainer.py#146-176#77a4dac0 — [[F:src/models/trainer.py#146-176#77a4dac0]].
- hmac_compare (function, lines 179-183): CHUNK_ID = src/models/trainer.py#179-183#77a4dac0 — [[F:src/models/trainer.py#179-183#77a4dac0]].
- CPCVFold (class, lines 192-197): CHUNK_ID = src/models/trainer.py#192-197#77a4dac0 — [[F:src/models/trainer.py#192-197#77a4dac0]].
- _build_groups (function, lines 200-209): CHUNK_ID = src/models/trainer.py#200-209#77a4dac0 — [[F:src/models/trainer.py#200-209#77a4dac0]].
- _apply_purge_embargo (function, lines 212-226): CHUNK_ID = src/models/trainer.py#212-226#77a4dac0 — [[F:src/models/trainer.py#212-226#77a4dac0]].
- _build_train_indices (function, lines 229-255): CHUNK_ID = src/models/trainer.py#229-255#77a4dac0 — [[F:src/models/trainer.py#229-255#77a4dac0]].
- build_cpcv_folds (function, lines 258-295, slice 1): CHUNK_ID = src/models/trainer.py#258-295#77a4dac0 — [[F:src/models/trainer.py#258-295#77a4dac0]].
- build_cpcv_folds (function, lines 296-333, slice 2): CHUNK_ID = src/models/trainer.py#296-333#77a4dac0 — [[F:src/models/trainer.py#296-333#77a4dac0]].
- compute_sample_weights (function, lines 341-355): CHUNK_ID = src/models/trainer.py#341-355#77a4dac0 — [[F:src/models/trainer.py#341-355#77a4dac0]].
- FoldMetrics (class, lines 364-373): CHUNK_ID = src/models/trainer.py#364-373#77a4dac0 — [[F:src/models/trainer.py#364-373#77a4dac0]].
- TrainingResult (class, lines 377-414, slice 1): CHUNK_ID = src/models/trainer.py#377-414#77a4dac0 — [[F:src/models/trainer.py#377-414#77a4dac0]].
- TrainingResult (class, lines 415-424, slice 2): CHUNK_ID = src/models/trainer.py#415-424#77a4dac0 — [[F:src/models/trainer.py#415-424#77a4dac0]].
- TrainingResult.to_metrics_record (method, lines 406-424): CHUNK_ID = src/models/trainer.py#406-424#77a4dac0 — [[F:src/models/trainer.py#406-424#77a4dac0]].
- oos_sharpe_and_drawdown (function, lines 432-469, slice 1): CHUNK_ID = src/models/trainer.py#432-469#77a4dac0 — [[F:src/models/trainer.py#432-469#77a4dac0]].
- oos_sharpe_and_drawdown (function, lines 470-478, slice 2): CHUNK_ID = src/models/trainer.py#470-478#77a4dac0 — [[F:src/models/trainer.py#470-478#77a4dac0]].
- _build_xgb (function, lines 486-505): CHUNK_ID = src/models/trainer.py#486-505#77a4dac0 — [[F:src/models/trainer.py#486-505#77a4dac0]].
- _attach_feature_columns (function, lines 520-533): CHUNK_ID = src/models/trainer.py#520-533#77a4dac0 — [[F:src/models/trainer.py#520-533#77a4dac0]].
- ModelTrainer (class, lines 536-573, slice 1): CHUNK_ID = src/models/trainer.py#536-573#77a4dac0 — [[F:src/models/trainer.py#536-573#77a4dac0]].
- ModelTrainer (class, lines 574-611, slice 2): CHUNK_ID = src/models/trainer.py#574-611#77a4dac0 — [[F:src/models/trainer.py#574-611#77a4dac0]].
- ModelTrainer (class, lines 612-649, slice 3): CHUNK_ID = src/models/trainer.py#612-649#77a4dac0 — [[F:src/models/trainer.py#612-649#77a4dac0]].
- ModelTrainer (class, lines 650-687, slice 4): CHUNK_ID = src/models/trainer.py#650-687#77a4dac0 — [[F:src/models/trainer.py#650-687#77a4dac0]].
- ModelTrainer (class, lines 688-725, slice 5): CHUNK_ID = src/models/trainer.py#688-725#77a4dac0 — [[F:src/models/trainer.py#688-725#77a4dac0]].
- ModelTrainer (class, lines 726-763, slice 6): CHUNK_ID = src/models/trainer.py#726-763#77a4dac0 — [[F:src/models/trainer.py#726-763#77a4dac0]].
- ModelTrainer (class, lines 764-801, slice 7): CHUNK_ID = src/models/trainer.py#764-801#77a4dac0 — [[F:src/models/trainer.py#764-801#77a4dac0]].
- ModelTrainer (class, lines 802-839, slice 8): CHUNK_ID = src/models/trainer.py#802-839#77a4dac0 — [[F:src/models/trainer.py#802-839#77a4dac0]].
- ModelTrainer (class, lines 840-877, slice 9): CHUNK_ID = src/models/trainer.py#840-877#77a4dac0 — [[F:src/models/trainer.py#840-877#77a4dac0]].
- ModelTrainer (class, lines 878-915, slice 10): CHUNK_ID = src/models/trainer.py#878-915#77a4dac0 — [[F:src/models/trainer.py#878-915#77a4dac0]].
- ModelTrainer (class, lines 916-953, slice 11): CHUNK_ID = src/models/trainer.py#916-953#77a4dac0 — [[F:src/models/trainer.py#916-953#77a4dac0]].
- ModelTrainer (class, lines 954-991, slice 12): CHUNK_ID = src/models/trainer.py#954-991#77a4dac0 — [[F:src/models/trainer.py#954-991#77a4dac0]].
- ModelTrainer (class, lines 992-1029, slice 13): CHUNK_ID = src/models/trainer.py#992-1029#77a4dac0 — [[F:src/models/trainer.py#992-1029#77a4dac0]].
- ModelTrainer (class, lines 1030-1067, slice 14): CHUNK_ID = src/models/trainer.py#1030-1067#77a4dac0 — [[F:src/models/trainer.py#1030-1067#77a4dac0]].
- ModelTrainer (class, lines 1068-1105, slice 15): CHUNK_ID = src/models/trainer.py#1068-1105#77a4dac0 — [[F:src/models/trainer.py#1068-1105#77a4dac0]].
- ModelTrainer (class, lines 1106-1143, slice 16): CHUNK_ID = src/models/trainer.py#1106-1143#77a4dac0 — [[F:src/models/trainer.py#1106-1143#77a4dac0]].
- ModelTrainer (class, lines 1144-1181, slice 17): CHUNK_ID = src/models/trainer.py#1144-1181#77a4dac0 — [[F:src/models/trainer.py#1144-1181#77a4dac0]].
- ModelTrainer (class, lines 1182-1219, slice 18): CHUNK_ID = src/models/trainer.py#1182-1219#77a4dac0 — [[F:src/models/trainer.py#1182-1219#77a4dac0]].
- ModelTrainer (class, lines 1220-1257, slice 19): CHUNK_ID = src/models/trainer.py#1220-1257#77a4dac0 — [[F:src/models/trainer.py#1220-1257#77a4dac0]].
- ModelTrainer (class, lines 1258-1295, slice 20): CHUNK_ID = src/models/trainer.py#1258-1295#77a4dac0 — [[F:src/models/trainer.py#1258-1295#77a4dac0]].
- ModelTrainer (class, lines 1296-1333, slice 21): CHUNK_ID = src/models/trainer.py#1296-1333#77a4dac0 — [[F:src/models/trainer.py#1296-1333#77a4dac0]].
- ModelTrainer (class, lines 1334-1371, slice 22): CHUNK_ID = src/models/trainer.py#1334-1371#77a4dac0 — [[F:src/models/trainer.py#1334-1371#77a4dac0]].
- ModelTrainer (class, lines 1372-1409, slice 23): CHUNK_ID = src/models/trainer.py#1372-1409#77a4dac0 — [[F:src/models/trainer.py#1372-1409#77a4dac0]].
- ModelTrainer (class, lines 1410-1447, slice 24): CHUNK_ID = src/models/trainer.py#1410-1447#77a4dac0 — [[F:src/models/trainer.py#1410-1447#77a4dac0]].
- ModelTrainer (class, lines 1448-1485, slice 25): CHUNK_ID = src/models/trainer.py#1448-1485#77a4dac0 — [[F:src/models/trainer.py#1448-1485#77a4dac0]].
- ModelTrainer (class, lines 1486-1523, slice 26): CHUNK_ID = src/models/trainer.py#1486-1523#77a4dac0 — [[F:src/models/trainer.py#1486-1523#77a4dac0]].
- ModelTrainer (class, lines 1524-1561, slice 27): CHUNK_ID = src/models/trainer.py#1524-1561#77a4dac0 — [[F:src/models/trainer.py#1524-1561#77a4dac0]].
- ModelTrainer (class, lines 1562-1599, slice 28): CHUNK_ID = src/models/trainer.py#1562-1599#77a4dac0 — [[F:src/models/trainer.py#1562-1599#77a4dac0]].
- ModelTrainer (class, lines 1600-1637, slice 29): CHUNK_ID = src/models/trainer.py#1600-1637#77a4dac0 — [[F:src/models/trainer.py#1600-1637#77a4dac0]].
- ModelTrainer (class, lines 1638-1639, slice 30): CHUNK_ID = src/models/trainer.py#1638-1639#77a4dac0 — [[F:src/models/trainer.py#1638-1639#77a4dac0]].
- ModelTrainer.__init__ (method, lines 548-572): CHUNK_ID = src/models/trainer.py#548-572#77a4dac0 — [[F:src/models/trainer.py#548-572#77a4dac0]].
- ModelTrainer._record_provenance (method, lines 578-608): CHUNK_ID = src/models/trainer.py#578-608#77a4dac0 — [[F:src/models/trainer.py#578-608#77a4dac0]].
- ModelTrainer._cpcv_methodology (method, lines 610-616): CHUNK_ID = src/models/trainer.py#610-616#77a4dac0 — [[F:src/models/trainer.py#610-616#77a4dac0]].
- ModelTrainer.provenance_for (method, lines 618-621): CHUNK_ID = src/models/trainer.py#618-621#77a4dac0 — [[F:src/models/trainer.py#618-621#77a4dac0]].
- ModelTrainer._finish_provenance (method, lines 623-642): CHUNK_ID = src/models/trainer.py#623-642#77a4dac0 — [[F:src/models/trainer.py#623-642#77a4dac0]].
- ModelTrainer.train_direction (method, lines 648-685, slice 1): CHUNK_ID = src/models/trainer.py#648-685#77a4dac0 — [[F:src/models/trainer.py#648-685#77a4dac0]].
- ModelTrainer.train_direction (method, lines 686-723, slice 2): CHUNK_ID = src/models/trainer.py#686-723#77a4dac0 — [[F:src/models/trainer.py#686-723#77a4dac0]].
- ModelTrainer.train_direction (method, lines 724-761, slice 3): CHUNK_ID = src/models/trainer.py#724-761#77a4dac0 — [[F:src/models/trainer.py#724-761#77a4dac0]].
- ModelTrainer.train_direction (method, lines 762-799, slice 4): CHUNK_ID = src/models/trainer.py#762-799#77a4dac0 — [[F:src/models/trainer.py#762-799#77a4dac0]].
- ModelTrainer.train_direction (method, lines 800-836, slice 5): CHUNK_ID = src/models/trainer.py#800-836#77a4dac0 — [[F:src/models/trainer.py#800-836#77a4dac0]].
- ModelTrainer.train_ensemble (method, lines 842-872): CHUNK_ID = src/models/trainer.py#842-872#77a4dac0 — [[F:src/models/trainer.py#842-872#77a4dac0]].
- ModelTrainer.save_ensemble (method, lines 874-880): CHUNK_ID = src/models/trainer.py#874-880#77a4dac0 — [[F:src/models/trainer.py#874-880#77a4dac0]].
- ModelTrainer.load_ensemble (method, lines 883-892): CHUNK_ID = src/models/trainer.py#883-892#77a4dac0 — [[F:src/models/trainer.py#883-892#77a4dac0]].
- ModelTrainer.train_meta_label (method, lines 898-935, slice 1): CHUNK_ID = src/models/trainer.py#898-935#77a4dac0 — [[F:src/models/trainer.py#898-935#77a4dac0]].
- ModelTrainer.train_meta_label (method, lines 936-973, slice 2): CHUNK_ID = src/models/trainer.py#936-973#77a4dac0 — [[F:src/models/trainer.py#936-973#77a4dac0]].
- ModelTrainer.train_meta_label (method, lines 974-1011, slice 3): CHUNK_ID = src/models/trainer.py#974-1011#77a4dac0 — [[F:src/models/trainer.py#974-1011#77a4dac0]].
- ModelTrainer.train_meta_label (method, lines 1012-1049, slice 4): CHUNK_ID = src/models/trainer.py#1012-1049#77a4dac0 — [[F:src/models/trainer.py#1012-1049#77a4dac0]].
- ModelTrainer.train_meta_label (method, lines 1050-1069, slice 5): CHUNK_ID = src/models/trainer.py#1050-1069#77a4dac0 — [[F:src/models/trainer.py#1050-1069#77a4dac0]].
- ModelTrainer.predict_direction (method, lines 1075-1112, slice 1): CHUNK_ID = src/models/trainer.py#1075-1112#77a4dac0 — [[F:src/models/trainer.py#1075-1112#77a4dac0]].
- ModelTrainer.predict_direction (method, lines 1113-1123, slice 2): CHUNK_ID = src/models/trainer.py#1113-1123#77a4dac0 — [[F:src/models/trainer.py#1113-1123#77a4dac0]].
- ModelTrainer.predict_meta (method, lines 1125-1162, slice 1): CHUNK_ID = src/models/trainer.py#1125-1162#77a4dac0 — [[F:src/models/trainer.py#1125-1162#77a4dac0]].
- ModelTrainer.predict_meta (method, lines 1163-1198, slice 2): CHUNK_ID = src/models/trainer.py#1163-1198#77a4dac0 — [[F:src/models/trainer.py#1163-1198#77a4dac0]].
- ModelTrainer.save (method, lines 1204-1241, slice 1): CHUNK_ID = src/models/trainer.py#1204-1241#77a4dac0 — [[F:src/models/trainer.py#1204-1241#77a4dac0]].
- ModelTrainer.save (method, lines 1242-1262, slice 2): CHUNK_ID = src/models/trainer.py#1242-1262#77a4dac0 — [[F:src/models/trainer.py#1242-1262#77a4dac0]].
- ModelTrainer.load_direction (method, lines 1265-1278): CHUNK_ID = src/models/trainer.py#1265-1278#77a4dac0 — [[F:src/models/trainer.py#1265-1278#77a4dac0]].
- ModelTrainer.load_meta (method, lines 1281-1294): CHUNK_ID = src/models/trainer.py#1281-1294#77a4dac0 — [[F:src/models/trainer.py#1281-1294#77a4dac0]].
- ModelTrainer.cached_model_version (method, lines 1297-1299): CHUNK_ID = src/models/trainer.py#1297-1299#77a4dac0 — [[F:src/models/trainer.py#1297-1299#77a4dac0]].
- ModelTrainer.load_compatible_cached_models (method, lines 1301-1338, slice 1): CHUNK_ID = src/models/trainer.py#1301-1338#77a4dac0 — [[F:src/models/trainer.py#1301-1338#77a4dac0]].
- ModelTrainer.load_compatible_cached_models (method, lines 1339-1376, slice 2): CHUNK_ID = src/models/trainer.py#1339-1376#77a4dac0 — [[F:src/models/trainer.py#1339-1376#77a4dac0]].
- ModelTrainer.load_compatible_cached_models (method, lines 1377-1407, slice 3): CHUNK_ID = src/models/trainer.py#1377-1407#77a4dac0 — [[F:src/models/trainer.py#1377-1407#77a4dac0]].
- ModelTrainer._cached_provenance_matches (method, lines 1409-1433): CHUNK_ID = src/models/trainer.py#1409-1433#77a4dac0 — [[F:src/models/trainer.py#1409-1433#77a4dac0]].
- ModelTrainer._valid_provenance_timestamp (method, lines 1436-1441): CHUNK_ID = src/models/trainer.py#1436-1441#77a4dac0 — [[F:src/models/trainer.py#1436-1441#77a4dac0]].
- ModelTrainer._cached_training_result (method, lines 1443-1479): CHUNK_ID = src/models/trainer.py#1443-1479#77a4dac0 — [[F:src/models/trainer.py#1443-1479#77a4dac0]].
- ModelTrainer._run_cpcv (method, lines 1485-1522, slice 1): CHUNK_ID = src/models/trainer.py#1485-1522#77a4dac0 — [[F:src/models/trainer.py#1485-1522#77a4dac0]].
- ModelTrainer._run_cpcv (method, lines 1523-1560, slice 2): CHUNK_ID = src/models/trainer.py#1523-1560#77a4dac0 — [[F:src/models/trainer.py#1523-1560#77a4dac0]].
- ModelTrainer._run_cpcv (method, lines 1561-1598, slice 3): CHUNK_ID = src/models/trainer.py#1561-1598#77a4dac0 — [[F:src/models/trainer.py#1561-1598#77a4dac0]].
- ModelTrainer._run_cpcv (method, lines 1599-1607, slice 4): CHUNK_ID = src/models/trainer.py#1599-1607#77a4dac0 — [[F:src/models/trainer.py#1599-1607#77a4dac0]].
- ModelTrainer._check_live_gate (method, lines 1609-1639): CHUNK_ID = src/models/trainer.py#1609-1639#77a4dac0 — [[F:src/models/trainer.py#1609-1639#77a4dac0]].

## src/models/model_registry.py

SHA8 91ea9f0b; total lines 156.

- ShadowPrediction (class, lines 21-25): CHUNK_ID = src/models/model_registry.py#21-25#91ea9f0b — [[F:src/models/model_registry.py#21-25#91ea9f0b]].
- ShadowModelState (class, lines 29-34): CHUNK_ID = src/models/model_registry.py#29-34#91ea9f0b — [[F:src/models/model_registry.py#29-34#91ea9f0b]].
- ModelRegistry (class, lines 37-74, slice 1): CHUNK_ID = src/models/model_registry.py#37-74#91ea9f0b — [[F:src/models/model_registry.py#37-74#91ea9f0b]].
- ModelRegistry (class, lines 75-112, slice 2): CHUNK_ID = src/models/model_registry.py#75-112#91ea9f0b — [[F:src/models/model_registry.py#75-112#91ea9f0b]].
- ModelRegistry (class, lines 113-148, slice 3): CHUNK_ID = src/models/model_registry.py#113-148#91ea9f0b — [[F:src/models/model_registry.py#113-148#91ea9f0b]].
- ModelRegistry.__init__ (method, lines 45-50): CHUNK_ID = src/models/model_registry.py#45-50#91ea9f0b — [[F:src/models/model_registry.py#45-50#91ea9f0b]].
- ModelRegistry.set_live_model (method, lines 52-53): CHUNK_ID = src/models/model_registry.py#52-53#91ea9f0b — [[F:src/models/model_registry.py#52-53#91ea9f0b]].
- ModelRegistry.live_model_id (method, lines 56-57): CHUNK_ID = src/models/model_registry.py#56-57#91ea9f0b — [[F:src/models/model_registry.py#56-57#91ea9f0b]].
- ModelRegistry.register_shadow (method, lines 59-62): CHUNK_ID = src/models/model_registry.py#59-62#91ea9f0b — [[F:src/models/model_registry.py#59-62#91ea9f0b]].
- ModelRegistry.record_shadow_prediction (method, lines 64-71): CHUNK_ID = src/models/model_registry.py#64-71#91ea9f0b — [[F:src/models/model_registry.py#64-71#91ea9f0b]].
- ModelRegistry.record_live_prediction_for_comparison (method, lines 73-81): CHUNK_ID = src/models/model_registry.py#73-81#91ea9f0b — [[F:src/models/model_registry.py#73-81#91ea9f0b]].
- ModelRegistry._accuracy (method, lines 84-90): CHUNK_ID = src/models/model_registry.py#84-90#91ea9f0b — [[F:src/models/model_registry.py#84-90#91ea9f0b]].
- ModelRegistry.evaluate_shadow (method, lines 92-109): CHUNK_ID = src/models/model_registry.py#92-109#91ea9f0b — [[F:src/models/model_registry.py#92-109#91ea9f0b]].
- ModelRegistry.promote_shadow (method, lines 111-121): CHUNK_ID = src/models/model_registry.py#111-121#91ea9f0b — [[F:src/models/model_registry.py#111-121#91ea9f0b]].
- ModelRegistry.discard_shadow (method, lines 123-132): CHUNK_ID = src/models/model_registry.py#123-132#91ea9f0b — [[F:src/models/model_registry.py#123-132#91ea9f0b]].
- ModelRegistry.evaluation_count (method, lines 134-138): CHUNK_ID = src/models/model_registry.py#134-138#91ea9f0b — [[F:src/models/model_registry.py#134-138#91ea9f0b]].
- ModelRegistry.accuracies (method, lines 140-145): CHUNK_ID = src/models/model_registry.py#140-145#91ea9f0b — [[F:src/models/model_registry.py#140-145#91ea9f0b]].
- ModelRegistry.shadow_ids (method, lines 147-148): CHUNK_ID = src/models/model_registry.py#147-148#91ea9f0b — [[F:src/models/model_registry.py#147-148#91ea9f0b]].
- get_model_registry (function, lines 154-156): CHUNK_ID = src/models/model_registry.py#154-156#91ea9f0b — [[F:src/models/model_registry.py#154-156#91ea9f0b]].

## src/models/online_trainer.py

SHA8 6c961c51; total lines 366.

- OnlinePrediction (class, lines 75-82): CHUNK_ID = src/models/online_trainer.py#75-82#6c961c51 — [[F:src/models/online_trainer.py#75-82#6c961c51]].
- _OnlineModel (class, lines 86-111): CHUNK_ID = src/models/online_trainer.py#86-111#6c961c51 — [[F:src/models/online_trainer.py#86-111#6c961c51]].
- _OnlineModel.partial_fit (method, lines 94-97): CHUNK_ID = src/models/online_trainer.py#94-97#6c961c51 — [[F:src/models/online_trainer.py#94-97#6c961c51]].
- _OnlineModel.predict_proba (method, lines 99-102): CHUNK_ID = src/models/online_trainer.py#99-102#6c961c51 — [[F:src/models/online_trainer.py#99-102#6c961c51]].
- _OnlineModel.record_outcome (method, lines 104-105): CHUNK_ID = src/models/online_trainer.py#104-105#6c961c51 — [[F:src/models/online_trainer.py#104-105#6c961c51]].
- _OnlineModel.rolling_accuracy (method, lines 108-111): CHUNK_ID = src/models/online_trainer.py#108-111#6c961c51 — [[F:src/models/online_trainer.py#108-111#6c961c51]].
- OnlineTrainer (class, lines 119-156, slice 1): CHUNK_ID = src/models/online_trainer.py#119-156#6c961c51 — [[F:src/models/online_trainer.py#119-156#6c961c51]].
- OnlineTrainer (class, lines 157-194, slice 2): CHUNK_ID = src/models/online_trainer.py#157-194#6c961c51 — [[F:src/models/online_trainer.py#157-194#6c961c51]].
- OnlineTrainer (class, lines 195-232, slice 3): CHUNK_ID = src/models/online_trainer.py#195-232#6c961c51 — [[F:src/models/online_trainer.py#195-232#6c961c51]].
- OnlineTrainer (class, lines 233-270, slice 4): CHUNK_ID = src/models/online_trainer.py#233-270#6c961c51 — [[F:src/models/online_trainer.py#233-270#6c961c51]].
- OnlineTrainer (class, lines 271-308, slice 5): CHUNK_ID = src/models/online_trainer.py#271-308#6c961c51 — [[F:src/models/online_trainer.py#271-308#6c961c51]].
- OnlineTrainer (class, lines 309-346, slice 6): CHUNK_ID = src/models/online_trainer.py#309-346#6c961c51 — [[F:src/models/online_trainer.py#309-346#6c961c51]].
- OnlineTrainer (class, lines 347-366, slice 7): CHUNK_ID = src/models/online_trainer.py#347-366#6c961c51 — [[F:src/models/online_trainer.py#347-366#6c961c51]].
- OnlineTrainer.__init__ (method, lines 142-149): CHUNK_ID = src/models/online_trainer.py#142-149#6c961c51 — [[F:src/models/online_trainer.py#142-149#6c961c51]].
- OnlineTrainer._make_dir_model (method, lines 156-165): CHUNK_ID = src/models/online_trainer.py#156-165#6c961c51 — [[F:src/models/online_trainer.py#156-165#6c961c51]].
- OnlineTrainer._make_meta_model (method, lines 168-177): CHUNK_ID = src/models/online_trainer.py#168-177#6c961c51 — [[F:src/models/online_trainer.py#168-177#6c961c51]].
- OnlineTrainer.learn_direction (method, lines 183-205): CHUNK_ID = src/models/online_trainer.py#183-205#6c961c51 — [[F:src/models/online_trainer.py#183-205#6c961c51]].
- OnlineTrainer.learn_meta (method, lines 207-232): CHUNK_ID = src/models/online_trainer.py#207-232#6c961c51 — [[F:src/models/online_trainer.py#207-232#6c961c51]].
- OnlineTrainer.blend (method, lines 238-275, slice 1): CHUNK_ID = src/models/online_trainer.py#238-275#6c961c51 — [[F:src/models/online_trainer.py#238-275#6c961c51]].
- OnlineTrainer.blend (method, lines 276-288, slice 2): CHUNK_ID = src/models/online_trainer.py#276-288#6c961c51 — [[F:src/models/online_trainer.py#276-288#6c961c51]].
- OnlineTrainer.accuracy_report (method, lines 294-301): CHUNK_ID = src/models/online_trainer.py#294-301#6c961c51 — [[F:src/models/online_trainer.py#294-301#6c961c51]].
- OnlineTrainer.save (method, lines 307-323): CHUNK_ID = src/models/online_trainer.py#307-323#6c961c51 — [[F:src/models/online_trainer.py#307-323#6c961c51]].
- OnlineTrainer._try_load (method, lines 325-346): CHUNK_ID = src/models/online_trainer.py#325-346#6c961c51 — [[F:src/models/online_trainer.py#325-346#6c961c51]].
- OnlineTrainer.reset (method, lines 352-366): CHUNK_ID = src/models/online_trainer.py#352-366#6c961c51 — [[F:src/models/online_trainer.py#352-366#6c961c51]].

## src/strategies/bootstrap.py

SHA8 7c5e2f94; total lines 205.

- StrategySpec (class, lines 60-70): CHUNK_ID = src/strategies/bootstrap.py#60-70#7c5e2f94 — [[F:src/strategies/bootstrap.py#60-70#7c5e2f94]].
- _build_options_carry (function, lines 73-83): CHUNK_ID = src/strategies/bootstrap.py#73-83#7c5e2f94 — [[F:src/strategies/bootstrap.py#73-83#7c5e2f94]].
- enabled_specs (function, lines 142-144): CHUNK_ID = src/strategies/bootstrap.py#142-144#7c5e2f94 — [[F:src/strategies/bootstrap.py#142-144#7c5e2f94]].
- total_enabled_fraction (function, lines 147-155): CHUNK_ID = src/strategies/bootstrap.py#147-155#7c5e2f94 — [[F:src/strategies/bootstrap.py#147-155#7c5e2f94]].
- register_default_strategies (function, lines 158-195, slice 1): CHUNK_ID = src/strategies/bootstrap.py#158-195#7c5e2f94 — [[F:src/strategies/bootstrap.py#158-195#7c5e2f94]].
- register_default_strategies (function, lines 196-205, slice 2): CHUNK_ID = src/strategies/bootstrap.py#196-205#7c5e2f94 — [[F:src/strategies/bootstrap.py#196-205#7c5e2f94]].

## src/strategies/registry.py

SHA8 5ef08896; total lines 143.

- Signal (class, lines 41-62): CHUNK_ID = src/strategies/registry.py#41-62#5ef08896 — [[F:src/strategies/registry.py#41-62#5ef08896]].
- Signal.__post_init__ (method, lines 56-62): CHUNK_ID = src/strategies/registry.py#56-62#5ef08896 — [[F:src/strategies/registry.py#56-62#5ef08896]].
- StrategyProtocol (class, lines 66-79): CHUNK_ID = src/strategies/registry.py#66-79#5ef08896 — [[F:src/strategies/registry.py#66-79#5ef08896]].
- StrategyProtocol.generate_signal (method, lines 71-74): CHUNK_ID = src/strategies/registry.py#71-74#5ef08896 — [[F:src/strategies/registry.py#71-74#5ef08896]].
- StrategyProtocol.required_capital_fraction (method, lines 76-79): CHUNK_ID = src/strategies/registry.py#76-79#5ef08896 — [[F:src/strategies/registry.py#76-79#5ef08896]].
- DuplicateStrategyError (class, lines 82-83): CHUNK_ID = src/strategies/registry.py#82-83#5ef08896 — [[F:src/strategies/registry.py#82-83#5ef08896]].
- StrategyRegistry (class, lines 86-130): CHUNK_ID = src/strategies/registry.py#86-130#5ef08896 — [[F:src/strategies/registry.py#86-130#5ef08896]].
- StrategyRegistry.__init__ (method, lines 95-96): CHUNK_ID = src/strategies/registry.py#95-96#5ef08896 — [[F:src/strategies/registry.py#95-96#5ef08896]].
- StrategyRegistry.register (method, lines 98-115): CHUNK_ID = src/strategies/registry.py#98-115#5ef08896 — [[F:src/strategies/registry.py#98-115#5ef08896]].
- StrategyRegistry.unregister (method, lines 117-118): CHUNK_ID = src/strategies/registry.py#117-118#5ef08896 — [[F:src/strategies/registry.py#117-118#5ef08896]].
- StrategyRegistry.get (method, lines 120-121): CHUNK_ID = src/strategies/registry.py#120-121#5ef08896 — [[F:src/strategies/registry.py#120-121#5ef08896]].
- StrategyRegistry.all (method, lines 123-124): CHUNK_ID = src/strategies/registry.py#123-124#5ef08896 — [[F:src/strategies/registry.py#123-124#5ef08896]].
- StrategyRegistry.__len__ (method, lines 126-127): CHUNK_ID = src/strategies/registry.py#126-127#5ef08896 — [[F:src/strategies/registry.py#126-127#5ef08896]].
- StrategyRegistry.__contains__ (method, lines 129-130): CHUNK_ID = src/strategies/registry.py#129-130#5ef08896 — [[F:src/strategies/registry.py#129-130#5ef08896]].
- get_default_registry (function, lines 134-143): CHUNK_ID = src/strategies/registry.py#134-143#5ef08896 — [[F:src/strategies/registry.py#134-143#5ef08896]].

## src/tuning/scheduler.py

SHA8 3e03669b; total lines 661.

- _shannon_entropy (function, lines 106-117): CHUNK_ID = src/tuning/scheduler.py#106-117#3e03669b — [[F:src/tuning/scheduler.py#106-117#3e03669b]].
- AutoTuningScheduler (class, lines 120-157, slice 1): CHUNK_ID = src/tuning/scheduler.py#120-157#3e03669b — [[F:src/tuning/scheduler.py#120-157#3e03669b]].
- AutoTuningScheduler (class, lines 158-195, slice 2): CHUNK_ID = src/tuning/scheduler.py#158-195#3e03669b — [[F:src/tuning/scheduler.py#158-195#3e03669b]].
- AutoTuningScheduler (class, lines 196-233, slice 3): CHUNK_ID = src/tuning/scheduler.py#196-233#3e03669b — [[F:src/tuning/scheduler.py#196-233#3e03669b]].
- AutoTuningScheduler (class, lines 234-271, slice 4): CHUNK_ID = src/tuning/scheduler.py#234-271#3e03669b — [[F:src/tuning/scheduler.py#234-271#3e03669b]].
- AutoTuningScheduler (class, lines 272-309, slice 5): CHUNK_ID = src/tuning/scheduler.py#272-309#3e03669b — [[F:src/tuning/scheduler.py#272-309#3e03669b]].
- AutoTuningScheduler (class, lines 310-347, slice 6): CHUNK_ID = src/tuning/scheduler.py#310-347#3e03669b — [[F:src/tuning/scheduler.py#310-347#3e03669b]].
- AutoTuningScheduler (class, lines 348-385, slice 7): CHUNK_ID = src/tuning/scheduler.py#348-385#3e03669b — [[F:src/tuning/scheduler.py#348-385#3e03669b]].
- AutoTuningScheduler (class, lines 386-423, slice 8): CHUNK_ID = src/tuning/scheduler.py#386-423#3e03669b — [[F:src/tuning/scheduler.py#386-423#3e03669b]].
- AutoTuningScheduler (class, lines 424-461, slice 9): CHUNK_ID = src/tuning/scheduler.py#424-461#3e03669b — [[F:src/tuning/scheduler.py#424-461#3e03669b]].
- AutoTuningScheduler (class, lines 462-499, slice 10): CHUNK_ID = src/tuning/scheduler.py#462-499#3e03669b — [[F:src/tuning/scheduler.py#462-499#3e03669b]].
- AutoTuningScheduler (class, lines 500-537, slice 11): CHUNK_ID = src/tuning/scheduler.py#500-537#3e03669b — [[F:src/tuning/scheduler.py#500-537#3e03669b]].
- AutoTuningScheduler (class, lines 538-575, slice 12): CHUNK_ID = src/tuning/scheduler.py#538-575#3e03669b — [[F:src/tuning/scheduler.py#538-575#3e03669b]].
- AutoTuningScheduler (class, lines 576-613, slice 13): CHUNK_ID = src/tuning/scheduler.py#576-613#3e03669b — [[F:src/tuning/scheduler.py#576-613#3e03669b]].
- AutoTuningScheduler (class, lines 614-651, slice 14): CHUNK_ID = src/tuning/scheduler.py#614-651#3e03669b — [[F:src/tuning/scheduler.py#614-651#3e03669b]].
- AutoTuningScheduler (class, lines 652-661, slice 15): CHUNK_ID = src/tuning/scheduler.py#652-661#3e03669b — [[F:src/tuning/scheduler.py#652-661#3e03669b]].
- AutoTuningScheduler.__init__ (method, lines 125-159): CHUNK_ID = src/tuning/scheduler.py#125-159#3e03669b — [[F:src/tuning/scheduler.py#125-159#3e03669b]].
- AutoTuningScheduler.start (method, lines 161-192): CHUNK_ID = src/tuning/scheduler.py#161-192#3e03669b — [[F:src/tuning/scheduler.py#161-192#3e03669b]].
- AutoTuningScheduler.stop (method, lines 194-197): CHUNK_ID = src/tuning/scheduler.py#194-197#3e03669b — [[F:src/tuning/scheduler.py#194-197#3e03669b]].
- AutoTuningScheduler._loop (method, lines 199-221): CHUNK_ID = src/tuning/scheduler.py#199-221#3e03669b — [[F:src/tuning/scheduler.py#199-221#3e03669b]].
- AutoTuningScheduler._check_redteam_due (method, lines 223-240): CHUNK_ID = src/tuning/scheduler.py#223-240#3e03669b — [[F:src/tuning/scheduler.py#223-240#3e03669b]].
- AutoTuningScheduler._attempt_all (method, lines 242-279, slice 1): CHUNK_ID = src/tuning/scheduler.py#242-279#3e03669b — [[F:src/tuning/scheduler.py#242-279#3e03669b]].
- AutoTuningScheduler._attempt_all (method, lines 280-317, slice 2): CHUNK_ID = src/tuning/scheduler.py#280-317#3e03669b — [[F:src/tuning/scheduler.py#280-317#3e03669b]].
- AutoTuningScheduler._attempt_all (method, lines 318-355, slice 3): CHUNK_ID = src/tuning/scheduler.py#318-355#3e03669b — [[F:src/tuning/scheduler.py#318-355#3e03669b]].
- AutoTuningScheduler._attempt_all (method, lines 356-393, slice 4): CHUNK_ID = src/tuning/scheduler.py#356-393#3e03669b — [[F:src/tuning/scheduler.py#356-393#3e03669b]].
- AutoTuningScheduler._attempt_all (method, lines 394-431, slice 5): CHUNK_ID = src/tuning/scheduler.py#394-431#3e03669b — [[F:src/tuning/scheduler.py#394-431#3e03669b]].
- AutoTuningScheduler._attempt_all (method, lines 432-469, slice 6): CHUNK_ID = src/tuning/scheduler.py#432-469#3e03669b — [[F:src/tuning/scheduler.py#432-469#3e03669b]].
- AutoTuningScheduler._attempt_all (method, lines 470-507, slice 7): CHUNK_ID = src/tuning/scheduler.py#470-507#3e03669b — [[F:src/tuning/scheduler.py#470-507#3e03669b]].
- AutoTuningScheduler._attempt_all (method, lines 508-526, slice 8): CHUNK_ID = src/tuning/scheduler.py#508-526#3e03669b — [[F:src/tuning/scheduler.py#508-526#3e03669b]].
- AutoTuningScheduler._maybe_retrain_e09 (method, lines 528-546): CHUNK_ID = src/tuning/scheduler.py#528-546#3e03669b — [[F:src/tuning/scheduler.py#528-546#3e03669b]].
- AutoTuningScheduler._load_direction_model (method, lines 548-554): CHUNK_ID = src/tuning/scheduler.py#548-554#3e03669b — [[F:src/tuning/scheduler.py#548-554#3e03669b]].
- AutoTuningScheduler._build_feature_bars_df (method, lines 556-574): CHUNK_ID = src/tuning/scheduler.py#556-574#3e03669b — [[F:src/tuning/scheduler.py#556-574#3e03669b]].
- AutoTuningScheduler._closed_trade_count (method, lines 576-594): CHUNK_ID = src/tuning/scheduler.py#576-594#3e03669b — [[F:src/tuning/scheduler.py#576-594#3e03669b]].
- AutoTuningScheduler._build_slippage_samples (method, lines 596-630): CHUNK_ID = src/tuning/scheduler.py#596-630#3e03669b — [[F:src/tuning/scheduler.py#596-630#3e03669b]].
- AutoTuningScheduler._build_ensemble_blend_samples (method, lines 632-638): CHUNK_ID = src/tuning/scheduler.py#632-638#3e03669b — [[F:src/tuning/scheduler.py#632-638#3e03669b]].
- AutoTuningScheduler._build_trade_samples (method, lines 640-661): CHUNK_ID = src/tuning/scheduler.py#640-661#3e03669b — [[F:src/tuning/scheduler.py#640-661#3e03669b]].

## src/runtime/contracts.py

SHA8 1cd648fb; total lines 507.

- RuntimeContractError (class, lines 35-36): CHUNK_ID = src/runtime/contracts.py#35-36#1cd648fb — [[F:src/runtime/contracts.py#35-36#1cd648fb]].
- InvalidTransitionError (class, lines 39-45): CHUNK_ID = src/runtime/contracts.py#39-45#1cd648fb — [[F:src/runtime/contracts.py#39-45#1cd648fb]].
- InvalidTransitionError.__init__ (method, lines 42-45): CHUNK_ID = src/runtime/contracts.py#42-45#1cd648fb — [[F:src/runtime/contracts.py#42-45#1cd648fb]].
- UnsupportedActionError (class, lines 48-54): CHUNK_ID = src/runtime/contracts.py#48-54#1cd648fb — [[F:src/runtime/contracts.py#48-54#1cd648fb]].
- UnsupportedActionError.__init__ (method, lines 51-54): CHUNK_ID = src/runtime/contracts.py#51-54#1cd648fb — [[F:src/runtime/contracts.py#51-54#1cd648fb]].
- ComponentType (class, lines 57-66): CHUNK_ID = src/runtime/contracts.py#57-66#1cd648fb — [[F:src/runtime/contracts.py#57-66#1cd648fb]].
- LifecycleState (class, lines 69-79): CHUNK_ID = src/runtime/contracts.py#69-79#1cd648fb — [[F:src/runtime/contracts.py#69-79#1cd648fb]].
- LifecycleAction (class, lines 82-96): CHUNK_ID = src/runtime/contracts.py#82-96#1cd648fb — [[F:src/runtime/contracts.py#82-96#1cd648fb]].
- ChangeClass (class, lines 99-108): CHUNK_ID = src/runtime/contracts.py#99-108#1cd648fb — [[F:src/runtime/contracts.py#99-108#1cd648fb]].
- HealthState (class, lines 114-118): CHUNK_ID = src/runtime/contracts.py#114-118#1cd648fb — [[F:src/runtime/contracts.py#114-118#1cd648fb]].
- _table (function, lines 134-161): CHUNK_ID = src/runtime/contracts.py#134-161#1cd648fb — [[F:src/runtime/contracts.py#134-161#1cd648fb]].
- _name (function, lines 175-176): CHUNK_ID = src/runtime/contracts.py#175-176#1cd648fb — [[F:src/runtime/contracts.py#175-176#1cd648fb]].
- CapabilitySet (class, lines 180-224): CHUNK_ID = src/runtime/contracts.py#180-224#1cd648fb — [[F:src/runtime/contracts.py#180-224#1cd648fb]].
- CapabilitySet.__post_init__ (method, lines 193-207): CHUNK_ID = src/runtime/contracts.py#193-207#1cd648fb — [[F:src/runtime/contracts.py#193-207#1cd648fb]].
- CapabilitySet.supports_reload (method, lines 210-211): CHUNK_ID = src/runtime/contracts.py#210-211#1cd648fb — [[F:src/runtime/contracts.py#210-211#1cd648fb]].
- CapabilitySet.supports_pause (method, lines 214-215): CHUNK_ID = src/runtime/contracts.py#214-215#1cd648fb — [[F:src/runtime/contracts.py#214-215#1cd648fb]].
- CapabilitySet.to_dict (method, lines 217-224): CHUNK_ID = src/runtime/contracts.py#217-224#1cd648fb — [[F:src/runtime/contracts.py#217-224#1cd648fb]].
- next_state (function, lines 230-252): CHUNK_ID = src/runtime/contracts.py#230-252#1cd648fb — [[F:src/runtime/contracts.py#230-252#1cd648fb]].
- make_component_id (function, lines 258-262): CHUNK_ID = src/runtime/contracts.py#258-262#1cd648fb — [[F:src/runtime/contracts.py#258-262#1cd648fb]].
- _canonical_json (function, lines 265-269): CHUNK_ID = src/runtime/contracts.py#265-269#1cd648fb — [[F:src/runtime/contracts.py#265-269#1cd648fb]].
- ComponentVersion (class, lines 273-310, slice 1): CHUNK_ID = src/runtime/contracts.py#273-310#1cd648fb — [[F:src/runtime/contracts.py#273-310#1cd648fb]].
- ComponentVersion (class, lines 311-323, slice 2): CHUNK_ID = src/runtime/contracts.py#311-323#1cd648fb — [[F:src/runtime/contracts.py#311-323#1cd648fb]].
- ComponentVersion.__post_init__ (method, lines 284-294): CHUNK_ID = src/runtime/contracts.py#284-294#1cd648fb — [[F:src/runtime/contracts.py#284-294#1cd648fb]].
- ComponentVersion.create (method, lines 297-303): CHUNK_ID = src/runtime/contracts.py#297-303#1cd648fb — [[F:src/runtime/contracts.py#297-303#1cd648fb]].
- ComponentVersion.configuration (method, lines 306-308): CHUNK_ID = src/runtime/contracts.py#306-308#1cd648fb — [[F:src/runtime/contracts.py#306-308#1cd648fb]].
- ComponentVersion.fingerprint (method, lines 311-315): CHUNK_ID = src/runtime/contracts.py#311-315#1cd648fb — [[F:src/runtime/contracts.py#311-315#1cd648fb]].
- ComponentVersion.to_dict (method, lines 317-323): CHUNK_ID = src/runtime/contracts.py#317-323#1cd648fb — [[F:src/runtime/contracts.py#317-323#1cd648fb]].
- DependencyDescriptor (class, lines 327-339): CHUNK_ID = src/runtime/contracts.py#327-339#1cd648fb — [[F:src/runtime/contracts.py#327-339#1cd648fb]].
- DependencyDescriptor.to_dict (method, lines 334-339): CHUNK_ID = src/runtime/contracts.py#334-339#1cd648fb — [[F:src/runtime/contracts.py#334-339#1cd648fb]].
- ComponentSpec (class, lines 343-380): CHUNK_ID = src/runtime/contracts.py#343-380#1cd648fb — [[F:src/runtime/contracts.py#343-380#1cd648fb]].
- ComponentSpec.__post_init__ (method, lines 351-370): CHUNK_ID = src/runtime/contracts.py#351-370#1cd648fb — [[F:src/runtime/contracts.py#351-370#1cd648fb]].
- ComponentSpec.with_version (method, lines 372-380): CHUNK_ID = src/runtime/contracts.py#372-380#1cd648fb — [[F:src/runtime/contracts.py#372-380#1cd648fb]].
- DesiredState (class, lines 384-408): CHUNK_ID = src/runtime/contracts.py#384-408#1cd648fb — [[F:src/runtime/contracts.py#384-408#1cd648fb]].
- DesiredState.__post_init__ (method, lines 391-399): CHUNK_ID = src/runtime/contracts.py#391-399#1cd648fb — [[F:src/runtime/contracts.py#391-399#1cd648fb]].
- DesiredState.to_dict (method, lines 401-408): CHUNK_ID = src/runtime/contracts.py#401-408#1cd648fb — [[F:src/runtime/contracts.py#401-408#1cd648fb]].
- HealthReport (class, lines 412-422): CHUNK_ID = src/runtime/contracts.py#412-422#1cd648fb — [[F:src/runtime/contracts.py#412-422#1cd648fb]].
- HealthReport.to_dict (method, lines 417-422): CHUNK_ID = src/runtime/contracts.py#417-422#1cd648fb — [[F:src/runtime/contracts.py#417-422#1cd648fb]].
- TransitionRecord (class, lines 426-455): CHUNK_ID = src/runtime/contracts.py#426-455#1cd648fb — [[F:src/runtime/contracts.py#426-455#1cd648fb]].
- TransitionRecord.to_dict (method, lines 442-455): CHUNK_ID = src/runtime/contracts.py#442-455#1cd648fb — [[F:src/runtime/contracts.py#442-455#1cd648fb]].
- ComponentRecord (class, lines 459-496, slice 1): CHUNK_ID = src/runtime/contracts.py#459-496#1cd648fb — [[F:src/runtime/contracts.py#459-496#1cd648fb]].
- ComponentRecord (class, lines 497-507, slice 2): CHUNK_ID = src/runtime/contracts.py#497-507#1cd648fb — [[F:src/runtime/contracts.py#497-507#1cd648fb]].
- ComponentRecord.component_id (method, lines 475-476): CHUNK_ID = src/runtime/contracts.py#475-476#1cd648fb — [[F:src/runtime/contracts.py#475-476#1cd648fb]].
- ComponentRecord.version (method, lines 479-480): CHUNK_ID = src/runtime/contracts.py#479-480#1cd648fb — [[F:src/runtime/contracts.py#479-480#1cd648fb]].
- ComponentRecord.to_dict (method, lines 482-507): CHUNK_ID = src/runtime/contracts.py#482-507#1cd648fb — [[F:src/runtime/contracts.py#482-507#1cd648fb]].

## src/runtime/registry.py

SHA8 c2307736; total lines 537.

- DuplicateComponentError (class, lines 59-60): CHUNK_ID = src/runtime/registry.py#59-60#c2307736 — [[F:src/runtime/registry.py#59-60#c2307736]].
- UnknownComponentError (class, lines 63-64): CHUNK_ID = src/runtime/registry.py#63-64#c2307736 — [[F:src/runtime/registry.py#63-64#c2307736]].
- _utc_now (function, lines 67-68): CHUNK_ID = src/runtime/registry.py#67-68#c2307736 — [[F:src/runtime/registry.py#67-68#c2307736]].
- RuntimeRegistry (class, lines 71-108, slice 1): CHUNK_ID = src/runtime/registry.py#71-108#c2307736 — [[F:src/runtime/registry.py#71-108#c2307736]].
- RuntimeRegistry (class, lines 109-146, slice 2): CHUNK_ID = src/runtime/registry.py#109-146#c2307736 — [[F:src/runtime/registry.py#109-146#c2307736]].
- RuntimeRegistry (class, lines 147-184, slice 3): CHUNK_ID = src/runtime/registry.py#147-184#c2307736 — [[F:src/runtime/registry.py#147-184#c2307736]].
- RuntimeRegistry (class, lines 185-222, slice 4): CHUNK_ID = src/runtime/registry.py#185-222#c2307736 — [[F:src/runtime/registry.py#185-222#c2307736]].
- RuntimeRegistry (class, lines 223-260, slice 5): CHUNK_ID = src/runtime/registry.py#223-260#c2307736 — [[F:src/runtime/registry.py#223-260#c2307736]].
- RuntimeRegistry (class, lines 261-298, slice 6): CHUNK_ID = src/runtime/registry.py#261-298#c2307736 — [[F:src/runtime/registry.py#261-298#c2307736]].
- RuntimeRegistry (class, lines 299-336, slice 7): CHUNK_ID = src/runtime/registry.py#299-336#c2307736 — [[F:src/runtime/registry.py#299-336#c2307736]].
- RuntimeRegistry (class, lines 337-374, slice 8): CHUNK_ID = src/runtime/registry.py#337-374#c2307736 — [[F:src/runtime/registry.py#337-374#c2307736]].
- RuntimeRegistry (class, lines 375-412, slice 9): CHUNK_ID = src/runtime/registry.py#375-412#c2307736 — [[F:src/runtime/registry.py#375-412#c2307736]].
- RuntimeRegistry (class, lines 413-450, slice 10): CHUNK_ID = src/runtime/registry.py#413-450#c2307736 — [[F:src/runtime/registry.py#413-450#c2307736]].
- RuntimeRegistry (class, lines 451-488, slice 11): CHUNK_ID = src/runtime/registry.py#451-488#c2307736 — [[F:src/runtime/registry.py#451-488#c2307736]].
- RuntimeRegistry (class, lines 489-526, slice 12): CHUNK_ID = src/runtime/registry.py#489-526#c2307736 — [[F:src/runtime/registry.py#489-526#c2307736]].
- RuntimeRegistry (class, lines 527-537, slice 13): CHUNK_ID = src/runtime/registry.py#527-537#c2307736 — [[F:src/runtime/registry.py#527-537#c2307736]].
- RuntimeRegistry.__init__ (method, lines 72-88): CHUNK_ID = src/runtime/registry.py#72-88#c2307736 — [[F:src/runtime/registry.py#72-88#c2307736]].
- RuntimeRegistry.register (method, lines 92-133): CHUNK_ID = src/runtime/registry.py#92-133#c2307736 — [[F:src/runtime/registry.py#92-133#c2307736]].
- RuntimeRegistry.register_all (method, lines 135-147): CHUNK_ID = src/runtime/registry.py#135-147#c2307736 — [[F:src/runtime/registry.py#135-147#c2307736]].
- RuntimeRegistry.get (method, lines 151-156): CHUNK_ID = src/runtime/registry.py#151-156#c2307736 — [[F:src/runtime/registry.py#151-156#c2307736]].
- RuntimeRegistry.find (method, lines 158-160): CHUNK_ID = src/runtime/registry.py#158-160#c2307736 — [[F:src/runtime/registry.py#158-160#c2307736]].
- RuntimeRegistry.components (method, lines 162-170): CHUNK_ID = src/runtime/registry.py#162-170#c2307736 — [[F:src/runtime/registry.py#162-170#c2307736]].
- RuntimeRegistry.dependents (method, lines 172-178): CHUNK_ID = src/runtime/registry.py#172-178#c2307736 — [[F:src/runtime/registry.py#172-178#c2307736]].
- RuntimeRegistry.history (method, lines 180-184): CHUNK_ID = src/runtime/registry.py#180-184#c2307736 — [[F:src/runtime/registry.py#180-184#c2307736]].
- RuntimeRegistry.versions (method, lines 186-190): CHUNK_ID = src/runtime/registry.py#186-190#c2307736 — [[F:src/runtime/registry.py#186-190#c2307736]].
- RuntimeRegistry.snapshot (method, lines 192-194): CHUNK_ID = src/runtime/registry.py#192-194#c2307736 — [[F:src/runtime/registry.py#192-194#c2307736]].
- RuntimeRegistry.add_transition_listener (method, lines 198-201): CHUNK_ID = src/runtime/registry.py#198-201#c2307736 — [[F:src/runtime/registry.py#198-201#c2307736]].
- RuntimeRegistry._remember (method, lines 203-213): CHUNK_ID = src/runtime/registry.py#203-213#c2307736 — [[F:src/runtime/registry.py#203-213#c2307736]].
- RuntimeRegistry._prune_versions (method, lines 215-229): CHUNK_ID = src/runtime/registry.py#215-229#c2307736 — [[F:src/runtime/registry.py#215-229#c2307736]].
- RuntimeRegistry.add_desired_listener (method, lines 231-234): CHUNK_ID = src/runtime/registry.py#231-234#c2307736 — [[F:src/runtime/registry.py#231-234#c2307736]].
- RuntimeRegistry.set_desired (method, lines 236-259): CHUNK_ID = src/runtime/registry.py#236-259#c2307736 — [[F:src/runtime/registry.py#236-259#c2307736]].
- RuntimeRegistry.record_health (method, lines 261-263): CHUNK_ID = src/runtime/registry.py#261-263#c2307736 — [[F:src/runtime/registry.py#261-263#c2307736]].
- RuntimeRegistry.apply (method, lines 265-305): CHUNK_ID = src/runtime/registry.py#265-305#c2307736 — [[F:src/runtime/registry.py#265-305#c2307736]].
- RuntimeRegistry.preview (method, lines 307-320): CHUNK_ID = src/runtime/registry.py#307-320#c2307736 — [[F:src/runtime/registry.py#307-320#c2307736]].
- RuntimeRegistry._plan (method, lines 322-356): CHUNK_ID = src/runtime/registry.py#322-356#c2307736 — [[F:src/runtime/registry.py#322-356#c2307736]].
- RuntimeRegistry.observe (method, lines 358-391): CHUNK_ID = src/runtime/registry.py#358-391#c2307736 — [[F:src/runtime/registry.py#358-391#c2307736]].
- RuntimeRegistry.mark_failed (method, lines 393-426): CHUNK_ID = src/runtime/registry.py#393-426#c2307736 — [[F:src/runtime/registry.py#393-426#c2307736]].
- RuntimeRegistry.resync (method, lines 428-465, slice 1): CHUNK_ID = src/runtime/registry.py#428-465#c2307736 — [[F:src/runtime/registry.py#428-465#c2307736]].
- RuntimeRegistry.resync (method, lines 466-484, slice 2): CHUNK_ID = src/runtime/registry.py#466-484#c2307736 — [[F:src/runtime/registry.py#466-484#c2307736]].
- RuntimeRegistry.retire (method, lines 486-513): CHUNK_ID = src/runtime/registry.py#486-513#c2307736 — [[F:src/runtime/registry.py#486-513#c2307736]].
- RuntimeRegistry.note_restart (method, lines 515-518): CHUNK_ID = src/runtime/registry.py#515-518#c2307736 — [[F:src/runtime/registry.py#515-518#c2307736]].
- RuntimeRegistry._store (method, lines 520-537): CHUNK_ID = src/runtime/registry.py#520-537#c2307736 — [[F:src/runtime/registry.py#520-537#c2307736]].

## src/runtime/changes.py

SHA8 7bce4a55; total lines 788.

- ActorKind (class, lines 68-71): CHUNK_ID = src/runtime/changes.py#68-71#7bce4a55 — [[F:src/runtime/changes.py#68-71#7bce4a55]].
- Actor (class, lines 75-81): CHUNK_ID = src/runtime/changes.py#75-81#7bce4a55 — [[F:src/runtime/changes.py#75-81#7bce4a55]].
- Actor.to_dict (method, lines 80-81): CHUNK_ID = src/runtime/changes.py#80-81#7bce4a55 — [[F:src/runtime/changes.py#80-81#7bce4a55]].
- ChangeStatus (class, lines 88-98): CHUNK_ID = src/runtime/changes.py#88-98#7bce4a55 — [[F:src/runtime/changes.py#88-98#7bce4a55]].
- ChangeError (class, lines 136-137): CHUNK_ID = src/runtime/changes.py#136-137#7bce4a55 — [[F:src/runtime/changes.py#136-137#7bce4a55]].
- RuntimeLifecycleUnavailableError (class, lines 140-141): CHUNK_ID = src/runtime/changes.py#140-141#7bce4a55 — [[F:src/runtime/changes.py#140-141#7bce4a55]].
- UnauthorizedError (class, lines 144-145): CHUNK_ID = src/runtime/changes.py#144-145#7bce4a55 — [[F:src/runtime/changes.py#144-145#7bce4a55]].
- ChangeRequest (class, lines 149-167): CHUNK_ID = src/runtime/changes.py#149-167#7bce4a55 — [[F:src/runtime/changes.py#149-167#7bce4a55]].
- ChangeRequest.to_dict (method, lines 158-167): CHUNK_ID = src/runtime/changes.py#158-167#7bce4a55 — [[F:src/runtime/changes.py#158-167#7bce4a55]].
- StageResult (class, lines 171-176): CHUNK_ID = src/runtime/changes.py#171-176#7bce4a55 — [[F:src/runtime/changes.py#171-176#7bce4a55]].
- ChangeRecord (class, lines 180-217): CHUNK_ID = src/runtime/changes.py#180-217#7bce4a55 — [[F:src/runtime/changes.py#180-217#7bce4a55]].
- ChangeRecord.change_id (method, lines 196-197): CHUNK_ID = src/runtime/changes.py#196-197#7bce4a55 — [[F:src/runtime/changes.py#196-197#7bce4a55]].
- ChangeRecord.to_dict (method, lines 199-217): CHUNK_ID = src/runtime/changes.py#199-217#7bce4a55 — [[F:src/runtime/changes.py#199-217#7bce4a55]].
- AuditEntry (class, lines 221-237): CHUNK_ID = src/runtime/changes.py#221-237#7bce4a55 — [[F:src/runtime/changes.py#221-237#7bce4a55]].
- AuditEntry.to_dict (method, lines 229-237): CHUNK_ID = src/runtime/changes.py#229-237#7bce4a55 — [[F:src/runtime/changes.py#229-237#7bce4a55]].
- _utc_now (function, lines 243-244): CHUNK_ID = src/runtime/changes.py#243-244#7bce4a55 — [[F:src/runtime/changes.py#243-244#7bce4a55]].
- ChangeManager (class, lines 256-293, slice 1): CHUNK_ID = src/runtime/changes.py#256-293#7bce4a55 — [[F:src/runtime/changes.py#256-293#7bce4a55]].
- ChangeManager (class, lines 294-331, slice 2): CHUNK_ID = src/runtime/changes.py#294-331#7bce4a55 — [[F:src/runtime/changes.py#294-331#7bce4a55]].
- ChangeManager (class, lines 332-369, slice 3): CHUNK_ID = src/runtime/changes.py#332-369#7bce4a55 — [[F:src/runtime/changes.py#332-369#7bce4a55]].
- ChangeManager (class, lines 370-407, slice 4): CHUNK_ID = src/runtime/changes.py#370-407#7bce4a55 — [[F:src/runtime/changes.py#370-407#7bce4a55]].
- ChangeManager (class, lines 408-445, slice 5): CHUNK_ID = src/runtime/changes.py#408-445#7bce4a55 — [[F:src/runtime/changes.py#408-445#7bce4a55]].
- ChangeManager (class, lines 446-483, slice 6): CHUNK_ID = src/runtime/changes.py#446-483#7bce4a55 — [[F:src/runtime/changes.py#446-483#7bce4a55]].
- ChangeManager (class, lines 484-521, slice 7): CHUNK_ID = src/runtime/changes.py#484-521#7bce4a55 — [[F:src/runtime/changes.py#484-521#7bce4a55]].
- ChangeManager (class, lines 522-559, slice 8): CHUNK_ID = src/runtime/changes.py#522-559#7bce4a55 — [[F:src/runtime/changes.py#522-559#7bce4a55]].
- ChangeManager (class, lines 560-597, slice 9): CHUNK_ID = src/runtime/changes.py#560-597#7bce4a55 — [[F:src/runtime/changes.py#560-597#7bce4a55]].
- ChangeManager (class, lines 598-635, slice 10): CHUNK_ID = src/runtime/changes.py#598-635#7bce4a55 — [[F:src/runtime/changes.py#598-635#7bce4a55]].
- ChangeManager (class, lines 636-673, slice 11): CHUNK_ID = src/runtime/changes.py#636-673#7bce4a55 — [[F:src/runtime/changes.py#636-673#7bce4a55]].
- ChangeManager (class, lines 674-711, slice 12): CHUNK_ID = src/runtime/changes.py#674-711#7bce4a55 — [[F:src/runtime/changes.py#674-711#7bce4a55]].
- ChangeManager (class, lines 712-749, slice 13): CHUNK_ID = src/runtime/changes.py#712-749#7bce4a55 — [[F:src/runtime/changes.py#712-749#7bce4a55]].
- ChangeManager (class, lines 750-787, slice 14): CHUNK_ID = src/runtime/changes.py#750-787#7bce4a55 — [[F:src/runtime/changes.py#750-787#7bce4a55]].
- ChangeManager (class, lines 788-788, slice 15): CHUNK_ID = src/runtime/changes.py#788-788#7bce4a55 — [[F:src/runtime/changes.py#788-788#7bce4a55]].
- ChangeManager.__init__ (method, lines 257-275): CHUNK_ID = src/runtime/changes.py#257-275#7bce4a55 — [[F:src/runtime/changes.py#257-275#7bce4a55]].
- ChangeManager.get (method, lines 279-284): CHUNK_ID = src/runtime/changes.py#279-284#7bce4a55 — [[F:src/runtime/changes.py#279-284#7bce4a55]].
- ChangeManager.changes (method, lines 286-292): CHUNK_ID = src/runtime/changes.py#286-292#7bce4a55 — [[F:src/runtime/changes.py#286-292#7bce4a55]].
- ChangeManager.audit_log (method, lines 294-296): CHUNK_ID = src/runtime/changes.py#294-296#7bce4a55 — [[F:src/runtime/changes.py#294-296#7bce4a55]].
- ChangeManager.open_change (method, lines 298-303): CHUNK_ID = src/runtime/changes.py#298-303#7bce4a55 — [[F:src/runtime/changes.py#298-303#7bce4a55]].
- ChangeManager.submit (method, lines 307-344, slice 1): CHUNK_ID = src/runtime/changes.py#307-344#7bce4a55 — [[F:src/runtime/changes.py#307-344#7bce4a55]].
- ChangeManager.submit (method, lines 345-382, slice 2): CHUNK_ID = src/runtime/changes.py#345-382#7bce4a55 — [[F:src/runtime/changes.py#345-382#7bce4a55]].
- ChangeManager.submit (method, lines 383-384, slice 3): CHUNK_ID = src/runtime/changes.py#383-384#7bce4a55 — [[F:src/runtime/changes.py#383-384#7bce4a55]].
- ChangeManager._precheck (method, lines 386-399): CHUNK_ID = src/runtime/changes.py#386-399#7bce4a55 — [[F:src/runtime/changes.py#386-399#7bce4a55]].
- ChangeManager.request_desired (method, lines 401-432): CHUNK_ID = src/runtime/changes.py#401-432#7bce4a55 — [[F:src/runtime/changes.py#401-432#7bce4a55]].
- ChangeManager.approve (method, lines 434-445): CHUNK_ID = src/runtime/changes.py#434-445#7bce4a55 — [[F:src/runtime/changes.py#434-445#7bce4a55]].
- ChangeManager.record_stage (method, lines 447-481): CHUNK_ID = src/runtime/changes.py#447-481#7bce4a55 — [[F:src/runtime/changes.py#447-481#7bce4a55]].
- ChangeManager.execute (method, lines 483-520, slice 1): CHUNK_ID = src/runtime/changes.py#483-520#7bce4a55 — [[F:src/runtime/changes.py#483-520#7bce4a55]].
- ChangeManager.execute (method, lines 521-545, slice 2): CHUNK_ID = src/runtime/changes.py#521-545#7bce4a55 — [[F:src/runtime/changes.py#521-545#7bce4a55]].
- ChangeManager.promote (method, lines 547-556): CHUNK_ID = src/runtime/changes.py#547-556#7bce4a55 — [[F:src/runtime/changes.py#547-556#7bce4a55]].
- ChangeManager.decide_lifecycle (method, lines 558-595, slice 1): CHUNK_ID = src/runtime/changes.py#558-595#7bce4a55 — [[F:src/runtime/changes.py#558-595#7bce4a55]].
- ChangeManager.decide_lifecycle (method, lines 596-630, slice 2): CHUNK_ID = src/runtime/changes.py#596-630#7bce4a55 — [[F:src/runtime/changes.py#596-630#7bce4a55]].
- ChangeManager.rollback (method, lines 632-637): CHUNK_ID = src/runtime/changes.py#632-637#7bce4a55 — [[F:src/runtime/changes.py#632-637#7bce4a55]].
- ChangeManager.cancel (method, lines 639-646): CHUNK_ID = src/runtime/changes.py#639-646#7bce4a55 — [[F:src/runtime/changes.py#639-646#7bce4a55]].
- ChangeManager._observe (method, lines 650-667): CHUNK_ID = src/runtime/changes.py#650-667#7bce4a55 — [[F:src/runtime/changes.py#650-667#7bce4a55]].
- ChangeManager._rollback (method, lines 669-707): CHUNK_ID = src/runtime/changes.py#669-707#7bce4a55 — [[F:src/runtime/changes.py#669-707#7bce4a55]].
- ChangeManager._expect (method, lines 709-713): CHUNK_ID = src/runtime/changes.py#709-713#7bce4a55 — [[F:src/runtime/changes.py#709-713#7bce4a55]].
- ChangeManager._new (method, lines 715-743): CHUNK_ID = src/runtime/changes.py#715-743#7bce4a55 — [[F:src/runtime/changes.py#715-743#7bce4a55]].
- ChangeManager._move (method, lines 745-753): CHUNK_ID = src/runtime/changes.py#745-753#7bce4a55 — [[F:src/runtime/changes.py#745-753#7bce4a55]].
- ChangeManager._forget_unexecuted (method, lines 755-760): CHUNK_ID = src/runtime/changes.py#755-760#7bce4a55 — [[F:src/runtime/changes.py#755-760#7bce4a55]].
- ChangeManager._audit_entry (method, lines 762-763): CHUNK_ID = src/runtime/changes.py#762-763#7bce4a55 — [[F:src/runtime/changes.py#762-763#7bce4a55]].
- ChangeManager._append_audit (method, lines 765-788): CHUNK_ID = src/runtime/changes.py#765-788#7bce4a55 — [[F:src/runtime/changes.py#765-788#7bce4a55]].

## src/runtime/reconcile.py

SHA8 e3ebc015; total lines 303.

- _signature (function, lines 73-83): CHUNK_ID = src/runtime/reconcile.py#73-83#e3ebc015 — [[F:src/runtime/reconcile.py#73-83#e3ebc015]].
- MismatchKind (class, lines 86-90): CHUNK_ID = src/runtime/reconcile.py#86-90#e3ebc015 — [[F:src/runtime/reconcile.py#86-90#e3ebc015]].
- Mismatch (class, lines 94-122): CHUNK_ID = src/runtime/reconcile.py#94-122#e3ebc015 — [[F:src/runtime/reconcile.py#94-122#e3ebc015]].
- Mismatch.detail (method, lines 104-111): CHUNK_ID = src/runtime/reconcile.py#104-111#e3ebc015 — [[F:src/runtime/reconcile.py#104-111#e3ebc015]].
- Mismatch.to_dict (method, lines 113-122): CHUNK_ID = src/runtime/reconcile.py#113-122#e3ebc015 — [[F:src/runtime/reconcile.py#113-122#e3ebc015]].
- plan_path (function, lines 125-152): CHUNK_ID = src/runtime/reconcile.py#125-152#e3ebc015 — [[F:src/runtime/reconcile.py#125-152#e3ebc015]].
- diff (function, lines 155-196): CHUNK_ID = src/runtime/reconcile.py#155-196#e3ebc015 — [[F:src/runtime/reconcile.py#155-196#e3ebc015]].
- ReconcileOutcome (class, lines 200-206): CHUNK_ID = src/runtime/reconcile.py#200-206#e3ebc015 — [[F:src/runtime/reconcile.py#200-206#e3ebc015]].
- ReconcileOutcome.to_dict (method, lines 205-206): CHUNK_ID = src/runtime/reconcile.py#205-206#e3ebc015 — [[F:src/runtime/reconcile.py#205-206#e3ebc015]].
- Reconciler (class, lines 209-246, slice 1): CHUNK_ID = src/runtime/reconcile.py#209-246#e3ebc015 — [[F:src/runtime/reconcile.py#209-246#e3ebc015]].
- Reconciler (class, lines 247-284, slice 2): CHUNK_ID = src/runtime/reconcile.py#247-284#e3ebc015 — [[F:src/runtime/reconcile.py#247-284#e3ebc015]].
- Reconciler (class, lines 285-303, slice 3): CHUNK_ID = src/runtime/reconcile.py#285-303#e3ebc015 — [[F:src/runtime/reconcile.py#285-303#e3ebc015]].
- Reconciler.__init__ (method, lines 210-229): CHUNK_ID = src/runtime/reconcile.py#210-229#e3ebc015 — [[F:src/runtime/reconcile.py#210-229#e3ebc015]].
- Reconciler._raise_alert (method, lines 231-234): CHUNK_ID = src/runtime/reconcile.py#231-234#e3ebc015 — [[F:src/runtime/reconcile.py#231-234#e3ebc015]].
- Reconciler.reconcile_once (method, lines 236-272): CHUNK_ID = src/runtime/reconcile.py#236-272#e3ebc015 — [[F:src/runtime/reconcile.py#236-272#e3ebc015]].
- Reconciler._step (method, lines 274-303): CHUNK_ID = src/runtime/reconcile.py#274-303#e3ebc015 — [[F:src/runtime/reconcile.py#274-303#e3ebc015]].

## src/runtime/production.py

SHA8 55696d76; total lines 418.

- _OrchestratorView (class, lines 107-119): CHUNK_ID = src/runtime/production.py#107-119#55696d76 — [[F:src/runtime/production.py#107-119#55696d76]].
- _OrchestratorView.crypto_box (method, lines 111-111): CHUNK_ID = src/runtime/production.py#111-111#55696d76 — [[F:src/runtime/production.py#111-111#55696d76]].
- _OrchestratorView.signal_engines (method, lines 113-113): CHUNK_ID = src/runtime/production.py#113-113#55696d76 — [[F:src/runtime/production.py#113-113#55696d76]].
- _OrchestratorView.background_tasks (method, lines 115-115): CHUNK_ID = src/runtime/production.py#115-115#55696d76 — [[F:src/runtime/production.py#115-115#55696d76]].
- _OrchestratorView.provider_tasks (method, lines 117-117): CHUNK_ID = src/runtime/production.py#117-117#55696d76 — [[F:src/runtime/production.py#117-117#55696d76]].
- _OrchestratorView.worker_pools (method, lines 119-119): CHUNK_ID = src/runtime/production.py#119-119#55696d76 — [[F:src/runtime/production.py#119-119#55696d76]].
- _PauseSwitch (class, lines 122-126): CHUNK_ID = src/runtime/production.py#122-126#55696d76 — [[F:src/runtime/production.py#122-126#55696d76]].
- _PauseSwitch.paused (method, lines 124-124): CHUNK_ID = src/runtime/production.py#124-124#55696d76 — [[F:src/runtime/production.py#124-124#55696d76]].
- _PauseSwitch.set_paused_now (method, lines 126-126): CHUNK_ID = src/runtime/production.py#126-126#55696d76 — [[F:src/runtime/production.py#126-126#55696d76]].
- _utc_ms (function, lines 129-130): CHUNK_ID = src/runtime/production.py#129-130#55696d76 — [[F:src/runtime/production.py#129-130#55696d76]].
- ProductionSources (class, lines 134-150): CHUNK_ID = src/runtime/production.py#134-150#55696d76 — [[F:src/runtime/production.py#134-150#55696d76]].
- _impl (function, lines 153-155): CHUNK_ID = src/runtime/production.py#153-155#55696d76 — [[F:src/runtime/production.py#153-155#55696d76]].
- _orchestrator_task_dependencies (function, lines 158-180): CHUNK_ID = src/runtime/production.py#158-180#55696d76 — [[F:src/runtime/production.py#158-180#55696d76]].
- production_discoveries (function, lines 183-225): CHUNK_ID = src/runtime/production.py#183-225#55696d76 — [[F:src/runtime/production.py#183-225#55696d76]].
- production_controllers (function, lines 228-256): CHUNK_ID = src/runtime/production.py#228-256#55696d76 — [[F:src/runtime/production.py#228-256#55696d76]].
- SyncReport (class, lines 260-263): CHUNK_ID = src/runtime/production.py#260-263#55696d76 — [[F:src/runtime/production.py#260-263#55696d76]].
- RuntimeLoop (class, lines 266-303, slice 1): CHUNK_ID = src/runtime/production.py#266-303#55696d76 — [[F:src/runtime/production.py#266-303#55696d76]].
- RuntimeLoop (class, lines 304-341, slice 2): CHUNK_ID = src/runtime/production.py#304-341#55696d76 — [[F:src/runtime/production.py#304-341#55696d76]].
- RuntimeLoop (class, lines 342-372, slice 3): CHUNK_ID = src/runtime/production.py#342-372#55696d76 — [[F:src/runtime/production.py#342-372#55696d76]].
- RuntimeLoop.__init__ (method, lines 272-298): CHUNK_ID = src/runtime/production.py#272-298#55696d76 — [[F:src/runtime/production.py#272-298#55696d76]].
- RuntimeLoop.sync_once (method, lines 300-338): CHUNK_ID = src/runtime/production.py#300-338#55696d76 — [[F:src/runtime/production.py#300-338#55696d76]].
- RuntimeLoop.step (method, lines 340-349): CHUNK_ID = src/runtime/production.py#340-349#55696d76 — [[F:src/runtime/production.py#340-349#55696d76]].
- RuntimeLoop.run (method, lines 351-372): CHUNK_ID = src/runtime/production.py#351-372#55696d76 — [[F:src/runtime/production.py#351-372#55696d76]].
- UpgradeListing (class, lines 375-418): CHUNK_ID = src/runtime/production.py#375-418#55696d76 — [[F:src/runtime/production.py#375-418#55696d76]].
- UpgradeListing.__init__ (method, lines 384-388): CHUNK_ID = src/runtime/production.py#384-388#55696d76 — [[F:src/runtime/production.py#384-388#55696d76]].
- UpgradeListing.refresh (method, lines 390-414): CHUNK_ID = src/runtime/production.py#390-414#55696d76 — [[F:src/runtime/production.py#390-414#55696d76]].
- UpgradeListing.close (method, lines 416-418): CHUNK_ID = src/runtime/production.py#416-418#55696d76 — [[F:src/runtime/production.py#416-418#55696d76]].

## src/runtime/platform.py

SHA8 1c7162da; total lines 145.

- RuntimePlatform (class, lines 47-84, slice 1): CHUNK_ID = src/runtime/platform.py#47-84#1c7162da — [[F:src/runtime/platform.py#47-84#1c7162da]].
- RuntimePlatform (class, lines 85-98, slice 2): CHUNK_ID = src/runtime/platform.py#85-98#1c7162da — [[F:src/runtime/platform.py#85-98#1c7162da]].
- RuntimePlatform.flush (method, lines 58-63): CHUNK_ID = src/runtime/platform.py#58-63#1c7162da — [[F:src/runtime/platform.py#58-63#1c7162da]].
- RuntimePlatform.restore (method, lines 65-67): CHUNK_ID = src/runtime/platform.py#65-67#1c7162da — [[F:src/runtime/platform.py#65-67#1c7162da]].
- RuntimePlatform.summary (method, lines 69-84): CHUNK_ID = src/runtime/platform.py#69-84#1c7162da — [[F:src/runtime/platform.py#69-84#1c7162da]].
- RuntimePlatform.dependencies (method, lines 86-98): CHUNK_ID = src/runtime/platform.py#86-98#1c7162da — [[F:src/runtime/platform.py#86-98#1c7162da]].
- build_runtime_platform (function, lines 101-145): CHUNK_ID = src/runtime/platform.py#101-145#1c7162da — [[F:src/runtime/platform.py#101-145#1c7162da]].

## src/terminal/server.py

SHA8 10681519; total lines 644.

- DaemonError (class, lines 53-54): CHUNK_ID = src/terminal/server.py#53-54#10681519 — [[F:src/terminal/server.py#53-54#10681519]].
- ClientConnection (class, lines 57-101): CHUNK_ID = src/terminal/server.py#57-101#10681519 — [[F:src/terminal/server.py#57-101#10681519]].
- ClientConnection.__init__ (method, lines 60-75): CHUNK_ID = src/terminal/server.py#60-75#10681519 — [[F:src/terminal/server.py#60-75#10681519]].
- ClientConnection.push (method, lines 77-85): CHUNK_ID = src/terminal/server.py#77-85#10681519 — [[F:src/terminal/server.py#77-85#10681519]].
- ClientConnection.run_writer (method, lines 87-92): CHUNK_ID = src/terminal/server.py#87-92#10681519 — [[F:src/terminal/server.py#87-92#10681519]].
- ClientConnection.drain_and_stop (method, lines 94-97): CHUNK_ID = src/terminal/server.py#94-97#10681519 — [[F:src/terminal/server.py#94-97#10681519]].
- ClientConnection.close (method, lines 99-101): CHUNK_ID = src/terminal/server.py#99-101#10681519 — [[F:src/terminal/server.py#99-101#10681519]].
- TerminalServer (class, lines 104-141, slice 1): CHUNK_ID = src/terminal/server.py#104-141#10681519 — [[F:src/terminal/server.py#104-141#10681519]].
- TerminalServer (class, lines 142-179, slice 2): CHUNK_ID = src/terminal/server.py#142-179#10681519 — [[F:src/terminal/server.py#142-179#10681519]].
- TerminalServer (class, lines 180-217, slice 3): CHUNK_ID = src/terminal/server.py#180-217#10681519 — [[F:src/terminal/server.py#180-217#10681519]].
- TerminalServer (class, lines 218-255, slice 4): CHUNK_ID = src/terminal/server.py#218-255#10681519 — [[F:src/terminal/server.py#218-255#10681519]].
- TerminalServer (class, lines 256-293, slice 5): CHUNK_ID = src/terminal/server.py#256-293#10681519 — [[F:src/terminal/server.py#256-293#10681519]].
- TerminalServer (class, lines 294-331, slice 6): CHUNK_ID = src/terminal/server.py#294-331#10681519 — [[F:src/terminal/server.py#294-331#10681519]].
- TerminalServer (class, lines 332-369, slice 7): CHUNK_ID = src/terminal/server.py#332-369#10681519 — [[F:src/terminal/server.py#332-369#10681519]].
- TerminalServer (class, lines 370-407, slice 8): CHUNK_ID = src/terminal/server.py#370-407#10681519 — [[F:src/terminal/server.py#370-407#10681519]].
- TerminalServer (class, lines 408-445, slice 9): CHUNK_ID = src/terminal/server.py#408-445#10681519 — [[F:src/terminal/server.py#408-445#10681519]].
- TerminalServer (class, lines 446-483, slice 10): CHUNK_ID = src/terminal/server.py#446-483#10681519 — [[F:src/terminal/server.py#446-483#10681519]].
- TerminalServer (class, lines 484-521, slice 11): CHUNK_ID = src/terminal/server.py#484-521#10681519 — [[F:src/terminal/server.py#484-521#10681519]].
- TerminalServer (class, lines 522-554, slice 12): CHUNK_ID = src/terminal/server.py#522-554#10681519 — [[F:src/terminal/server.py#522-554#10681519]].
- TerminalServer.__init__ (method, lines 105-131): CHUNK_ID = src/terminal/server.py#105-131#10681519 — [[F:src/terminal/server.py#105-131#10681519]].
- TerminalServer.start (method, lines 135-157): CHUNK_ID = src/terminal/server.py#135-157#10681519 — [[F:src/terminal/server.py#135-157#10681519]].
- TerminalServer.stop (method, lines 159-178): CHUNK_ID = src/terminal/server.py#159-178#10681519 — [[F:src/terminal/server.py#159-178#10681519]].
- TerminalServer.spawn (method, lines 180-185): CHUNK_ID = src/terminal/server.py#180-185#10681519 — [[F:src/terminal/server.py#180-185#10681519]].
- TerminalServer._task_done (method, lines 187-190): CHUNK_ID = src/terminal/server.py#187-190#10681519 — [[F:src/terminal/server.py#187-190#10681519]].
- TerminalServer._check_handshake (method, lines 194-216): CHUNK_ID = src/terminal/server.py#194-216#10681519 — [[F:src/terminal/server.py#194-216#10681519]].
- TerminalServer._handle_ws (method, lines 218-230): CHUNK_ID = src/terminal/server.py#218-230#10681519 — [[F:src/terminal/server.py#218-230#10681519]].
- TerminalServer._handle_unix (method, lines 234-272): CHUNK_ID = src/terminal/server.py#234-272#10681519 — [[F:src/terminal/server.py#234-272#10681519]].
- TerminalServer._serve (method, lines 276-320): CHUNK_ID = src/terminal/server.py#276-320#10681519 — [[F:src/terminal/server.py#276-320#10681519]].
- TerminalServer._handle_raw (method, lines 322-336): CHUNK_ID = src/terminal/server.py#322-336#10681519 — [[F:src/terminal/server.py#322-336#10681519]].
- TerminalServer._dispatch (method, lines 338-356): CHUNK_ID = src/terminal/server.py#338-356#10681519 — [[F:src/terminal/server.py#338-356#10681519]].
- TerminalServer._hello (method, lines 358-393): CHUNK_ID = src/terminal/server.py#358-393#10681519 — [[F:src/terminal/server.py#358-393#10681519]].
- TerminalServer._req_ping (method, lines 397-398): CHUNK_ID = src/terminal/server.py#397-398#10681519 — [[F:src/terminal/server.py#397-398#10681519]].
- TerminalServer._req_session_create (method, lines 400-415): CHUNK_ID = src/terminal/server.py#400-415#10681519 — [[F:src/terminal/server.py#400-415#10681519]].
- TerminalServer._req_session_attach (method, lines 417-428): CHUNK_ID = src/terminal/server.py#417-428#10681519 — [[F:src/terminal/server.py#417-428#10681519]].
- TerminalServer._replay (method, lines 430-445): CHUNK_ID = src/terminal/server.py#430-445#10681519 — [[F:src/terminal/server.py#430-445#10681519]].
- TerminalServer._req_session_detach (method, lines 447-450): CHUNK_ID = src/terminal/server.py#447-450#10681519 — [[F:src/terminal/server.py#447-450#10681519]].
- TerminalServer._req_session_input (method, lines 452-456): CHUNK_ID = src/terminal/server.py#452-456#10681519 — [[F:src/terminal/server.py#452-456#10681519]].
- TerminalServer._req_session_resize (method, lines 458-463): CHUNK_ID = src/terminal/server.py#458-463#10681519 — [[F:src/terminal/server.py#458-463#10681519]].
- TerminalServer._req_session_rename (method, lines 465-468): CHUNK_ID = src/terminal/server.py#465-468#10681519 — [[F:src/terminal/server.py#465-468#10681519]].
- TerminalServer._req_session_signal (method, lines 470-474): CHUNK_ID = src/terminal/server.py#470-474#10681519 — [[F:src/terminal/server.py#470-474#10681519]].
- TerminalServer._req_session_close (method, lines 476-482): CHUNK_ID = src/terminal/server.py#476-482#10681519 — [[F:src/terminal/server.py#476-482#10681519]].
- TerminalServer._req_process_kill (method, lines 484-488): CHUNK_ID = src/terminal/server.py#484-488#10681519 — [[F:src/terminal/server.py#484-488#10681519]].
- TerminalServer._req_process_output (method, lines 490-503): CHUNK_ID = src/terminal/server.py#490-503#10681519 — [[F:src/terminal/server.py#490-503#10681519]].
- TerminalServer._job (method, lines 505-530): CHUNK_ID = src/terminal/server.py#505-530#10681519 — [[F:src/terminal/server.py#505-530#10681519]].
- TerminalServer._broadcast (method, lines 534-538): CHUNK_ID = src/terminal/server.py#534-538#10681519 — [[F:src/terminal/server.py#534-538#10681519]].
- TerminalServer._on_session_event (method, lines 540-544): CHUNK_ID = src/terminal/server.py#540-544#10681519 — [[F:src/terminal/server.py#540-544#10681519]].
- TerminalServer._on_process_event (method, lines 546-547): CHUNK_ID = src/terminal/server.py#546-547#10681519 — [[F:src/terminal/server.py#546-547#10681519]].
- TerminalServer._on_output (method, lines 549-554): CHUNK_ID = src/terminal/server.py#549-554#10681519 — [[F:src/terminal/server.py#549-554#10681519]].
- _next (function, lines 557-561): CHUNK_ID = src/terminal/server.py#557-561#10681519 — [[F:src/terminal/server.py#557-561#10681519]].
- _reply (function, lines 564-567): CHUNK_ID = src/terminal/server.py#564-567#10681519 — [[F:src/terminal/server.py#564-567#10681519]].
- _error (function, lines 570-571): CHUNK_ID = src/terminal/server.py#570-571#10681519 — [[F:src/terminal/server.py#570-571#10681519]].
- InstanceLock (class, lines 577-596): CHUNK_ID = src/terminal/server.py#577-596#10681519 — [[F:src/terminal/server.py#577-596#10681519]].
- InstanceLock.__init__ (method, lines 580-582): CHUNK_ID = src/terminal/server.py#580-582#10681519 — [[F:src/terminal/server.py#580-582#10681519]].
- InstanceLock.acquire (method, lines 584-591): CHUNK_ID = src/terminal/server.py#584-591#10681519 — [[F:src/terminal/server.py#584-591#10681519]].
- InstanceLock.release (method, lines 593-596): CHUNK_ID = src/terminal/server.py#593-596#10681519 — [[F:src/terminal/server.py#593-596#10681519]].
- run_daemon (function, lines 599-636, slice 1): CHUNK_ID = src/terminal/server.py#599-636#10681519 — [[F:src/terminal/server.py#599-636#10681519]].
- run_daemon (function, lines 637-644, slice 2): CHUNK_ID = src/terminal/server.py#637-644#10681519 — [[F:src/terminal/server.py#637-644#10681519]].

## src/terminal/protocol.py

SHA8 ed293ffb; total lines 216.

- ProtocolError (class, lines 80-86): CHUNK_ID = src/terminal/protocol.py#80-86#ed293ffb — [[F:src/terminal/protocol.py#80-86#ed293ffb]].
- ProtocolError.__init__ (method, lines 83-86): CHUNK_ID = src/terminal/protocol.py#83-86#ed293ffb — [[F:src/terminal/protocol.py#83-86#ed293ffb]].
- new_session_id (function, lines 89-90): CHUNK_ID = src/terminal/protocol.py#89-90#ed293ffb — [[F:src/terminal/protocol.py#89-90#ed293ffb]].
- new_process_id (function, lines 93-94): CHUNK_ID = src/terminal/protocol.py#93-94#ed293ffb — [[F:src/terminal/protocol.py#93-94#ed293ffb]].
- decode_frame (function, lines 97-118): CHUNK_ID = src/terminal/protocol.py#97-118#ed293ffb — [[F:src/terminal/protocol.py#97-118#ed293ffb]].
- encode_frame (function, lines 121-122): CHUNK_ID = src/terminal/protocol.py#121-122#ed293ffb — [[F:src/terminal/protocol.py#121-122#ed293ffb]].
- b64encode (function, lines 125-126): CHUNK_ID = src/terminal/protocol.py#125-126#ed293ffb — [[F:src/terminal/protocol.py#125-126#ed293ffb]].
- session_id (function, lines 129-133): CHUNK_ID = src/terminal/protocol.py#129-133#ed293ffb — [[F:src/terminal/protocol.py#129-133#ed293ffb]].
- process_id (function, lines 136-140): CHUNK_ID = src/terminal/protocol.py#136-140#ed293ffb — [[F:src/terminal/protocol.py#136-140#ed293ffb]].
- bounded_int (function, lines 143-151): CHUNK_ID = src/terminal/protocol.py#143-151#ed293ffb — [[F:src/terminal/protocol.py#143-151#ed293ffb]].
- optional_offset (function, lines 154-160): CHUNK_ID = src/terminal/protocol.py#154-160#ed293ffb — [[F:src/terminal/protocol.py#154-160#ed293ffb]].
- text_field (function, lines 163-169): CHUNK_ID = src/terminal/protocol.py#163-169#ed293ffb — [[F:src/terminal/protocol.py#163-169#ed293ffb]].
- validate_name (function, lines 172-179): CHUNK_ID = src/terminal/protocol.py#172-179#ed293ffb — [[F:src/terminal/protocol.py#172-179#ed293ffb]].
- optional_name (function, lines 182-183): CHUNK_ID = src/terminal/protocol.py#182-183#ed293ffb — [[F:src/terminal/protocol.py#182-183#ed293ffb]].
- validate_argv (function, lines 186-195): CHUNK_ID = src/terminal/protocol.py#186-195#ed293ffb — [[F:src/terminal/protocol.py#186-195#ed293ffb]].
- validate_cwd (function, lines 198-209): CHUNK_ID = src/terminal/protocol.py#198-209#ed293ffb — [[F:src/terminal/protocol.py#198-209#ed293ffb]].
- signal_from (function, lines 212-216): CHUNK_ID = src/terminal/protocol.py#212-216#ed293ffb — [[F:src/terminal/protocol.py#212-216#ed293ffb]].

## src/workers/trader.py

SHA8 687738d8; total lines 138.

- _run (function, lines 53-90, slice 1): CHUNK_ID = src/workers/trader.py#53-90#687738d8 — [[F:src/workers/trader.py#53-90#687738d8]].
- _run (function, lines 91-124, slice 2): CHUNK_ID = src/workers/trader.py#91-124#687738d8 — [[F:src/workers/trader.py#91-124#687738d8]].
- main (function, lines 127-134): CHUNK_ID = src/workers/trader.py#127-134#687738d8 — [[F:src/workers/trader.py#127-134#687738d8]].

## src/workers/orchestrator.py

SHA8 a2efe8f2; total lines 805.

- WorkerTask (class, lines 42-54): CHUNK_ID = src/workers/orchestrator.py#42-54#a2efe8f2 — [[F:src/workers/orchestrator.py#42-54#a2efe8f2]].
- WorkerResult (class, lines 58-88): CHUNK_ID = src/workers/orchestrator.py#58-88#a2efe8f2 — [[F:src/workers/orchestrator.py#58-88#a2efe8f2]].
- _handle_worker_sigterm (function, lines 91-93): CHUNK_ID = src/workers/orchestrator.py#91-93#a2efe8f2 — [[F:src/workers/orchestrator.py#91-93#a2efe8f2]].
- _model_worker (function, lines 96-135): CHUNK_ID = src/workers/orchestrator.py#96-135#a2efe8f2 — [[F:src/workers/orchestrator.py#96-135#a2efe8f2]].
- _run_horizon_inference (function, lines 138-175, slice 1): CHUNK_ID = src/workers/orchestrator.py#138-175#a2efe8f2 — [[F:src/workers/orchestrator.py#138-175#a2efe8f2]].
- _run_horizon_inference (function, lines 176-213, slice 2): CHUNK_ID = src/workers/orchestrator.py#176-213#a2efe8f2 — [[F:src/workers/orchestrator.py#176-213#a2efe8f2]].
- _run_horizon_inference (function, lines 214-251, slice 3): CHUNK_ID = src/workers/orchestrator.py#214-251#a2efe8f2 — [[F:src/workers/orchestrator.py#214-251#a2efe8f2]].
- _run_horizon_inference (function, lines 252-289, slice 4): CHUNK_ID = src/workers/orchestrator.py#252-289#a2efe8f2 — [[F:src/workers/orchestrator.py#252-289#a2efe8f2]].
- _run_horizon_inference (function, lines 290-327, slice 5): CHUNK_ID = src/workers/orchestrator.py#290-327#a2efe8f2 — [[F:src/workers/orchestrator.py#290-327#a2efe8f2]].
- _run_horizon_inference (function, lines 328-365, slice 6): CHUNK_ID = src/workers/orchestrator.py#328-365#a2efe8f2 — [[F:src/workers/orchestrator.py#328-365#a2efe8f2]].
- _run_horizon_inference (function, lines 366-397, slice 7): CHUNK_ID = src/workers/orchestrator.py#366-397#a2efe8f2 — [[F:src/workers/orchestrator.py#366-397#a2efe8f2]].
- _utxos_with_ages (function, lines 439-456): CHUNK_ID = src/workers/orchestrator.py#439-456#a2efe8f2 — [[F:src/workers/orchestrator.py#439-456#a2efe8f2]].
- _fetch_recent_block_transactions (function, lines 459-487): CHUNK_ID = src/workers/orchestrator.py#459-487#a2efe8f2 — [[F:src/workers/orchestrator.py#459-487#a2efe8f2]].
- _ecc_worker (function, lines 490-528): CHUNK_ID = src/workers/orchestrator.py#490-528#a2efe8f2 — [[F:src/workers/orchestrator.py#490-528#a2efe8f2]].
- _run_ecc_cycle (function, lines 531-568, slice 1): CHUNK_ID = src/workers/orchestrator.py#531-568#a2efe8f2 — [[F:src/workers/orchestrator.py#531-568#a2efe8f2]].
- _run_ecc_cycle (function, lines 569-606, slice 2): CHUNK_ID = src/workers/orchestrator.py#569-606#a2efe8f2 — [[F:src/workers/orchestrator.py#569-606#a2efe8f2]].
- _run_ecc_cycle (function, lines 607-642, slice 3): CHUNK_ID = src/workers/orchestrator.py#607-642#a2efe8f2 — [[F:src/workers/orchestrator.py#607-642#a2efe8f2]].
- WorkerOrchestrator (class, lines 645-682, slice 1): CHUNK_ID = src/workers/orchestrator.py#645-682#a2efe8f2 — [[F:src/workers/orchestrator.py#645-682#a2efe8f2]].
- WorkerOrchestrator (class, lines 683-720, slice 2): CHUNK_ID = src/workers/orchestrator.py#683-720#a2efe8f2 — [[F:src/workers/orchestrator.py#683-720#a2efe8f2]].
- WorkerOrchestrator (class, lines 721-758, slice 3): CHUNK_ID = src/workers/orchestrator.py#721-758#a2efe8f2 — [[F:src/workers/orchestrator.py#721-758#a2efe8f2]].
- WorkerOrchestrator (class, lines 759-796, slice 4): CHUNK_ID = src/workers/orchestrator.py#759-796#a2efe8f2 — [[F:src/workers/orchestrator.py#759-796#a2efe8f2]].
- WorkerOrchestrator (class, lines 797-805, slice 5): CHUNK_ID = src/workers/orchestrator.py#797-805#a2efe8f2 — [[F:src/workers/orchestrator.py#797-805#a2efe8f2]].
- WorkerOrchestrator.__init__ (method, lines 658-680): CHUNK_ID = src/workers/orchestrator.py#658-680#a2efe8f2 — [[F:src/workers/orchestrator.py#658-680#a2efe8f2]].
- WorkerOrchestrator.start (method, lines 682-688): CHUNK_ID = src/workers/orchestrator.py#682-688#a2efe8f2 — [[F:src/workers/orchestrator.py#682-688#a2efe8f2]].
- WorkerOrchestrator._spawn (method, lines 690-714): CHUNK_ID = src/workers/orchestrator.py#690-714#a2efe8f2 — [[F:src/workers/orchestrator.py#690-714#a2efe8f2]].
- WorkerOrchestrator._pin_cpu (method, lines 716-724): CHUNK_ID = src/workers/orchestrator.py#716-724#a2efe8f2 — [[F:src/workers/orchestrator.py#716-724#a2efe8f2]].
- WorkerOrchestrator.submit (method, lines 726-744): CHUNK_ID = src/workers/orchestrator.py#726-744#a2efe8f2 — [[F:src/workers/orchestrator.py#726-744#a2efe8f2]].
- WorkerOrchestrator.collect (method, lines 746-751): CHUNK_ID = src/workers/orchestrator.py#746-751#a2efe8f2 — [[F:src/workers/orchestrator.py#746-751#a2efe8f2]].
- WorkerOrchestrator.scale (method, lines 753-765): CHUNK_ID = src/workers/orchestrator.py#753-765#a2efe8f2 — [[F:src/workers/orchestrator.py#753-765#a2efe8f2]].
- WorkerOrchestrator.shutdown (method, lines 767-777): CHUNK_ID = src/workers/orchestrator.py#767-777#a2efe8f2 — [[F:src/workers/orchestrator.py#767-777#a2efe8f2]].
- WorkerOrchestrator.worker_count (method, lines 780-781): CHUNK_ID = src/workers/orchestrator.py#780-781#a2efe8f2 — [[F:src/workers/orchestrator.py#780-781#a2efe8f2]].
- WorkerOrchestrator.dropped_tasks (method, lines 784-785): CHUNK_ID = src/workers/orchestrator.py#784-785#a2efe8f2 — [[F:src/workers/orchestrator.py#784-785#a2efe8f2]].
- WorkerOrchestrator.health_snapshot (method, lines 787-805): CHUNK_ID = src/workers/orchestrator.py#787-805#a2efe8f2 — [[F:src/workers/orchestrator.py#787-805#a2efe8f2]].

## src/intelligence/client.py

SHA8 e799d7be; total lines 706.

- CacheEntry (class, lines 30-46): CHUNK_ID = src/intelligence/client.py#30-46#e799d7be — [[F:src/intelligence/client.py#30-46#e799d7be]].
- CacheEntry.is_stale (method, lines 43-46): CHUNK_ID = src/intelligence/client.py#43-46#e799d7be — [[F:src/intelligence/client.py#43-46#e799d7be]].
- IntelligenceAggregator (class, lines 49-86, slice 1): CHUNK_ID = src/intelligence/client.py#49-86#e799d7be — [[F:src/intelligence/client.py#49-86#e799d7be]].
- IntelligenceAggregator (class, lines 87-124, slice 2): CHUNK_ID = src/intelligence/client.py#87-124#e799d7be — [[F:src/intelligence/client.py#87-124#e799d7be]].
- IntelligenceAggregator (class, lines 125-162, slice 3): CHUNK_ID = src/intelligence/client.py#125-162#e799d7be — [[F:src/intelligence/client.py#125-162#e799d7be]].
- IntelligenceAggregator (class, lines 163-200, slice 4): CHUNK_ID = src/intelligence/client.py#163-200#e799d7be — [[F:src/intelligence/client.py#163-200#e799d7be]].
- IntelligenceAggregator (class, lines 201-238, slice 5): CHUNK_ID = src/intelligence/client.py#201-238#e799d7be — [[F:src/intelligence/client.py#201-238#e799d7be]].
- IntelligenceAggregator (class, lines 239-276, slice 6): CHUNK_ID = src/intelligence/client.py#239-276#e799d7be — [[F:src/intelligence/client.py#239-276#e799d7be]].
- IntelligenceAggregator (class, lines 277-314, slice 7): CHUNK_ID = src/intelligence/client.py#277-314#e799d7be — [[F:src/intelligence/client.py#277-314#e799d7be]].
- IntelligenceAggregator (class, lines 315-352, slice 8): CHUNK_ID = src/intelligence/client.py#315-352#e799d7be — [[F:src/intelligence/client.py#315-352#e799d7be]].
- IntelligenceAggregator (class, lines 353-390, slice 9): CHUNK_ID = src/intelligence/client.py#353-390#e799d7be — [[F:src/intelligence/client.py#353-390#e799d7be]].
- IntelligenceAggregator (class, lines 391-428, slice 10): CHUNK_ID = src/intelligence/client.py#391-428#e799d7be — [[F:src/intelligence/client.py#391-428#e799d7be]].
- IntelligenceAggregator (class, lines 429-466, slice 11): CHUNK_ID = src/intelligence/client.py#429-466#e799d7be — [[F:src/intelligence/client.py#429-466#e799d7be]].
- IntelligenceAggregator (class, lines 467-504, slice 12): CHUNK_ID = src/intelligence/client.py#467-504#e799d7be — [[F:src/intelligence/client.py#467-504#e799d7be]].
- IntelligenceAggregator (class, lines 505-542, slice 13): CHUNK_ID = src/intelligence/client.py#505-542#e799d7be — [[F:src/intelligence/client.py#505-542#e799d7be]].
- IntelligenceAggregator (class, lines 543-580, slice 14): CHUNK_ID = src/intelligence/client.py#543-580#e799d7be — [[F:src/intelligence/client.py#543-580#e799d7be]].
- IntelligenceAggregator (class, lines 581-618, slice 15): CHUNK_ID = src/intelligence/client.py#581-618#e799d7be — [[F:src/intelligence/client.py#581-618#e799d7be]].
- IntelligenceAggregator (class, lines 619-656, slice 16): CHUNK_ID = src/intelligence/client.py#619-656#e799d7be — [[F:src/intelligence/client.py#619-656#e799d7be]].
- IntelligenceAggregator (class, lines 657-694, slice 17): CHUNK_ID = src/intelligence/client.py#657-694#e799d7be — [[F:src/intelligence/client.py#657-694#e799d7be]].
- IntelligenceAggregator (class, lines 695-695, slice 18): CHUNK_ID = src/intelligence/client.py#695-695#e799d7be — [[F:src/intelligence/client.py#695-695#e799d7be]].
- IntelligenceAggregator.__init__ (method, lines 66-103, slice 1): CHUNK_ID = src/intelligence/client.py#66-103#e799d7be — [[F:src/intelligence/client.py#66-103#e799d7be]].
- IntelligenceAggregator.__init__ (method, lines 104-116, slice 2): CHUNK_ID = src/intelligence/client.py#104-116#e799d7be — [[F:src/intelligence/client.py#104-116#e799d7be]].
- IntelligenceAggregator.get_exchange_netflow (method, lines 118-161): CHUNK_ID = src/intelligence/client.py#118-161#e799d7be — [[F:src/intelligence/client.py#118-161#e799d7be]].
- IntelligenceAggregator.get_whale_activity (method, lines 163-202): CHUNK_ID = src/intelligence/client.py#163-202#e799d7be — [[F:src/intelligence/client.py#163-202#e799d7be]].
- IntelligenceAggregator.get_funding_rate (method, lines 204-240): CHUNK_ID = src/intelligence/client.py#204-240#e799d7be — [[F:src/intelligence/client.py#204-240#e799d7be]].
- IntelligenceAggregator._fetch_glassnode_netflow (method, lines 246-283, slice 1): CHUNK_ID = src/intelligence/client.py#246-283#e799d7be — [[F:src/intelligence/client.py#246-283#e799d7be]].
- IntelligenceAggregator._fetch_glassnode_netflow (method, lines 284-321, slice 2): CHUNK_ID = src/intelligence/client.py#284-321#e799d7be — [[F:src/intelligence/client.py#284-321#e799d7be]].
- IntelligenceAggregator._fetch_glassnode_netflow (method, lines 322-324, slice 3): CHUNK_ID = src/intelligence/client.py#322-324#e799d7be — [[F:src/intelligence/client.py#322-324#e799d7be]].
- IntelligenceAggregator._fetch_glassnode_whale_activity (method, lines 326-363, slice 1): CHUNK_ID = src/intelligence/client.py#326-363#e799d7be — [[F:src/intelligence/client.py#326-363#e799d7be]].
- IntelligenceAggregator._fetch_glassnode_whale_activity (method, lines 364-401, slice 2): CHUNK_ID = src/intelligence/client.py#364-401#e799d7be — [[F:src/intelligence/client.py#364-401#e799d7be]].
- IntelligenceAggregator._fetch_glassnode_whale_activity (method, lines 402-402, slice 3): CHUNK_ID = src/intelligence/client.py#402-402#e799d7be — [[F:src/intelligence/client.py#402-402#e799d7be]].
- IntelligenceAggregator._fetch_cryptoquant_funding_rate (method, lines 404-441, slice 1): CHUNK_ID = src/intelligence/client.py#404-441#e799d7be — [[F:src/intelligence/client.py#404-441#e799d7be]].
- IntelligenceAggregator._fetch_cryptoquant_funding_rate (method, lines 442-463, slice 2): CHUNK_ID = src/intelligence/client.py#442-463#e799d7be — [[F:src/intelligence/client.py#442-463#e799d7be]].
- IntelligenceAggregator._rate_limit_glassnode (method, lines 469-476): CHUNK_ID = src/intelligence/client.py#469-476#e799d7be — [[F:src/intelligence/client.py#469-476#e799d7be]].
- IntelligenceAggregator._base_url (method, lines 479-490): CHUNK_ID = src/intelligence/client.py#479-490#e799d7be — [[F:src/intelligence/client.py#479-490#e799d7be]].
- IntelligenceAggregator.get_exchange_netflow_history (method, lines 500-537, slice 1): CHUNK_ID = src/intelligence/client.py#500-537#e799d7be — [[F:src/intelligence/client.py#500-537#e799d7be]].
- IntelligenceAggregator.get_exchange_netflow_history (method, lines 538-575, slice 2): CHUNK_ID = src/intelligence/client.py#538-575#e799d7be — [[F:src/intelligence/client.py#538-575#e799d7be]].
- IntelligenceAggregator.get_exchange_netflow_history (method, lines 576-578, slice 3): CHUNK_ID = src/intelligence/client.py#576-578#e799d7be — [[F:src/intelligence/client.py#576-578#e799d7be]].
- IntelligenceAggregator.get_whale_activity_history (method, lines 580-617, slice 1): CHUNK_ID = src/intelligence/client.py#580-617#e799d7be — [[F:src/intelligence/client.py#580-617#e799d7be]].
- IntelligenceAggregator.get_whale_activity_history (method, lines 618-647, slice 2): CHUNK_ID = src/intelligence/client.py#618-647#e799d7be — [[F:src/intelligence/client.py#618-647#e799d7be]].
- IntelligenceAggregator.get_funding_rate_history (method, lines 649-686, slice 1): CHUNK_ID = src/intelligence/client.py#649-686#e799d7be — [[F:src/intelligence/client.py#649-686#e799d7be]].
- IntelligenceAggregator.get_funding_rate_history (method, lines 687-695, slice 2): CHUNK_ID = src/intelligence/client.py#687-695#e799d7be — [[F:src/intelligence/client.py#687-695#e799d7be]].
- get_intelligence_aggregator (function, lines 698-706): CHUNK_ID = src/intelligence/client.py#698-706#e799d7be — [[F:src/intelligence/client.py#698-706#e799d7be]].

## src/agent_control/cli.py

SHA8 4995ee3c; total lines 500.

- CliError (class, lines 86-87): CHUNK_ID = src/agent_control/cli.py#86-87#4995ee3c — [[F:src/agent_control/cli.py#86-87#4995ee3c]].
- _print_json (function, lines 90-91): CHUNK_ID = src/agent_control/cli.py#90-91#4995ee3c — [[F:src/agent_control/cli.py#90-91#4995ee3c]].
- _task_view (function, lines 94-100): CHUNK_ID = src/agent_control/cli.py#94-100#4995ee3c — [[F:src/agent_control/cli.py#94-100#4995ee3c]].
- _deliverable_arg (function, lines 103-107): CHUNK_ID = src/agent_control/cli.py#103-107#4995ee3c — [[F:src/agent_control/cli.py#103-107#4995ee3c]].
- _validation_arg (function, lines 110-114): CHUNK_ID = src/agent_control/cli.py#110-114#4995ee3c — [[F:src/agent_control/cli.py#110-114#4995ee3c]].
- _scope_file (function, lines 117-127): CHUNK_ID = src/agent_control/cli.py#117-127#4995ee3c — [[F:src/agent_control/cli.py#117-127#4995ee3c]].
- _create (function, lines 130-154): CHUNK_ID = src/agent_control/cli.py#130-154#4995ee3c — [[F:src/agent_control/cli.py#130-154#4995ee3c]].
- _task (function, lines 157-192): CHUNK_ID = src/agent_control/cli.py#157-192#4995ee3c — [[F:src/agent_control/cli.py#157-192#4995ee3c]].
- _evidence (function, lines 195-203): CHUNK_ID = src/agent_control/cli.py#195-203#4995ee3c — [[F:src/agent_control/cli.py#195-203#4995ee3c]].
- _final_audit (function, lines 206-229): CHUNK_ID = src/agent_control/cli.py#206-229#4995ee3c — [[F:src/agent_control/cli.py#206-229#4995ee3c]].
- _git (function, lines 232-259): CHUNK_ID = src/agent_control/cli.py#232-259#4995ee3c — [[F:src/agent_control/cli.py#232-259#4995ee3c]].
- _branch_audit (function, lines 262-299, slice 1): CHUNK_ID = src/agent_control/cli.py#262-299#4995ee3c — [[F:src/agent_control/cli.py#262-299#4995ee3c]].
- _branch_audit (function, lines 300-319, slice 2): CHUNK_ID = src/agent_control/cli.py#300-319#4995ee3c — [[F:src/agent_control/cli.py#300-319#4995ee3c]].
- documented_commands (function, lines 322-330): CHUNK_ID = src/agent_control/cli.py#322-330#4995ee3c — [[F:src/agent_control/cli.py#322-330#4995ee3c]].
- docs_problems (function, lines 333-340): CHUNK_ID = src/agent_control/cli.py#333-340#4995ee3c — [[F:src/agent_control/cli.py#333-340#4995ee3c]].
- _docs (function, lines 343-351): CHUNK_ID = src/agent_control/cli.py#343-351#4995ee3c — [[F:src/agent_control/cli.py#343-351#4995ee3c]].
- build_parser (function, lines 354-366): CHUNK_ID = src/agent_control/cli.py#354-366#4995ee3c — [[F:src/agent_control/cli.py#354-366#4995ee3c]].
- _arguments (function, lines 369-406, slice 1): CHUNK_ID = src/agent_control/cli.py#369-406#4995ee3c — [[F:src/agent_control/cli.py#369-406#4995ee3c]].
- _arguments (function, lines 407-439, slice 2): CHUNK_ID = src/agent_control/cli.py#407-439#4995ee3c — [[F:src/agent_control/cli.py#407-439#4995ee3c]].
- main (function, lines 442-452): CHUNK_ID = src/agent_control/cli.py#442-452#4995ee3c — [[F:src/agent_control/cli.py#442-452#4995ee3c]].
- _dispatch (function, lines 455-492, slice 1): CHUNK_ID = src/agent_control/cli.py#455-492#4995ee3c — [[F:src/agent_control/cli.py#455-492#4995ee3c]].
- _dispatch (function, lines 493-500, slice 2): CHUNK_ID = src/agent_control/cli.py#493-500#4995ee3c — [[F:src/agent_control/cli.py#493-500#4995ee3c]].

## common/command_schema.py

SHA8 1de280b9; total lines 616.

- is_local_check_execution (function, lines 169-175): CHUNK_ID = common/command_schema.py#169-175#1de280b9 — [[F:common/command_schema.py#169-175#1de280b9]].
- classify (function, lines 489-505): CHUNK_ID = common/command_schema.py#489-505#1de280b9 — [[F:common/command_schema.py#489-505#1de280b9]].
- is_exact_patch_apply_command (function, lines 508-521): CHUNK_ID = common/command_schema.py#508-521#1de280b9 — [[F:common/command_schema.py#508-521#1de280b9]].
- is_ci_log_access (function, lines 535-548): CHUNK_ID = common/command_schema.py#535-548#1de280b9 — [[F:common/command_schema.py#535-548#1de280b9]].
- rank (function, lines 551-556): CHUNK_ID = common/command_schema.py#551-556#1de280b9 — [[F:common/command_schema.py#551-556#1de280b9]].
- redact (function, lines 559-589): CHUNK_ID = common/command_schema.py#559-589#1de280b9 — [[F:common/command_schema.py#559-589#1de280b9]].
- build_env (function, lines 592-616): CHUNK_ID = common/command_schema.py#592-616#1de280b9 — [[F:common/command_schema.py#592-616#1de280b9]].

## common/shell_exec.py

SHA8 cc45e7b8; total lines 464.

- _command_hash (function, lines 88-96): CHUNK_ID = common/shell_exec.py#88-96#cc45e7b8 — [[F:common/shell_exec.py#88-96#cc45e7b8]].
- _refused (function, lines 99-120): CHUNK_ID = common/shell_exec.py#99-120#cc45e7b8 — [[F:common/shell_exec.py#99-120#cc45e7b8]].
- _capture (function, lines 123-160, slice 1): CHUNK_ID = common/shell_exec.py#123-160#cc45e7b8 — [[F:common/shell_exec.py#123-160#cc45e7b8]].
- _capture (function, lines 161-178, slice 2): CHUNK_ID = common/shell_exec.py#161-178#cc45e7b8 — [[F:common/shell_exec.py#161-178#cc45e7b8]].
- _filter (function, lines 186-223, slice 1): CHUNK_ID = common/shell_exec.py#186-223#cc45e7b8 — [[F:common/shell_exec.py#186-223#cc45e7b8]].
- _filter (function, lines 224-250, slice 2): CHUNK_ID = common/shell_exec.py#224-250#cc45e7b8 — [[F:common/shell_exec.py#224-250#cc45e7b8]].
- _cap_bytes (function, lines 258-273): CHUNK_ID = common/shell_exec.py#258-273#cc45e7b8 — [[F:common/shell_exec.py#258-273#cc45e7b8]].
- _cap (function, lines 276-284): CHUNK_ID = common/shell_exec.py#276-284#cc45e7b8 — [[F:common/shell_exec.py#276-284#cc45e7b8]].
- _should_retry (function, lines 292-304): CHUNK_ID = common/shell_exec.py#292-304#cc45e7b8 — [[F:common/shell_exec.py#292-304#cc45e7b8]].
- run (function, lines 312-349, slice 1): CHUNK_ID = common/shell_exec.py#312-349#cc45e7b8 — [[F:common/shell_exec.py#312-349#cc45e7b8]].
- run (function, lines 350-387, slice 2): CHUNK_ID = common/shell_exec.py#350-387#cc45e7b8 — [[F:common/shell_exec.py#350-387#cc45e7b8]].
- run (function, lines 388-425, slice 3): CHUNK_ID = common/shell_exec.py#388-425#cc45e7b8 — [[F:common/shell_exec.py#388-425#cc45e7b8]].
- run (function, lines 426-463, slice 4): CHUNK_ID = common/shell_exec.py#426-463#cc45e7b8 — [[F:common/shell_exec.py#426-463#cc45e7b8]].
- run (function, lines 464-464, slice 5): CHUNK_ID = common/shell_exec.py#464-464#cc45e7b8 — [[F:common/shell_exec.py#464-464#cc45e7b8]].

## src/engines/orchestrator.py

SHA8 10e2649d; total lines 457.

- _describe_failure (function, lines 103-108): CHUNK_ID = src/engines/orchestrator.py#103-108#10e2649d — [[F:src/engines/orchestrator.py#103-108#10e2649d]].
- _engine_row (function, lines 111-123): CHUNK_ID = src/engines/orchestrator.py#111-123#10e2649d — [[F:src/engines/orchestrator.py#111-123#10e2649d]].
- _publish_cycle (function, lines 126-169): CHUNK_ID = src/engines/orchestrator.py#126-169#10e2649d — [[F:src/engines/orchestrator.py#126-169#10e2649d]].
- EngineRunStats (class, lines 173-209): CHUNK_ID = src/engines/orchestrator.py#173-209#10e2649d — [[F:src/engines/orchestrator.py#173-209#10e2649d]].
- EngineRunStats.record (method, lines 188-198): CHUNK_ID = src/engines/orchestrator.py#188-198#10e2649d — [[F:src/engines/orchestrator.py#188-198#10e2649d]].
- EngineRunStats.snapshot (method, lines 200-209): CHUNK_ID = src/engines/orchestrator.py#200-209#10e2649d — [[F:src/engines/orchestrator.py#200-209#10e2649d]].
- OrchestratorResult (class, lines 213-220): CHUNK_ID = src/engines/orchestrator.py#213-220#10e2649d — [[F:src/engines/orchestrator.py#213-220#10e2649d]].
- EngineOrchestrator (class, lines 223-260, slice 1): CHUNK_ID = src/engines/orchestrator.py#223-260#10e2649d — [[F:src/engines/orchestrator.py#223-260#10e2649d]].
- EngineOrchestrator (class, lines 261-298, slice 2): CHUNK_ID = src/engines/orchestrator.py#261-298#10e2649d — [[F:src/engines/orchestrator.py#261-298#10e2649d]].
- EngineOrchestrator (class, lines 299-336, slice 3): CHUNK_ID = src/engines/orchestrator.py#299-336#10e2649d — [[F:src/engines/orchestrator.py#299-336#10e2649d]].
- EngineOrchestrator (class, lines 337-374, slice 4): CHUNK_ID = src/engines/orchestrator.py#337-374#10e2649d — [[F:src/engines/orchestrator.py#337-374#10e2649d]].
- EngineOrchestrator (class, lines 375-412, slice 5): CHUNK_ID = src/engines/orchestrator.py#375-412#10e2649d — [[F:src/engines/orchestrator.py#375-412#10e2649d]].
- EngineOrchestrator (class, lines 413-450, slice 6): CHUNK_ID = src/engines/orchestrator.py#413-450#10e2649d — [[F:src/engines/orchestrator.py#413-450#10e2649d]].
- EngineOrchestrator (class, lines 451-457, slice 7): CHUNK_ID = src/engines/orchestrator.py#451-457#10e2649d — [[F:src/engines/orchestrator.py#451-457#10e2649d]].
- EngineOrchestrator.__init__ (method, lines 224-250): CHUNK_ID = src/engines/orchestrator.py#224-250#10e2649d — [[F:src/engines/orchestrator.py#224-250#10e2649d]].
- EngineOrchestrator.engine_roster (method, lines 252-257): CHUNK_ID = src/engines/orchestrator.py#252-257#10e2649d — [[F:src/engines/orchestrator.py#252-257#10e2649d]].
- EngineOrchestrator.stage_roster (method, lines 259-269): CHUNK_ID = src/engines/orchestrator.py#259-269#10e2649d — [[F:src/engines/orchestrator.py#259-269#10e2649d]].
- EngineOrchestrator.cache_inputs (method, lines 272-274): CHUNK_ID = src/engines/orchestrator.py#272-274#10e2649d — [[F:src/engines/orchestrator.py#272-274#10e2649d]].
- EngineOrchestrator.stage_inputs (method, lines 277-279): CHUNK_ID = src/engines/orchestrator.py#277-279#10e2649d — [[F:src/engines/orchestrator.py#277-279#10e2649d]].
- EngineOrchestrator.engine_health (method, lines 281-283): CHUNK_ID = src/engines/orchestrator.py#281-283#10e2649d — [[F:src/engines/orchestrator.py#281-283#10e2649d]].
- EngineOrchestrator._timed (method, lines 286-293): CHUNK_ID = src/engines/orchestrator.py#286-293#10e2649d — [[F:src/engines/orchestrator.py#286-293#10e2649d]].
- EngineOrchestrator._stage (method, lines 295-306): CHUNK_ID = src/engines/orchestrator.py#295-306#10e2649d — [[F:src/engines/orchestrator.py#295-306#10e2649d]].
- EngineOrchestrator.run (method, lines 308-345, slice 1): CHUNK_ID = src/engines/orchestrator.py#308-345#10e2649d — [[F:src/engines/orchestrator.py#308-345#10e2649d]].
- EngineOrchestrator.run (method, lines 346-383, slice 2): CHUNK_ID = src/engines/orchestrator.py#346-383#10e2649d — [[F:src/engines/orchestrator.py#346-383#10e2649d]].
- EngineOrchestrator.run (method, lines 384-421, slice 3): CHUNK_ID = src/engines/orchestrator.py#384-421#10e2649d — [[F:src/engines/orchestrator.py#384-421#10e2649d]].
- EngineOrchestrator.run (method, lines 422-428, slice 4): CHUNK_ID = src/engines/orchestrator.py#422-428#10e2649d — [[F:src/engines/orchestrator.py#422-428#10e2649d]].
- EngineOrchestrator._log_engine_outputs (method, lines 430-457): CHUNK_ID = src/engines/orchestrator.py#430-457#10e2649d — [[F:src/engines/orchestrator.py#430-457#10e2649d]].

## frontend/src/App.jsx

SHA8 babdff7e; AST parse unavailable near line 65: unterminated string literal (detected at line 65). Use bounded textual slices.

## frontend/src/hooks/useApi.js

SHA8 79cc9d3c; AST parse unavailable near line 1: invalid syntax. Use bounded textual slices.

## frontend/src/terminal/client.js

SHA8 97805d86; AST parse unavailable near line 8: unterminated string literal (detected at line 8). Use bounded textual slices.

## frontend/electron/main.cjs

SHA8 2846114f; AST parse unavailable near line 1: invalid character '—' (U+2014). Use bounded textual slices.

## frontend/electron/terminalBridge.cjs

SHA8 df9b68c6; AST parse unavailable near line 11: leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers. Use bounded textual slices.

## tests/test_engine_seam_contract.py

SHA8 fd684c46; total lines 205.

- _engine_modules (function, lines 50-56): CHUNK_ID = tests/test_engine_seam_contract.py#50-56#fd684c46 — [[F:tests/test_engine_seam_contract.py#50-56#fd684c46]].
- engine_modules (function, lines 60-61): CHUNK_ID = tests/test_engine_seam_contract.py#60-61#fd684c46 — [[F:tests/test_engine_seam_contract.py#60-61#fd684c46]].
- orchestrator (function, lines 65-68): CHUNK_ID = tests/test_engine_seam_contract.py#65-68#fd684c46 — [[F:tests/test_engine_seam_contract.py#65-68#fd684c46]].
- _engine_class (function, lines 71-79): CHUNK_ID = tests/test_engine_seam_contract.py#71-79#fd684c46 — [[F:tests/test_engine_seam_contract.py#71-79#fd684c46]].
- _assert_contract (function, lines 82-100): CHUNK_ID = tests/test_engine_seam_contract.py#82-100#fd684c46 — [[F:tests/test_engine_seam_contract.py#82-100#fd684c46]].
- TestTheProducerSide (class, lines 103-147): CHUNK_ID = tests/test_engine_seam_contract.py#103-147#fd684c46 — [[F:tests/test_engine_seam_contract.py#103-147#fd684c46]].
- TestTheProducerSide.test_there_are_exactly_eighteen_engine_modules (method, lines 104-113): CHUNK_ID = tests/test_engine_seam_contract.py#104-113#fd684c46 — [[F:tests/test_engine_seam_contract.py#104-113#fd684c46]].
- TestTheProducerSide.test_the_declared_id_matches_the_filename (method, lines 116-124): CHUNK_ID = tests/test_engine_seam_contract.py#116-124#fd684c46 — [[F:tests/test_engine_seam_contract.py#116-124#fd684c46]].
- TestTheProducerSide.test_every_engine_offers_the_same_call (method, lines 127-137): CHUNK_ID = tests/test_engine_seam_contract.py#127-137#fd684c46 — [[F:tests/test_engine_seam_contract.py#127-137#fd684c46]].
- TestTheProducerSide.test_an_engine_given_nothing_still_honours_the_contract (method, lines 140-147): CHUNK_ID = tests/test_engine_seam_contract.py#140-147#fd684c46 — [[F:tests/test_engine_seam_contract.py#140-147#fd684c46]].
- TestTheConsumerSide (class, lines 150-173): CHUNK_ID = tests/test_engine_seam_contract.py#150-173#fd684c46 — [[F:tests/test_engine_seam_contract.py#150-173#fd684c46]].
- TestTheConsumerSide.test_the_composition_root_registers_every_engine (method, lines 151-153): CHUNK_ID = tests/test_engine_seam_contract.py#151-153#fd684c46 — [[F:tests/test_engine_seam_contract.py#151-153#fd684c46]].
- TestTheConsumerSide.test_position_in_the_list_agrees_with_the_engine_it_holds (method, lines 155-165): CHUNK_ID = tests/test_engine_seam_contract.py#155-165#fd684c46 — [[F:tests/test_engine_seam_contract.py#155-165#fd684c46]].
- TestTheConsumerSide.test_every_engine_has_an_sla_and_every_sla_an_engine (method, lines 167-173): CHUNK_ID = tests/test_engine_seam_contract.py#167-173#fd684c46 — [[F:tests/test_engine_seam_contract.py#167-173#fd684c46]].
- TestTheSeamEndToEnd (class, lines 176-205): CHUNK_ID = tests/test_engine_seam_contract.py#176-205#fd684c46 — [[F:tests/test_engine_seam_contract.py#176-205#fd684c46]].
- TestTheSeamEndToEnd.test_a_cycle_accounts_for_every_engine (method, lines 177-192): CHUNK_ID = tests/test_engine_seam_contract.py#177-192#fd684c46 — [[F:tests/test_engine_seam_contract.py#177-192#fd684c46]].
- TestTheSeamEndToEnd.test_nothing_is_dropped_and_nothing_is_duplicated (method, lines 194-196): CHUNK_ID = tests/test_engine_seam_contract.py#194-196#fd684c46 — [[F:tests/test_engine_seam_contract.py#194-196#fd684c46]].
- TestTheSeamEndToEnd.test_every_output_that_reaches_consensus_honours_the_contract (method, lines 198-205): CHUNK_ID = tests/test_engine_seam_contract.py#198-205#fd684c46 — [[F:tests/test_engine_seam_contract.py#198-205#fd684c46]].

## tests/terminal/test_terminal_protocol.py

SHA8 57c8c650; total lines 161.

- _code (function, lines 24-27): CHUNK_ID = tests/terminal/test_terminal_protocol.py#24-27#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#24-27#57c8c650]].
- TestFrames (class, lines 30-58): CHUNK_ID = tests/terminal/test_terminal_protocol.py#30-58#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#30-58#57c8c650]].
- TestFrames.test_a_well_formed_frame_is_returned_as_a_dict (method, lines 31-32): CHUNK_ID = tests/terminal/test_terminal_protocol.py#31-32#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#31-32#57c8c650]].
- TestFrames.test_bytes_are_accepted_too (method, lines 34-35): CHUNK_ID = tests/terminal/test_terminal_protocol.py#34-35#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#34-35#57c8c650]].
- TestFrames.test_a_bad_frame_is_refused_with_a_stable_code (method, lines 51-52): CHUNK_ID = tests/terminal/test_terminal_protocol.py#51-52#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#51-52#57c8c650]].
- TestFrames.test_encode_round_trips_unicode_without_escaping (method, lines 54-55): CHUNK_ID = tests/terminal/test_terminal_protocol.py#54-55#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#54-55#57c8c650]].
- TestFrames.test_output_is_base64 (method, lines 57-58): CHUNK_ID = tests/terminal/test_terminal_protocol.py#57-58#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#57-58#57c8c650]].
- TestIdentifiers (class, lines 61-78): CHUNK_ID = tests/terminal/test_terminal_protocol.py#61-78#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#61-78#57c8c650]].
- TestIdentifiers.test_new_ids_have_the_validated_shape (method, lines 62-64): CHUNK_ID = tests/terminal/test_terminal_protocol.py#62-64#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#62-64#57c8c650]].
- TestIdentifiers.test_a_malformed_session_id_is_refused (method, lines 67-68): CHUNK_ID = tests/terminal/test_terminal_protocol.py#67-68#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#67-68#57c8c650]].
- TestIdentifiers.test_a_well_formed_session_id_passes (method, lines 70-71): CHUNK_ID = tests/terminal/test_terminal_protocol.py#70-71#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#70-71#57c8c650]].
- TestIdentifiers.test_a_malformed_process_id_is_refused (method, lines 74-75): CHUNK_ID = tests/terminal/test_terminal_protocol.py#74-75#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#74-75#57c8c650]].
- TestIdentifiers.test_a_well_formed_process_id_passes (method, lines 77-78): CHUNK_ID = tests/terminal/test_terminal_protocol.py#77-78#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#77-78#57c8c650]].
- TestFields (class, lines 81-109): CHUNK_ID = tests/terminal/test_terminal_protocol.py#81-109#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#81-109#57c8c650]].
- TestFields.test_bounded_int_takes_the_default_when_absent (method, lines 82-83): CHUNK_ID = tests/terminal/test_terminal_protocol.py#82-83#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#82-83#57c8c650]].
- TestFields.test_bounded_int_refuses_missing_or_out_of_range (method, lines 88-89): CHUNK_ID = tests/terminal/test_terminal_protocol.py#88-89#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#88-89#57c8c650]].
- TestFields.test_offsets (method, lines 91-95): CHUNK_ID = tests/terminal/test_terminal_protocol.py#91-95#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#91-95#57c8c650]].
- TestFields.test_text_fields_are_bounded (method, lines 97-100): CHUNK_ID = tests/terminal/test_terminal_protocol.py#97-100#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#97-100#57c8c650]].
- TestFields.test_a_name_must_be_short_printable_text (method, lines 103-104): CHUNK_ID = tests/terminal/test_terminal_protocol.py#103-104#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#103-104#57c8c650]].
- TestFields.test_a_name_is_trimmed (method, lines 106-109): CHUNK_ID = tests/terminal/test_terminal_protocol.py#106-109#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#106-109#57c8c650]].
- TestArgvAndCwd (class, lines 112-131): CHUNK_ID = tests/terminal/test_terminal_protocol.py#112-131#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#112-131#57c8c650]].
- TestArgvAndCwd.test_argv_is_passed_through_as_a_list (method, lines 113-118): CHUNK_ID = tests/terminal/test_terminal_protocol.py#113-118#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#113-118#57c8c650]].
- TestArgvAndCwd.test_anything_but_a_list_of_clean_strings_is_refused (method, lines 124-125): CHUNK_ID = tests/terminal/test_terminal_protocol.py#124-125#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#124-125#57c8c650]].
- TestArgvAndCwd.test_cwd_defaults_and_must_be_an_existing_absolute_directory (method, lines 127-131): CHUNK_ID = tests/terminal/test_terminal_protocol.py#127-131#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#127-131#57c8c650]].
- TestSignals (class, lines 134-156): CHUNK_ID = tests/terminal/test_terminal_protocol.py#134-156#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#134-156#57c8c650]].
- TestSignals.test_the_four_terminal_signals (method, lines 144-145): CHUNK_ID = tests/terminal/test_terminal_protocol.py#144-145#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#144-145#57c8c650]].
- TestSignals.test_the_default_applies_when_absent (method, lines 147-148): CHUNK_ID = tests/terminal/test_terminal_protocol.py#147-148#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#147-148#57c8c650]].
- TestSignals.test_any_other_signal_is_refused (method, lines 151-152): CHUNK_ID = tests/terminal/test_terminal_protocol.py#151-152#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#151-152#57c8c650]].
- TestSignals.test_the_signal_table_cannot_be_extended_at_runtime (method, lines 154-156): CHUNK_ID = tests/terminal/test_terminal_protocol.py#154-156#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#154-156#57c8c650]].
- test_job_registration_is_not_a_client_request (function, lines 159-161): CHUNK_ID = tests/terminal/test_terminal_protocol.py#159-161#57c8c650 — [[F:tests/terminal/test_terminal_protocol.py#159-161#57c8c650]].

## tests/terminal/test_terminal_server.py

SHA8 1537322c; total lines 514.

- _output (function, lines 44-46): CHUNK_ID = tests/terminal/test_terminal_server.py#44-46#1537322c — [[F:tests/terminal/test_terminal_server.py#44-46#1537322c]].
- _collect_output (function, lines 49-54): CHUNK_ID = tests/terminal/test_terminal_server.py#49-54#1537322c — [[F:tests/terminal/test_terminal_server.py#49-54#1537322c]].
- finished (function, lines 57-58): CHUNK_ID = tests/terminal/test_terminal_server.py#57-58#1537322c — [[F:tests/terminal/test_terminal_server.py#57-58#1537322c]].
- session_event (function, lines 61-62): CHUNK_ID = tests/terminal/test_terminal_server.py#61-62#1537322c — [[F:tests/terminal/test_terminal_server.py#61-62#1537322c]].
- foreground_sleep (function, lines 65-78): CHUNK_ID = tests/terminal/test_terminal_server.py#65-78#1537322c — [[F:tests/terminal/test_terminal_server.py#65-78#1537322c]].
- _error_code (function, lines 81-83): CHUNK_ID = tests/terminal/test_terminal_server.py#81-83#1537322c — [[F:tests/terminal/test_terminal_server.py#81-83#1537322c]].
- TestHello (class, lines 86-123, slice 1): CHUNK_ID = tests/terminal/test_terminal_server.py#86-123#1537322c — [[F:tests/terminal/test_terminal_server.py#86-123#1537322c]].
- TestHello (class, lines 124-156, slice 2): CHUNK_ID = tests/terminal/test_terminal_server.py#124-156#1537322c — [[F:tests/terminal/test_terminal_server.py#124-156#1537322c]].
- TestHello.test_hello_returns_a_welcome_and_a_snapshot (method, lines 87-95): CHUNK_ID = tests/terminal/test_terminal_server.py#87-95#1537322c — [[F:tests/terminal/test_terminal_server.py#87-95#1537322c]].
- TestHello.test_the_welcome_describes_the_daemon (method, lines 97-106): CHUNK_ID = tests/terminal/test_terminal_server.py#97-106#1537322c — [[F:tests/terminal/test_terminal_server.py#97-106#1537322c]].
- TestHello.test_a_bad_first_frame_closes_the_connection (method, lines 115-120): CHUNK_ID = tests/terminal/test_terminal_server.py#115-120#1537322c — [[F:tests/terminal/test_terminal_server.py#115-120#1537322c]].
- TestHello.test_a_bad_client_kind_is_refused_but_hello_can_be_retried (method, lines 122-132): CHUNK_ID = tests/terminal/test_terminal_server.py#122-132#1537322c — [[F:tests/terminal/test_terminal_server.py#122-132#1537322c]].
- TestHello.test_malformed_frames_are_answered_not_fatal (method, lines 134-148): CHUNK_ID = tests/terminal/test_terminal_server.py#134-148#1537322c — [[F:tests/terminal/test_terminal_server.py#134-148#1537322c]].
- TestHello.test_an_oversized_frame_ends_the_connection (method, lines 150-156): CHUNK_ID = tests/terminal/test_terminal_server.py#150-156#1537322c — [[F:tests/terminal/test_terminal_server.py#150-156#1537322c]].
- TestSharedSessions (class, lines 159-196, slice 1): CHUNK_ID = tests/terminal/test_terminal_server.py#159-196#1537322c — [[F:tests/terminal/test_terminal_server.py#159-196#1537322c]].
- TestSharedSessions (class, lines 197-234, slice 2): CHUNK_ID = tests/terminal/test_terminal_server.py#197-234#1537322c — [[F:tests/terminal/test_terminal_server.py#197-234#1537322c]].
- TestSharedSessions (class, lines 235-254, slice 3): CHUNK_ID = tests/terminal/test_terminal_server.py#235-254#1537322c — [[F:tests/terminal/test_terminal_server.py#235-254#1537322c]].
- TestSharedSessions.test_two_clients_see_one_set_of_sessions (method, lines 160-197, slice 1): CHUNK_ID = tests/terminal/test_terminal_server.py#160-197#1537322c — [[F:tests/terminal/test_terminal_server.py#160-197#1537322c]].
- TestSharedSessions.test_two_clients_see_one_set_of_sessions (method, lines 198-212, slice 2): CHUNK_ID = tests/terminal/test_terminal_server.py#198-212#1537322c — [[F:tests/terminal/test_terminal_server.py#198-212#1537322c]].
- TestSharedSessions.test_running_output_signals_and_kill (method, lines 214-241): CHUNK_ID = tests/terminal/test_terminal_server.py#214-241#1537322c — [[F:tests/terminal/test_terminal_server.py#214-241#1537322c]].
- TestSharedSessions.test_a_job_and_its_result (method, lines 243-254): CHUNK_ID = tests/terminal/test_terminal_server.py#243-254#1537322c — [[F:tests/terminal/test_terminal_server.py#243-254#1537322c]].
- TestJobRegistration (class, lines 257-295): CHUNK_ID = tests/terminal/test_terminal_server.py#257-295#1537322c — [[F:tests/terminal/test_terminal_server.py#257-295#1537322c]].
- TestJobRegistration.test_an_application_job_runs_through_the_registry (method, lines 258-285): CHUNK_ID = tests/terminal/test_terminal_server.py#258-285#1537322c — [[F:tests/terminal/test_terminal_server.py#258-285#1537322c]].
- TestJobRegistration.test_job_requests_cannot_touch_terminal_processes (method, lines 287-295): CHUNK_ID = tests/terminal/test_terminal_server.py#287-295#1537322c — [[F:tests/terminal/test_terminal_server.py#287-295#1537322c]].
- TestConnectionLimits (class, lines 298-326): CHUNK_ID = tests/terminal/test_terminal_server.py#298-326#1537322c — [[F:tests/terminal/test_terminal_server.py#298-326#1537322c]].
- TestConnectionLimits.test_beyond_the_client_limit_a_connection_is_refused (method, lines 299-309): CHUNK_ID = tests/terminal/test_terminal_server.py#299-309#1537322c — [[F:tests/terminal/test_terminal_server.py#299-309#1537322c]].
- TestConnectionLimits.test_a_silent_connection_is_dropped (method, lines 311-321): CHUNK_ID = tests/terminal/test_terminal_server.py#311-321#1537322c — [[F:tests/terminal/test_terminal_server.py#311-321#1537322c]].
- TestConnectionLimits.test_a_peer_running_as_another_user_is_refused (method, lines 323-326): CHUNK_ID = tests/terminal/test_terminal_server.py#323-326#1537322c — [[F:tests/terminal/test_terminal_server.py#323-326#1537322c]].
- TestLifecycle (class, lines 329-370): CHUNK_ID = tests/terminal/test_terminal_server.py#329-370#1537322c — [[F:tests/terminal/test_terminal_server.py#329-370#1537322c]].
- TestLifecycle.test_stopping_ends_every_session_and_removes_files (method, lines 330-341): CHUNK_ID = tests/terminal/test_terminal_server.py#330-341#1537322c — [[F:tests/terminal/test_terminal_server.py#330-341#1537322c]].
- TestLifecycle.test_a_second_daemon_is_refused (method, lines 343-345): CHUNK_ID = tests/terminal/test_terminal_server.py#343-345#1537322c — [[F:tests/terminal/test_terminal_server.py#343-345#1537322c]].
- TestLifecycle.test_root_is_refused_unless_allowed (method, lines 347-350): CHUNK_ID = tests/terminal/test_terminal_server.py#347-350#1537322c — [[F:tests/terminal/test_terminal_server.py#347-350#1537322c]].
- TestLifecycle.test_the_websocket_listener_binds_loopback_only (method, lines 352-360): CHUNK_ID = tests/terminal/test_terminal_server.py#352-360#1537322c — [[F:tests/terminal/test_terminal_server.py#352-360#1537322c]].
- TestLifecycle.test_a_failed_background_task_is_logged_not_raised (method, lines 362-370): CHUNK_ID = tests/terminal/test_terminal_server.py#362-370#1537322c — [[F:tests/terminal/test_terminal_server.py#362-370#1537322c]].
- FakeWebSocket (class, lines 373-396): CHUNK_ID = tests/terminal/test_terminal_server.py#373-396#1537322c — [[F:tests/terminal/test_terminal_server.py#373-396#1537322c]].
- FakeWebSocket.__init__ (method, lines 376-380): CHUNK_ID = tests/terminal/test_terminal_server.py#376-380#1537322c — [[F:tests/terminal/test_terminal_server.py#376-380#1537322c]].
- FakeWebSocket.__aiter__ (method, lines 382-383): CHUNK_ID = tests/terminal/test_terminal_server.py#382-383#1537322c — [[F:tests/terminal/test_terminal_server.py#382-383#1537322c]].
- FakeWebSocket.__anext__ (method, lines 385-390): CHUNK_ID = tests/terminal/test_terminal_server.py#385-390#1537322c — [[F:tests/terminal/test_terminal_server.py#385-390#1537322c]].
- FakeWebSocket.send (method, lines 392-393): CHUNK_ID = tests/terminal/test_terminal_server.py#392-393#1537322c — [[F:tests/terminal/test_terminal_server.py#392-393#1537322c]].
- FakeWebSocket.close (method, lines 395-396): CHUNK_ID = tests/terminal/test_terminal_server.py#395-396#1537322c — [[F:tests/terminal/test_terminal_server.py#395-396#1537322c]].
- FakeHandshake (class, lines 399-401): CHUNK_ID = tests/terminal/test_terminal_server.py#399-401#1537322c — [[F:tests/terminal/test_terminal_server.py#399-401#1537322c]].
- FakeHandshake.respond (method, lines 400-401): CHUNK_ID = tests/terminal/test_terminal_server.py#400-401#1537322c — [[F:tests/terminal/test_terminal_server.py#400-401#1537322c]].
- ws_server (function, lines 405-409): CHUNK_ID = tests/terminal/test_terminal_server.py#405-409#1537322c — [[F:tests/terminal/test_terminal_server.py#405-409#1537322c]].
- _request (function, lines 412-413): CHUNK_ID = tests/terminal/test_terminal_server.py#412-413#1537322c — [[F:tests/terminal/test_terminal_server.py#412-413#1537322c]].
- _hello (function, lines 416-420): CHUNK_ID = tests/terminal/test_terminal_server.py#416-420#1537322c — [[F:tests/terminal/test_terminal_server.py#416-420#1537322c]].
- TestWebSocket (class, lines 427-464, slice 1): CHUNK_ID = tests/terminal/test_terminal_server.py#427-464#1537322c — [[F:tests/terminal/test_terminal_server.py#427-464#1537322c]].
- TestWebSocket (class, lines 465-474, slice 2): CHUNK_ID = tests/terminal/test_terminal_server.py#465-474#1537322c — [[F:tests/terminal/test_terminal_server.py#465-474#1537322c]].
- TestWebSocket.test_the_dashboard_origin_on_loopback_is_admitted (method, lines 436-437): CHUNK_ID = tests/terminal/test_terminal_server.py#436-437#1537322c — [[F:tests/terminal/test_terminal_server.py#436-437#1537322c]].
- TestWebSocket.test_anything_else_is_refused_before_the_socket_opens (method, lines 451-452): CHUNK_ID = tests/terminal/test_terminal_server.py#451-452#1537322c — [[F:tests/terminal/test_terminal_server.py#451-452#1537322c]].
- TestWebSocket.test_a_browser_needs_the_token (method, lines 454-474): CHUNK_ID = tests/terminal/test_terminal_server.py#454-474#1537322c — [[F:tests/terminal/test_terminal_server.py#454-474#1537322c]].
- _never (function, lines 477-479): CHUNK_ID = tests/terminal/test_terminal_server.py#477-479#1537322c — [[F:tests/terminal/test_terminal_server.py#477-479#1537322c]].
- TestClientConnection (class, lines 482-514): CHUNK_ID = tests/terminal/test_terminal_server.py#482-514#1537322c — [[F:tests/terminal/test_terminal_server.py#482-514#1537322c]].
- TestClientConnection.test_a_client_that_cannot_keep_up_is_cut_off (method, lines 483-501): CHUNK_ID = tests/terminal/test_terminal_server.py#483-501#1537322c — [[F:tests/terminal/test_terminal_server.py#483-501#1537322c]].
- TestClientConnection.test_a_dead_transport_ends_the_loop (method, lines 503-514): CHUNK_ID = tests/terminal/test_terminal_server.py#503-514#1537322c — [[F:tests/terminal/test_terminal_server.py#503-514#1537322c]].

## Additional non-Python source slices

Python AST parsing is not valid for JSX, JavaScript, YAML or Markdown. These ranges provide bounded navigation anchors for the frontend, workflow and architecture docs. Inspect declarations around each anchor before changing behavior.

### frontend/src/App.jsx

SHA8 babdff7e; total lines 470.

- CHUNK_ID = frontend/src/App.jsx#1-38#babdff7e — [[F:frontend/src/App.jsx#1-38#babdff7e]].
- CHUNK_ID = frontend/src/App.jsx#39-76#babdff7e — [[F:frontend/src/App.jsx#39-76#babdff7e]] declarations nearby: REGIME_COLOR, REGIME_NAME, SPEC_BY_ID, App, Dashboard.
- CHUNK_ID = frontend/src/App.jsx#77-114#babdff7e — [[F:frontend/src/App.jsx#77-114#babdff7e]] declarations nearby: onEvent, status, readiness, equityCurve, trades.
- CHUNK_ID = frontend/src/App.jsx#115-152#babdff7e — [[F:frontend/src/App.jsx#115-152#babdff7e]] declarations nearby: riskControls, modelsStatus, handleModeSwitch, handleRiskUpdate, handleApprovalResolve.
- CHUNK_ID = frontend/src/App.jsx#153-190#babdff7e — [[F:frontend/src/App.jsx#153-190#babdff7e]] declarations nearby: activeTimeframes, equity, dailyPnl, positions, regime.
- CHUNK_ID = frontend/src/App.jsx#191-228#babdff7e — [[F:frontend/src/App.jsx#191-228#babdff7e]] declarations nearby: renderPanel, spec, panel, item.
- CHUNK_ID = frontend/src/App.jsx#229-266#babdff7e — [[F:frontend/src/App.jsx#229-266#babdff7e]] declarations nearby: hiddenCount.
- CHUNK_ID = frontend/src/App.jsx#267-304#babdff7e — [[F:frontend/src/App.jsx#267-304#babdff7e]].
- CHUNK_ID = frontend/src/App.jsx#305-342#babdff7e — [[F:frontend/src/App.jsx#305-342#babdff7e]] declarations nearby: Header.
- CHUNK_ID = frontend/src/App.jsx#343-380#babdff7e — [[F:frontend/src/App.jsx#343-380#babdff7e]].
- CHUNK_ID = frontend/src/App.jsx#381-418#babdff7e — [[F:frontend/src/App.jsx#381-418#babdff7e]] declarations nearby: StatsRow, regimeState, regimeColor, regimeName.
- CHUNK_ID = frontend/src/App.jsx#419-456#babdff7e — [[F:frontend/src/App.jsx#419-456#babdff7e]] declarations nearby: PanelManager, visible.
- CHUNK_ID = frontend/src/App.jsx#457-470#babdff7e — [[F:frontend/src/App.jsx#457-470#babdff7e]].

### frontend/src/hooks/useApi.js

SHA8 79cc9d3c; total lines 463.

- CHUNK_ID = frontend/src/hooks/useApi.js#1-38#79cc9d3c — [[F:frontend/src/hooks/useApi.js#1-38#79cc9d3c]] declarations nearby:_RAW_API, API_KEY, _ALLOWED_API_RE, API, WS_URL.
- CHUNK_ID = frontend/src/hooks/useApi.js#39-76#79cc9d3c — [[F:frontend/src/hooks/useApi.js#39-76#79cc9d3c]] declarations nearby: err,_topicListeners, _emit, listeners,_resyncListeners.
- CHUNK_ID = frontend/src/hooks/useApi.js#77-114#79cc9d3c — [[F:frontend/src/hooks/useApi.js#77-114#79cc9d3c]] declarations nearby:_liveSocket, _sendSubscribe, topics.
- CHUNK_ID = frontend/src/hooks/useApi.js#115-152#79cc9d3c — [[F:frontend/src/hooks/useApi.js#115-152#79cc9d3c]] declarations nearby: RECONNECT_BASE_MS, RECONNECT_CAP_MS, reconnectDelay, backoff, useWebSocket.
- CHUNK_ID = frontend/src/hooks/useApi.js#153-190#79cc9d3c — [[F:frontend/src/hooks/useApi.js#153-190#79cc9d3c]] declarations nearby: connect, wsUrl, ws, wasReconnect, msg.
- CHUNK_ID = frontend/src/hooks/useApi.js#191-228#79cc9d3c — [[F:frontend/src/hooks/useApi.js#191-228#79cc9d3c]].
- CHUNK_ID = frontend/src/hooks/useApi.js#229-266#79cc9d3c — [[F:frontend/src/hooks/useApi.js#229-266#79cc9d3c]] declarations nearby: useStream, transformRef, applyRef, refetchRef, cancelled.
- CHUNK_ID = frontend/src/hooks/useApi.js#267-304#79cc9d3c — [[F:frontend/src/hooks/useApi.js#267-304#79cc9d3c]] declarations nearby: isNewTopic, API_ORIGIN.
- CHUNK_ID = frontend/src/hooks/useApi.js#305-342#79cc9d3c — [[F:frontend/src/hooks/useApi.js#305-342#79cc9d3c]] declarations nearby: apiProblem.
- CHUNK_ID = frontend/src/hooks/useApi.js#343-380#79cc9d3c — [[F:frontend/src/hooks/useApi.js#343-380#79cc9d3c]] declarations nearby: useApiResource, transformRef, live, inFlight, poll.
- CHUNK_ID = frontend/src/hooks/useApi.js#381-418#79cc9d3c — [[F:frontend/src/hooks/useApi.js#381-418#79cc9d3c]] declarations nearby: useReadiness, usePolling, transformRef, inFlight, poll.
- CHUNK_ID = frontend/src/hooks/useApi.js#419-456#79cc9d3c — [[F:frontend/src/hooks/useApi.js#419-456#79cc9d3c]] declarations nearby: body, fn, id, useOperatorAction, action.
- CHUNK_ID = frontend/src/hooks/useApi.js#457-463#79cc9d3c — [[F:frontend/src/hooks/useApi.js#457-463#79cc9d3c]].

### frontend/src/terminal/client.js

SHA8 97805d86; total lines 326.

- CHUNK_ID = frontend/src/terminal/client.js#1-38#97805d86 — [[F:frontend/src/terminal/client.js#1-38#97805d86]] declarations nearby: PROTOCOL_VERSION, TOKEN_STORAGE_KEY, DEFAULT_WS_URL, _LOOPBACK_WS_RE, decodeBase64.
- CHUNK_ID = frontend/src/terminal/client.js#39-76#97805d86 — [[F:frontend/src/terminal/client.js#39-76#97805d86]] declarations nearby: createWebSocketTransport, socket, frame, createIpcTransport, unsubscribe.
- CHUNK_ID = frontend/src/terminal/client.js#77-114#97805d86 — [[F:frontend/src/terminal/client.js#77-114#97805d86]] declarations nearby: result, TerminalClient.
- CHUNK_ID = frontend/src/terminal/client.js#115-152#97805d86 — [[F:frontend/src/terminal/client.js#115-152#97805d86]] declarations nearby: transport.
- CHUNK_ID = frontend/src/terminal/client.js#153-190#97805d86 — [[F:frontend/src/terminal/client.js#153-190#97805d86]] declarations nearby: welcome.
- CHUNK_ID = frontend/src/terminal/client.js#191-228#97805d86 — [[F:frontend/src/terminal/client.js#191-228#97805d86]] declarations nearby: error, live.
- CHUNK_ID = frontend/src/terminal/client.js#229-266#97805d86 — [[F:frontend/src/terminal/client.js#229-266#97805d86]] declarations nearby: bytes, offset, expected, delay, error.
- CHUNK_ID = frontend/src/terminal/client.js#267-304#97805d86 — [[F:frontend/src/terminal/client.js#267-304#97805d86]] declarations nearby: error, error, id, timer, error.
- CHUNK_ID = frontend/src/terminal/client.js#305-326#97805d86 — [[F:frontend/src/terminal/client.js#305-326#97805d86]] declarations nearby: reply.

### frontend/src/components/workspace/Workspace.jsx

SHA8 e63a327a; total lines 119.

- CHUNK_ID = frontend/src/components/workspace/Workspace.jsx#1-38#e63a327a — [[F:frontend/src/components/workspace/Workspace.jsx#1-38#e63a327a]] declarations nearby: DRAG_HANDLE, DRAG_CANCEL, STACK_BELOW_PX, Workspace, stacked.
- CHUNK_ID = frontend/src/components/workspace/Workspace.jsx#39-76#e63a327a — [[F:frontend/src/components/workspace/Workspace.jsx#39-76#e63a327a]] declarations nearby: measure, r, top, bottom, observer.
- CHUNK_ID = frontend/src/components/workspace/Workspace.jsx#77-114#e63a327a — [[F:frontend/src/components/workspace/Workspace.jsx#77-114#e63a327a]] declarations nearby: interactive, commit.
- CHUNK_ID = frontend/src/components/workspace/Workspace.jsx#115-119#e63a327a — [[F:frontend/src/components/workspace/Workspace.jsx#115-119#e63a327a]].

### frontend/electron/main.cjs

SHA8 2846114f; total lines 166.

- CHUNK_ID = frontend/electron/main.cjs#1-38#2846114f — [[F:frontend/electron/main.cjs#1-38#2846114f]] declarations nearby: path, isDev, REPO_ROOT, terminalBridge, DEV_URL.
- CHUNK_ID = frontend/electron/main.cjs#39-76#2846114f — [[F:frontend/electron/main.cjs#39-76#2846114f]] declarations nearby: createWindow.
- CHUNK_ID = frontend/electron/main.cjs#77-114#2846114f — [[F:frontend/electron/main.cjs#77-114#2846114f]] declarations nearby: trayIconForBadge, iconPath, updateTrayBadge, createTray, menu.
- CHUNK_ID = frontend/electron/main.cjs#115-152#2846114f — [[F:frontend/electron/main.cjs#115-152#2846114f]].
- CHUNK_ID = frontend/electron/main.cjs#153-166#2846114f — [[F:frontend/electron/main.cjs#153-166#2846114f]].

### frontend/electron/terminalBridge.cjs

SHA8 df9b68c6; total lines 221.

- CHUNK_ID = frontend/electron/terminalBridge.cjs#1-38#df9b68c6 — [[F:frontend/electron/terminalBridge.cjs#1-38#df9b68c6]] declarations nearby: fs, net, path, ALLOWED_TYPES, MAX_FRAME_BYTES.
- CHUNK_ID = frontend/electron/terminalBridge.cjs#39-76#df9b68c6 — [[F:frontend/electron/terminalBridge.cjs#39-76#df9b68c6]] declarations nearby: validateFrame, line, resolvePython, venv, runTerminalCli.
- CHUNK_ID = frontend/electron/terminalBridge.cjs#77-114#df9b68c6 — [[F:frontend/electron/terminalBridge.cjs#77-114#df9b68c6]] declarations nearby: ensureService, result, info, TerminalBridge.
- CHUNK_ID = frontend/electron/terminalBridge.cjs#115-152#df9b68c6 — [[F:frontend/electron/terminalBridge.cjs#115-152#df9b68c6]] declarations nearby: service, socket, record, settled, newline.
- CHUNK_ID = frontend/electron/terminalBridge.cjs#153-190#df9b68c6 — [[F:frontend/electron/terminalBridge.cjs#153-190#df9b68c6]] declarations nearby: frame, line, record.
- CHUNK_ID = frontend/electron/terminalBridge.cjs#191-221#df9b68c6 — [[F:frontend/electron/terminalBridge.cjs#191-221#df9b68c6]] declarations nearby: record.

### frontend/package.json

SHA8 397d38f6; total lines 77.

- CHUNK_ID = frontend/package.json#1-38#397d38f6 — [[F:frontend/package.json#1-38#397d38f6]].
- CHUNK_ID = frontend/package.json#39-77#397d38f6 — [[F:frontend/package.json#39-77#397d38f6]].

### .github/workflows/ci.yml

SHA8 1afd1d2e; total lines 408.

- CHUNK_ID = .github/workflows/ci.yml#1-38#1afd1d2e — [[F:.github/workflows/ci.yml#1-38#1afd1d2e]].
- CHUNK_ID = .github/workflows/ci.yml#39-76#1afd1d2e — [[F:.github/workflows/ci.yml#39-76#1afd1d2e]].
- CHUNK_ID = .github/workflows/ci.yml#77-114#1afd1d2e — [[F:.github/workflows/ci.yml#77-114#1afd1d2e]].
- CHUNK_ID = .github/workflows/ci.yml#115-152#1afd1d2e — [[F:.github/workflows/ci.yml#115-152#1afd1d2e]].
- CHUNK_ID = .github/workflows/ci.yml#153-190#1afd1d2e — [[F:.github/workflows/ci.yml#153-190#1afd1d2e]].
- CHUNK_ID = .github/workflows/ci.yml#191-228#1afd1d2e — [[F:.github/workflows/ci.yml#191-228#1afd1d2e]].
- CHUNK_ID = .github/workflows/ci.yml#229-266#1afd1d2e — [[F:.github/workflows/ci.yml#229-266#1afd1d2e]].
- CHUNK_ID = .github/workflows/ci.yml#267-304#1afd1d2e — [[F:.github/workflows/ci.yml#267-304#1afd1d2e]].
- CHUNK_ID = .github/workflows/ci.yml#305-342#1afd1d2e — [[F:.github/workflows/ci.yml#305-342#1afd1d2e]].
- CHUNK_ID = .github/workflows/ci.yml#343-380#1afd1d2e — [[F:.github/workflows/ci.yml#343-380#1afd1d2e]].
- CHUNK_ID = .github/workflows/ci.yml#381-408#1afd1d2e — [[F:.github/workflows/ci.yml#381-408#1afd1d2e]].
### docs/terminal/ARCHITECTURE.md

SHA8 ac1b11e0; total lines 217.

- CHUNK_ID = docs/terminal/ARCHITECTURE.md#1-38#ac1b11e0 — [[F:docs/terminal/ARCHITECTURE.md#1-38#ac1b11e0]].
- CHUNK_ID = docs/terminal/ARCHITECTURE.md#39-76#ac1b11e0 — [[F:docs/terminal/ARCHITECTURE.md#39-76#ac1b11e0]].
- CHUNK_ID = docs/terminal/ARCHITECTURE.md#77-114#ac1b11e0 — [[F:docs/terminal/ARCHITECTURE.md#77-114#ac1b11e0]].
- CHUNK_ID = docs/terminal/ARCHITECTURE.md#115-152#ac1b11e0 — [[F:docs/terminal/ARCHITECTURE.md#115-152#ac1b11e0]].
- CHUNK_ID = docs/terminal/ARCHITECTURE.md#153-190#ac1b11e0 — [[F:docs/terminal/ARCHITECTURE.md#153-190#ac1b11e0]].
- CHUNK_ID = docs/terminal/ARCHITECTURE.md#191-217#ac1b11e0 — [[F:docs/terminal/ARCHITECTURE.md#191-217#ac1b11e0]].

### docs/runtime/RUNTIME_PLATFORM.md

SHA8 37fde0ad; total lines 296.

- CHUNK_ID = docs/runtime/RUNTIME_PLATFORM.md#1-38#37fde0ad — [[F:docs/runtime/RUNTIME_PLATFORM.md#1-38#37fde0ad]].
- CHUNK_ID = docs/runtime/RUNTIME_PLATFORM.md#39-76#37fde0ad — [[F:docs/runtime/RUNTIME_PLATFORM.md#39-76#37fde0ad]].
- CHUNK_ID = docs/runtime/RUNTIME_PLATFORM.md#77-114#37fde0ad — [[F:docs/runtime/RUNTIME_PLATFORM.md#77-114#37fde0ad]].
- CHUNK_ID = docs/runtime/RUNTIME_PLATFORM.md#115-152#37fde0ad — [[F:docs/runtime/RUNTIME_PLATFORM.md#115-152#37fde0ad]].
- CHUNK_ID = docs/runtime/RUNTIME_PLATFORM.md#153-190#37fde0ad — [[F:docs/runtime/RUNTIME_PLATFORM.md#153-190#37fde0ad]].
- CHUNK_ID = docs/runtime/RUNTIME_PLATFORM.md#191-228#37fde0ad — [[F:docs/runtime/RUNTIME_PLATFORM.md#191-228#37fde0ad]].
- CHUNK_ID = docs/runtime/RUNTIME_PLATFORM.md#229-266#37fde0ad — [[F:docs/runtime/RUNTIME_PLATFORM.md#229-266#37fde0ad]].
- CHUNK_ID = docs/runtime/RUNTIME_PLATFORM.md#267-296#37fde0ad — [[F:docs/runtime/RUNTIME_PLATFORM.md#267-296#37fde0ad]].
