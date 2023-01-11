import os
import logging
from telegram import (
    Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Updater, CommandHandler, ConversationHandler, CallbackQueryHandler,
    MessageHandler, Filters, CallbackContext, Defaults,
)
from telegram.constants import PARSEMODE_MARKDOWN_V2
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

EVENT_BUTTONS = ['День рождения', 'Свадьба', 'Школа', 'Без повода'] # TODO выбор категорий из базы данных?
PRICE_BUTTONS = ['500', '1000', '2000', 'Больше', 'Не важно']

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
    reply_markup = ReplyKeyboardMarkup(event_keyboard, resize_keyboard=True, one_time_keyboard=True)

    update.message.reply_text(
        text=(
            'К какому событию готовимся?\n'
            'Выберите один из вариантов:\n'
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


def other_event(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text=(
            'Введите свое событие:'
        ),
    # reply_markup=ReplyKeyboardRemove()
    )


def show_relevant_flower(update: Update, context: CallbackContext) -> None:

    price = update.message.text
    context.user_data['price'] = price
    event = context.user_data.get('event')
    # TODO запрос к базе для выбора варианта

    keyboard = [[InlineKeyboardButton('Заказать', callback_data='zakaz')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        text=(
            f'Запрос: \n'
            f'Категория: {event}\n'
            f'Цена: {price.replace("~", "")}'
        ),
    reply_markup=reply_markup
    )

    option_keyboard = [['Заказать консультацию', 'Посмотреть всю коллекцию']]
    reply_markup = ReplyKeyboardMarkup(option_keyboard, resize_keyboard=True)
    update.message.reply_text(
        text=(
            'Хотите что\-то еще более уникальное?\n'
            'Подберите другой букет из нашей коллекции или закажите консультацию флориста'
        ),
    reply_markup=reply_markup
    )


def show_catalog_flower(update: Update, context: CallbackContext) -> None:

    # TODO запрос к базе для выбора варианта

    keyboard = [[InlineKeyboardButton('Заказать', callback_data='zakaz')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        text=(
            f'Другой букет из каталога'
        ),
    reply_markup=reply_markup
    )

    update.message.reply_text(
        text=(
            'Хотите что\-то еще более уникальное?\n'
            'Подберите другой букет из нашей коллекции или закажите консультацию флориста'
        ),
    )


def price_request(update: Update, context: CallbackContext) -> None:

    context.user_data['event'] = update.message.text

    price_keyboard = build_menu(PRICE_BUTTONS, 3)
    reply_markup = ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(
        text=(
            'На какую сумму рассчитываете?'
        ),
    reply_markup=reply_markup
    )

def start_zakaz(update: Update, context: CallbackContext):
    pass


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
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Другой повод)$'), other_event))
    dispatcher.add_handler(MessageHandler(Filters.text(PRICE_BUTTONS), show_relevant_flower))
    dispatcher.add_handler(MessageHandler(
        Filters.text &
        (~Filters.command) &
        (~Filters.text(EVENT_BUTTONS)) &
        (~Filters.text(PRICE_BUTTONS)) &
        (~Filters.regex('^(Посмотреть всю коллекцию)$')), price_request))
    dispatcher.add_handler(CommandHandler('cancel', cancel))
    dispatcher.add_handler(CallbackQueryHandler(start_zakaz, pattern='^zakaz'))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Посмотреть всю коллекцию)$'), show_catalog_flower))

    updater.start_polling()
    updater.idle()
