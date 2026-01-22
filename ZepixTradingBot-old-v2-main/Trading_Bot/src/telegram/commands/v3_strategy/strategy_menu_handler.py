from ..base_command_handler import BaseCommandHandler
from telegram import Update
from telegram.ext import ContextTypes

class StrategyMenuHandler(BaseCommandHandler):
    def get_command_name(self) -> str: return "/strategy"
    def requires_plugin_selection(self) -> bool: return False
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE, plugin_context=None):
        if hasattr(self.bot, 'v3_menu'):
            await self.bot.v3_menu.send_menu(update, context)
        else:
            await update.message.reply_text("Strategy Menu Placeholder")
