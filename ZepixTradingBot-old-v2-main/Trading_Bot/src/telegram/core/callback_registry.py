"""
Callback Registry - Central Dictionary of Valid Callbacks

Maps callback strings to descriptions for validation and documentation.
Part of V5 Zero-Typing System.

Version: 1.0.0
Created: 2026-01-21
"""

CALLBACK_REGISTRY = {
    # System
    'system_status': 'Show bot status',
    'system_pause': 'Pause menu',
    'system_resume': 'Resume menu',
    'system_restart': 'Restart bot',

    # Trading
    'trading_positions': 'Show positions',
    'trading_buy_start': 'Start buy wizard',
    'trading_sell_start': 'Start sell wizard',
    'trading_closeall': 'Close all positions',

    # Risk
    'risk_setlot_start': 'Start setlot wizard',
    'risk_setsl_start': 'Start setsl wizard',

    # Flows (Dynamic patterns handled by regex in router, but prefixes listed here)
    'flow_trade_': 'Trading flow actions',
    'flow_risk_': 'Risk flow actions',

    # Navigation
    'nav_main_menu': 'Return to main',
    'nav_back': 'Go back',

    # Plugin Selection
    'plugin_select_': 'Plugin context selection'
}

def parse_callback_data(callback_data: str) -> dict:
    """
    Parse standard callback format: category_action_target_value
    """
    parts = callback_data.split('_')
    return {
        'category': parts[0],
        'action': parts[1] if len(parts) > 1 else None,
        'target': parts[2] if len(parts) > 2 else None,
        'value': "_".join(parts[3:]) if len(parts) > 3 else None
    }
