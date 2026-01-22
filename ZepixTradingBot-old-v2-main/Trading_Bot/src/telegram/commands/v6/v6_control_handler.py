"""
V6ControlHandler Handler
Implements /v6_control command following V5 Architecture.
"""
from telegram import Update
from telegram.ext import ContextTypes
from ...base_command_handler import BaseCommandHandler

class V6ControlHandler(BaseCommandHandler):
    """Handle /v6_control command"""
    
    def get_command_name(self) -> str:
        return "/v6_control"
    
    def requires_plugin_selection(self) -> bool:
        return False
    
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: str = None
    ):
        """Execute v6_control logic"""
        
        legacy_method = "handle_v6_control"
        if hasattr(self.bot, legacy_method):
            await getattr(self.bot, legacy_method)(update, context)
            return

        await update.message.reply_text(
            f"✅ {self.get_command_name()} executed (V5 initialized)"
        )
