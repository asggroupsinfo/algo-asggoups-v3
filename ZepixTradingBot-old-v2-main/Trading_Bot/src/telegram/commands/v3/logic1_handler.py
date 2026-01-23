"""
Logic1Handler Handler
Implements /logic1 command following V5 Architecture.
"""
from telegram import Update
from telegram.ext import ContextTypes
from ..base_command_handler import BaseCommandHandler

class Logic1Handler(BaseCommandHandler):
    """Handle /logic1 command"""
    
    def get_command_name(self) -> str:
        return "/logic1"
    
    def requires_plugin_selection(self) -> bool:
        return False
    
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: str = None
    ):
        """Execute logic1 logic"""
        
        legacy_method = "handle_logic1"
        if hasattr(self.bot, legacy_method):
            await getattr(self.bot, legacy_method)(update, context)
            return

        await update.message.reply_text(
            f"✅ {self.get_command_name()} executed (V5 initialized)"
        )
