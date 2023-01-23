from telegram import Update
from telegram.ext import CallbackContext

from budget.models import Category, UserStatusEnum, Expense
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_enter_expense
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User


def handle_incoming_message(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.objects.get(user_id=user_id)
    user_status = user.status

    if user_status.status == UserStatusEnum.DEFAULT:
        context.bot.send_message(
            chat_id=user_id,
            text='I am not sure what do you mean...',
        )
    elif user_status.status == UserStatusEnum.CHOOSING_CATEGORY.value:
        category = Category.objects.create(name=update.message.text)
        category.users.add(user)
        context.bot.send_message(
            chat_id=user_id,
            text=f'Created category: {category.name}',
        )
    elif user_status.status == UserStatusEnum.ENTERING_EXPENSE.value:
        if update.message.text:
            expense_value = float(update.message.text)
            expense = Expense.objects.create(category=user_status.category,
                                             amount=expense_value)
            expense.users.add(user)
            context.bot.send_message(
                chat_id=user_id,
                text=f'Expense entered',
                reply_markup=make_keyboard_for_enter_expense()
            )
