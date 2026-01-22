from ..base_command_handler import BaseCommandHandler
from telegram import Update
from telegram.ext import ContextTypes

class PnLHandler(BaseCommandHandler):
    def get_command_name(self) -> str:
        return "/pnl"

    def requires_plugin_selection(self) -> bool:
        return True

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE, plugin_context=None):
        if hasattr(self.bot, 'trading_info_handler'):
            await self.bot.trading_info_handler.handle_pnl(update, context)
        else:
            await update.message.reply_text("💰 P&L: Not available yet.")
