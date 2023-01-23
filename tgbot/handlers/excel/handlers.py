from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.excel.keyboards import make_keyboard_for_open_excel
from tgbot.handlers.utils.info import extract_user_data_from_update


def export_to_excel(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']

    context.bot.send_message(
        chat_id=user_id,
        text='Exporting to Excel',
        reply_markup=make_keyboard_for_open_excel()
    )


def open_excel(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']

    context.bot.send_message(
        chat_id=user_id,
        text='Here will be a link to excel sheet',
        reply_markup=make_keyboard_for_open_excel()
    )