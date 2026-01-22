"""
Base Menu Builder
All menu builders inherit from this.
Provides consistent button and keyboard creation.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class BaseMenuBuilder(ABC):
    """
    Base class for all menu builders.
    """

    @abstractmethod
    def build_menu(
        self,
        menu_type: str,
        plugin_context: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Build menu with text and keyboard.

        Args:
            menu_type: Type of menu to build
            plugin_context: 'v3', 'v6', 'both', or None
            **kwargs: Additional parameters

        Returns:
            {
                'text': 'Menu text (HTML formatted)',
                'keyboard': InlineKeyboardMarkup,
                'parse_mode': 'HTML'
            }
        """
        pass

    def create_button(
        self,
        text: str,
        callback_data: str
    ) -> InlineKeyboardButton:
        """Create a single button"""
        return InlineKeyboardButton(text=text, callback_data=callback_data)

    def create_keyboard(
        self,
        buttons: List[List[InlineKeyboardButton]]
    ) -> InlineKeyboardMarkup:
        """Create keyboard from button layout"""
        return InlineKeyboardMarkup(buttons)

    def create_row(
        self,
        *buttons: InlineKeyboardButton
    ) -> List[InlineKeyboardButton]:
        """Create a row of buttons"""
        return list(buttons)
