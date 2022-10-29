import os

from db import db, get_or_create_user, save_pic
from utils import (create_pic_from_bynary, has_oblect_on_images, main_keyboard,
                   random_emoji)


def greet_user(update, context):
    user = get_or_create_user(
        db, update.effective_user,
        update.message.chat.id)
    emoji = random_emoji()
    update.message.reply_text(
        f'Привет, котик {user["first_name"]}! {emoji}',
        reply_markup=main_keyboard())


def want_to_send_pic(update, context):
    emoji = random_emoji()
    update.message.reply_text(
        f'Просто отправь мне мемас с котиком в любой момент {emoji}',
        reply_markup=main_keyboard())


def get_pic(update, context):
    emoji = random_emoji()
    update.message.reply_text(f'Спасибо, что прислал мемас, обрабатываю {emoji}')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join(
        'downloads',
        f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    if has_oblect_on_images(file_name, object_name='cat'):
        save_pic(db, file_name)
        os.remove(file_name)
        update.message.reply_text(
            f'Мемас сохранен! {emoji}',
            reply_markup=main_keyboard())
    else:
        os.remove(file_name)
        update.message.reply_text(
            f'Тревога! Котик на мемасе не обнаружен! {emoji}',
            reply_markup=main_keyboard())


def send_pic(update, context):
    chat_id = update.effective_chat.id
    file_name = create_pic_from_bynary()
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(file_name, 'rb'),
        reply_markup=main_keyboard()
    )
    os.remove(file_name)
