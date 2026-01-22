import os

BASE_PATH = "ZepixTradingBot-old-v2-main/Trading_Bot/src/telegram/commands"

FOLDERS = {
    "trading": [
        "close_handler.py", "closeall_handler.py", "orders_handler.py", 
        "history_handler.py", "pnl_handler.py", "balance_handler.py", 
        "equity_handler.py", "margin_handler.py", "symbols_handler.py", 
        "trades_handler.py", "price_handler.py", "spread_handler.py", 
        "signals_handler.py", "filters_handler.py", "partial_handler.py"
    ],
    "risk": [
        "dailylimit_handler.py", "maxloss_handler.py", "maxprofit_handler.py",
        "risktier_handler.py", "slsystem_handler.py", "trailsl_handler.py",
        "breakeven_handler.py", "protection_handler.py", "multiplier_handler.py",
        "maxtrades_handler.py", "drawdown_handler.py", "risk_handler.py"
    ],
    "system": [
        "help_handler.py", "pause_handler.py", "resume_handler.py", 
        "restart_handler.py", "shutdown_handler.py", "config_handler.py", 
        "health_handler.py", "version_handler.py"
    ],
    "v3": [
        "logic1_handler.py", "logic2_handler.py", "logic3_handler.py",
        "logic1_on_handler.py", "logic1_off_handler.py",
        "logic2_on_handler.py", "logic2_off_handler.py",
        "logic3_on_handler.py", "logic3_off_handler.py",
        "logic1_config_handler.py", "logic2_config_handler.py", 
        "logic3_config_handler.py"
    ],
    "v6": [
        "v6_status_handler.py", "v6_control_handler.py", "v6_config_handler.py",
        "v6_menu_handler.py", 
        "tf1m_handler.py", "tf1m_on_handler.py", "tf1m_off_handler.py",
        "tf5m_handler.py", "tf5m_on_handler.py", "tf5m_off_handler.py",
        "tf15m_handler.py", "tf15m_on_handler.py", "tf15m_off_handler.py",
        "tf30m_handler.py", "tf30m_on_handler.py", "tf30m_off_handler.py",
        "tf1h_handler.py", "tf1h_on_handler.py", "tf1h_off_handler.py",
        "tf4h_handler.py", "tf4h_on_handler.py", "tf4h_off_handler.py",
        "tf1d_handler.py", "v6_performance_handler.py"
    ],
    "analytics": [
        "daily_handler.py", "weekly_handler.py", "monthly_handler.py",
        "compare_handler.py", "pairreport_handler.py", "strategyreport_handler.py",
        "tpreport_handler.py", "stats_handler.py", "winrate_handler.py",
        "drawdown_handler.py", "profit_stats_handler.py", "performance_handler.py",
        "dashboard_handler.py", "export_handler.py", "trends_handler.py"
    ],
    "reentry": [
        "slhunt_handler.py", "sl_hunt_handler.py", "tpcontinue_handler.py",
        "tp_cont_handler.py", "reentry_handler.py", "reentry_config_handler.py",
        "recovery_handler.py", "cooldown_handler.py", "chains_handler.py",
        "autonomous_handler.py", "chainlimit_handler.py", "reentry_v3_handler.py",
        "reentry_v6_handler.py", "autonomous_control_handler.py",
        "sl_hunt_stats_handler.py"
    ],
    "profit": [
        "dualorder_handler.py", "orderb_handler.py", "order_b_handler.py",
        "profit_handler.py", "booking_handler.py", "levels_handler.py",
        "dual_status_handler.py", "profit_config_handler.py"
    ]
}

TEMPLATE = """\"\"\"
{class_name} Handler
Implements /{command_name} command following V5 Architecture.
\"\"\"
from telegram import Update
from telegram.ext import ContextTypes
from ...base_command_handler import BaseCommandHandler

class {class_name}(BaseCommandHandler):
    \"\"\"Handle /{command_name} command\"\"\"
    
    def get_command_name(self) -> str:
        return "/{command_name}"
    
    def requires_plugin_selection(self) -> bool:
        return False
    
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        plugin_context: str = None
    ):
        \"\"\"Execute {command_name} logic\"\"\"
        
        legacy_method = "handle_{command_name}"
        if hasattr(self.bot, legacy_method):
            await getattr(self.bot, legacy_method)(update, context)
            return

        await update.message.reply_text(
            f"✅ {{self.get_command_name()}} executed (V5 initialized)"
        )
"""

def to_class_name(filename):
    name = filename.replace("_handler.py", "")
    parts = name.split('_')
    return "".join(p.capitalize() for p in parts) + "Handler"

def to_command(filename):
    return filename.replace("_handler.py", "")

def main():
    print(f"Creating handlers in {BASE_PATH}...")
    
    for folder, files in FOLDERS.items():
        folder_path = os.path.join(BASE_PATH, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        for filename in files:
            file_path = os.path.join(folder_path, filename)
            if not os.path.exists(file_path):
                class_name = to_class_name(filename)
                command_name = to_command(filename)
                content = TEMPLATE.format(
                    class_name=class_name,
                    command_name=command_name
                )
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Created: {folder}/{filename}")
            else:
                print(f"Skipped (Exists): {folder}/{filename}")

    print("Done! All handlers created.")

if __name__ == "__main__":
    main()
