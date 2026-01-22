"""
Sticky Header Builder - Aggregator

Combines Clock, Session, Symbols, and Status into the final header string.
Supports Full and Compact styles.
Part of V5 Sticky Header System.

Version: 1.1.0 (Modular Status)
Created: 2026-01-21
"""

from .header_clock import HeaderClock
from .header_session import HeaderSession
from .header_symbols import HeaderSymbols
from .header_status import HeaderStatus

class StickyHeaderBuilder:
    """Builder for standardized sticky headers"""

    def __init__(self, mt5_client=None, trading_engine=None):
        self.mt5_client = mt5_client
        self.trading_engine = trading_engine
        self.symbol_handler = HeaderSymbols(mt5_client)
        self.status_handler = HeaderStatus(mt5_client, trading_engine)

    def set_dependencies(self, mt5_client=None, trading_engine=None):
        """Update dependencies"""
        self.mt5_client = mt5_client
        self.trading_engine = trading_engine
        self.symbol_handler = HeaderSymbols(mt5_client)
        self.status_handler = HeaderStatus(mt5_client, trading_engine)

    def build_header(self, style: str = 'full', bot_status: str = None, account_info: str = "") -> str:
        """
        Build the header string.
        Args:
            style: 'full' or 'compact'
            bot_status: Override status text (optional)
            account_info: Optional extra info
        """

        # 1. Get Components
        time_text = HeaderClock.get_current_time_display()
        session_text, _ = HeaderSession.get_current_session()

        prices = self.symbol_handler.get_live_prices()
        price_text = self.symbol_handler.format_prices(prices)

        # Use dynamic status if not provided override
        status_text = bot_status if bot_status else self.status_handler.get_status()

        # 2. Build Layout
        if style == 'full':
            return self._build_full(status_text, time_text, session_text, price_text)
        else:
            return self._build_compact(status_text, time_text, session_text, price_text)

    def _build_full(self, status, time, session, prices) -> str:
        """Full Box Layout"""
        return (
            "╔══════════════════════════════════════╗\n"
            "║   🤖 ZEPIX TRADING BOT V5.0          ║\n"
            "╠══════════════════════════════════════╣\n"
            f"║  📊 Status: {status:<25}║\n"
            f"║  {time:<36}║\n"
            f"║  {session:<36}║\n"
            f"║  {prices:<36}║\n"
            "╚══════════════════════════════════════╝"
        )

    def _build_compact(self, status, time, session, prices) -> str:
        """Compact Layout for submenus"""
        t_short = time.replace("🕐 Time: ", "🕐 ")
        s_short = session.replace("📈 Session: ", "📈 ").split('(')[0].strip()

        return (
            f"🤖 {status} | {t_short} | {s_short}\n"
            f"{prices}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━"
        )
