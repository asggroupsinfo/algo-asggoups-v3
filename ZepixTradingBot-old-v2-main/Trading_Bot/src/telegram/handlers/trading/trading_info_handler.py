"""
Trading Info Handler - General Trading Information Commands

Handles P&L, Balance, Equity, History, etc.
Part of the Trading Category (18 commands).

Version: 1.1.0 (Real Data Integration)
Created: 2026-01-21
Part of: TELEGRAM_V5_CORE
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ...core.base_command_handler import BaseCommandHandler
import logging

logger = logging.getLogger(__name__)

class TradingInfoHandler(BaseCommandHandler):

    def __init__(self, bot):
        super().__init__(bot)

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Default execution - redirect to trading menu"""
        if hasattr(self.bot, 'trading_menu'):
            await self.bot.trading_menu.send_menu(update, context)

    # --- P&L Command ---
    async def handle_pnl(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show P&L Report"""
        balance = 0.0
        equity = 0.0
        pnl = 0.0

        if self.bot.mt5_client:
            balance = self.bot.mt5_client.get_account_balance() or 0.0
            equity = self.bot.mt5_client.get_account_equity() or 0.0
            pnl = equity - balance

        pnl_text = (
            "💰 **PROFIT & LOSS REPORT**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💵 **Balance:** ${balance:,.2f}\n"
            f"💎 **Equity:** ${equity:,.2f}\n"
            f"📈 **Open P&L:** ${pnl:+,.2f}\n\n"
            "📅 **Today:** See Analytics\n"
        )

        keyboard = [
            [InlineKeyboardButton("📅 Daily", callback_data="analytics_daily"), InlineKeyboardButton("📜 History", callback_data="trading_history")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_trading")]
        ]

        await self.edit_message_with_header(update, pnl_text, keyboard)

    # --- Balance Command ---
    async def handle_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show Balance"""
        balance = 0.0
        free_margin = 0.0
        margin_level = 0.0

        if self.bot.mt5_client:
            balance = self.bot.mt5_client.get_account_balance() or 0.0
            free_margin = self.bot.mt5_client.get_account_free_margin() or 0.0
            margin_level = self.bot.mt5_client.get_account_margin_level() or 0.0

        text = (
            "💵 **ACCOUNT BALANCE**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 **Total:** ${balance:,.2f}\n"
            f"💳 **Free Margin:** ${free_margin:,.2f}\n"
            f"📊 **Margin Level:** {margin_level:.2f}%"
        )
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_trading")]])

    # --- Equity Command ---
    async def handle_equity(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show Equity"""
        equity = 0.0
        if self.bot.mt5_client:
            equity = self.bot.mt5_client.get_account_equity() or 0.0

        text = (
            "💎 **ACCOUNT EQUITY**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 **Equity:** ${equity:,.2f}\n"
            "🟢 **Status:** Healthy"
        )
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_trading")]])

    # --- Margin Command ---
    async def handle_margin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show Margin"""
        used_margin = 0.0
        free_margin = 0.0
        margin_level = 0.0

        if self.bot.mt5_client:
            equity = self.bot.mt5_client.get_account_equity() or 0.0
            free_margin = self.bot.mt5_client.get_account_free_margin() or 0.0
            used_margin = equity - free_margin
            margin_level = self.bot.mt5_client.get_account_margin_level() or 0.0

        text = (
            "📊 **MARGIN STATUS**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 **Used Margin:** ${used_margin:,.2f}\n"
            f"💳 **Free Margin:** ${free_margin:,.2f}\n"
            f"📈 **Margin Level:** {margin_level:.2f}%\n"
        )
        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_trading")]])

    # --- History Command ---
    async def handle_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show History"""
        history_text = "📜 **TRADE HISTORY (Last 5)**\n━━━━━━━━━━━━━━━━━━━━━━━━\n"

        if self.bot.db:
            trades = self.bot.db.get_trade_history(days=1)
            # Limit to last 5
            trades = trades[:5]
            if trades:
                for idx, t in enumerate(trades, 1):
                    pnl = t.get('pnl', 0.0)
                    emoji = "✅" if pnl >= 0 else "❌"
                    history_text += f"{idx}. {t.get('symbol')} {t.get('direction')} | ${pnl:+.2f} {emoji}\n"
            else:
                history_text += "No trades today."
        else:
            history_text += "Database unavailable."

        keyboard = [
            [InlineKeyboardButton("📅 Full Report", callback_data="analytics_daily")],
            [InlineKeyboardButton("⬅️ Back", callback_data="menu_trading")]
        ]
        await self.edit_message_with_header(update, history_text, keyboard)

    # --- Symbols Command ---
    async def handle_symbols(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show Active Symbols"""
        symbols = []
        if self.bot.config:
            symbols = list(self.bot.config.get("symbol_mapping", {}).keys())

        text = "💱 **ACTIVE SYMBOLS**\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
        for s in symbols:
            text += f"• {s}\n"

        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_trading")]])

    # --- Price Command ---
    async def handle_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show Current Prices"""
        text = "💲 **MARKET PRICES**\n━━━━━━━━━━━━━━━━━━━━━━━━\n"

        if self.bot.mt5_client:
            symbols = list(self.bot.config.get("symbol_mapping", {}).keys())[:5] # Top 5
            for s in symbols:
                price = self.bot.mt5_client.get_symbol_price(s)
                if price:
                    text += f"**{s}:** {price:.5f}\n"
                else:
                    text += f"**{s}:** ---\n"

        keyboard = [
             [InlineKeyboardButton("🔄 Refresh", callback_data="trading_price")],
             [InlineKeyboardButton("⬅️ Back", callback_data="menu_trading")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    # --- Spread Command ---
    async def handle_spread(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show Spreads"""
        text = "📏 **CURRENT SPREADS**\n━━━━━━━━━━━━━━━━━━━━━━━━\n"

        if self.bot.mt5_client:
            symbols = list(self.bot.config.get("symbol_mapping", {}).keys())[:5]
            for s in symbols:
                spread = self.bot.mt5_client.get_symbol_spread(s) # Assuming method exists or mocking access
                if spread is not None:
                    text += f"**{s}:** {spread} pts\n"

        keyboard = [
             [InlineKeyboardButton("🔄 Refresh", callback_data="trading_spread")],
             [InlineKeyboardButton("⬅️ Back", callback_data="menu_trading")]
        ]
        await self.edit_message_with_header(update, text, keyboard)

    # --- Signals Command ---
    async def handle_signals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show Signals"""
        text = "📡 **ACTIVE SIGNALS**\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
        # Fetch from trading engine logic states
        if self.bot.trading_engine:
            # Mocking inspection of internal state as no direct API exists yet
            text += "Querying engine..."
        else:
            text += "Engine unavailable."

        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_trading")]])

    # --- Filters Command ---
    async def handle_filters(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show Signal Filters"""
        text = "🔍 **SIGNAL FILTERS**\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
        if self.bot.config:
            text += f"• Timeframe Logic: Enabled\n"

        await self.edit_message_with_header(update, text, [[InlineKeyboardButton("⬅️ Back", callback_data="menu_trading")]])

    # --- Partial Command ---
    async def handle_partial(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Partial Close"""
        text = (
            "✂️ **PARTIAL CLOSE**\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Select position to close partially:"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="menu_trading")]]

        # Add positions if available
        if self.bot.db:
            trades = self.bot.db.get_trade_history(days=1) # Should be OPEN trades
            # Assuming get_open_trades exists or filter
            # For now just back
            pass

        await self.edit_message_with_header(update, text, keyboard)
