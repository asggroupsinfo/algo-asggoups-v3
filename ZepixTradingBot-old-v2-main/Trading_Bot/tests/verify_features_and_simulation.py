import sys
import os
import asyncio
import logging
import time
from unittest.mock import MagicMock, AsyncMock

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.clients.mt5_client import MT5Client
from src.managers.risk_manager import RiskManager
from src.core.trading_engine import TradingEngine
from src.processors.alert_processor import AlertProcessor
from src.managers.session_manager import SessionManager
from src.database import TradeDatabase
from src.telegram.core.multi_bot_manager import MultiBotManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Test")

async def main():
    logger.info("🚀 Starting Feature Verification & Simulation")

    # 1. Initialize Config
    config = Config()
    # Force simulation mode
    config.config["simulate_orders"] = True
    config.config["mt5_enabled"] = False

    # 2. Mock MT5 Client
    mt5_client = MT5Client(config)
    if not mt5_client.initialize():
        logger.error("Failed to initialize MT5 Client (Sim)")
        return

    # 3. Initialize Database & Session Manager
    db = TradeDatabase()
    session_manager = SessionManager(config, db, mt5_client)

    # 4. Initialize Risk Manager
    risk_manager = RiskManager(config)
    risk_manager.set_mt5_client(mt5_client)

    # 5. Mock Telegram Manager
    telegram_manager = MagicMock(spec=MultiBotManager)
    telegram_manager.send_message = AsyncMock()
    telegram_manager.send_alert = AsyncMock()
    telegram_manager.session_manager = session_manager

    # 6. Initialize Alert Processor
    alert_processor = AlertProcessor(config, telegram_bot=telegram_manager)

    # 7. Initialize Trading Engine
    trading_engine = TradingEngine(config, risk_manager, mt5_client, telegram_manager, alert_processor)
    trading_engine.session_manager = session_manager

    # --- MOCK MT5 STATE FOR SIMULATION ---
    # We override get_positions to return what the engine thinks is open
    def mock_get_positions(symbol=None):
        positions = []
        for trade in trading_engine.open_trades:
            if symbol and trade.symbol != symbol:
                continue

            # Create a mock position object (MT5 returns objects, not dicts usually, but client converts)
            # The client's get_positions returns list of dicts or objects depending on impl.
            # Looking at code: MT5Client.get_positions returns list of DICTS.
            pos = {
                'ticket': trade.trade_id,
                'volume': trade.lot_size,
                'price_open': trade.entry,
                'sl': trade.sl,
                'tp': trade.tp,
                'profit': 10.0, # Simulate profit
                'comment': f"Simulated_{trade.strategy}",
                'symbol': trade.symbol,
                'type': 0 if trade.direction.upper() == "BUY" else 1
            }
            # MT5Client uses mt5.positions_get which returns named tuples.
            # But the client wraps it? Let's check client code.
            # Client code: result.append({...}) -> returns dicts.
            positions.append(MagicMock(**pos)) # The client code might expect attributes if it calls MT5 directly,
                                               # but here we are patching the CLIENT method or MT5?
                                               # Actually, trading_engine calls mt5_client.get_positions() which returns dicts?
                                               # Wait, trading_engine calls self.mt5_client.get_position(ticket) too.

        # NOTE: MT5Client.get_positions returns list of DICTS.
        # But wait, does TradingEngine use MT5Client.get_positions or direct mt5?
        # TradingEngine uses self.mt5_client.get_position(ticket).
        return positions

    # Override the client methods
    # We need to monkeypatch the INSTANCE methods

    # Patch get_positions (returns list of objects with attributes in simulation usually?)
    # In simulation mode of MT5Client, get_positions returns [].
    # We want it to return our mock list.
    # But MT5Client.get_positions returns dicts.
    # Let's see how TradingEngine uses it.
    # It calls mt5_client.get_position(ticket) in close_trade.

    def mock_get_position(ticket):
        for trade in trading_engine.open_trades:
            if trade.trade_id == ticket:
                return {
                    'ticket': trade.trade_id,
                    'volume': trade.lot_size,
                    'price_open': trade.entry,
                    'sl': trade.sl,
                    'tp': trade.tp,
                    'profit': 50.0, # Simulated profit
                'comment': "Sim_v3_combined", # Hack to pass plugin filter
                    'symbol': trade.symbol,
                    'type': 0 if trade.direction.upper() == "BUY" else 1
                }
        return None

    mt5_client.get_position = mock_get_position
    mt5_client.get_positions = lambda symbol=None: [mock_get_position(t.trade_id) for t in trading_engine.open_trades if (not symbol or t.symbol == symbol)]

    # Patch close_position to always succeed
    mt5_client.close_position = MagicMock(return_value=True)
    mt5_client.get_closed_trade_profit = MagicMock(return_value=50.0)

    # Initialize engine
    await trading_engine.initialize()

    logger.info("✅ Components Initialized")

    # --- SIMULATION ---

    # Test 1: V3 Entry Signal
    logger.info("--- Test 1: V3 Entry Signal ---")
    entry_signal = {
        "type": "entry_v3",
        "symbol": "EURUSD",
        "tf": "5",
        "direction": "buy",
        "price": 1.1050,
        "sl_price": 1.1030,
        "tp1_price": 1.1070,
        "tp2_price": 1.1090,
        "signal_type": "Screener_Full_Bullish",
        "consensus_score": 8,
        "market_trend": "1", # Fix: use string or int based on model
        "mtf_trends": "1,1,1,1,1,1",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

    # Process signal
    result = await trading_engine.process_alert(entry_signal)

    # Verify
    if result:
        logger.info("✅ Signal processed successfully")
    else:
        logger.error("❌ Signal processing failed")

    # Check open trades
    open_trades = trading_engine.get_open_trades()
    logger.info(f"Open Trades: {len(open_trades)}")

    if len(open_trades) >= 1:
        logger.info("✅ Trade created successfully")
        for trade in open_trades:
            logger.info(f"   Trade #{trade.trade_id}: {trade.direction} {trade.symbol} @ {trade.entry}")
    else:
        logger.error("❌ No trade created")

    # Test 2: V3 Exit Signal
    logger.info("--- Test 2: V3 Exit Signal ---")
    exit_signal = {
        "type": "exit_v3",
        "symbol": "EURUSD",
        "tf": "5",
        "direction": "sell",
        "signal_type": "Bearish_Exit", # Closes BUY positions
        "price": 1.1080, # Profit
        "consensus_score": 8,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

    result = await trading_engine.process_alert(exit_signal)

    # Verify closure
    # Wait a moment for async close ops if any
    open_trades_after = trading_engine.get_open_trades()
    logger.info(f"Open Trades after Exit: {len(open_trades_after)}")

    if len(open_trades_after) == 0:
        logger.info("✅ Trades closed successfully")
    else:
        logger.error(f"❌ Trades not closed (Remaining: {len(open_trades_after)})")

    # --- EDGE CASES ---

    # Test 3: Invalid Symbol
    logger.info("--- Test 3: Invalid Symbol ---")
    invalid_signal = entry_signal.copy()
    invalid_signal["symbol"] = "INVALID_SYM"

    # Should handle gracefully (log error but not crash)
    try:
        await trading_engine.process_alert(invalid_signal)
        logger.info("✅ Invalid symbol handled gracefully")
    except Exception as e:
        logger.error(f"❌ Crash on invalid symbol: {e}")

    # Test 4: Missing Fields
    logger.info("--- Test 4: Missing Fields ---")
    broken_signal = {"type": "entry_v3"} # Missing symbol, etc.
    try:
        await trading_engine.process_alert(broken_signal)
        logger.info("✅ Broken signal handled gracefully")
    except Exception as e:
        logger.error(f"❌ Crash on broken signal: {e}")

    logger.info("🏁 Simulation Complete")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
