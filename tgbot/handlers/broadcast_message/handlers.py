import json

import telegram
from telegram import Update
from telegram.ext import CallbackContext

from budget.models import UserStatusEnum, Category, Expense
from dtb.settings import DEBUG
from users.models import User
from users.tasks import broadcast_message
from .keyboards import keyboard_confirm_decline_broadcasting
from .manage_data import CONFIRM_DECLINE_BROADCAST, CONFIRM_BROADCAST
from .static_text import broadcast_command, broadcast_wrong_format, broadcast_no_access, error_with_html, \
    message_is_sent, declined_message_broadcasting
from ..onboarding.keyboards import make_keyboard_for_enter_expense
from ..utils.info import extract_user_data_from_update


def broadcast_command_with_message(update: Update, context: CallbackContext):
    """ Type /broadcast <some_text>. Then check your message in HTML format and broadcast to users."""
    u = User.get_user(update, context)

    if not u.is_admin:
        update.message.reply_text(
            text=broadcast_no_access,
        )
    else:
        if update.message.text == broadcast_command:
            # user typed only command without text for the message.
            update.message.reply_text(
                text=broadcast_wrong_format,
                parse_mode=telegram.ParseMode.HTML,
            )
            return

        text = f"{update.message.text.replace(f'{broadcast_command} ', '')}"
        markup = keyboard_confirm_decline_broadcasting()

        try:
            update.message.reply_text(
                text=text,
                parse_mode=telegram.ParseMode.HTML,
                reply_markup=markup,
            )
        except telegram.error.BadRequest as e:
            update.message.reply_text(
                text=error_with_html.format(reason=e),
                parse_mode=telegram.ParseMode.HTML,
            )


def broadcast_decision_handler(update: Update, context: CallbackContext) -> None:
    # callback_data: CONFIRM_DECLINE_BROADCAST variable from manage_data.py
    """ Entered /broadcast <some_text>.
        Shows text in HTML style with two buttons:
        Confirm and Decline
    """
    broadcast_decision = update.callback_query.data[len(CONFIRM_DECLINE_BROADCAST):]

    entities_for_celery = update.callback_query.message.to_dict().get('entities')
    entities, text = update.callback_query.message.entities, update.callback_query.message.text

    if broadcast_decision == CONFIRM_BROADCAST:
        admin_text = message_is_sent
        user_ids = list(User.objects.all().values_list('user_id', flat=True))

        if DEBUG:
            broadcast_message(
                user_ids=user_ids,
                text=text,
                entities=entities_for_celery,
            )
        else:
            # send in async mode via celery
            broadcast_message.delay(
                user_ids=user_ids,
                text=text,
                entities=entities_for_celery,
            )
    else:
        context.bot.send_message(
            chat_id=update.callback_query.message.chat_id,
            text=declined_message_broadcasting,
        )
        admin_text = text

    context.bot.edit_message_text(
        text=admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        entities=None if broadcast_decision == CONFIRM_BROADCAST else entities,
    )


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
        if update.message.text:
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
