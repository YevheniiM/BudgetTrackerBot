from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def make_keyboard_for_expenses_categories() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton('Category 1', callback_data=f'{"111"}'),
        InlineKeyboardButton('Category 2', callback_data=f'{"111"}'),
        InlineKeyboardButton('Category 3', callback_data=f'{"111"}'),],[
        InlineKeyboardButton('Category 4', callback_data=f'{"111"}'),
        InlineKeyboardButton('Category 5', callback_data=f'{"111"}'),
        InlineKeyboardButton('Category 6', callback_data=f'{"111"}'),],[
        InlineKeyboardButton('Category 7', callback_data=f'{"111"}'),
        InlineKeyboardButton('Category 8', callback_data=f'{"111"}'),
        InlineKeyboardButton('Category 9', callback_data=f'{"111"}'),],[
        InlineKeyboardButton('Category 10', callback_data=f'{"111"}'),
        InlineKeyboardButton('Category 11', callback_data=f'{"111"}'),
    ]]
    return InlineKeyboardMarkup(buttons)