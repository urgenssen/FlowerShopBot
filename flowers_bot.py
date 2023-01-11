import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater, CommandHandler, ConversationHandler,
    MessageHandler, Filters, CallbackContext, Defaults,
)
from telegram.constants import PARSEMODE_MARKDOWN_V2
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

EVENT_BUTTONS = ['День рождения', 'Свадьба', 'Школа', 'Без повода'] # TODO выбор категорий из базы данных?
PRICE_BUTTONS = ['~ 500', '~ 1000', '~ 2000', 'Больше', 'Не важно']

def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])

    return menu


def start(update: Update, context: CallbackContext) -> None:

    event_keyboard = build_menu(EVENT_BUTTONS, 2, footer_buttons='Другой повод')
    reply_markup = ReplyKeyboardMarkup(event_keyboard, resize_keyboard=True)

    update.message.reply_text(
        text=(
            '*'
            'К какому событию готовимся?\n'
            'Выберите один из вариантов:\n'
            '*'
        ),
    reply_markup=reply_markup
    )


def cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text=(
            'До свидания, ждем следующего заказа'
        ),
    reply_markup=ReplyKeyboardRemove()
    )


def another_event(update: Update, context: CallbackContext) -> None:
    pass


def send_flower_version(update: Update, context: CallbackContext) -> None:

    price = update.message.text
    context.user_data['price'] = price
    event = context.user_data.get('event')

    update.message.reply_text(
        text=(
            f'Запрос: \n'
            f'Категория: {event}\n'
            f'Цена {price}'
        ),
    reply_markup=ReplyKeyboardRemove()
    )


def price_request(update: Update, context: CallbackContext) -> None:

    context.user_data['event'] = update.message.text

    price_keyboard = build_menu(PRICE_BUTTONS, 3)
    reply_markup = ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True)
    update.message.reply_text(
        text=(
            'На какую сумму рассчитываете?'
        ),
    reply_markup=reply_markup
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
    dispatcher.add_handler(MessageHandler(Filters.text(EVENT_BUTTONS), price_request))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Другой повод)$'), another_event))
    dispatcher.add_handler(MessageHandler(Filters.text(PRICE_BUTTONS), send_flower_version))
    dispatcher.add_handler(CommandHandler('cancel', cancel))

    updater.start_polling()
    updater.idle()
