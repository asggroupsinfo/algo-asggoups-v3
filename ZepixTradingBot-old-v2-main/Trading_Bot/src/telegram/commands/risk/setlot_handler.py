"""
/setlot command handler
"""
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
from ..base_command_handler import BaseCommandHandler

class SetLotHandler(BaseCommandHandler):

    def get_command_name(self) -> str:
        return '/setlot'

    def requires_plugin_selection(self) -> bool:
        return True

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: Optional[str] = None
    ):
        # Trigger risk flow
        if hasattr(self.bot, 'risk_flow'):
            await self.bot.risk_flow.start_set_lot(update, context)
