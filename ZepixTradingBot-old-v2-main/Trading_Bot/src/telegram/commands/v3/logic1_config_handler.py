"""
Logic1ConfigHandler Handler
Implements /logic1_config command following V5 Architecture.
"""
from telegram import Update
from telegram.ext import ContextTypes
from ..base_command_handler import BaseCommandHandler

class Logic1ConfigHandler(BaseCommandHandler):
    """Handle /logic1_config command"""
    
    def get_command_name(self) -> str:
        return "/logic1_config"
    
    def requires_plugin_selection(self) -> bool:
        return False
    
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: str = None
    ):
        """Execute logic1_config logic"""
        
        legacy_method = "handle_logic1_config"
        if hasattr(self.bot, legacy_method):
            await getattr(self.bot, legacy_method)(update, context)
            return

        await update.message.reply_text(
            f"✅ {self.get_command_name()} executed (V5 initialized)"
        )
