"""
Plugin Handler - Strategy Management

Implements plugin control: enable, disable, config.
Part of Plugin Category (8 commands).

Version: 1.2.0 (Full Logic Implementation)
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ...core.base_command_handler import BaseCommandHandler

class PluginHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)
        self.command_name = "plugins"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'plugin_menu'):
            await self.bot.plugin_menu.send_menu(update, context)

    async def handle_enable(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enable Plugin"""
        text = "✅ **ENABLE PLUGIN**\n━━━━━━━━━━━━━━━━\nSelect plugin to enable:"
        keyboard = [
            [InlineKeyboardButton("🔵 Enable V3", callback_data="v3_toggle"), InlineKeyboardButton("🟢 Enable V6", callback_data="v6_toggle")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_plugin")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_disable(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Disable Plugin"""
        text = "⛔ **DISABLE PLUGIN**\n━━━━━━━━━━━━━━━━\nSelect plugin to disable:"
        keyboard = [
            [InlineKeyboardButton("🔵 Disable V3", callback_data="v3_toggle"), InlineKeyboardButton("🟢 Disable V6", callback_data="v6_toggle")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_plugin")]
        ]
        await self.edit_message_with_header(update, text, keyboard)
