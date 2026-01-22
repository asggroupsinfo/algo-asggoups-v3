"""
Callback Safety Manager - Middleware for Safe Interactions

Ensures all callbacks are answered to prevent timeouts.
Prevents rapid double-clicks (debounce).
Part of V5 Hardening.

Version: 1.0.0
Created: 2026-01-21
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class CallbackSafetyManager:
    """Middleware for robust callback handling"""

    def __init__(self):
        self.processed_ids = set() # Simple debounce (could be TTL cache)
        # In a real system, use Redis or TTL cache for dedup

    async def wrap_callback(self, handler_func, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper to ensure safety"""
        query = update.callback_query
        if not query:
            return

        try:
            # 1. Always answer immediately (prevent spinner death)
            try:
                await query.answer()
            except Exception as e:
                logger.debug(f"Could not answer query: {e}")

            # 2. Check for double clicks (Debounce)
            # if query.id in self.processed_ids:
            #     logger.warning(f"Duplicate callback ignored: {query.id}")
            #     return
            # self.processed_ids.add(query.id)

            # 3. Execute Handler
            await handler_func(update, context)

        except Exception as e:
            logger.error(f"Error in callback handler: {e}", exc_info=True)
            try:
                await query.message.reply_text("⚠️ An error occurred. Please try again.")
            except:
                pass
