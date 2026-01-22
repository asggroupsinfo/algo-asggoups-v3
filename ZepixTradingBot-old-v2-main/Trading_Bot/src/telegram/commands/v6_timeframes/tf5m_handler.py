from ..base_command_handler import BaseCommandHandler
from telegram import Update
from telegram.ext import ContextTypes

class TF5mHandler(BaseCommandHandler):
    def get_command_name(self) -> str: return "/tf5m"
    def requires_plugin_selection(self) -> bool: return False
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE, plugin_context=None):
        await update.message.reply_text("5m Config Placeholder")
