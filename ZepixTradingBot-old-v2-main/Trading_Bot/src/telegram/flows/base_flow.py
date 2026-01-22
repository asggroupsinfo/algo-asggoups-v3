"""
Base Flow - Abstract Class for Wizards

Provides common logic for step-by-step flows.
Integrates with ConversationStateManager.

Version: 1.0.0
Created: 2026-01-21
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..core.conversation_state_manager import state_manager
from ..core.sticky_header_builder import StickyHeaderBuilder

class BaseFlow:

    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.state_manager = state_manager
        # Init header builder safely
        if hasattr(self.bot, 'sticky_header'):
            self.header_builder = self.bot.sticky_header
        else:
            self.header_builder = StickyHeaderBuilder()

    async def start_flow(self, update: Update, context: ContextTypes.DEFAULT_TYPE, command: str):
        """Initialize a flow"""
        chat_id = update.effective_chat.id
        self.state_manager.start_flow(chat_id, command)
        await self.show_step(update, context)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Handle flow callback"""
        # To be implemented by subclasses
        return False

    async def show_step(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show current step UI"""
        # To be implemented by subclasses
        pass

    async def cancel_flow(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel and clean up"""
        chat_id = update.effective_chat.id
        self.state_manager.clear_state(chat_id)
        if hasattr(self.bot, 'handle_start'):
            await self.bot.handle_start(update, context)

    async def edit_message(self, update: Update, text: str, keyboard: list):
        """Helper to edit message with header"""
        header = self.header_builder.build_header(style='compact')
        full_text = f"{header}\n{text}"

        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=full_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                text=full_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
