"""
Header Session Component

Handles trading session detection (London, NY, Tokyo, Sydney).
Supports overlap detection and status formatting.
Part of V5 Sticky Header System.

Version: 1.0.0
Created: 2026-01-21
"""

from datetime import datetime, timedelta
import pytz

class HeaderSession:
    """Manages session display for sticky header"""

    # Session Schedule (GMT)
    TRADING_SESSIONS = {
        'SYDNEY': {
            'start': '22:00', # Starts previous day GMT
            'end': '07:00',
            'emoji': '🇦🇺'
        },
        'TOKYO': {
            'start': '00:00',
            'end': '09:00',
            'emoji': '🇯🇵'
        },
        'LONDON': {
            'start': '08:00',
            'end': '17:00',
            'emoji': '🇬🇧'
        },
        'NEW YORK': {
            'start': '13:00',
            'end': '22:00',
            'emoji': '🇺🇸'
        }
    }

    @classmethod
    def get_current_session(cls) -> tuple[str, list]:
        """
        Get active trading session(s).
        Returns: (Formatted Text, List of Active Session Names)
        """
        current_time = datetime.now(pytz.UTC).time()
        active_sessions = []

        # Check each session
        for session_name, details in cls.TRADING_SESSIONS.items():
            start = datetime.strptime(details['start'], '%H:%M').time()
            end = datetime.strptime(details['end'], '%H:%M').time()

            # Handle overnight sessions (e.g. Sydney starting 22:00)
            if start > end:
                if current_time >= start or current_time < end:
                    active_sessions.append(session_name)
            else:
                if start <= current_time < end:
                    active_sessions.append(session_name)

        # Format Output
        if not active_sessions:
            return "📈 Session: After Hours ⛔", []

        elif len(active_sessions) == 1:
            session = active_sessions[0]
            # emoji = cls.TRADING_SESSIONS[session]['emoji']
            return f"📈 Session: {session} (Active) ✅", active_sessions

        else:
            # Overlap
            names = " + ".join(active_sessions)
            return f"📈 Sessions: {names} (Overlap) 🔥", active_sessions

    @classmethod
    def get_session_time_remaining(cls) -> str:
        """Calculate time remaining for current session(s)"""
        # Simplified for header usage: usually just session name is enough
        # This can be expanded for detailed view
        return ""
