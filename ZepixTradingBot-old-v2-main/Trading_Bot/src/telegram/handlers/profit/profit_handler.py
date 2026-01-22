"""
Profit Handler - Manage Profit Booking & Dual Orders

Handles Profit Chains, Dual Order System, and Levels.
Part of Profit Category (10 commands).

Version: 1.1.0 (Real Data Integration)
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ...core.base_command_handler import BaseCommandHandler

class ProfitHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'profit_menu'):
            await self.bot.profit_menu.send_menu(update, context)

    # --- Booking Command ---
    async def handle_booking(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Profit Booking"""
        status = "UNKNOWN"
        if self.bot.profit_booking_manager:
            status = "ACTIVE ✅"

        text = (
            "📖 **PROFIT BOOKING**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Status: {status}\n"
            "Type: Pyramid (Levels 1-5)\n\n"
            "Strategy: Secure 50% at TP1, let rest run."
        )
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_profit")]])

    # --- Levels Command ---
    async def handle_levels(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Profit Levels"""
        targets = []
        if self.bot.config:
            targets = self.bot.config.get("profit_booking_config", {}).get("profit_targets", [])

        text = "🎯 **PROFIT LEVELS**\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
        if targets:
            for idx, target in enumerate(targets, 1):
                multiplier = 2**(idx-1)
                text += f"L{idx}: {target} pips (x{multiplier})\n"
        else:
            text += "Using Default Levels."

        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_profit")]])

    # --- Order B Command ---
    async def handle_order_b(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Order B Stats"""
        text = "🔄 **ORDER B STATUS**\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
        if self.bot.db:
            # Assuming method to get order B stats or query
            # Placeholder query logic via DB if method existed
            pass

        text += "Active: --\nProfit: --\n\nRole: Profit Accumulation (Trailing)"

        keyboard = [
            [InlineKeyboardButton("🔄 Close All Order B", callback_data="trading_close_b")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_profit")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    # --- Dual Order Command ---
    async def handle_dual_order(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Dual Order System"""
        chat_id = update.effective_chat.id
        self.command_name = "dualorder"

        if not self.plugin_context.has_active_context(chat_id):
            await self.show_plugin_selection(update, context)
            return

        plugin_ctx = self.plugin_context.get_plugin_context(chat_id)
        plugin_name = plugin_ctx['plugin'].upper()

        status = "UNKNOWN"
        if self.bot.dual_order_manager:
            status = "ACTIVE ✅"

        text = (
            f"💰 **DUAL ORDER SYSTEM ({plugin_name})**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Status: {status}\n"
            f"Plugin: {plugin_name}\n"
        )

        keyboard = [
            [InlineKeyboardButton("✅ Turn ON", callback_data=f"dual_on_{plugin_name}"), InlineKeyboardButton("⛔ Turn OFF", callback_data=f"dual_off_{plugin_name}")],
            [InlineKeyboardButton("⚙️ Configure", callback_data="dual_config")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_profit")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    # --- Partial Command ---
    async def handle_partial(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Partial Close (Profit Context)"""
        text = (
            "✂️ **PARTIAL CLOSE**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Manual profit taking.\n"
            "Select trade to close 50%."
        )
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_profit")]])
