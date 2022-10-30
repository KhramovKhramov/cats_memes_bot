from emoji import emojize
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup

from db import db, get_or_create_user, save_anketa
from utils import main_keyboard, random_emoji


def anketa_start(update, context):
    reply_keyboard = [['1', '2', '3', '4', '5']]
    emoji = random_emoji()
    update.message.reply_text(
        f'Котик, оцени, пожалуйста, работу бота {emoji}',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
    )

    return 'rating'


def anketa_rating(update, context):
    context.user_data['anketa'] = {'rating': int(update.message.text)}
    update.message.reply_text(
        'Оставь комментарий о работе бота:'
    )

    return "comment"


def anketa_comment(update, context):
    context.user_data['anketa']['comment'] = update.message.text
    user = get_or_create_user(
        db, update.effective_user,
        update.message.chat.id)
    save_anketa(db, user['user_id'], context.user_data['anketa'])
    emoji = random_emoji()
    update.message.reply_text(
        f'Спасибо, котик! {emoji}',
        reply_markup=main_keyboard()
    )

    return ConversationHandler.END


def anketa_dontknow(update, context):
    emoji = emojize(':crying_cat_face:', language='alias')
    update.message.reply_text(
        f'Котик, не понимаю {emoji}'
    )
