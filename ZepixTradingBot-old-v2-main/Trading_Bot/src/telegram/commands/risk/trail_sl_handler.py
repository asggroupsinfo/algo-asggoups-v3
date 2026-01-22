from ..base_command_handler import BaseCommandHandler
from telegram import Update
from telegram.ext import ContextTypes

class TrailSLHandler(BaseCommandHandler):
    def get_command_name(self) -> str: return "/trailsl"
    def requires_plugin_selection(self) -> bool: return True
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE, plugin_context=None):
        await update.message.reply_text("Trailing SL Placeholder")
