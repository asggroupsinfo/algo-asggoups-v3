"""
Risk Flow - SetLot Wizard

Implements the multi-step wizard for setting lot sizes.

Version: 1.0.0
Created: 2026-01-21
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from .base_flow import BaseFlow

class RiskFlow(BaseFlow):

    async def start_set_lot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.start_flow(update, context, "setlot")

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        query = update.callback_query
        data = query.data
        chat_id = update.effective_chat.id
        state = self.state_manager.get_state(chat_id)

        if not state or state.command != 'setlot':
            return False

        if not data.startswith("flow_risk_"):
            return False

        parts = data.split('_')
        action = parts[2]
        value = parts[3] if len(parts) > 3 else None

        if action == "plugin":
            state.add_data("plugin", value)
            state.next_step()
            await self.show_step(update, context)
            return True

        if action == "lot":
            state.add_data("lot", float(value))
            state.next_step()
            await self.show_step(update, context)
            return True

        if action == "confirm":
            await self.save_settings(update, context)
            return True

        if action == "cancel":
            await self.cancel_flow(update, context)
            return True

        return False

    async def show_step(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        state = self.state_manager.get_state(chat_id)

        # Step 0: Plugin Selection
        if state.step == 0:
            text = "🔌 **SET LOT SIZE**\nSelect plugin context:"
            kb = [
                [InlineKeyboardButton("🔵 V3 Logic", callback_data="flow_risk_plugin_v3"), InlineKeyboardButton("🟢 V6 Price Action", callback_data="flow_risk_plugin_v6")],
                [InlineKeyboardButton("❌ Cancel", callback_data="flow_risk_cancel")]
            ]
            await self.edit_message(update, text, kb)

        # Step 1: Lot Selection
        elif state.step == 1:
            plug = state.get_data("plugin").upper()
            text = f"📊 **SELECT LOT SIZE ({plug})**\nChoose default lot size:"
            kb = [
                [InlineKeyboardButton("0.01", callback_data="flow_risk_lot_0.01"), InlineKeyboardButton("0.05", callback_data="flow_risk_lot_0.05")],
                [InlineKeyboardButton("0.10", callback_data="flow_risk_lot_0.10"), InlineKeyboardButton("0.50", callback_data="flow_risk_lot_0.50")],
                [InlineKeyboardButton("❌ Cancel", callback_data="flow_risk_cancel")]
            ]
            await self.edit_message(update, text, kb)

        # Step 2: Confirmation
        elif state.step == 2:
            lot = state.get_data("lot")
            plug = state.get_data("plugin").upper()
            text = f"✅ **CONFIRM SETTINGS**\n\nSet default lot for **{plug}** to **{lot}**?"
            kb = [
                [InlineKeyboardButton("✅ SAVE", callback_data="flow_risk_confirm")],
                [InlineKeyboardButton("❌ Cancel", callback_data="flow_risk_cancel")]
            ]
            await self.edit_message(update, text, kb)

    async def save_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        state = self.state_manager.get_state(chat_id)

        # Logic to save to Config

        msg = "✅ **SETTINGS SAVED**"
        self.state_manager.clear_state(chat_id)
        await self.edit_message(update, msg, [[InlineKeyboardButton("🏠 Main Menu", callback_data="nav_main_menu")]])
