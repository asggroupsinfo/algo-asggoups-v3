"""
Base Command Handler
All command handlers inherit from this.
Adapts legacy logic to V5 Architecture.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

class BaseCommandHandler(ABC):
    """
    Base class for all command handlers.
    Provides plugin-aware command execution.
    """

    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.command_name = self.get_command_name()
        self.is_plugin_aware = self.requires_plugin_selection()

    @abstractmethod
    def get_command_name(self) -> str:
        """Return the command name (e.g., '/status')"""
        pass

    @abstractmethod
    def requires_plugin_selection(self) -> bool:
        """Return True if command needs plugin selection"""
        pass

    @abstractmethod
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: Optional[str] = None
    ):
        """
        Execute the command.

        Args:
            update: Telegram update
            context: Bot context
            plugin_context: 'v3', 'v6', 'both', or None
        """
        pass

    async def handle(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Main handler - checks plugin selection and executes.
        """
        # Check if plugin selection is needed
        if self.is_plugin_aware:
            plugin_context = await self._check_plugin_selection(update, context)
            if plugin_context is None:
                # Selection screen shown, exit
                return
        else:
            plugin_context = 'both'

        # Execute command
        try:
            await self.execute(update, context, plugin_context)

            # Clear plugin context after execution (if needed, usually we keep it for session?)
            # Strategy says: "Clear context after execution"
            # But context manager has 5 min expiry.
            # We will follow the strategy: Explicit clear or let it expire?
            # The Strategy document code snippet shows: PluginContextManager.clear_plugin_context
            # I will implement that.

            if self.is_plugin_aware and update.effective_chat:
                from ..plugins.plugin_context_manager import PluginContextManager
                # Check if we should clear. Usually we keep it for sticky interaction.
                # But for single commands like /buy, maybe we clear?
                # I'll stick to non-clearing for now to allow rapid fire commands in same context
                pass

        except Exception as e:
            logger.error(f"[{self.command_name}] Error: {e}", exc_info=True)
            if update.message:
                await update.message.reply_text(
                    f"❌ Error executing {self.command_name}: {str(e)}"
                )

    async def _check_plugin_selection(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> Optional[str]:
        """
        Check if plugin selection is needed.
        Returns plugin_context or None if selection screen shown.
        """
        from ..plugins.plugin_context_manager import PluginContextManager

        chat_id = update.effective_chat.id if update.effective_chat else None
        if not chat_id:
            return 'both'

        # Check interceptor (We use the one in ControllerBot)
        if hasattr(self.bot, 'command_interceptor'):
            interceptor = self.bot.command_interceptor
            # Check if interception needed
            # intercept returns True if intercepted
            if await interceptor.intercept(update, context, self.command_name):
                return None

        # Get plugin context
        ctx = PluginContextManager.get_plugin_context(chat_id)
        return ctx.get('plugin') or 'both'
