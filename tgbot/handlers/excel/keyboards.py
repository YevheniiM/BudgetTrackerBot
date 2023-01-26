from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from excel.core.sheet_manager import SheetManager
from tgbot.handlers.excel.manage_data import GET_ACCESS_BUTTON


def make_keyboard_for_open_excel(user) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton('Follow Link', url=SheetManager(user).working_sheet.url),
        InlineKeyboardButton('Get Access', callback_data=GET_ACCESS_BUTTON),
    ]]

    return InlineKeyboardMarkup(buttons)