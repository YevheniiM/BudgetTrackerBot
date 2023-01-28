import json

from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.categories.keyboards import make_keyboard_for_expenses_categories
from budget.models import Category, UserStatusEnum, UserStatus
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User


def handle_incoming_category_button(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.objects.get(user_id=user_id)
    user_status = user.status

    input_category = json.loads(update.callback_query.data).get('id')

    category = Category.objects.get(id=int(input_category))
    user_status.category = category
    user_status.status = UserStatusEnum.ENTERING_EXPENSE.value
    user_status.save()

    context.bot.send_message(
        chat_id=user_id,
        text='Enter an expense',
    )


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

def batch_expenses(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    user_status, _ = UserStatus.objects.get_or_create(user_id=user_id)
    user_status.status = UserStatusEnum.BATCH_ENTERING_EXPENSE.value
    user_status.save()

    context.bot.send_message(
        text='Enter all expenses in the following format: \n'
             'expense, category, date(YY-mm-dd)',
        chat_id=user_id,
    )


def budget_new_category(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    user_status, _ = UserStatus.objects.get_or_create(user_id=user_id)
    user_status.status = UserStatusEnum.CHOOSING_CATEGORY.value
    user_status.save()

    context.bot.send_message(
        text='Type in, to add a category (you can type as many as you want in one message)',
        chat_id=user_id
    )
