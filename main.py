import logging

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

import settings
from anketa import anketa_comment, anketa_dontknow, anketa_rating, anketa_start
from handlers import (get_pic, greet_user, send_pic, subscribe, unsubscribe,
                      want_to_send_pic)

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY)
    dp = mybot.dispatcher

    anketa = ConversationHandler(
        entry_points=[MessageHandler(
            Filters.regex('^(Пройти опрос)$'),
            anketa_start)],
        states={'rating': [MessageHandler(
            Filters.regex('^(1|2|3|4|5)$'),
            anketa_rating)],
            'comment': [MessageHandler(Filters.text, anketa_comment)]
        },
        fallbacks=[
            MessageHandler(
                Filters.text | Filters.video |
                Filters.photo | Filters.document |
                Filters.location | Filters.attachment, anketa_dontknow)
        ]
    )

    dp.add_handler(anketa)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex(
        '^(Отправить мемас)$'),
        want_to_send_pic))
    dp.add_handler(MessageHandler(Filters.photo, get_pic))
    dp.add_handler(MessageHandler(Filters.regex(
        '^(Получить мемас)$'),
        send_pic))
    dp.add_handler(MessageHandler(Filters.regex(
        '^(Подписаться)$'),
        subscribe))
    dp.add_handler(MessageHandler(Filters.regex(
        '^(Отписаться)$'),
        unsubscribe))

    logging.info('bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
