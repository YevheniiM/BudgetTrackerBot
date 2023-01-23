from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import CHOOSE_CATEGORY_BUTTON


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton('Excel Document', url="https://github.com/ohld/django-telegram-bot"),
        InlineKeyboardButton('Enter Expense', callback_data=f'{CHOOSE_CATEGORY_BUTTON}')
    ]]

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_enter_expense() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton('Categories', callback_data=f'{CHOOSE_CATEGORY_BUTTON}')
    ]]

    return InlineKeyboardMarkup(buttons)
