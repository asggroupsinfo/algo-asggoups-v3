"""
ProfitStatsHandler Handler
Implements /profit_stats command following V5 Architecture.
"""
from telegram import Update
from telegram.ext import ContextTypes
from ..base_command_handler import BaseCommandHandler

class ProfitStatsHandler(BaseCommandHandler):
    """Handle /profit_stats command"""
    
    def get_command_name(self) -> str:
        return "/profit_stats"
    
    def requires_plugin_selection(self) -> bool:
        return False
    
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: str = None
    ):
        """Execute profit_stats logic"""
        
        legacy_method = "handle_profit_stats"
        if hasattr(self.bot, legacy_method):
            await getattr(self.bot, legacy_method)(update, context)
            return

        await update.message.reply_text(
            f"✅ {self.get_command_name()} executed (V5 initialized)"
        )
