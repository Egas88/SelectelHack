from bot import bot

def handle_login(message):
    bot.send_message(message.from_user.id, "Привет!")