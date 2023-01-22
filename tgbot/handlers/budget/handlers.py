from telegram import Update
from telegram.ext import CallbackContext

from budget.models import UserStatusEnum, UserStatus
from tgbot.handlers.budget.keyboards import make_keyboard_for_expenses_categories
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User


def budget_categories(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    user_status, _ = UserStatus.objects.get_or_create(user_id=user_id)
    user_status.status = UserStatusEnum.CHOOSING_CATEGORY.value
    user_status.save()

    context.bot.send_message(
        text='Select category. Or just type in, to add a category',
        chat_id=user_id,
        reply_markup=make_keyboard_for_expenses_categories(user_id)
    )