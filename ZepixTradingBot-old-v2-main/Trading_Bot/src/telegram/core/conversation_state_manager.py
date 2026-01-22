"""
Conversation State Manager - Multi-Step Flow Tracking

Manages user state for multi-step wizards (e.g., Buy, SetLot).
Stores temporary data (e.g., selected symbol, lot size) until execution.
Includes Thread-Safe Locking.
Part of V5 Zero-Typing System.

Version: 1.1.0 (Async Locking)
Created: 2026-01-21
"""

from typing import Dict, Any, Optional, List, Callable
import asyncio

class ConversationState:
    """Stores state for a single user's conversation flow"""

    def __init__(self, command: str = None):
        self.command = command
        self.step = 0
        self.data: Dict[str, Any] = {}
        self.breadcrumb: List[str] = []
        self.last_message_id: Optional[int] = None

    def add_data(self, key: str, value: Any):
        self.data[key] = value

    def next_step(self):
        self.step += 1

    def get_data(self, key: str, default=None):
        return self.data.get(key, default)

    def set_breadcrumb(self, path: List[str]):
        self.breadcrumb = path

class ConversationStateManager:
    """Singleton to manage states for all users with locking"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConversationStateManager, cls).__new__(cls)
            cls._instance.states = {}  # {chat_id: ConversationState}
            cls._instance.locks = {}   # {chat_id: asyncio.Lock}
        return cls._instance

    def _get_lock(self, chat_id: int) -> asyncio.Lock:
        if chat_id not in self.locks:
            self.locks[chat_id] = asyncio.Lock()
        return self.locks[chat_id]

    async def update_state(self, chat_id: int, updater_func: Callable[[ConversationState], None]):
        """Thread-safe state update"""
        lock = self._get_lock(chat_id)
        async with lock:
            state = self.get_state(chat_id)
            if state:
                updater_func(state)

    def start_flow(self, chat_id: int, command: str) -> ConversationState:
        """Start a new flow (Not locked, usually entry point)"""
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
        # Clean up lock if exists? Usually keep lock object to avoid churn
        # but could remove if memory constraint.

# Global instance
state_manager = ConversationStateManager()
