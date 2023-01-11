import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater, CommandHandler, ConversationHandler,
    MessageHandler, Filters, CallbackContext, Defaults,
)
from telegram.constants import PARSEMODE_MARKDOWN_V2
from random import choice
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:

    # keyboard = [
    #     ['Новый вопрос', 'Сдаться'],
    #     ['Мой счет']
    # ]
    # reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text(
        text=(
            '*'
            'К какому событию готовимся?\n'
            'Выберите один из вариантов, либо укажите свой:\n'
            '*'
        ),
    )


if __name__ == '__main__':

    logger.setLevel(logging.INFO)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    logger.info('Запущен FlowerShopBot')

    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']

    defaults = Defaults(parse_mode=PARSEMODE_MARKDOWN_V2)
    updater = Updater(token=bot_token, defaults=defaults)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()
