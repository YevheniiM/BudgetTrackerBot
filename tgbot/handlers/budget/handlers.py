from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.budget.keyboards import make_keyboard_for_expenses_categories
from tgbot.handlers.utils.info import extract_user_data_from_update


def budget_categories(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']

    context.bot.send_message(
        text='Select category',
        chat_id=user_id,
        reply_markup=make_keyboard_for_expenses_categories()
    )