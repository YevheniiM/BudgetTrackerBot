from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.utils.info import extract_user_data_from_update


def show_stats(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']

    context.bot.send_message(
        chat_id=user_id,
        text='Some stats here',
    )
