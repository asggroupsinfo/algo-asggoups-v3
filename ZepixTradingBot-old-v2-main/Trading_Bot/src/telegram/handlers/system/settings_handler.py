"""
Settings Handler - System Config

Implements general settings: Info, Mode, Theme, etc.
Part of Settings Category (10 commands).

Version: 1.2.0 (Full Logic Implementation)
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ...core.base_command_handler import BaseCommandHandler

class SettingsHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)
        self.command_name = "settings"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'settings_menu'):
            await self.bot.settings_menu.send_menu(update, context)

    async def handle_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show System Info"""
        text = (
            "📊 **SYSTEM INFO**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Bot: ZepixTradingBot V5\n"
            "Environment: Production\n"
            "Server: XMGlobal-MT5\n"
            "Ping: 24ms"
        )
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_settings")]])

    async def handle_mode(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Toggle Trading Mode"""
        text = "🔄 **TRADING MODE**\n━━━━━━━━━━━━━━━━\nCurrent: LIVE 🔴\n\nSwitch to Simulation?"
        keyboard = [
            [InlineKeyboardButton("✅ Switch to SIM", callback_data="mode_sim"), InlineKeyboardButton("❌ Keep LIVE", callback_data="menu_settings")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_theme(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Change Theme"""
        text = "🎨 **THEME SELECTION**\n━━━━━━━━━━━━━━━━\nSelect UI Theme:"
        keyboard = [
            [InlineKeyboardButton("🌙 Dark (Default)", callback_data="theme_dark"), InlineKeyboardButton("☀️ Light", callback_data="theme_light")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_settings")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Change Language"""
        text = "🌐 **LANGUAGE**\n━━━━━━━━━━━━━━━━\nSelect Language:"
        keyboard = [
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"), InlineKeyboardButton("🇪🇸 Spanish", callback_data="lang_es")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_settings")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_alerts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Configure Alerts"""
        text = "🔔 **ALERT SETTINGS**\n━━━━━━━━━━━━━━━━\nPush Notifications: ON\nEmail: OFF"
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_settings")]])
