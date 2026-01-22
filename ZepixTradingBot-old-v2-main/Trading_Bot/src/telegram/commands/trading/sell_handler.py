from ..base_command_handler import BaseCommandHandler
from telegram import Update
from telegram.ext import ContextTypes

class SellHandler(BaseCommandHandler):
    def get_command_name(self) -> str:
        return "/sell"

    def requires_plugin_selection(self) -> bool:
        return True

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE, plugin_context=None):
        if hasattr(self.bot, 'trading_flow'):
            await self.bot.trading_flow.start_sell(update, context)
        else:
            await update.message.reply_text("💰 Sell Wizard: Not available yet.")
