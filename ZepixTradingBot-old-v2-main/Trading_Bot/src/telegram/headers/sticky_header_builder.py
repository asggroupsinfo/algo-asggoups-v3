"""
Sticky Header Builder - Aggregator

Combines Clock, Session, and Symbols into the final header string.
Supports Full and Compact styles.
Part of V5 Sticky Header System.

Version: 1.0.0
Created: 2026-01-21
"""

from .header_clock import HeaderClock
from .header_session import HeaderSession
from .header_symbols import HeaderSymbols

class StickyHeaderBuilder:
    """Builder for standardized sticky headers"""

    def __init__(self, mt5_client=None, trading_engine=None):
        self.mt5_client = mt5_client
        self.trading_engine = trading_engine
        self.symbol_handler = HeaderSymbols(mt5_client)

    def build_header(self, style: str = 'full', bot_status: str = "ACTIVE ✅", account_info: str = "") -> str:
        """
        Build the header string.
        Args:
            style: 'full' or 'compact'
            bot_status: Status text (e.g. "ACTIVE ✅")
            account_info: Optional extra info (e.g. "Risk: 2%")
        """

        # 1. Get Components
        time_text = HeaderClock.get_current_time_display() # "🕐 Time: 14:35:22 GMT"
        session_text, _ = HeaderSession.get_current_session() # "📈 Session: LONDON (Active) ✅"

        prices = self.symbol_handler.get_live_prices()
        price_text = self.symbol_handler.format_prices(prices) # "💱 EUR:1.0825 | GBP:1.2645"

        # 2. Build Layout
        if style == 'full':
            return self._build_full(bot_status, time_text, session_text, price_text)
        else:
            return self._build_compact(bot_status, time_text, session_text, price_text)

    def _build_full(self, status, time, session, prices) -> str:
        """Full Box Layout"""
        # Ensure fixed width alignment (approx 38 chars content inside box)
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
        # Clean up texts for compact line
        t_short = time.replace("🕐 Time: ", "🕐 ")
        s_short = session.replace("📈 Session: ", "📈 ").split('(')[0].strip() # Just name

        return (
            f"🤖 {status} | {t_short} | {s_short}\n"
            f"{prices}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━"
        )
