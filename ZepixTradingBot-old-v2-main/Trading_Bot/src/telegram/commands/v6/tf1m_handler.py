"""
Tf1mHandler Handler
Implements /tf1m command following V5 Architecture.
"""
from telegram import Update
from telegram.ext import ContextTypes
from ...base_command_handler import BaseCommandHandler

class Tf1mHandler(BaseCommandHandler):
    """Handle /tf1m command"""
    
    def get_command_name(self) -> str:
        return "/tf1m"
    
    def requires_plugin_selection(self) -> bool:
        return False
    
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: str = None
    ):
        """Execute tf1m logic"""
        
        legacy_method = "handle_tf1m"
        if hasattr(self.bot, legacy_method):
            await getattr(self.bot, legacy_method)(update, context)
            return

        await update.message.reply_text(
            f"✅ {self.get_command_name()} executed (V5 initialized)"
        )
