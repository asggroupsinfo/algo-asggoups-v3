"""
Header Symbols Component

Handles fetching and formatting of live symbol prices.
Uses MT5 Client if available, otherwise graceful fallback.
Part of V5 Sticky Header System.

Version: 1.0.0
Created: 2026-01-21
"""

import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class HeaderSymbols:
    """Manages symbol prices for sticky header"""

    DEFAULT_SYMBOLS = ['EURUSD', 'GBPUSD']

    def __init__(self, mt5_client=None):
        self.mt5_client = mt5_client
        self.last_prices = {}

    def get_live_prices(self, symbols: List[str] = None) -> Dict[str, float]:
        """Fetch current prices"""
        target_symbols = symbols or self.DEFAULT_SYMBOLS
        prices = {}

        if self.mt5_client and hasattr(self.mt5_client, 'is_connected') and self.mt5_client.is_connected():
            for symbol in target_symbols:
                try:
                    price = self.mt5_client.get_symbol_price(symbol)
                    if price:
                        prices[symbol] = price
                except Exception as e:
                    logger.debug(f"Price fetch failed for {symbol}: {e}")

        return prices

    def format_prices(self, prices: Dict[str, float]) -> str:
        """Format prices for display: '💱 EUR:1.0825 | GBP:1.2645'"""
        if not prices:
            return "💱 Prices: --"

        parts = []
        for symbol, price in prices.items():
            # Shorten names
            short = symbol.replace("USD", "") if "USD" in symbol else symbol[:3]

            # Format digits
            if "JPY" in symbol:
                fmt = f"{price:.2f}"
            else:
                fmt = f"{price:.4f}"

            parts.append(f"{short}:{fmt}")

        return "💱 " + " | ".join(parts)
