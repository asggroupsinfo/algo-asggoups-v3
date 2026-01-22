from src.core.plugin_system import BaseLogicPlugin
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class TemplatePlugin(BaseLogicPlugin):
    """
    Template plugin - copy this to create new plugins.
    
    Steps to create a new plugin:
    1. Copy this template directory
    2. Rename to your plugin ID (e.g., `my_logic`)
    3. Update class name (e.g., `MyLogicPlugin`)
    4. Implement process_entry_signal, process_exit_signal, process_reversal_signal
    5. Update config.json with your plugin settings
    6. Register plugin in main config
    """
    
    def __init__(self, plugin_id: str, config: Dict[str, Any], service_api):
        super().__init__(plugin_id, config, service_api)
        
        # Plugin-specific initialization
        self.logger.info(f"Template Plugin '{plugin_id}' initialized")
    
    async def process_entry_signal(self, alert) -> Dict[str, Any]:
        """
        Process entry signal.
        
        Example implementation:
        1. Validate alert
        2. Calculate lot size using service_api.risk_management
        3. Place order using service_api.order_execution
        4. Record trade in database
        5. Send notification using service_api.telegram
        """
        self.logger.info(f"Processing entry signal for {getattr(alert, 'symbol', 'UNKNOWN')}")

        try:
            # Step 1: Validate the alert to ensure it contains the necessary data.
            # This is a crucial first step to prevent errors in subsequent processing.
            if not all(hasattr(alert, attr) for attr in ['symbol', 'price', 'stop_loss']):
                error_message = "Invalid alert received: Missing required fields (symbol, price, or stop_loss)."
                self.logger.error(error_message)
                return {"success": False, "message": error_message, "plugin_id": self.plugin_id}

            # Step 2: Calculate the appropriate lot size based on risk management rules.
            # This helps in managing the trade risk effectively.
            lot_size = await self.service_api.risk_management.calculate_lot_size(
                symbol=alert.symbol,
                entry_price=alert.price,
                stop_loss_price=alert.stop_loss
            )
            if lot_size is None or lot_size <= 0:
                message = "Failed to calculate a valid lot size."
                self.logger.warning(message)
                return {"success": False, "message": message, "plugin_id": self.plugin_id}

            # Step 3: Prepare and place the order with the calculated details.
            # The order_details dictionary gathers all necessary information for execution.
            order_details = {
                "symbol": alert.symbol,
                "lot_size": lot_size,
                "entry_price": alert.price,
                "stop_loss": alert.stop_loss,
                "take_profit": getattr(alert, 'take_profit', None),
                "order_type": "MARKET"
            }
            order_result = await self.service_api.order_execution.place_order(order_details)
            if not order_result or not order_result.get('success'):
                message = f"Failed to place order for {alert.symbol}."
                self.logger.error(message)
                return {"success": False, "message": message, "plugin_id": self.plugin_id}

            trade_id = order_result.get('trade_id')
            self.logger.info(f"Successfully placed order for {alert.symbol} with trade ID {trade_id}.")

            # Step 4: Record the trade in the database
            db_record = {**order_details, "trade_id": trade_id, "status": "OPEN"}
            record_success = await self.service_api.database.record_trade(db_record)
            if not record_success:
                self.logger.warning(f"Failed to record trade {trade_id} in the database.")

            # Step 5: Send a notification
            notification_message = (
                f"✅ New Entry Signal Processed\n"
                f"Plugin: {self.plugin_id}\n"
                f"Symbol: {alert.symbol}\n"
                f"Lot Size: {lot_size}\n"
                f"Entry Price: {alert.price}"
            )
            await self.service_api.telegram.send_notification(notification_message)

            return {
                "success": True,
                "message": f"Entry signal for {alert.symbol} processed successfully.",
                "plugin_id": self.plugin_id,
                "trade_id": trade_id
            }

        except Exception as e:
            self.logger.error(f"An unexpected error occurred in process_entry_signal for {getattr(alert, 'symbol', 'UNKNOWN')}: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"An unexpected error occurred: {e}",
                "plugin_id": self.plugin_id
            }
    
    async def process_exit_signal(self, alert) -> Dict[str, Any]:
        """Process exit signal"""
        self.logger.info(f"Processing exit signal for {getattr(alert, 'symbol', 'UNKNOWN')}")
        
        # TODO: Implement your exit logic
        
        return {
            "success": True,
            "message": "Exit processed (template)",
            "plugin_id": self.plugin_id
        }
    
    async def process_reversal_signal(self, alert) -> Dict[str, Any]:
        """Process reversal signal"""
        self.logger.info(f"Processing reversal signal for {getattr(alert, 'symbol', 'UNKNOWN')}")
        
        # TODO: Implement your reversal logic
        
        return {
            "success": True,
            "message": "Reversal processed (template)",
            "plugin_id": self.plugin_id
        }
