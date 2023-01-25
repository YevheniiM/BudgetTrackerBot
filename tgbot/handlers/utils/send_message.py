def send_message(user, bot, **kwargs):
    message = bot.send_message(
        **kwargs
    )
    user.last_message = message.message_id
    user.save()
