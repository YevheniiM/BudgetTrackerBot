from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def make_keyboard_for_open_excel() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton('Follow Link', url="https://google.com/"),
    ]]

    return InlineKeyboardMarkup(buttons)