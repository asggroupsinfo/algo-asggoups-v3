from ..base_command_handler import BaseCommandHandler
from telegram import Update
from telegram.ext import ContextTypes

class TradeMenuHandler(BaseCommandHandler):
    def get_command_name(self) -> str: return "/trade"
    def requires_plugin_selection(self) -> bool: return False
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE, plugin_context=None):
        if hasattr(self.bot, 'trading_menu'):
             await self.bot.trading_menu.send_menu(update, context)
        else:
             await update.message.reply_text("Trading Menu Placeholder")
