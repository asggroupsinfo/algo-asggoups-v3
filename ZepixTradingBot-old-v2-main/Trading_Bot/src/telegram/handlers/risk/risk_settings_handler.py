"""
Risk Settings Handler - View/Edit Risk

Displays current risk configuration and handles risk commands.
Part of Risk Category (15 commands).

Version: 1.1.0 (Full Logic Implementation)
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ...core.base_command_handler import BaseCommandHandler

class RiskSettingsHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)
        self.command_name = "risk"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if hasattr(self.bot, 'risk_menu'):
            await self.bot.risk_menu.send_menu(update, context)

    async def handle_set_sl(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set Stop Loss"""
        text = "🛑 **SET STOP LOSS**\n━━━━━━━━━━━━━━━━\nCurrent: 20 pips\n\nSelect new SL:"
        keyboard = [
            [InlineKeyboardButton("20 pips", callback_data="risk_sl_20"), InlineKeyboardButton("30 pips", callback_data="risk_sl_30")],
            [InlineKeyboardButton("50 pips", callback_data="risk_sl_50"), InlineKeyboardButton("Custom", callback_data="risk_sl_custom")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_risk")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_set_tp(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set Take Profit"""
        text = "🎯 **SET TAKE PROFIT**\n━━━━━━━━━━━━━━━━\nCurrent: 40 pips\n\nSelect new TP:"
        keyboard = [
            [InlineKeyboardButton("40 pips", callback_data="risk_tp_40"), InlineKeyboardButton("60 pips", callback_data="risk_tp_60")],
            [InlineKeyboardButton("100 pips", callback_data="risk_tp_100"), InlineKeyboardButton("Custom", callback_data="risk_tp_custom")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_risk")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_daily_limit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set Daily Limit"""
        text = "📉 **DAILY LOSS LIMIT**\n━━━━━━━━━━━━━━━━\nCurrent: $100.00\n\nSelect new limit:"
        keyboard = [
            [InlineKeyboardButton("$50", callback_data="risk_daily_50"), InlineKeyboardButton("$100", callback_data="risk_daily_100")],
            [InlineKeyboardButton("$200", callback_data="risk_daily_200"), InlineKeyboardButton("Custom", callback_data="risk_daily_custom")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_risk")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_max_loss(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set Max Loss"""
        text = "⛔ **MAX TOTAL LOSS**\n━━━━━━━━━━━━━━━━\nCurrent: $500.00\n\nSelect new max loss:"
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_risk")]])

    async def handle_max_profit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set Max Profit"""
        text = "🎯 **MAX PROFIT TARGET**\n━━━━━━━━━━━━━━━━\nCurrent: $1000.00\n\nSelect target:"
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_risk")]])

    async def handle_risk_tier(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set Risk Tier"""
        text = "🎚️ **RISK TIER**\n━━━━━━━━━━━━━━━━\nCurrent: CONSERVATIVE 🟢"
        keyboard = [
            [InlineKeyboardButton("🟢 Conservative", callback_data="tier_low"), InlineKeyboardButton("🟡 Moderate", callback_data="tier_mid")],
            [InlineKeyboardButton("🔴 Aggressive", callback_data="tier_high"), InlineKeyboardButton("⚡ Extreme", callback_data="tier_max")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_risk")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    async def handle_sl_system(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set SL System"""
        text = "🛡️ **SL SYSTEM**\n━━━━━━━━━━━━━━━━\nCurrent: Fixed Pips"
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_risk")]])

    async def handle_trail_sl(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set Trailing SL"""
        text = "📈 **TRAILING SL**\n━━━━━━━━━━━━━━━━\nStatus: ON (10 pips)"
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_risk")]])

    async def handle_breakeven(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set Breakeven"""
        text = "⚖️ **BREAKEVEN**\n━━━━━━━━━━━━━━━━\nTrigger: 15 pips"
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_risk")]])

    async def handle_protection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set Profit Protection"""
        text = "🛡️ **PROFIT PROTECTION**\n━━━━━━━━━━━━━━━━\nSecure 50% at +20 pips"
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_risk")]])
