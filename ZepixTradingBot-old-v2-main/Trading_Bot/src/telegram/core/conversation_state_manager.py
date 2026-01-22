"""
Conversation State Manager - Multi-Step Flow Tracking

Manages user state for multi-step wizards (e.g., Buy, SetLot).
Stores temporary data (e.g., selected symbol, lot size) until execution.
Part of V5 Zero-Typing System.

Version: 1.0.0
Created: 2026-01-21
"""

from typing import Dict, Any, Optional, List

class ConversationState:
    """Stores state for a single user's conversation flow"""

    def __init__(self, command: str = None):
        self.command = command  # e.g., 'buy', 'setlot'
        self.step = 0  # Current step number
        self.data: Dict[str, Any] = {}  # Collected data
        self.breadcrumb: List[str] = []  # Navigation path for header
        self.last_message_id: Optional[int] = None # To edit same message

    def add_data(self, key: str, value: Any):
        """Add data collected in this step"""
        self.data[key] = value

    def next_step(self):
        """Move to next step"""
        self.step += 1

    def get_data(self, key: str, default=None):
        """Get previously collected data"""
        return self.data.get(key, default)

    def set_breadcrumb(self, path: List[str]):
        """Update breadcrumb"""
        self.breadcrumb = path

class ConversationStateManager:
    """Singleton to manage states for all users"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConversationStateManager, cls).__new__(cls)
            cls._instance.states = {}  # {chat_id: ConversationState}
        return cls._instance

    def start_flow(self, chat_id: int, command: str) -> ConversationState:
        """Start a new flow"""
        state = ConversationState(command)
        self.states[chat_id] = state
        return state

    def get_state(self, chat_id: int) -> Optional[ConversationState]:
        """Get active state"""
        return self.states.get(chat_id)

    def clear_state(self, chat_id: int):
        """Clear state after completion or cancel"""
        if chat_id in self.states:
            del self.states[chat_id]

# Global instance
state_manager = ConversationStateManager()
