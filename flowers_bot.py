import os
import logging
import django

from telegram import (
    Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton,
    InlineKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    Updater, CommandHandler, ConversationHandler, CallbackQueryHandler,
    MessageHandler, Filters, CallbackContext,
)

os.environ['DJANGO_SETTINGS_MODULE'] = 'flowershop.settings'
django.setup()

from environs import Env
from interface import (
    get_categories, get_bouquets_by_filter, add_category, get_user, add_user
)

logger = logging.getLogger(__name__)

# EVENT_BUTTONS = ['День рождения', 'Свадьба', 'Школа', 'Без повода'] # TODO выбор категорий из базы данных?
EVENT_BUTTONS = get_categories()

PRICE_BUTTONS = ['1000', '3000', '5000', '10000', 'Не важно']

# labels ConversationHandler
OTHER_EVENT, PRICE = range(2)
USER_NAME, USER_PHONE, USER_ADDRESS, USER_DELIVERY, ORDER_CONFIRM = range(2, 7)
PHONE_NUMBER = 7


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        if len(menu[-1]) == n_cols:
            menu.append([footer_buttons])
        else:
            menu[-1].append(footer_buttons)

    return menu


def start(update: Update, context: CallbackContext) -> None:

    EVENT_BUTTONS = get_categories()
    context.user_data['user'] = get_user(update.message.from_user.id)
    print(context.user_data['user'])

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


def price_request(update: Update, context: CallbackContext) -> int:

    event = update.message.text
    context.user_data['event'] = event

    if event not in get_categories():
        add_category(category=event)

    price_keyboard = build_menu(PRICE_BUTTONS, 3)
    reply_markup = ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(
        text=(
            'На какую сумму рассчитываете?'
        ),
    reply_markup=reply_markup
    )
    return PRICE


def show_relevant_flower(update: Update, context: CallbackContext) -> int:

    price = update.message.text
    context.user_data['price'] = price
    event = context.user_data.get('event')

    bouquets = get_bouquets_by_filter(event, price)
    print(bouquets)
    if bouquets:
        relevant = bouquets[0]
        print(relevant.price)
        keyboard = [[InlineKeyboardButton('Заказать', callback_data='zakaz')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        user_id = update.message.from_user.id
        update.effective_user.bot.send_photo(
            chat_id=user_id,
            photo= relevant.img_url,
            caption=(
                f'{relevant.name}\n\n'
                f'Описание: {relevant.text}\n'
                f'Состав: {relevant.content}\n\n'
                f'Цена: {relevant.price}'
            ),
        reply_markup=reply_markup
        )
    else:
        text='К сожалению в указанной категории нет букетов.'
        reply_markup = InlineKeyboardMarkup([])
        update.message.reply_text(
            text=text,
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

    option_keyboard = [['Заказать консультацию', 'Посмотреть всю коллекцию']]
    reply_markup = ReplyKeyboardMarkup(option_keyboard, resize_keyboard=True)

    update.message.reply_text(
        text=(
            'Хотите что-то еще более уникальное?\n'
            'Подберите другой букет из нашей коллекции или закажите консультацию флориста.'
        ),
    reply_markup=reply_markup
    )


def phonenumber_request(update: Update, context: CallbackContext) -> int:

    if not context.user_data['user']:
        keyboard = [[KeyboardButton('Отправить номер телефона', request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(
            text=(
                'Укажите номер телефона в формате 7ХХХХХХХХХХ, и наш флорист перезвонит вам в течение 20 минут.'
            ),
        reply_markup=reply_markup
        )
        return PHONE_NUMBER
    else:
        update.message.reply_text(
            text=(
                'Нашли Ваш номер в базе данных.'
            ),
        )
        return ConversationHandler.END


def userphone_request(update: Update, context: CallbackContext) -> int:

    keyboard = [[KeyboardButton('Отправить номер телефона', request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(
        text=(
            'Укажите номер телефона в формате 7ХХХХХХХХХХ, и наш флорист перезвонит вам в течение 20 минут.'
        ),
    reply_markup=reply_markup
    )
    return USER_ADDRESS


def florist_answer(update: Update, context: CallbackContext) -> int:

    if not context.user_data['user']:
        phone_number = update.message.text
        if not phone_number:
            phone_number = update.message.contact.phone_number
        phone_number = phone_number.replace('+', '')
        add_user(tg_user_id=update.message.from_user.id, name='', phone_number=phone_number[1:])
        context.user_data['user'] = get_user(update.message.from_user.id)
    else:
        phone_number = context.user_data['user']['phone_number']

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
    return ConversationHandler.END


def start_order_prepare(update: Update, context: CallbackContext):

    chat_id = update.message.chat_id
    context.user_data['id'] = chat_id

    if context.user_data['id'] == 10425229:
        # TODO данные из БД
        context.user_data['username'] = 'Иванов Иван Иванович'
        context.user_data['phone_number'] = '7123456789'

        update.effective_user.bot.send_message (
            chat_id=chat_id,
            text=(
                'Введите адрес доставки:'
            ),
            reply_markup=ReplyKeyboardRemove()
        )
        return USER_ADDRESS
    else:
        update.effective_user.bot.send_message(
            chat_id=chat_id,
            text=(
                'Введите ФИО:'
            ),
            reply_markup=ReplyKeyboardRemove()
        )
        return USER_NAME


def address_request(update: Update, context: CallbackContext) -> int:

    phone_number = update.message.text
    if not phone_number:
        phone_number = update.message.contact.phone_number
    phone_number = phone_number.replace('+', '')

    context.user_data['phone_number'] = phone_number

    update.message.reply_text(
        text=(
            'Введите адрес доставки:'
        ),
    )

    return USER_DELIVERY


def datetime_request(update: Update, context: CallbackContext) -> int:

    context.user_data['address'] = update.message.text

    update.message.reply_text(
        text=(
            'Введите дату и время доставки:\n'
            '(в формате ДД.ММ.ГГГГ)\n'
            'PS: можно и так: завтра утром, в субботу к 14 часам'
        ),
    )

    return ORDER_CONFIRM


def order_confirmation(update: Update, context: CallbackContext) -> int:

    delivery = update.message.text
    context.user_data['delivery'] = delivery

    option_keyboard = [['Да, все верно!', 'Я передумал']]
    reply_markup = ReplyKeyboardMarkup(option_keyboard, resize_keyboard=True)

    update.message.reply_text(
        text=(
            f'{context.user_data}'
        ),
    reply_markup=reply_markup
    )

    return ConversationHandler.END


def order_to_work(update: Update, context: CallbackContext) -> int:

    print(context.user_data)

    update.message.reply_text(
        text=(
            'Спасибо за Ваш заказ.\n'
            'Курьеры доставят его по указанному адресу в указанное Вами время.\n\n'
            'Будем ждать Ваши новые заказы!'
        ),
    reply_markup=ReplyKeyboardRemove()
    )

    # отправка уведомления курьерам
    service_id = context.bot_data['service_id']
    user_data = context.user_data

    update.effective_user.bot.send_message(
        chat_id=service_id,
        text=(
            'Заявка на доставку!\n\n'
            f'Адрес: {user_data["address"]}\n'
            f'Дата и время доставки: {user_data["delivery"]}\n'
            f'Контактный телефон: {user_data["phone_number"]}'
        ),
    )
    return ConversationHandler.END



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

    # # regex номера телефона '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    # # (Источник: https://habr.com/ru/post/110731/)

    order_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Согласен)$'), start_order_prepare)],
        states={
            USER_NAME: [
                MessageHandler(Filters.text & (~Filters.command), userphone_request)
            ],
            USER_PHONE: [
                MessageHandler(Filters.regex('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'), address_request),
                MessageHandler(Filters.contact, address_request)
            ],
            USER_ADDRESS: [
                MessageHandler(Filters.text & (~Filters.command), address_request)
            ],
            USER_DELIVERY: [
                MessageHandler(Filters.text & (~Filters.command), datetime_request)
                ],
            ORDER_CONFIRM: [
                MessageHandler(Filters.text & (~Filters.command), order_confirmation)
                            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    florist_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Заказать консультацию)$'), phonenumber_request)],
        states={
            PHONE_NUMBER: [
                MessageHandler(Filters.regex('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'), florist_answer),
                MessageHandler(Filters.contact, florist_answer)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text(EVENT_BUTTONS), price_request))
    dispatcher.add_handler(other_event_handler)
    dispatcher.add_handler(order_handler)
    dispatcher.add_handler(florist_handler)
    dispatcher.add_handler(MessageHandler(Filters.text(PRICE_BUTTONS), show_relevant_flower))
    dispatcher.add_handler(CommandHandler('cancel', cancel))
    dispatcher.add_handler(CallbackQueryHandler(confirm_agreement, pattern='^zakaz'))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Посмотреть всю коллекцию)$'), show_catalog_flower))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Да, все верно!)$'), order_to_work))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Я передумал)$'), start))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(Не согласен)$'), start))

    updater.start_polling()
    updater.idle()
