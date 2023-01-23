"""
    Telegram event handlers
"""

from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from budget.handlers.categories.patterns import match_category_callback
from budget.handlers.stats.handlers import show_stats
from dtb.settings import DEBUG
from tgbot.handlers.admin import handlers as admin_handlers
from budget.handlers.general.handlers import handle_incoming_message
from budget.handlers.categories.handlers import handle_incoming_category_button, budget_categories, budget_new_category
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.onboarding.manage_data import CHOOSE_CATEGORY_BUTTON
from tgbot.handlers.utils import error
from tgbot.main import bot
from tgbot.system_commands import set_up_commands


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    dp.add_handler(CommandHandler("enter_expense", budget_categories))
    dp.add_handler(CommandHandler("add_category", budget_new_category))
    dp.add_handler(CommandHandler("show_stats", show_stats))
    dp.add_handler(CommandHandler("export_to_excel", admin_handlers.export_users))
    dp.add_handler(CommandHandler("open_excel", admin_handlers.export_users))
    dp.add_handler(CommandHandler("github_repo", admin_handlers.export_users))

    dp.add_handler(CallbackQueryHandler(budget_categories, pattern=f"^{CHOOSE_CATEGORY_BUTTON}"))
    dp.add_handler(CallbackQueryHandler(handle_incoming_category_button, pattern=match_category_callback))


    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # general handler for incoming messages
    dp.add_handler(MessageHandler(Filters.all, handle_incoming_message))
    return dp


set_up_commands(bot)
n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
