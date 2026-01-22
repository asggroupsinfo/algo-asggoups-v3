"""
Trading Flow - Buy/Sell Wizard

Implements the 4-step wizard for placing trades:
1. Plugin Selection
2. Symbol Selection
3. Lot Selection
4. Confirmation

Version: 1.0.0
Created: 2026-01-21
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from .base_flow import BaseFlow

class TradingFlow(BaseFlow):

    async def start_buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start Buy Wizard"""
        await self.start_flow(update, context, "buy")

    async def start_sell(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start Sell Wizard"""
        await self.start_flow(update, context, "sell")

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Handle flow callbacks"""
        query = update.callback_query
        data = query.data
        chat_id = update.effective_chat.id
        state = self.state_manager.get_state(chat_id)

        if not state or state.command not in ['buy', 'sell']:
            return False

        # Parse Data
        # format: flow_trade_{action}_{value}
        if not data.startswith("flow_trade_"):
            return False

        parts = data.split('_')
        action = parts[2]
        value = parts[3] if len(parts) > 3 else None

        if action == "plugin":
            state.add_data("plugin", value)
            state.next_step()
            await self.show_step(update, context)
            return True

        if action == "symbol":
            state.add_data("symbol", value)
            state.next_step()
            await self.show_step(update, context)
            return True

        if action == "lot":
            state.add_data("lot", float(value))
            state.next_step()
            await self.show_step(update, context)
            return True

        if action == "confirm":
            await self.execute_trade(update, context)
            return True

        if action == "cancel":
            await self.cancel_flow(update, context)
            return True

        return False

    async def show_step(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        state = self.state_manager.get_state(chat_id)

        # Step 0: Plugin Selection (if not set)
        if state.step == 0:
            text = f"🔌 **SELECT PLUGIN**\nWhich logic to use for **{state.command.upper()}**?"
            kb = [
                [InlineKeyboardButton("🔵 V3 Logic", callback_data="flow_trade_plugin_v3"), InlineKeyboardButton("🟢 V6 Price Action", callback_data="flow_trade_plugin_v6")],
                [InlineKeyboardButton("❌ Cancel", callback_data="flow_trade_cancel")]
            ]
            await self.edit_message(update, text, kb)

        # Step 1: Symbol Selection
        elif state.step == 1:
            plugin = state.get_data("plugin").upper()
            text = f"💱 **SELECT SYMBOL ({plugin})**\nChoose pair to trade:"
            # Mock symbols
            kb = [
                [InlineKeyboardButton("EURUSD", callback_data="flow_trade_symbol_EURUSD"), InlineKeyboardButton("GBPUSD", callback_data="flow_trade_symbol_GBPUSD")],
                [InlineKeyboardButton("USDJPY", callback_data="flow_trade_symbol_USDJPY"), InlineKeyboardButton("XAUUSD", callback_data="flow_trade_symbol_XAUUSD")],
                [InlineKeyboardButton("❌ Cancel", callback_data="flow_trade_cancel")]
            ]
            await self.edit_message(update, text, kb)

        # Step 2: Lot Selection
        elif state.step == 2:
            sym = state.get_data("symbol")
            text = f"📊 **SELECT LOT SIZE**\nSymbol: {sym}\nPlugin: {state.get_data('plugin').upper()}"
            kb = [
                [InlineKeyboardButton("0.01", callback_data="flow_trade_lot_0.01"), InlineKeyboardButton("0.05", callback_data="flow_trade_lot_0.05")],
                [InlineKeyboardButton("0.10", callback_data="flow_trade_lot_0.10"), InlineKeyboardButton("0.50", callback_data="flow_trade_lot_0.50")],
                [InlineKeyboardButton("❌ Cancel", callback_data="flow_trade_cancel")]
            ]
            await self.edit_message(update, text, kb)

        # Step 3: Confirmation
        elif state.step == 3:
            cmd = state.command.upper()
            sym = state.get_data("symbol")
            lot = state.get_data("lot")
            plug = state.get_data("plugin").upper()

            text = (
                f"✅ **CONFIRM TRADE**\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"Type: **{cmd}**\n"
                f"Symbol: **{sym}**\n"
                f"Lot: **{lot}**\n"
                f"Plugin: **{plug}**\n"
            )
            kb = [
                [InlineKeyboardButton("✅ EXECUTE", callback_data="flow_trade_confirm")],
                [InlineKeyboardButton("❌ Cancel", callback_data="flow_trade_cancel")]
            ]
            await self.edit_message(update, text, kb)

    async def execute_trade(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Execute the final trade"""
        chat_id = update.effective_chat.id
        state = self.state_manager.get_state(chat_id)

        # Here we would call self.bot.trading_engine.execute_trade(...)

        msg = (
            f"✅ **ORDER PLACED!**\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"Ticket: #12345\n"
            f"{state.command.upper()} {state.get_data('symbol')} {state.get_data('lot')}"
        )

        self.state_manager.clear_state(chat_id)
        await self.edit_message(update, msg, [[InlineKeyboardButton("🏠 Main Menu", callback_data="nav_main_menu")]])
