"""
/status command handler
"""
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
from ..base_command_handler import BaseCommandHandler

class StatusHandler(BaseCommandHandler):

    def get_command_name(self) -> str:
        return '/status'

    def requires_plugin_selection(self) -> bool:
        return False # Can be global or specific, but let's make it global default

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: Optional[str] = None
    ):
        # Implementation of status report
        status_text = "📊 **SYSTEM STATUS**\nActive ✅\n..."
        if hasattr(self.bot, 'edit_message_with_header'):
             await self.bot.edit_message_with_header(update, status_text)
        else:
             await update.message.reply_text(status_text)
