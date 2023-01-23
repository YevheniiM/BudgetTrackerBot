import json

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from users.models import User


def make_keyboard_for_expenses_categories(user_id) -> InlineKeyboardMarkup:
    categories = User.objects.get(user_id=user_id).categories.all()
    buttons = []
    for i in range(0, len(categories), 3):
        row = []
        for j in range(i, min(i + 3, len(categories))):
            row.append(InlineKeyboardButton(categories[j].name, callback_data=json.dumps({
                'id': categories[j].id,
                'button_name': 'BUTTON_CATEGORY'
            })))
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)
