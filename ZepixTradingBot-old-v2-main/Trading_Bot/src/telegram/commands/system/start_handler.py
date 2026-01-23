"""
/start command handler
"""
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
from ..base_command_handler import BaseCommandHandler

class StartHandler(BaseCommandHandler):

    def get_command_name(self) -> str:
        return '/start'

    def requires_plugin_selection(self) -> bool:
        return False

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: Optional[str] = None
    ):
        # Delegate to main menu
        if hasattr(self.bot, 'main_menu'):
            await self.bot.main_menu.send_menu(update, context)
