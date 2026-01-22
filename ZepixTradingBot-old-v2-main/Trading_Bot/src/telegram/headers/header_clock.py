"""
Header Clock Component

Handles time formatting for the sticky header.
Part of V5 Sticky Header System.

Version: 1.0.0
Created: 2026-01-21
"""

from datetime import datetime
import pytz

class HeaderClock:
    """Manages clock display for sticky header"""

    @staticmethod
    def get_current_time_display() -> str:
        """
        Get formatted current time string.
        Format: 🕐 Time: HH:MM:SS GMT
        """
        # Always use UTC/GMT for trading standardization
        current_time = datetime.now(pytz.UTC)
        time_str = current_time.strftime("%H:%M:%S")

        return f"🕐 Time: {time_str} GMT"
