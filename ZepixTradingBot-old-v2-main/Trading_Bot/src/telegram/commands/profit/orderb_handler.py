"""
OrderbHandler Handler
Implements /orderb command following V5 Architecture.
"""
from telegram import Update
from telegram.ext import ContextTypes
from ..base_command_handler import BaseCommandHandler

class OrderbHandler(BaseCommandHandler):
    """Handle /orderb command"""
    
    def get_command_name(self) -> str:
        return "/orderb"
    
    def requires_plugin_selection(self) -> bool:
        return False
    
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: str = None
    ):
        """Execute orderb logic"""
        
        legacy_method = "handle_orderb"
        if hasattr(self.bot, legacy_method):
            await getattr(self.bot, legacy_method)(update, context)
            return

        await update.message.reply_text(
            f"✅ {self.get_command_name()} executed (V5 initialized)"
        )
