from db import db, get_or_create_user


def greet_user(update, context):
    user = get_or_create_user(
        db, update.effective_user,
        update.message.chat.id)
    update.message.reply_text(f'Привет, котик {user["first_name"]}!')
