"""
Logic2ConfigHandler Handler
Implements /logic2_config command following V5 Architecture.
"""
from telegram import Update
from telegram.ext import ContextTypes
from ...base_command_handler import BaseCommandHandler

class Logic2ConfigHandler(BaseCommandHandler):
    """Handle /logic2_config command"""
    
    def get_command_name(self) -> str:
        return "/logic2_config"
    
    def requires_plugin_selection(self) -> bool:
        return False
    
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: str = None
    ):
        """Execute logic2_config logic"""
        
        legacy_method = "handle_logic2_config"
        if hasattr(self.bot, legacy_method):
            await getattr(self.bot, legacy_method)(update, context)
            return

        await update.message.reply_text(
            f"✅ {self.get_command_name()} executed (V5 initialized)"
        )
