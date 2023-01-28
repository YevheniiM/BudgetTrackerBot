"""
    Telegram event handlers
"""

from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from tgbot.handlers.categories.patterns import match_category_callback
from tgbot.handlers.excel.handlers import export_to_excel, open_excel, request_email_address
from tgbot.handlers.excel.manage_data import GET_ACCESS_BUTTON
from tgbot.handlers.stats.handlers import show_stats
from dtb.settings import DEBUG
from tgbot.handlers.general.handlers import handle_incoming_message
from tgbot.handlers.categories.handlers import handle_incoming_category_button, budget_categories, budget_new_category, \
    batch_expenses
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.onboarding.manage_data import CHOOSE_CATEGORY_BUTTON
from tgbot.handlers.utils import error
from tgbot.main import bot
from tgbot.system_commands import set_up_commands


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    dp.add_handler(CommandHandler("enter_expense", budget_categories))
    dp.add_handler(CommandHandler("enter_batch_expense", batch_expenses))
    dp.add_handler(CommandHandler("add_category", budget_new_category))
    dp.add_handler(CommandHandler("show_stats", show_stats))
    dp.add_handler(CommandHandler("export_to_excel", export_to_excel))
    dp.add_handler(CommandHandler("open_excel", open_excel))

    dp.add_handler(CallbackQueryHandler(budget_categories, pattern=f"^{CHOOSE_CATEGORY_BUTTON}"))
    dp.add_handler(CallbackQueryHandler(handle_incoming_category_button, pattern=match_category_callback))

    dp.add_handler(CallbackQueryHandler(request_email_address, pattern=f"^{GET_ACCESS_BUTTON}"))

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # general handler for incoming messages
    dp.add_handler(MessageHandler(Filters.all, handle_incoming_message))
    return dp


# set_up_commands(bot)
n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
