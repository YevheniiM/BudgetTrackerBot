from telegram import Update
from telegram.ext import CallbackContext

from budget.models import Category, UserStatusEnum, Expense
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_enter_expense
from tgbot.handlers.utils.categories import split_categories
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.handlers.utils.send_message import send_message
from users.models import User


def send_or_edit_message(user, bot, expense, chat_id, user_status, users_message):
    text = f'Expense saved: {expense.amount} ({expense.category.name})'
    if user_status.status == UserStatusEnum.ENTERING_EXPENSE.value:
        send_message(user, bot, chat_id=chat_id, text=text, reply_markup=make_keyboard_for_enter_expense())
    elif user.last_message:
        bot.delete_message(chat_id=chat_id, message_id=users_message)
        bot.edit_message_text(chat_id=chat_id, message_id=user.last_message, text=text,
                              reply_markup=make_keyboard_for_enter_expense())
    else:
        raise Exception()


def handle_incoming_message(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.objects.get(user_id=user_id)
    user_status = user.status

    if user_status.status == UserStatusEnum.DEFAULT:
        context.bot.send_message(chat_id=user_id, text='I am not sure what do you mean...')
    elif user_status.status == UserStatusEnum.CHOOSING_CATEGORY.value:
        categories = split_categories(update.message.text)
        Category.objects.bulk_create([Category(name=c) for c in categories])
        user.categories.add(*Category.objects.filter(name__in=categories))
        send_message(
            user,
            context.bot,
            chat_id=user_id,
            text=f'Created categories: '
                 f'{", ".join(categories)[:-2] + "." if len(categories) > 1 else categories[0] + "."}',
        )
    elif user_status.status.startswith(UserStatusEnum.ENTERING_EXPENSE.value):
        if update.message.text:
            expense_value = float(update.message.text)
            expense = Expense.objects.create(category=user_status.category, amount=expense_value)
            expense.users.add(user)
            send_message(
                user,
                context.bot,
                chat_id=user_id,
                text=f'Expense saved: {expense.amount} ({expense.category.name})',
                reply_markup=make_keyboard_for_enter_expense()
            )
            user_status.status = UserStatusEnum.ENTERING_EXPENSE_MORE_THAN_ONE.value
            user_status.save()
