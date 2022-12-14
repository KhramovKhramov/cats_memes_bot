import logging
import pytz
from datetime import time
from jobs import send_random_pic
from telegram.bot import Bot
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

import settings
from anketa import anketa_comment, anketa_dontknow, anketa_rating, anketa_start
from handlers import (get_pic, greet_user, send_pic, subscribe, unsubscribe,
                      want_to_send_pic)

logging.basicConfig(filename='bot.log', level=logging.INFO)


class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, msg_queue=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = msg_queue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super().send_message(*args, **kwargs)


def main():
    request = Request(con_pool_size=8)
    bot = MQBot(settings.API_KEY, request=request)
    mybot = Updater(bot=bot)

    jq = mybot.job_queue
    target_time = time(12, 0, tzinfo=pytz.timezone('Europe/Moscow'))
    jq.run_daily(send_random_pic, target_time, days=(0, 1, 2, 3, 4, 5, 6))

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
