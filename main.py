import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import settings
from handlers import send_pic, greet_user, get_pic, want_to_send_pic

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex(
        '^(Отправить мемас)$'),
        want_to_send_pic))
    dp.add_handler(MessageHandler(Filters.photo, get_pic))
    dp.add_handler(MessageHandler(Filters.regex(
        '^(Получить мемас)$'),
        send_pic))

    logging.info('bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
