"""
    Telegram event handlers
"""
import json

from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from dtb.settings import DEBUG
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.broadcast_message.handlers import handle_incoming_message, handle_incoming_category_button
from tgbot.handlers.budget.handlers import budget_categories
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.onboarding.manage_data import ENTER_EXPENSE_BUTTON
from tgbot.handlers.utils import error
from tgbot.main import bot


def match_category_callback(callback_query):
    data = json.loads(callback_query)
    return data.get('button_name') == 'BUTTON_CATEGORY'



def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    # onboarding
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))

    # admin commands
    dp.add_handler(CommandHandler("admin", admin_handlers.admin))
    dp.add_handler(CommandHandler("stats", admin_handlers.stats))
    dp.add_handler(CommandHandler('export_users', admin_handlers.export_users))

    dp.add_handler(CallbackQueryHandler(budget_categories, pattern=f"^{ENTER_EXPENSE_BUTTON}"))

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # EXAMPLES FOR HANDLERS
    dp.add_handler(MessageHandler(Filters.all, handle_incoming_message))

    dp.add_handler(CallbackQueryHandler(handle_incoming_category_button, pattern=match_category_callback))

    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
