from ..base_command_handler import BaseCommandHandler
from telegram import Update
from telegram.ext import ContextTypes

class RiskMenuHandler(BaseCommandHandler):
    def get_command_name(self) -> str: return "/risk"
    def requires_plugin_selection(self) -> bool: return False
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE, plugin_context=None):
        if hasattr(self.bot, 'risk_menu'):
             await self.bot.risk_menu.send_menu(update, context)
        else:
             await update.message.reply_text("Risk Menu Placeholder")
