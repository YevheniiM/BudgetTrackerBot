from telegram import Update
from telegram.ext import CallbackContext

from budget.models import UserStatusEnum
from excel.core.core import populate_google_sheet_with_expenses_data
from tgbot.handlers.excel.keyboards import make_keyboard_for_open_excel
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User


def export_to_excel(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.objects.get(user_id=user_id)

    populated = populate_google_sheet_with_expenses_data(user)
    text = 'Exporting to Excel' if populated else 'No expenses found so far'
    context.bot.send_message(
        chat_id=user_id,
        text=text,
        reply_markup=make_keyboard_for_open_excel(user)
    )


def open_excel(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.objects.get(user_id=user_id)

    context.bot.send_message(
        chat_id=user_id,
        text='Here is the link to excel sheet',
        reply_markup=make_keyboard_for_open_excel(user)
    )


def request_email_address(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.objects.get(user_id=user_id)
    user.status.status = UserStatusEnum.ENTERING_EMAIL.value
    user.status.save()

    context.bot.send_message(
        chat_id=user_id,
        text='Enter your email address:',
    )