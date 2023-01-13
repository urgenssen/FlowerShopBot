import os
import logging
from telegram import (
    Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton,
    InlineKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    Updater, CommandHandler, ConversationHandler, CallbackQueryHandler,
    MessageHandler, Filters, CallbackContext, Defaults,
)
from environs import Env

logger = logging.getLogger(__name__)

EVENT_BUTTONS = ['День рождения', 'Свадьба', 'Школа', 'Без повода'] # TODO выбор категорий из базы данных?

PRICE_BUTTONS = ['1000', '3000', '5000', 'Больше', 'Не важно']

OTHER_EVENT, PRICE = range(2)

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


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        text=(
            'До свидания, ждем следующего заказа.'
        ),
    reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def other_event(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        text=(
            'Введите свое событие:'
        ),
    )

    return OTHER_EVENT


def show_relevant_flower(update: Update, context: CallbackContext) -> int:

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
            'Хотите что-то еще более уникальное?\n'
            'Подберите другой букет из нашей коллекции или закажите консультацию флориста.'
        ),
    reply_markup=reply_markup
    )

    return ConversationHandler.END


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
            'Хотите что-то еще более уникальное?\n'
            'Подберите другой букет из нашей коллекции или закажите консультацию флориста.'
        ),
    )


def price_request(update: Update, context: CallbackContext) -> int:

    context.user_data['event'] = update.message.text

    price_keyboard = build_menu(PRICE_BUTTONS, 3)
    reply_markup = ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(
        text=(
            'На какую сумму рассчитываете?'
        ),
    reply_markup=reply_markup
    )
    return PRICE


def phonenumber_request(update: Update, context: CallbackContext) -> None:

    keyboard = [[KeyboardButton('Отправить номер телефона', request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(
        text=(
            'Укажите номер телефона в формате 7ХХХХХХХХХХ, и наш флорист перезвонит вам в течение 20 минут.'
        ),
    reply_markup=reply_markup
    )


def florist_answer(update: Update, context: CallbackContext) -> None:

    phone_number = update.message.text
    if not phone_number:
        phone_number = update.message.contact.phone_number
    phone_number = phone_number.replace('+', '')

    context.user_data['phone_number'] = phone_number

    event_keyboard = build_menu(EVENT_BUTTONS, 2, footer_buttons='Другой повод')
    reply_markup = ReplyKeyboardMarkup(event_keyboard, resize_keyboard=True, one_time_keyboard=True)

    update.message.reply_text(
        text=(
            'Флорист скоро свяжется с вами.'
            'А пока можете присмотреть что-нибудь из готовой коллекции.'
        ),
    reply_markup=reply_markup
    )

    # отправка уведомления флористу
    florist_id = context.bot_data['florist_id']
    user_data = context.user_data
    update.effective_user.bot.send_message(
        chat_id=florist_id,
        text=(
            'Заявка на обратный звонок для флориста!\n\n'
            f'Номер телефона: {phone_number}\n'
            f'Категория: {user_data["event"]}\n'
            f'Цена: {user_data["price"]}'
        ),
    )


def start_chekout_order(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id

    context.user_data['id'] = update.effective_user.id
    print(context.user_data)

    if context.user_data['id'] == 104252299:
        update.effective_user.bot.send_message (
            chat_id=chat_id,
            text=(
                'Введите адрес доставки:'
            ),
            reply_markup=ReplyKeyboardRemove()
        )
        return 1
    else:
        update.effective_user.bot.send_message(
            chat_id=chat_id,
            text=(
                'Введите ФИО:'
            ),
            reply_markup=ReplyKeyboardRemove()
        )
        return 2


def confirm_agreement(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id

    context.user_data['id'] = update.effective_user.id
    print(context.user_data)

    agree_keyboard = [['Согласен', 'Не согласен']]
    reply_markup = ReplyKeyboardMarkup(agree_keyboard, resize_keyboard=True)

    update.effective_user.bot.send_document(
        chat_id=chat_id,
        document=open('soglasie.pdf', 'rb'),
        caption='Для оформления заказа требуется подтвердить согласие на обработку персональных данных',
        reply_markup=reply_markup
)

if __name__ == '__main__':

    logger.setLevel(logging.INFO)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.info('Запущен FlowerShopBot')

    env = Env()
    env.read_env()
    bot_token = env.str("TG_TOKEN")
    florist_id = env('FLORIST_ID')
    service_id = env('SERVICE_ID')

    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data = {
        'florist_id': florist_id,
        'service_id': service_id
    }

    other_event_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Другой повод)$'), other_event)],
        states={
            OTHER_EVENT: [MessageHandler(Filters.text & (~Filters.command), price_request)
            ],

            PRICE: [
                MessageHandler(Filters.text(PRICE_BUTTONS), show_relevant_flower)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )


    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text(EVENT_BUTTONS), price_request))
    dispatcher.add_handler(other_event_handler)
    dispatcher.add_handler(MessageHandler(Filters.text(PRICE_BUTTONS), show_relevant_flower))
    dispatcher.add_handler(CommandHandler('cancel', cancel))
    dispatcher.add_handler(CallbackQueryHandler(confirm_agreement, pattern='^zakaz'))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Посмотреть всю коллекцию)$'), show_catalog_flower))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Заказать консультацию)$'), phonenumber_request))
    # regex номера телефона '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    # (Источник: https://habr.com/ru/post/110731/)
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$') | Filters.contact,
            florist_answer)
    )

    updater.start_polling()
    updater.idle()
