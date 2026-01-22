"""
Plugin Context Manager - User State Management

Stores user's plugin selection (V3/V6/Both) with expiry.
Part of V5 Plugin Architecture.

Version: 1.0.0
Created: 2026-01-21
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Any

class PluginContextManager:
    """Singleton to manage plugin contexts per user"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PluginContextManager, cls).__new__(cls)
            cls._instance.contexts = {}  # {chat_id: {'plugin': 'v3', 'command': 'cmd', 'timestamp': dt}}
            cls._instance.expiry_seconds = 300  # 5 minutes
        return cls._instance

    @classmethod
    def set_plugin_context(cls, chat_id: int, plugin: str, command: str = None):
        """
        Set the plugin context for a user.
        plugin: 'v3', 'v6', 'both'
        """
        instance = cls()
        instance.contexts[chat_id] = {
            'plugin': plugin.lower(),
            'command': command,
            'timestamp': datetime.now()
        }

    @classmethod
    def get_plugin_context(cls, chat_id: int) -> Dict[str, Any]:
        """
        Get the active plugin context.
        Returns dict with 'plugin' key or {'plugin': None} if expired/missing.
        """
        instance = cls()
        if chat_id not in instance.contexts:
            return {'plugin': None}

        ctx = instance.contexts[chat_id]

        # Check expiry
        if datetime.now() - ctx['timestamp'] > timedelta(seconds=instance.expiry_seconds):
            del instance.contexts[chat_id]
            return {'plugin': None}

        return ctx

    @classmethod
    def has_active_context(cls, chat_id: int) -> bool:
        """Check if user has a valid active context"""
        ctx = cls.get_plugin_context(chat_id)
        return ctx.get('plugin') is not None

    @classmethod
    def clear_context(cls, chat_id: int):
        """Clear user context"""
        instance = cls()
        if chat_id in instance.contexts:
            del instance.contexts[chat_id]

# Alias for compatibility if needed
set_user_plugin = PluginContextManager.set_plugin_context
get_user_plugin = PluginContextManager.get_plugin_context
