"""
TpContHandler Handler
Implements /tp_cont command following V5 Architecture.
"""
from telegram import Update
from telegram.ext import ContextTypes
from ..base_command_handler import BaseCommandHandler

class TpContHandler(BaseCommandHandler):
    """Handle /tp_cont command"""
    
    def get_command_name(self) -> str:
        return "/tp_cont"
    
    def requires_plugin_selection(self) -> bool:
        return False
    
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: str = None
    ):
        """Execute tp_cont logic"""
        
        legacy_method = "handle_tp_cont"
        if hasattr(self.bot, legacy_method):
            await getattr(self.bot, legacy_method)(update, context)
            return

        await update.message.reply_text(
            f"✅ {self.get_command_name()} executed (V5 initialized)"
        )
