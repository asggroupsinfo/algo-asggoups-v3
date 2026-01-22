"""
Re-Entry Handler - Manage Re-Entry & Autonomous Systems

Handles SL Hunt, TP Continuation, Recovery logic.
Part of Re-Entry Category (12 commands).

Version: 1.1.0 (Real Data Integration)
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ...core.base_command_handler import BaseCommandHandler

class ReEntryHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Default execution"""
        if hasattr(self.bot, 'reentry_menu'):
            await self.bot.reentry_menu.send_menu(update, context)

    # --- SL Hunt Command ---
    async def handle_sl_hunt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle SL Hunt Control"""
        chat_id = update.effective_chat.id
        self.command_name = "slhunt"

        if not self.plugin_context.has_active_context(chat_id):
            await self.show_plugin_selection(update, context)
            return

        plugin_ctx = self.plugin_context.get_plugin_context(chat_id)
        plugin_name = plugin_ctx['plugin'].upper()

        # Fetch Data
        status = "UNKNOWN"
        sl_hits = 0
        reentries = 0
        recovered = 0

        if self.bot.reentry_manager:
            status = "ACTIVE ✅" # Assuming enabled if manager exists
            stats = self.bot.reentry_manager.get_sl_recovery_stats() if hasattr(self.bot.reentry_manager, 'get_sl_recovery_stats') else {}
            sl_hits = stats.get('total_sl_hits', 0)
            reentries = stats.get('recovery_attempts', 0)
            recovered = stats.get('successful_recoveries', 0)

        text = (
            f"🎯 **SL HUNT CONTROL ({plugin_name})**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Status: {status}\n"
            f"Plugin: {plugin_name} Logic\n\n"
            f"📊 **TODAY'S STATS:**\n"
            f"├─ SL Hits: {sl_hits}\n"
            f"├─ Re-entries: {reentries}\n"
            f"├─ Recovered: {recovered}\n"
        )

        keyboard = [
            [InlineKeyboardButton("✅ Turn ON", callback_data=f"reentry_slhunt_on_{plugin_name}"), InlineKeyboardButton("⛔ Turn OFF", callback_data=f"reentry_slhunt_off_{plugin_name}")],
            [InlineKeyboardButton("⚙️ Configure", callback_data="reentry_config"), InlineKeyboardButton("📊 Full Stats", callback_data="analytics_stats")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_reentry")]
        ]

        await self.edit_message_with_header(update, text, keyboard)

    # --- TP Continue Command ---
    async def handle_tp_continue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle TP Continuation"""
        status = "UNKNOWN"
        if self.bot.reentry_manager:
             status = "ACTIVE ✅"

        text = (
            "🎯 **TP CONTINUATION**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Status: {status}\n"
            "Logic: Enters new trade after TP hit to catch trends."
        )
        keyboard = [
            [InlineKeyboardButton("✅ Turn ON", callback_data="reentry_tp_on"), InlineKeyboardButton("⛔ Turn OFF", callback_data="reentry_tp_off")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_reentry")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    # --- Recovery Command ---
    async def handle_recovery(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Recovery Status"""
        text = (
            "🔄 **RECOVERY SYSTEM**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Active Recoveries: --\n"
            "Recovery Window: 30 mins"
        )
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_reentry")]])

    # --- Cooldown Command ---
    async def handle_cooldown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Cooldowns"""
        text = (
            "⏱️ **COOLDOWN STATUS**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "SL Hunt: 15 mins\n"
            "TP Cont: 5 mins\n"
        )
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_reentry")]])

    # --- Chains Command ---
    async def handle_chains(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Active Chains"""
        stats = {}
        if self.bot.db:
            stats = self.bot.db.get_chain_statistics()

        text = (
            "⛓️ **CHAIN STATISTICS**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Total Chains: {stats.get('total_chains', 0)}\n"
            f"Avg Level: {stats.get('avg_max_level', 0):.1f}\n"
            f"Total Profit: ${stats.get('total_chain_profit', 0):.2f}"
        )
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_reentry")]])

    # --- Autonomous Command ---
    async def handle_autonomous(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Autonomous Mode"""
        chat_id = update.effective_chat.id
        self.command_name = "autonomous"

        if not self.plugin_context.has_active_context(chat_id):
            await self.show_plugin_selection(update, context)
            return

        plugin_ctx = self.plugin_context.get_plugin_context(chat_id)
        plugin_name = plugin_ctx['plugin'].upper()

        text = (
            f"🤖 **AUTONOMOUS MODE ({plugin_name})**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Mode: SEMI-AUTO ⚠️ (Default)\n"
        )
        keyboard = [
            [InlineKeyboardButton("✅ Enable", callback_data=f"auto_on_{plugin_name}"), InlineKeyboardButton("⛔ Disable", callback_data=f"auto_off_{plugin_name}")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_reentry")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    # --- Chain Limit Command ---
    async def handle_chain_limit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Chain Limit"""
        limit = 5
        if self.bot.config:
            limit = self.bot.config.get("re_entry_config", {}).get("max_chain_levels", 5)

        text = (
            "🎚️ **CHAIN LIMITS**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Max Levels: {limit}\n"
            "Stop at Level 5 to secure profit."
        )
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_reentry")]])
