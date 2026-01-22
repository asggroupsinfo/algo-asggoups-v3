from ..base_command_handler import BaseCommandHandler
from telegram import Update
from telegram.ext import ContextTypes

class RiskSettingsHandler(BaseCommandHandler):
    def get_command_name(self) -> str: return "/risksettings"
    def requires_plugin_selection(self) -> bool: return False
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE, plugin_context=None):
        if hasattr(self.bot, 'risk_settings_handler'):
            # This logic is circular if self.bot.risk_settings_handler IS this object.
            # But in ControllerBot, self.risk_settings_handler = RiskSettingsHandler(self)
            # So calling handle() calls this execute().
            # I must call the Menu or Logic.
            if hasattr(self.bot, 'risk_menu'):
                 await self.bot.risk_menu.send_menu(update, context)
            else:
                 await update.message.reply_text("Risk Settings Placeholder")
        else:
            await update.message.reply_text("Risk Settings Placeholder")

    # Stub methods for the legacy delegate calls from ControllerBot
    async def handle_set_sl(self, u, c): await SetSLHandler(self.bot).handle(u, c)
    async def handle_set_tp(self, u, c): await SetTPHandler(self.bot).handle(u, c)
    async def handle_daily_limit(self, u, c): await DailyLimitHandler(self.bot).handle(u, c)
    async def handle_max_loss(self, u, c): await MaxLossHandler(self.bot).handle(u, c)
    async def handle_max_profit(self, u, c): await MaxProfitHandler(self.bot).handle(u, c)
    async def handle_risk_tier(self, u, c): await RiskTierHandler(self.bot).handle(u, c)
    async def handle_sl_system(self, u, c): await SLSystemHandler(self.bot).handle(u, c)
    async def handle_trail_sl(self, u, c): await TrailSLHandler(self.bot).handle(u, c)
    async def handle_breakeven(self, u, c): await BreakevenHandler(self.bot).handle(u, c)
    async def handle_protection(self, u, c): await ProtectionHandler(self.bot).handle(u, c)
