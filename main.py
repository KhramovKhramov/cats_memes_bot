import logging

from telegram.ext import CommandHandler, Updater

import settings
from handlers import greet_user

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler('start', greet_user))

    logging.info('bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
