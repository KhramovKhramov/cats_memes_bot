import os

from db import db, get_or_create_user, save_pic
from utils import create_pic_from_bynary


def greet_user(update, context):
    user = get_or_create_user(
        db, update.effective_user,
        update.message.chat.id)
    update.message.reply_text(f'Привет, котик {user["first_name"]}!')


def want_to_send_pic(update, context):
    update.message.reply_text(
        'Просто отправь мне мемас с котиком в любой момент')


def get_pic(update, context):
    update.message.reply_text('Спасибо, что прислал мемас, обрабатываю')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join(
        'downloads',
        f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    save_pic(db, file_name)
    os.remove(file_name)
    update.message.reply_text('Фото сохранено')


def send_pic(update, context):
    chat_id = update.effective_chat.id
    file_name = create_pic_from_bynary()
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(file_name, 'rb')
    )
    os.remove(file_name)
