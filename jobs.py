import os

from telegram.error import BadRequest

from db import db, get_subscribed
from utils import create_pic_from_bynary, random_emoji


def send_random_pic(context):
    file_name = create_pic_from_bynary()
    emoji = random_emoji()
    text = f'Ежедневная рассылка мемасов! {emoji}'
    for user in get_subscribed(db):
        try:
            context.bot.send_message(chat_id=user["chat_id"], text=text)
            context.bot.send_photo(
                chat_id=user["chat_id"],
                photo=open(file_name, 'rb'))
        except BadRequest:
            print(f"Chat {user['chat_id']} not found")
    os.remove(file_name)
