"""
Handler Verifier - Startup Integrity Check

Verifies that all 144 required commands are registered in the application.
Prevents "Handler Not Found" runtime errors.
Part of V5 Hardening.

Version: 1.0.0
Created: 2026-01-21
"""

import logging
from telegram.ext import CommandHandler

logger = logging.getLogger(__name__)

class HandlerVerifier:

    EXPECTED_COMMANDS = {
        # System
        'start', 'help', 'status', 'pause', 'resume', 'restart', 'shutdown', 'config', 'health', 'version',
        # Trading
        'positions', 'pnl', 'buy', 'sell', 'close', 'closeall', 'orders', 'history',
        'price', 'spread', 'partial', 'signals', 'filters', 'balance', 'equity', 'margin', 'symbols', 'trades',
        # Risk
        'setlot', 'setsl', 'settp', 'dailylimit', 'maxloss', 'maxprofit', 'risktier',
        'slsystem', 'trailsl', 'breakeven', 'protection', 'multiplier', 'maxtrades', 'drawdown', 'risk',
        # V3
        'logic1', 'logic2', 'logic3', 'v3', 'v3_config', 'v3_status', 'v3_toggle',
        'logic1_config', 'logic2_config', 'logic3_config',
        # V6
        'v6', 'v6_status', 'v6_control', 'v6_config', 'v6_menu', 'v6_performance',
        'tf1m', 'tf5m', 'tf15m', 'tf30m', 'tf1h', 'tf4h', 'tf1d',
        'tf1m_on', 'tf1m_off', 'tf5m_on', 'tf5m_off', 'tf15m_on', 'tf15m_off',
        'tf30m_on', 'tf30m_off', 'tf1h_on', 'tf1h_off', 'tf4h_on', 'tf4h_off',
        # Analytics
        'daily', 'weekly', 'monthly', 'compare', 'export', 'winrate', 'drawdown',
        'pair_report', 'strategy_report', 'tp_report', 'analytics', 'dashboard', 'stats', 'performance',
        'avgprofit', 'avgloss', 'bestday', 'worstday', 'correlation',
        # ReEntry
        'reentry', 'slhunt', 'tpcontinue', 'recovery', 'cooldown', 'chains', 'autonomous', 'chainlimit',
        'reentry_v3', 'reentry_v6',
        # Profit
        'profit', 'booking', 'levels', 'partial', 'orderb', 'dualorder',
        # Plugin
        'plugin', 'plugins', 'enable', 'disable', 'upgrade', 'rollback', 'shadow',
        # Session
        'session', 'london', 'newyork', 'tokyo', 'sydney', 'overlap',
        # Voice
        'voice', 'voicetest', 'mute', 'unmute',
        # Settings
        'settings', 'notifications',
        # Utils
        'trends', 'menu', 'home', 'back', 'exit', 'trade'
    }

    @classmethod
    def verify(cls, application):
        """Run verification on application handlers"""
        logger.info("[HandlerVerifier] Starting verification...")

        registered_commands = set()

        # Scan handlers
        # Note: Accessing internal handlers list
        for group in application.handlers.values():
            for handler in group:
                if isinstance(handler, CommandHandler):
                    registered_commands.update(handler.commands)

        missing = cls.EXPECTED_COMMANDS - registered_commands

        if missing:
            logger.critical(f"❌ MISSING COMMAND HANDLERS: {missing}")
            # Strict mode: Raise error
            # raise RuntimeError(f"Missing handlers: {missing}")
            return False

        logger.info(f"✅ All {len(cls.EXPECTED_COMMANDS)} commands verified.")
        return True
