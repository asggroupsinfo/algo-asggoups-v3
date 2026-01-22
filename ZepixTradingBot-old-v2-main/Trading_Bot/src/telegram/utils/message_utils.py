"""
Message Utils - Safe Message Operations

Provides safe wrappers for editing messages to prevent common API errors
like 'Message Not Modified' or 'Message Not Found'.

Version: 1.0.0
Created: 2026-01-21
"""

import logging
from telegram import Update
from telegram.error import BadRequest

logger = logging.getLogger(__name__)

async def safe_edit_message(update: Update, text: str, reply_markup=None, parse_mode='Markdown'):
    """Safely edit a message or send new if edit fails"""
    query = update.callback_query

    if not query:
        # Not a callback, just send
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        return

    try:
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    except BadRequest as e:
        if "Message is not modified" in str(e):
            # Ignore harmless warning
            pass
        elif "Message to edit not found" in str(e):
            # Message gone, send new one
            await query.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        else:
            logger.error(f"Failed to edit message: {e}")
            # Try sending as new
            try:
                await query.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
            except Exception:
                pass
