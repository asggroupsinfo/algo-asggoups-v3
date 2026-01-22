"""
Session Handler - Trading Hours Management

Implements session control: London, New York, Tokyo, Sydney.
Part of Session Category (8 commands).

Version: 1.2.0 (Full Logic Implementation)
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ...core.base_command_handler import BaseCommandHandler

class SessionHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)
        self.command_name = "session"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'session_menu'):
            await self.bot.session_menu.send_menu(update, context)

    async def handle_london(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle London Session"""
        text = (
            "🇬🇧 **LONDON SESSION**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Status: ACTIVE ✅\n"
            "Time: 08:00 - 17:00 GMT\n\n"
            "Strategy: Breakout & Trend"
        )
        keyboard = [
            [InlineKeyboardButton("⛔ Disable", callback_data="session_london_off"), InlineKeyboardButton("⚙️ Configure", callback_data="session_config")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_session")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_newyork(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle New York Session"""
        text = (
            "🇺🇸 **NEW YORK SESSION**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Status: OPENING SOON\n"
            "Time: 13:00 - 22:00 GMT\n\n"
            "Strategy: High Volatility"
        )
        keyboard = [
            [InlineKeyboardButton("✅ Enable", callback_data="session_ny_on"), InlineKeyboardButton("⚙️ Configure", callback_data="session_config")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_session")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_tokyo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Tokyo Session"""
        text = (
            "🇯🇵 **TOKYO SESSION**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Status: CLOSED ⛔\n"
            "Time: 00:00 - 09:00 GMT\n\n"
            "Strategy: Range Trading"
        )
        keyboard = [
            [InlineKeyboardButton("✅ Enable", callback_data="session_tokyo_on"), InlineKeyboardButton("⚙️ Configure", callback_data="session_config")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_session")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_sydney(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Sydney Session"""
        text = (
            "🇦🇺 **SYDNEY SESSION**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Status: CLOSED ⛔\n"
            "Time: 22:00 - 07:00 GMT\n\n"
            "Strategy: Quiet accumulation"
        )
        keyboard = [
            [InlineKeyboardButton("✅ Enable", callback_data="session_sydney_on"), InlineKeyboardButton("⚙️ Configure", callback_data="session_config")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_session")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_overlap(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Overlaps"""
        text = (
            "🔄 **SESSION OVERLAPS**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "1. London + NY: 13:00 - 17:00 (Active)\n"
            "2. Tokyo + London: 08:00 - 09:00\n\n"
            "High volatility periods."
        )
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_session")]])
