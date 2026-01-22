"""
Header Status Component

Handles bot status detection (Active, Paused, Partial, Error).
Part of V5 Sticky Header System.

Version: 1.0.0
Created: 2026-01-21
"""

class HeaderStatus:
    """Manages bot status display for sticky header"""

    def __init__(self, mt5_client=None, trading_engine=None):
        self.mt5_client = mt5_client
        self.trading_engine = trading_engine

    def get_status(self) -> str:
        """
        Get current bot status string.
        Returns: "ACTIVE ✅", "PAUSED ⏸️", "PARTIAL ⚠️", etc.
        """
        # 1. Check Connection
        mt5_ok = self.mt5_client and hasattr(self.mt5_client, 'is_connected') and self.mt5_client.is_connected()
        if not mt5_ok:
            return "ERROR ❌ (MT5)"

        # 2. Check Paused State
        paused = False
        if self.trading_engine and hasattr(self.trading_engine, 'is_paused'):
            paused = self.trading_engine.is_paused()

        if paused:
            return "PAUSED ⏸️"

        # 3. Check Plugins (Mock logic if plugin manager not directly accessible here,
        # ideally passed or inferred)
        # For V5, we assume Active if not paused and MT5 ok, unless partial
        # We can expand this if we have access to PluginManager

        return "ACTIVE ✅"
