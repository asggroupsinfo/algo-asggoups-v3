INFO:Test:🚀 Starting Feature Verification & Simulation
INFO:src.managers.session_manager:Session Manager Initialized (Merged V5 Logic)
INFO:Test:✅ Components Initialized
INFO:Test:--- Test 1: V3 Entry Signal ---
INFO:plugin.v3_combined.orders:Order A: Using V3 Smart SL = 1.10300
INFO:plugin.v3_combined.orders:Order A: Using V3 Extended TP = 1.10900
INFO:plugin.v3_combined.orders:Order B: Using Fixed $10 SL = 1.03389
INFO:src.core.plugin_system.service_api:[ServiceAPI] Order placed: 727509 | EURUSD buy 0.014 lots
INFO:src.core.plugin_system.service_api:[ServiceAPI] Registered single order 727509 in engine
INFO:Test:✅ Signal processed successfully
INFO:Test:Open Trades: 2
INFO:Test:✅ Trade created successfully
INFO:Test:--- Test 2: V3 Exit Signal ---
INFO:plugin.v3_combined:[V3 Exit] Signal: Bearish_Exit | Symbol: EURUSD
INFO:src.core.plugin_system.service_api:[ServiceAPI] Closed 2 BUY positions for EURUSD
INFO:Test:Open Trades after Exit: 0
INFO:Test:✅ Trades closed successfully
INFO:Test:🏁 Simulation Complete
