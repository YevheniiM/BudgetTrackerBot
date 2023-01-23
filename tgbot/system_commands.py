from typing import Dict

from telegram import Bot, BotCommand

from tgbot.main import bot


def set_up_commands(bot_instance: Bot) -> None:

    langs_with_commands: Dict[str, Dict[str, str]] = {
        'en': {
            'start': 'Start django bot 🚀',
            'enter_expense': 'Enter Expense',
            'add_category': 'Add Category',
            'show_stats': 'Statistics of your budget 📊',
            'export_to_excel': 'Export to Excel',
            'open_excel': 'Open Excel Sheet',
            'github_repo': 'Github Repo',
        }
    }

    bot_instance.delete_my_commands()
    for language_code in langs_with_commands:
        bot_instance.set_my_commands(
            language_code=language_code,
            commands=[
                BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
            ]
        )


set_up_commands(bot)
