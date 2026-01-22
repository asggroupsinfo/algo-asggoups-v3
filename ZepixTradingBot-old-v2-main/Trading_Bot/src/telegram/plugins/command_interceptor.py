"""
Command Interceptor - Smart Routing Logic

Intercepts commands to check if plugin selection is needed.
Auto-routes V3/V6 specific commands.
Part of V5 Plugin Architecture.

Version: 1.0.0
Created: 2026-01-21
"""

from typing import Optional, Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from .plugin_context_manager import PluginContextManager

class CommandInterceptor:
    """Intercepts commands to enforce plugin context"""

    # 1. Commands that ALWAYS need selection if no context exists
    PLUGIN_AWARE_COMMANDS = {
        # Trading
        'positions', 'pnl', 'buy', 'sell', 'close', 'closeall',
        'orders', 'history', 'partial', 'signals', 'filters',

        # Risk
        'setlot', 'setsl', 'settp', 'dailylimit', 'maxloss', 'maxprofit',
        'risktier', 'slsystem', 'trailsl', 'breakeven', 'protection', 'multiplier',

        # Analytics
        'daily', 'weekly', 'monthly', 'pairreport', 'strategyreport',
        'tpreport', 'stats', 'winrate', 'drawdown', 'profit_stats', 'export',

        # Re-entry
        'slhunt', 'sl_hunt', 'tpcontinue', 'tp_cont', 'reentry', 'reentry_config',
        'recovery', 'cooldown', 'chains', 'chainlimit', 'sl_hunt_stats',

        # Dual Order
        'dualorder', 'orderb', 'order_b', 'profit', 'booking', 'levels', 'partial',

        # Plugin Management
        'enable', 'disable', 'upgrade', 'rollback', 'shadow', 'plugin_toggle',
    }

    # 2. Commands that AUTO-SET context to V3
    V3_AUTO_CONTEXT = {
        'logic1', 'logic2', 'logic3',
        'logic1_on', 'logic1_off', 'logic2_on', 'logic2_off', 'logic3_on', 'logic3_off',
        'logic1_config', 'logic2_config', 'logic3_config',
        'v3', 'v3_config', 'logic_status', 'v3_toggle', 'reentry_v3',
    }

    # 3. Commands that AUTO-SET context to V6
    V6_AUTO_CONTEXT = {
        'v6_status', 'v6_control', 'v6_config', 'v6_menu', 'v6_performance',
        'tf1m_on', 'tf1m_off', 'tf5m_on', 'tf5m_off',
        'tf15m_on', 'tf15m_off', 'tf30m_on', 'tf30m_off',
        'tf1h_on', 'tf1h_off', 'tf4h_on', 'tf4h_off',
        'tf15m', 'tf30m', 'tf1h', 'tf4h',
        'v6_toggle', 'reentry_v6',
        'v6'
    }

    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.context_manager = PluginContextManager

    async def intercept(self, update: Update, context: ContextTypes.DEFAULT_TYPE, command: str) -> bool:
        """
        Check if command needs interception.
        Returns: True if intercepted (selection shown), False if safe to proceed.
        """
        chat_id = update.effective_chat.id
        cmd_clean = command.lstrip('/').replace('@' + context.bot.username, '')

        # 1. Check Auto-Context
        if cmd_clean in self.V3_AUTO_CONTEXT:
            self.context_manager.set_plugin_context(chat_id, 'v3', cmd_clean)
            return False

        if cmd_clean in self.V6_AUTO_CONTEXT:
            self.context_manager.set_plugin_context(chat_id, 'v6', cmd_clean)
            return False

        # 2. Check Plugin-Aware
        if cmd_clean in self.PLUGIN_AWARE_COMMANDS:
            if self.context_manager.has_active_context(chat_id):
                return False # Has valid context
            else:
                await self._show_selection_menu(update, cmd_clean)
                return True # Intercepted

        # 3. Default (Global commands)
        return False

    async def _show_selection_menu(self, update: Update, command: str):
        """Show plugin selection UI"""
        # Create Selection Keyboard
        # Format: plugin_select_{type}_{command}
        keyboard = [
            [
                InlineKeyboardButton("🔵 V3 Only", callback_data=f"plugin_select_v3_{command}"),
                InlineKeyboardButton("🟢 V6 Only", callback_data=f"plugin_select_v6_{command}")
            ],
            [
                InlineKeyboardButton("🔷 Both Plugins", callback_data=f"plugin_select_both_{command}")
            ],
            [
                InlineKeyboardButton("❌ Cancel", callback_data="nav_main_menu")
            ]
        ]

        text = (
            f"🔌 **SELECT PLUGIN CONTEXT**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Command: `/{command}`\n\n"
            f"Please select which plugin to apply this command to:"
        )

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )

    async def handle_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[Dict]:
        """
        Handle selection callback.
        Returns: Context dict if successful, None otherwise.
        """
        query = update.callback_query
        data = query.data # plugin_select_v3_positions

        parts = data.split('_')
        if len(parts) < 4:
            return None

        plugin_type = parts[2] # v3
        command = "_".join(parts[3:]) # positions

        chat_id = update.effective_chat.id
        self.context_manager.set_plugin_context(chat_id, plugin_type, command)

        # Trigger original command execution is handled by ControllerBot routing
        return {'plugin': plugin_type, 'command': command}
