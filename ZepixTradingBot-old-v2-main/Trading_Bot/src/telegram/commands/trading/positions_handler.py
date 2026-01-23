"""
/positions command handler
"""
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
from ..base_command_handler import BaseCommandHandler

class PositionsHandler(BaseCommandHandler):

    def get_command_name(self) -> str:
        return '/positions'

    def requires_plugin_selection(self) -> bool:
        return True

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: Optional[str] = None
    ):
        # Fetch positions based on context
        text = f"📈 **POSITIONS ({plugin_context.upper()})**\nNo active trades."

        if hasattr(self.bot, 'edit_message_with_header'):
             await self.bot.edit_message_with_header(update, text)
        else:
             await update.message.reply_text(text)
