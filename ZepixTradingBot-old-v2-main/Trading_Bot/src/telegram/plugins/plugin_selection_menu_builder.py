"""
Plugin Selection Menu - Context Switcher UI

UI for selecting V3/V6/Both contexts.
Used by CommandInterceptor and BaseCommandHandler.

Version: 1.0.0
Created: 2026-01-21
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ..core.base_menu_builder import BaseMenuBuilder

class PluginSelectionMenu(BaseMenuBuilder):

    def build_menu(self, command: str) -> dict:
        """Build the selection menu for a specific command"""

        keyboard = [
            [
                InlineKeyboardButton("🔵 V3 Only", callback_data=f"plugin_select_v3_{command}"),
                InlineKeyboardButton("🟢 V6 Only", callback_data=f"plugin_select_v6_{command}")
            ],
            [
                InlineKeyboardButton("🔷 Both Plugins", callback_data=f"plugin_select_both_{command}")
            ],
            [
                InlineKeyboardButton("❌ Cancel", callback_data="nav_main_menu")
            ]
        ]

        return {
            "text": f"🔌 **SELECT PLUGIN CONTEXT**\n━━━━━━━━━━━━━━━━━━━━━━━━\nCommand: `/{command}`\n\nPlease select which plugin to apply this command to:",
            "reply_markup": InlineKeyboardMarkup(keyboard)
        }
