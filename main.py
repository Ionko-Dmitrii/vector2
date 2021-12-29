# coding=utf-8
import datetime
import logging
import os
import re
import urllib

import cherrypy
import telebot

import buttons
import config
import dbworker
from decimal import *
from decimal import Decimal

import random
import string
import requests

from validate_email import validate_email
from send_email_code import send_email_code

# import statesworker

# from memory_profiler import profile
import currency_price_online
from create_upload.scheduler import scheduler
scheduler.start()     #ОТПРАВКА ВЫГРУЗКИ

WEBHOOK_HOST = config.host_ip
WEBHOOK_PORT = config.host_port
WEBHOOK_LISTEN = '0.0.0.0'  # #config.host_ip

WEBHOOK_SSL_CERT = config.ssl_cert  # Путь к сертификату
WEBHOOK_SSL_PRIV = config.ssl_priv  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % config.token

bot = telebot.TeleBot(config.token)
bot_admin = telebot.TeleBot(config.token_admin)
bot_support = telebot.TeleBot(config.token_support)

log_file = 'main.log'
f = open(log_file, 'w')
f.close()
file_log = logging.FileHandler(log_file)
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out),
                    format=u'%(filename)s [LINE:%(lineno)s; FUNC:%(funcName)s] #%(levelname)2s  [%(asctime)s]  %('
                           u'message)s',
                    level=logging.INFO)


def logging_message(message):
    f = open(f'logs/{message.from_user.id}.txt', 'a')
    time = datetime.datetime.now()
    log_time = time.strftime("%d-%b-%y %H:%M:%S")
    f.write(f'[{log_time}]      Message: {message.text}\n')
    f.close()

    dt = datetime.datetime.now()
    t_id = message.chat.id

    dbworker.create_chat(dt, t_id, 'Сообщение', message.text)



def logging_call(call):
    f = open(f'logs/{call.from_user.id}.txt', 'a')
    time = datetime.datetime.now()
    log_time = time.strftime("%d-%b-%y %H:%M:%S")
    f.write(f'[{log_time}]      Call: {call.data}\n')
    f.close()

    dt = datetime.datetime.now()
    t_id = call.message.chat.id


    for x in call.message.json['reply_markup']['inline_keyboard']:
        data = x[0]['callback_data']
        if data == call.data:
            text = x[0]['text']

    dbworker.create_chat(dt, t_id, 'Inline кнопка', text)



current_shown_dates = {}
withdraw_banks = {}


def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None


def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@bot.message_handler(func=lambda m: (m.chat.id,) in dbworker.get_blocked_user())
def handle_delete(message):
    bot.send_message(message.chat.id, 'Вы заблокированы в боте')

@bot.message_handler(commands=['delete'])
def handle_delete(message):
    logging_message(message)

    try:
        dbworker.delete_user(message.chat.id)
        bot.send_message(message.chat.id, "Вы удалены из системы",
                         reply_markup=buttons.get_remove_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(commands=['check'])
def handle_delete(message):
    logging_message(message)
    try:
        dbworker.set_state(message.chat.id, config.State.ZERO.value)
        bot.send_message(message.chat.id, f"ID: {str(message.chat.id)}, state: {dbworker.get_state(message.chat.id)}")
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(commands=['currency'])
def handle_delete(message):
    logging_message(message)
    try:
        dbworker.set_state(message.chat.id, config.State.ZERO.value)
        bot.send_message(message.chat.id, f"BTC: "
                                          f"{currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close']}"
                                          f" USD\n"
                                          f"USD: {currency_price_online.get_latest_currency_price('USD').value} руб")
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(commands=['add1000rub'])
def handle_delete(message):
    logging_message(message)
    try:
        dbworker.add_1000_rub(message.chat.id)
        bot.send_message(message.chat.id, f"1000 rub добавлены")
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(commands=['add1000btc'])
def handle_delete(message):
    logging_message(message)
    try:
        dbworker.add_1000_btc(message.chat.id)
        bot.send_message(message.chat.id, f"1000 btc добавлены")
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(commands=['remove1000rub'])
def handle_delete(message):
    logging_message(message)
    try:
        dbworker.remove_1000_rub(message.chat.id)
        bot.send_message(message.chat.id, f"1000 rub добавлены")
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(commands=['remove1000btc'])
def handle_delete(message):
    logging_message(message)
    try:
        dbworker.remove_1000_btc(message.chat.id)
        bot.send_message(message.chat.id, f"1000 btc добавлены")
    except telebot.apihelper.ApiException as e:
        logging.exception(e)



# @profile
@bot.message_handler(commands=['start'])
def handle_start(message):

    print("telegram>>>>>>", message)
    #logging_message(message)
    try:
        dbworker.set_state(message.chat.id, config.State.START.value)
        username = 'None'
        if str(message.from_user.username) != "None":
            username = str(message.from_user.username)
        try:
            invited_by = int(message.text[6:])
        except:
            invited_by = 'Null'

        register_flag = dbworker.add_user(message.chat.id, username, invited_by)
        # if register_flag:
        #     bot.send_message(message.chat.id, "Введите ваше ФИО. Пример: Иванов Иван Иванович")
        #     dbworker.set_state(message.chat.id, config.State.SET_FIO.value)
        # else:
        #     dbworker.set_state(message.chat.id, config.State.MAIN_MENU.value)
        #     bot.send_message(message.chat.id, "Добро пожаловать.\nИнфо о нас\nВоспользуйтесь кнопками ниже:",
        #                      reply_markup=buttons.get_main_menu_keyboard())
        dbworker.set_state(message.chat.id, config.State.MAIN_MENU.value)
        bot.send_message(message.chat.id, "Добро пожаловать.\n"
                                          "Инфо о нас\n"
                                          "Воспользуйтесь кнопками ниже:",
                                           reply_markup=buttons.get_main_menu_keyboard())

    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    except Exception as e:
        logging.exception(e)


@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id)
                                          == config.State.SET_FIO.value)
def callback(message):
    logging_message(message)
    try:
        dbworker.set_fio(message.chat.id, message.text)
        bot.send_message(message.chat.id, "Введите вашу почту")
        dbworker.set_state(message.chat.id, config.State.SET_EMAIL.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id)
                                          == config.State.SET_EMAIL.value)
def callback(message):
    logging_message(message)
    try:
        dbworker.set_email(message.chat.id, message.text)  # todo add checking email

        bot.send_message(message.chat.id, "Для регистрации введите код, "
                                          "который пришел к вам на почту")
        bot.send_message(message.chat.id, "Код введён успешно")  # todo add checking code
        bot.send_message(message.chat.id, "Введите телефон (10 цифр)")
        dbworker.set_state(message.chat.id, config.State.SET_PHONE_NUMBER.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id)
                                          == config.State.SET_PHONE_NUMBER.value)
def callback(message):
    logging_message(message)
    try:
        if len(message.text) > 10:
            bot.send_message(message.chat.id, "Введите телефон (10 цифр)")
        else:
            dbworker.set_phone_number(message.chat.id, message.text)
        bot.send_message(message.chat.id, "Вы хотите сразу добавить шаблон кошелька BTC?",
                         reply_markup=buttons.get_first_add_btc_wallet())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'first_add_btc_wallet_yes' == call.data)
def callback(call):
    logging_call(call)
    try:
        bot.edit_message_text("Недоступно", call.from_user.id,
                              call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'first_add_btc_wallet_no' == call.data)
def callback(call):
    logging_call(call)
    try:
        bot.edit_message_text("Вы хотите сразу добавить шаблон "
                              "банковской карты/системы оплаты?", call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_first_add_rub_wallet())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'first_add_rub_wallet_yes' == call.data)
def callback(call):
    logging_call(call)
    try:
        bot.edit_message_text("Недоступно", call.from_user.id,
                              call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'first_add_rub_wallet_no' == call.data)
def callback(call):
    logging_call(call)
    try:
        dbworker.set_state(call.message.chat.id, config.State.MAIN_MENU.value)
        bot.send_message(call.message.chat.id,
                         "Регистрация завершена\n\nДобро пожаловать.\nИнфо о нас\nВоспользуйтесь кнопками ниже:",
                         reply_markup=buttons.get_main_menu_keyboard())
        dbworker.set_state(call.message.chat.id, config.State.MAIN_MENU.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(func=lambda message: "Личный кабинет" == message.text)
def handle(message):
    logging_message(message)
    try:
        # dbworker.cleanup_ads()
        dbworker.set_state(message.chat.id, config.State.LK.value)
        bot.send_message(message.chat.id, "Личный кабинет.",
                         reply_markup=buttons.get_lk_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'back_to_lk' == call.data)
def callback(call):
    logging_call(call)
    try:
        # dbworker.cleanup_ads()
        dbworker.set_state(call.message.chat.id, config.State.LK.value)
        bot.edit_message_text("Личный кабинет.", call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_lk_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'settings' == call.data)
def callback(call):
    logging_call(call)
    try:
        dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text("Настройки", call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_settings_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'ref_program' == call.data)
def callback(call):
    logging_call(call)
    referals = dbworker.get_count_referals(call.from_user.id)[0]
    bonuses = dbworker.get_bonuses(call.message.chat.id)
    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text(f"Вы можете заработать дополнительно пригласив сюда новых участников по свой реферальной "
                              f"ссылке.\n\n"
                              f"Количество приглашенных пользователей: {referals}\n"
                              f"Количество баллов: {bonuses}",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_ref_program_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'get_ref_link' == call.data)
def callback(call):
    logging_call(call)
    message_id = call.message.message_id
    chat_id = call.from_user.id
    bot_username = bot.get_me().username
    bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                          text=f't.me/{bot_username}?start={chat_id}')


@bot.callback_query_handler(func=lambda call: 'commission' == call.data)
def callback(call):
    logging_call(call)
    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text("Готовится бонусная программа", call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_commission_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'help' == call.data)
def callback(call):
    logging_call(call)
    support_username = bot_support.get_me().username
    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text(f"Список вопросов-ответов\n"
                              f"Если у вас остались вопросы напишите @{support_username},"
                              f" на ваши вопросы ответит оператор",
                              call.from_user.id,
                              call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'chat_with_operator' == call.data)
def callback(call):
    logging_call(call)
    try:
        #dbworker.set_state(call.message.chat.id, config.State.CHAT_WITH_SUPPORT.value)
        bot.edit_message_text(f"Напишите @{bot_support.get_me().username}", call.from_user.id,
                              call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


'''
@bot.message_handler(func= lambda message: dbworker.get_state(message.chat.id) == config.State.CHAT_WITH_SUPPORT.value)
def handle(message):
    logging_message(message)
    admins = dbworker.get_admins()
    username = message.from_user.username
    try:
        dbworker.create_support(t_id=message.chat.id, message_id=message.message_id, text=message.text)
        id = dbworker.get_support_id(message.chat.id, message.message_id)

        for admin in admins:
            try:
                admin_t_id = admin[0]
                bot_admin.send_message(admin_t_id, f'Вопрос в саппорт №{id} от @{username}:\n'
                                                   f'"{message.text}"',
                                       reply_markup=buttons.get_answer_support_question_keyboard(id))
            except telebot.apihelper.ApiException as e:
                logging.exception(e)

        bot.send_message(message.chat.id, text=f'Ваш вопрос отправлен админу:\n'
                                               f'Запрос №{id}\n'
                                               f'"{message.text}"')
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    dbworker.set_state(message.chat.id, config.State.ZERO.value)


@bot.edited_message_handler(func=lambda m: (m.message_id,) in dbworker.get_support_message_id(m.chat.id))
def edit_message(message):
    logging_message(message)
    admins = dbworker.get_admins()
    username = message.from_user.username
    id = dbworker.get_support_id(message.chat.id, message.message_id)

    try:
        dbworker.update_support_text(message.chat.id, message.message_id, message.text)
        for admin in admins:
            try:
                admin_t_id = admin[0]
                bot_admin.send_message(admin_t_id, f'Вопрос в саппорт №{id} от @{username}',
                                       reply_markup=buttons.get_answer_support_question_keyboard(id))
            except telebot.apihelper.ApiException as e:
                logging.exception(e)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
'''

@bot.callback_query_handler(func=lambda call: 'verification' == call.data)
def callback(call):
    logging_call(call)
    try:

        bot.edit_message_text("Отправьте ваше ФИО", call.from_user.id,
                              call.message.message_id)
        dbworker.set_state(call.message.chat.id, config.State.VERIFICATION_STEP1_FIO.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)

@bot.message_handler(func= lambda m:dbworker.get_state(m.chat.id) == config.State.VERIFICATION_STEP1_FIO.value)
def handle(message):
    try:
        fio = message.text
        dbworker.set_fio(message.chat.id, fio)
        bot.send_message(message.chat.id, 'Отправьте вашу дату рождения в формате дд.мм.гггг')
        dbworker.set_state(message.chat.id, config.State.VERIFICATION_STEP1_DATE_OF_BIRTH.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(func= lambda m:dbworker.get_state(m.chat.id) == config.State.VERIFICATION_STEP1_DATE_OF_BIRTH.value)
def handle(message):
    try:
        date = message.text.split('.')
        try:
            day = int(date[0])
            month = int(date[1])
            year = int(date[2])

            if len(date[0]) > 2 or len(date[0]) < 1 or len(date[1]) > 2 or len(date[1]) < 1 or len(date[2]) != 4:
                bot.send_message(message.chat.id, 'Вы неправильно ввели дату рождения')
                return
        except:
            bot.send_message(message.chat.id, 'Вы неправильно ввели дату рождения')
            return
        date_of_birth = datetime.date(year, month, day)
        dbworker.set_birth_date(message.chat.id, date_of_birth)
        bot.send_message(message.chat.id, 'Отправьте ваш адрес')
        dbworker.set_state(message.chat.id, config.State.VERIFICATION_STEP1_ADDRESS.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(func= lambda m:dbworker.get_state(m.chat.id) == config.State.VERIFICATION_STEP1_ADDRESS.value)
def handle(message):
    try:
        address = message.text
        dbworker.set_address(message.chat.id, address)
        bot.send_message(message.chat.id,
                         'Загрузите фото удостоверения личности (водительские права, паспорт, удост. личности)')
        dbworker.set_state(message.chat.id, config.State.VERIFICATION_STEP2.value)

    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(content_types='photo',
                     func=lambda m:dbworker.get_state(m.chat.id) == config.State.VERIFICATION_STEP2.value)
def handle(message):
    try:
        photo = message.photo[-1].file_id
        path = bot.get_file(photo).file_path
        link = f'https://api.telegram.org/file/bot{config.token}/{path}'
        if not os.path.isdir(f"verification/{message.chat.id}"):
            os.mkdir(f"verification/{message.chat.id}")
        f = open(rf'verification/{message.chat.id}/photo1.jpg', "wb")
        req = requests.get(link)
        f.write(req.content)
        f.close()
        dbworker.set_state(message.chat.id, config.State.VERIFICATION_STEP3.value)
        bot.send_message(message.chat.id,
                         'Сфотографируйте себя, чтобы подтвердить личность '
                         '(Фото в хорошем формате до 5 мб, отправленное напрямую с устройства, с которого делалось'
                         ' фото, фото с удоств. личности в руках, где хорошо видно лицо и документ)')
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(content_types='photo',
                     func=lambda m:dbworker.get_state(m.chat.id) == config.State.VERIFICATION_STEP3.value)
def handle(message):
    admins = dbworker.get_admins_type('verification')
    t_id = message.chat.id

    try:
        fio = dbworker.get_fio(t_id)
        date_of_birth = dbworker.get_birth_date(t_id)
        address = dbworker.get_address(t_id)



        photo = message.photo[-1].file_id
        path = bot.get_file(photo).file_path
        link = f'https://api.telegram.org/file/bot{config.token}/{path}'
        if not os.path.isdir(f"verification/{message.chat.id}"):
            os.mkdir(f"verification/{message.chat.id}")
        f = open(rf'verification/{message.chat.id}/photo2.jpg', "wb")
        req = requests.get(link)
        f.write(req.content)
        f.close()

        text = f'Заявка на верификацию:\n' \
                  f'id: {t_id}\n' \
                  f'ФИО: {fio}\n' \
                  f'Дата рождения(в формате гггг-мм-дд): {date_of_birth}\n' \
                  f'Адрес: {address}'
        for admin in admins:
            admin_t_id = admin[0]

            photo1 = open(f'verification/{message.chat.id}/photo1.jpg', "rb")
            photo2 = open(f'verification/{message.chat.id}/photo2.jpg', "rb")
            bot_admin.send_media_group(admin_t_id,
                                       [telebot.types.InputMediaPhoto(photo1, caption='Идентификация и проверка лица'),
                                        telebot.types.InputMediaPhoto(photo2, caption='Фото с документом')])
            bot_admin.send_message(admin_t_id, text, reply_markup=buttons.get_verification_keyboard(t_id))
            photo1.close()
            photo2.close()
            dbworker.set_status(t_id, 0)
            bot.send_message(message.chat.id, 'Данные отправлены администратору на проверку')
            dbworker.set_state(t_id, config.State.ZERO.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'promo' == call.data)
def callback(call):
    logging_call(call)
    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text("Текст", call.from_user.id,
                              call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'back_to_start' == call.data)
def callback(call):
    logging_call(call)
    try:
        dbworker.set_state(call.message.chat.id, config.State.MAIN_MENU.value)
        bot.edit_message_text("Добро пожаловать.\nИнфо о нас\nВоспользуйтесь кнопками ниже:", call.from_user.id,
                              call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'language' == call.data)
def callback(call):
    logging_call(call)
    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text("Скоро будет внедрено", call.from_user.id,
                              call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: '2fa' == call.data)
def callback(call):
    logging_call(call)
    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text("Скоро будет внедрено", call.from_user.id,
                              call.message.message_id, )
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'email' == call.data)
def callback(call):
    logging_call(call)
    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        e_mail = dbworker.get_email(call.message.chat.id)
        if e_mail != '':
            bot.edit_message_text(f"Ваш e-mail: {e_mail}\nДля изменения e-mail нужно ввести код подтверждения, "
                                  f"который придет на указанную вами почту", call.from_user.id,
                                  call.message.message_id,
                                  reply_markup=buttons.get_email_keyboard())
        else:
            bot.edit_message_text(f"Вы не указали e-mail\nДля изменения e-mail нужно сделать запрос, после этого "
                                  "администратор вам одобрит изменение почты.", call.from_user.id,
                                  call.message.message_id,
                                  reply_markup=buttons.get_email_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'change_email' == call.data)
def callback(call):
    logging_call(call)
    try:
        dbworker.set_state(call.message.chat.id, config.State.ENTER_EMAIL.value)
        bot.edit_message_text("Введите новый email:", call.from_user.id,
                              call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id)
                                          == config.State.ENTER_EMAIL.value)
def callback(message):
    try:

        email = message.text
        is_validate = validate_email(email)
        if is_validate == True:
            dbworker.set_state(message.chat.id, config.State.WAIT_EMAIL_VERIFICATION_CODE.value)
            active_email_codes = dbworker.get_active_email_code(message.chat.id)
            for email_code in active_email_codes:
                dbworker.set_email_code_status(email_code, 'Отклонен')
            code = random.randint(111111, 999999)
            dbworker.add_email_code(message.chat.id, code, email)
            send_email_code(email, code)
            bot.send_message(message.chat.id, 'Код отправлен. Отправьте код подтверждения')
        else:
            bot.send_message(message.chat.id, 'email введен неправильно. Пожалуйста, введите еще раз')

    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id)
                                          == config.State.WAIT_EMAIL_VERIFICATION_CODE.value)
def callback(message):
    logging_message(message)
    try:
        code = message.text
        codes = dbworker.get_email_code(code)
        for c in codes:
            if c.t_id == message.chat.id and c.status == 'Создан':
                email = c.email
                dbworker.set_email(message.chat.id, email)
                dbworker.add_email_history(message.chat.id, email)
                dbworker.set_email_code_status(c.id, 'Подтверждено')
                dbworker.set_email_end_dt(c.id)
                bot.send_message(message.chat.id, f'Ваша почта изменена: {email}')
                dbworker.set_state(message.chat.id, config.State.ZERO.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'relative_rate' == call.data)
def callback(call):
    logging_call(call)
    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text("Относительный курс", call.from_user.id,
                              call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'withdrawal_requisites' == call.data)
def callback(call):
    logging_call(call)
    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text("Реквизиты для вывода", call.from_user.id, call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'autoconv' == call.data)
def callback(call):
    logging_call(call)
    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text("Автоконвертация", call.from_user.id, call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(func=lambda message: "Управление активами" == message.text)
def handle(message):
    logging_message(message)
    try:
        user_rub_value = dbworker.get_rub_balance(message.chat.id)
        user_btc_value = dbworker.get_btc_balance(message.chat.id)
        # dbworker.cleanup_ads()
        # dbworker.set_state(message.chat.id, config.State.CALCULATOR.value)
        bot.send_message(message.chat.id, f"Управление активами.\nВаш баланс:\n{user_btc_value[0]:.8f} Bitcoin\n"
                                          f"{user_rub_value[0]} Рублей",
                         reply_markup=buttons.get_assets_managment_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'back_to_assets_managment' == call.data)
def callback(call):
    logging_call(call)
    try:
        user_rub_value = dbworker.get_rub_balance(call.message.chat.id)
        user_btc_value = dbworker.get_btc_balance(call.message.chat.id)
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text(f"Управление активами\nВаш баланс:\n{user_btc_value[0]:.8f} Bitcoin\n"
                              f"{user_rub_value[0]}Рублей", call.from_user.id, call.message.message_id,
                              reply_markup=buttons.get_assets_managment_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'replenish' == call.data)
def callback(call):
    logging_call(call)
    try:
        user_rub_value = dbworker.get_rub_balance(call.message.chat.id)
        user_btc_value = dbworker.get_btc_balance(call.message.chat.id)
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text(f"Пополнить баланс:\n{user_btc_value[0]:.8f} Bitcoin\n{user_rub_value[0]} "
                              f"Рублей\nВыберите валюту для "
                              "пополнения:", call.from_user.id,
                              call.message.message_id, reply_markup=buttons.get_replenish_currency_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'replenish_сode' == call.data)
def callback(call):
    logging_call(call)
    try:
        dbworker.set_state(call.message.chat.id, config.State.WAIT_REPLENISH_CODE.value)
        bot.edit_message_text("Ввести код для пополнения баланса", call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_back_to_replenish_currency_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id) == config.State.WAIT_REPLENISH_CODE.value)
def handle(message):
    logging_message(message)
    try:
        code_status = dbworker.check_code(message.text)
        if code_status == 'active':
            dbworker.set_state(message.chat.id, config.State.ZERO.value)
            code_id = dbworker.get_code_id(message.text)
            dbworker.set_balance_was_activator_code(code_id, message.chat.id)
            dbworker.set_code_status(code_id, '2')
            dbworker.set_code_end_dt(code_id)

            dbworker.set_code_used_by_user(code_id, message.chat.id)
            code_currency = dbworker.get_code_currency(code_id)
            if code_currency == 'rub':
                balance_was = dbworker.get_rub_balance(message.chat.id)
                replenish_value = dbworker.get_code_amount_rub(code_id)
                dbworker.user_rub_plus(message.chat.id, replenish_value)
                user_balance = dbworker.get_rub_balance(message.chat.id)
            else:
                balance_was = dbworker.get_btc_balance(message.chat.id)
                replenish_value = dbworker.get_code_amount_btc(code_id)
                dbworker.user_btc_plus(message.chat.id, replenish_value)
                user_balance = dbworker.get_btc_balance(message.chat.id)
            dbworker.set_balance_activator_code(code_id, message.chat.id)
            dt = dbworker.get_code_create_dt(code_id)

            dbworker.add_transaction_code(message.chat.id, dt, f'{replenish_value} {code_currency}',
                                          f'{balance_was[0]} {code_currency}', f'{user_balance[0]} {code_currency}',
                                          'Код активирован')
            bot.send_message(message.chat.id, f"Ваш баланс пополнен на: \n{replenish_value} {code_currency}\n"
                                              f"Ваш баланс: {user_balance[0]} {code_currency}")
        elif code_status == 'expired':
            bot.send_message(message.chat.id, 'Код устарел')
        else:
            bot.send_message(message.chat.id, 'Такого кода не существует. Проверьте корректность кода и повторите ввод')
            #dbworker.create_code(message.chat.id, '', 0)
            #code_id = dbworker.get_user_last_code(message.chat.id)
            #dbworker.set_code_status(code_id, 3)


    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'replenish_btc' == call.data)
def callback(call):
    logging_call(call)
    try:
        dbworker.set_state(call.message.chat.id, config.State.REPLENISH_BTC_VALUE.value)
        user_btc_value = dbworker.get_btc_balance(call.message.chat.id)
        bot.edit_message_text(f"Пополнить биткоин\n{user_btc_value[0]:.8f} Bitcoin\nВведите сумму "
                              f"пополнения:", call.from_user.id, call.message.message_id,
                              reply_markup=buttons.get_back_to_assets_managment_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id) == config.State.REPLENISH_BTC_VALUE.value)
def handle(message):
    logging_message(message)
    try:
        # dbworker.cleanup_ads()
        btc_amount = float(message.text.replace(',', '.')) * (1-float(dbworker.get_commission_replenish()/100))
    except:
        bot.send_message(message.chat.id, f"Сумма введена неправильно")
        return

    if btc_amount<=0:
        bot.send_message(message.chat.id, f"Сумма введена неправильно")
        return
    try:
        commission = float(message.text.replace(',', '.')) * float(dbworker.get_commission_replenish()/100)
        wallet = dbworker.get_btc_wallet()[0][0]
        dbworker.create_replenish(message.chat.id, 'btc', btc_amount, commission, wallet)
        replenish_id = dbworker.get_user_last_replenish(message.chat.id)

        btc_balance = dbworker.get_btc_balance(message.chat.id)[0]
        rub_balance = dbworker.get_rub_balance(message.chat.id)[0]
        dbworker.set_replenish_btc_balance_was(replenish_id, btc_balance)
        dbworker.set_replenish_rub_balance_was(replenish_id, rub_balance)
        dbworker.set_state(message.chat.id, config. State.ZERO.value)


        bot.send_message(message.chat.id, f"Переводите средства на кошелек: {wallet}",
                         reply_markup=buttons.get_payment_replenish_btc_done_keyboard(replenish_id))

    except telebot.apihelper.ApiException as e:
        logging.exception(e)

'''
@bot.callback_query_handler(func=lambda call: 'replenish_btc_wallet_1' == call.data)
def callback(call):
    logging_call(call)
    try:
        replenish_id = dbworker.get_user_last_replenish(call.message.chat.id)
        btc_value = dbworker.get_replenish_amaunt_btc(replenish_id)[0]
        bot.edit_message_text(f'Вы получите {btc_value} на кошелек <название кошелька 1>\n'
                              f'Переведите средства:\n'
                              f'Инструкция перевода\n'
                              f'Нажмите кнопку "перевод совершен", '
                              f'после перевода', call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_payment_replenish_btc_done_keyboard(replenish_id))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'replenish_btc_wallet_2' == call.data)
def callback(call):
    logging_call(call)
    try:
        replenish_id = dbworker.get_user_last_replenish(call.message.chat.id)
        btc_value = dbworker.get_replenish_amaunt_btc(replenish_id)[0]
        bot.edit_message_text(f'Вы получите {btc_value} на кошелек <название кошелька 2>\nПереведите '
                              f'средства:\nИнструкция перевода\nНажмите кнопку "перевод совершен", '
                              f'после перевода', call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_payment_replenish_btc_done_keyboard(replenish_id))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
'''

@bot.callback_query_handler(func=lambda call: 'replenish_btc_success_' in call.data[:22])
def callback(call):
    logging_call(call)
    try:
        dbworker.set_state(call.message.chat.id, config.State.REPLENISH_BTC_WALLET.value)
        bot.edit_message_text(f'Введите номер кошелька с которого совершен перевеод',
                              call.from_user.id,
                              call.message.message_id,)

    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(
    func=lambda message: dbworker.get_state(message.chat.id) == config.State.REPLENISH_BTC_WALLET.value)
def handle(message):
    logging_message(message)
    try:
        replenish_id = dbworker.get_user_last_replenish(message.chat.id)
        dbworker.set_state(message.chat.id, config.State.ZERO.value)
        admins = dbworker.get_admins_type('replenish')
        replenish_amount = dbworker.get_replenish_amaunt_btc(replenish_id)
        commission = dbworker.get_replenish_commission(replenish_id)
        replenish_user = dbworker.get_replenish_user(replenish_id)
        fio = dbworker.get_fio(replenish_user)
        email = dbworker.get_email(replenish_user)
        dbworker.set_replenish_status(replenish_id, '1')
        dbworker.set_replenish_wallet_from(replenish_id, f'{message.text}')

        for admin in admins:
            try:
                admin_t_id = admin[0]
                bot_admin.send_message(admin_t_id, f'⬇ Заявка №{replenish_id}\n'
                                                   f'Пополнение {replenish_amount[0]} btc'
                                                   f'(+комиссия: {commission} btc)\n'
                                                   f'ID: {replenish_user} '
                                                   f'username: @{bot.get_chat(replenish_user).username}\n'
                                                   f'Данные пользователя: \nФамилия: {fio}\nEmail: {email}\n'
                                                   f'🕓Пользователь отправил средства.',
                                       reply_markup=buttons.get_replenish_admin_approve_keyboard(replenish_id))
            except telebot.apihelper.ApiException as e:
                logging.exception(e)
                continue
        bot.send_message(text = 'Информация отправлена администратору, ожидайте пополнения.', chat_id = message.from_user.id,
                         reply_markup = buttons.get_back_to_replenish_currency_keyboard())

    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'replenish_btc_success_' in call.data)
def callback(call):
    logging_call(call)
    try:
        replenish_id = call.data[22:]
        admins = dbworker.get_admins_type('replenish')
        replenish_amount = dbworker.get_replenish_amaunt_btc(replenish_id)
        fio = dbworker.get_fio(call.message.chat.id)
        dbworker.set_replenish_status(replenish_id, '1')
        for admin in admins:
            try:
                admin_t_id = admin[0]
                bot_admin.send_message(admin_t_id, f'Запрос {replenish_id} на ввод '
                                                   f'{str(replenish_amount[0])} BTC от {fio}',
                                       reply_markup=buttons.get_replenish_admin_approve_keyboard(replenish_id))
            except telebot.apihelper.ApiException as e:
                logging.exception(e)
                continue
        bot.edit_message_text('Информация отправлена администратору, ожидайте пополнения.', call.from_user.id,
                              call.message.message_id, reply_markup=buttons.get_back_to_replenish_currency_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'replenish_rub' == call.data)
def callback(call):
    logging_call(call)
    try:
        bot.edit_message_text('Как пополнить', call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_replenish_rub_banks_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'replenish_rub_cash' in call.data)
def callback(call):
    logging_call(call)
    try:
        dbworker.create_replenish(call.message.chat.id, 'rub', 0, 0, '')
        bot.edit_message_text('Страна?', call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_replenish_cash_country_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'replenish_cash_country_russia' in call.data)
def callback(call):
    logging_call(call)
    try:
        replenish_id = dbworker.get_user_last_replenish(call.message.chat.id)
        dbworker.add_replenish_country(replenish_id, 'russia')
        bot.edit_message_text('В каком городе? Если город другой введите в поле', call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_replenish_cash_city_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(func=lambda message: dbworker.get_state(message.chat.id) == config.State.WAIT_COUNTRY.value)
def handle(message):
    logging_message(message)
    try:
        # dbworker.cleanup_ads()
        dbworker.set_state(message.chat.id, config.State.ZERO.value)
        bot.edit_message_text(message.chat.id, "Выберите кошелек пополнения:",
                              reply_markup=buttons.get_replenish_rub_wallets_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'withdraw' == call.data)
def callback(call):
    logging_call(call)
    try:
        user_rub_value = dbworker.get_rub_balance(call.message.chat.id)
        user_btc_value = dbworker.get_btc_balance(call.message.chat.id)
        bot.edit_message_text(f'Вывести средства:\n'
                              f'{user_btc_value[0]:.8f} Bitcoin\n'
                              f'{user_rub_value[0]} Рублей\n'
                              f'Выберите валюту для вывода:', call.from_user.id,
                              call.message.message_id, reply_markup=buttons.get_withdraw_currency_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'withdraw_btc' == call.data)
def callback(call):
    logging_call(call)
    try:
        user_btc_value = dbworker.get_btc_balance(call.message.chat.id)
        dbworker.set_state(call.message.chat.id, config.State.WAITING_WITHDRAW_BTC_SUM.value)
        bot.edit_message_text(f'Вывести биткоин\n'
                              f'{user_btc_value[0]:.8f} Bitcoin\n'
                              f'Какую сумму вывести:',
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_withdraw_btc_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(
    func=lambda message: dbworker.get_state(message.chat.id) == config.State.WAITING_WITHDRAW_BTC_SUM.value)
def handle(message):
    logging_message(message)
    try:
        float(message.text.replace(',', '.').replace(' ', ''))
    except:
        return

    commission = dbworker.get_commission_withdraw_btc()
    if Decimal(message.text.replace(',', '.').replace(' ', '')) > dbworker.get_btc_balance(message.chat.id)[0]:
        bot.send_message(message.chat.id, 'Недостаточно средств')
        return
    if Decimal(message.text.replace(',', '.').replace(' ', '')) < 0:
        bot.send_message(message.chat.id, 'Сумма введена неправильна')
        return
    try:

        value = Decimal(message.text.replace(',', '.').replace(' ', '')) - commission
        dbworker.create_withdraw(message.chat.id, 'btc', value)
        withdraw_id = dbworker.get_user_last_withdraw(message.chat.id)
        dbworker.set_withdraw_commission(withdraw_id, commission)

        dbworker.set_state(message.chat.id, config.State.WITHDRAW_BTC_WAIT_PAYMENT.value)
        bot.send_message(message.chat.id, "Введите кошелек на который надо выводить:",
                         reply_markup=buttons.get_back_to_assets_managment_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(
    func=lambda message: dbworker.get_state(message.chat.id) == config.State.WITHDRAW_BTC_WAIT_PAYMENT.value
)
def handle(message):
    logging_message(message)
    try:
        dbworker.set_state(message.chat.id, config.State.ZERO.value)
        admins = dbworker.get_admins_type('withdraw')
        withdraw_id = dbworker.get_user_last_withdraw(message.chat.id)
        withdraw_amount = dbworker.get_withdraw_amaunt_btc(withdraw_id)
        commission = dbworker.get_withdraw_commission(withdraw_id)
        dbworker.set_withdraw_btc_balance_was(withdraw_id, dbworker.get_btc_balance(message.chat.id)[0])
        dbworker.set_withdraw_rub_balance_was(withdraw_id, dbworker.get_rub_balance(message.chat.id)[0])
        dbworker.user_btc_minus(message.chat.id, withdraw_amount[0] + commission)
        fio = dbworker.get_fio(message.chat.id)
        username = dbworker.get_username(message.chat.id)
        email = dbworker.get_email(message.chat.id)
        dbworker.set_withdraw_status(withdraw_id, '1')
        dbworker.set_withdraw_btc_payment(withdraw_id, message.text)
        for admin in admins:
            try:
                admin_t_id = admin[0]
                bot_admin.send_message(admin_t_id, f'⬆️Заявка №{withdraw_id}\n'
                                                   f'на вывод {withdraw_amount[0]} btc\n'
                                                   f'На кошелек: {message.text}\n'
                                                   f'ID: {message.chat.id} username: @{username}\n'
                                                   f'Данные пользователя: \n'
                                                   f'{fio}\n'
                                                   f'{email}',
                                       reply_markup=buttons.get_withdraw_admin_approve_keyboard(withdraw_id))
            except telebot.apihelper.ApiException as e:
                logging.exception(e)
                continue
        bot.send_message(message.chat.id, 'Запрос на вывод отправлен администратору, скоро мы переведем средства')
    except telebot.apihelper.ApiException as e:
        logging.exception(e)

'''
@bot.callback_query_handler(func=lambda call: 'withdraw_btc_wallet_1' == call.data)
def callback(call):
    logging_call(call)
    dbworker.set_state(call.message.chat.id, config.State.ZERO.value)
    admins = dbworker.get_admins()
    withdraw_id = dbworker.get_user_last_withdraw(call.message.chat.id)
    withdraw_amount = dbworker.get_withdraw_amaunt_btc(withdraw_id)
    fio = dbworker.get_fio(call.message.chat.id)
    username = dbworker.get_username(call.message.chat.id)
    email = dbworker.get_email(call.message.chat.id)
    dbworker.set_withdraw_status(withdraw_id, '1')
    for admin in admins:
        try:
            admin_t_id = admin[0]
            bot_admin.send_message(admin_t_id, f'Заявка №{withdraw_id}\nна вывод {withdraw_amount[0]} btc\nНа '
                                               f'<платежная система>: <реквизиты>\nID: {call.message.chat.id} '
                                               f'username: @{username}'
                                               f'\nДанные пользователя: \n{fio}\n{email}',
                                   reply_markup=buttons.get_withdraw_admin_approve_keyboard(withdraw_id))
        except telebot.apihelper.ApiException as e:
            logging.exception(e)
            continue
    bot.edit_message_text('Запрос на вывод отправлен администратору, скоро мы переведем средства', call.from_user.id,
                          call.message.message_id)


@bot.callback_query_handler(func=lambda call: 'withdraw_btc_wallet_2' == call.data)
def callback(call):
    logging_call(call)
    try:
        bot.edit_message_text('Кошелёк недоступен', call.from_user.id,
                              call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
'''

@bot.callback_query_handler(func=lambda call: 'withdraw_rub' == call.data)
def callback(call):
    logging_call(call)
    try:
        bot.edit_message_text('Куда выводим?', call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_withdraw_rub_banks_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'withdraw_rub_bank_' == call.data[:18])
def callback(call):
    logging_call(call)
    try:
        bank = call.data[18:]
        withdraw_banks[call.message.chat.id] = bank
        user_rub_value = dbworker.get_rub_balance(call.message.chat.id)
        dbworker.set_state(call.message.chat.id, config.State.WAITING_WITHDRAW_RUB_SUM.value)
        bot.edit_message_text(f'Какую сумму вывести:\n\nУ вас: {user_rub_value[0]} руб', call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_back_to_withdraw_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(
    func=lambda message: dbworker.get_state(message.chat.id) == config.State.WAITING_WITHDRAW_RUB_SUM.value)
def handle(message):
    logging_message(message)
    try:
        float(message.text.replace(',', '.').replace(' ', ''))
    except:
        return
    bank = withdraw_banks[message.chat.id]
    if bank == 'sber':
        commission = float(dbworker.get_commission_withdraw_sber()/100)
    elif bank == 'tink':
        commission = float(dbworker.get_commission_withdraw_tink()/100)

    if float(message.text.replace(',', '.').replace(' ', '')) > float(dbworker.get_rub_balance(message.chat.id)[0]):
        bot.send_message(message.chat.id, 'Недостаточно средств')
        return
    try:
        # dbworker.cleanup_ads()
        value = float(message.text) * (1 - commission)
        id = dbworker.create_withdraw(message.chat.id, 'rub', value)
        comm = float(message.text) * commission
        dbworker.set_withdraw_commission(id, comm)
        dbworker.set_state(message.chat.id, config.State.WITHDRAW_RUB_WAIT_PAYMENT.value)
        bot.send_message(message.chat.id, "Введите реквизиты для получения перевода")

    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(
    func=lambda message: dbworker.get_state(message.chat.id) == config.State.WITHDRAW_RUB_WAIT_PAYMENT.value
)
def handle(message):
    logging_message(message)
    try:
        admins = dbworker.get_admins_type('withdraw')
        withdraw_id = dbworker.get_user_last_withdraw(message.chat.id)
        dbworker.set_withdraw_btc_balance_was(withdraw_id, dbworker.get_btc_balance(message.chat.id)[0])
        dbworker.set_withdraw_rub_balance_was(withdraw_id, dbworker.get_rub_balance(message.chat.id)[0])

        withdraw_amount = dbworker.get_withdraw_amaunt_rub(withdraw_id)
        comm = dbworker.get_withdraw_commission(withdraw_id)
        dbworker.user_rub_minus(message.chat.id, withdraw_amount[0] + comm)
        fio = dbworker.get_fio(message.chat.id)
        username = dbworker.get_username(message.chat.id)
        email = dbworker.get_email(message.chat.id)
        dbworker.set_withdraw_status(withdraw_id, '1')
        bank = withdraw_banks[message.chat.id]
        if bank == 'sber':
            bank = 'сбербанк'
        elif bank == 'tink':
            bank = 'тинькофф'
        dbworker.set_withdraw_rub_payment(withdraw_id, message.text, bank)
        for admin in admins:
            try:
                admin_t_id = admin[0]
                bot_admin.send_message(admin_t_id, f'Заявка №{withdraw_id}\nна вывод {withdraw_amount[0]} rub\nНа '
                                                   f'{bank}: {message.text}\nID: {message.chat.id} '
                                                   f'username: @{username}'
                                                   f'\nДанные пользователя: \n{fio}\n{email}',
                                       reply_markup=buttons.get_withdraw_admin_approve_keyboard(withdraw_id))
            except telebot.apihelper.ApiException as e:
                logging.exception(e)
                continue
        bot.send_message(message.chat.id, 'Запрос на вывод отправлен администратору, скоро мы переведем средства',
                         reply_markup=buttons.get_back_to_withdraw_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'requisites_' == call.data[:11])
def callback(call):
    logging_call(call)
    try:
        admins = dbworker.get_admins()
        withdraw_id = dbworker.get_user_last_withdraw(call.message.chat.id)
        withdraw_amount = dbworker.get_withdraw_amaunt_rub(withdraw_id)
        fio = dbworker.get_fio(call.message.chat.id)
        username = dbworker.get_username(call.message.chat.id)
        email = dbworker.get_email(call.message.chat.id)
        dbworker.set_withdraw_status(withdraw_id, '1')
        for admin in admins:
            try:
                admin_t_id = admin[0]
                bot_admin.send_message(admin_t_id, f'Заявка №{withdraw_id}\nна вывод {withdraw_amount[0]} rub\nНа '
                                                   f'<платежная система>: <реквизиты>\nID: {call.message.chat.id} '
                                                   f'username: @{username}'
                                                   f'\nДанные пользователя: \n{fio}\n{email}',
                                       reply_markup=buttons.get_withdraw_admin_approve_keyboard(withdraw_id))
            except telebot.apihelper.ApiException as e:
                logging.exception(e)
                continue
        bot.edit_message_text('Запрос на вывод отправлен администратору, скоро мы переведем средства',
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_back_to_withdraw_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'withdraw_rub_cash' == call.data)
def callback(call):
    logging_call(call)
    try:
        dbworker.set_state(call.message.chat.id, config.State.WAITING_WITHDRAW_RUB_CASH_CITY.value)
        bot.edit_message_text('Какая страна и какой город?', call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_back_to_withdraw_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(
    func=lambda message: dbworker.get_state(message.chat.id) == config.State.WAITING_WITHDRAW_RUB_CASH_CITY.value)
def handle(message):
    logging_message(message)
    try:
        # dbworker.cleanup_ads()
        user_rub_value = dbworker.get_rub_balance(message.chat.id)
        dbworker.set_state(message.chat.id, config.State.WAITING_WITHDRAW_RUB_CASH_SUM.value)
        bot.send_message(message.chat.id, f"У вас: {user_rub_value[0]}\nКакую сумму вывести?",
                         reply_markup=buttons.get_back_to_withdraw_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(
    func=lambda message: dbworker.get_state(message.chat.id) == config.State.WAITING_WITHDRAW_RUB_CASH_SUM.value)
def handle(message):
    logging_message(message)
    try:
        # dbworker.cleanup_ads()
        dbworker.set_state(message.chat.id, config.State.ZERO.value)
        support_username = bot_support.get_me().username

        bot.send_message(f" Напишите @{support_username},",
                         message.from_user.id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


#

@bot.callback_query_handler(func=lambda call: 'withdraw_code_' == call.data[:14])
def callback(call):
    logging_call(call)
    try:
        currency = call.data[14:]
        dbworker.create_code(call.message.chat.id, currency, 0)
        if currency == 'btc':
            user_btc_value = dbworker.get_btc_balance(call.message.chat.id)
            send_text = f"Ваш баланс: {user_btc_value[0]:.8f} Bitcoin\nВведите сумму передачи:"
        else:
            user_rub_value = dbworker.get_rub_balance(call.message.chat.id)
            send_text = f"Ваш баланс: {user_rub_value[0]} Рублей\nВведите сумму передачи:"
        bot.edit_message_text(send_text, call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_back_to_withdraw_keyboard())
        dbworker.set_state(call.message.chat.id, config.State.ENTER_CODE_SUM.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(
    func=lambda message: dbworker.get_state(message.chat.id) == config.State.ENTER_CODE_SUM.value)
def handle(message):
    logging_message(message)
    try:
        code_id = dbworker.get_user_last_code(message.chat.id)
        code_amount = message.text.replace(',', '.')
        code_currency = dbworker.get_code_currency(code_id)
        if code_currency == 'btc' and float(dbworker.get_btc_balance(message.chat.id)[0]) < float(code_amount):
            bot.send_message(message.chat.id,
                             f"Недостаточно средств на счету.",
                             reply_markup=buttons.get_not_enough_money_code_keyboard())
        elif code_currency == 'rub' and float(dbworker.get_rub_balance(message.chat.id)[0]) < float(code_amount):
            bot.send_message(message.chat.id,
                             f"Недостаточно средств на счету.",
                             reply_markup=buttons.get_not_enough_money_code_keyboard())
        else:
            if code_currency == 'btc':
                dbworker.set_code_amount_btc(code_id, code_amount)
            else:
                dbworker.set_code_amount_rub(code_id, code_amount)
            bot.send_message(message.chat.id,
                             f"С вашего счета будет списано {code_amount} {code_currency}. "
                             f"Вы сможете передать этот код другому человеку или "
                             f"зачислить на свой счет",
                             reply_markup=buttons.get_create_code_keyboard(code_id))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'create_code_' == call.data[:12])
def callback(call):
    logging_call(call)
    try:
        code_id = call.data[12:]
        code = get_random_string(64)
        dbworker.set_code(code_id, code)
        dbworker.set_balance_was_creator_code(code_id, call.message.chat.id)
        code_currency = dbworker.get_code_currency(code_id)
        if code_currency == 'btc':
            code_amount_btc = dbworker.get_code_amount_btc(code_id)
            dbworker.user_btc_minus(call.message.chat.id, code_amount_btc)
        else:
            code_amount_rub = dbworker.get_code_amount_rub(code_id)
            dbworker.user_rub_minus(call.message.chat.id, code_amount_rub)
        dbworker.set_code_status(code_id, '1')
        bot.send_message(call.message.chat.id, "Ваш код")
        bot.send_message(call.message.chat.id, code)
        dbworker.set_balance_creator_code(code_id, call.message.chat.id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'exchange' == call.data)
def callback(call):
    logging_call(call)
    try:
        user_rub_value = dbworker.get_rub_balance(call.message.chat.id)
        user_btc_value = dbworker.get_btc_balance(call.message.chat.id)
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text(f"Обменять\nВаш баланс:\n{user_btc_value[0]:.8f} "
                              f"Bitcoin\n{user_rub_value[0]} "
                              "Рублей", call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_exchange_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'exchange_btc_rub' == call.data)
def callback(call):
    logging_call(call)
    try:
        user_rub_value = dbworker.get_rub_balance(call.message.chat.id)
        user_btc_value = dbworker.get_btc_balance(call.message.chat.id)
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text(f"Обменять\nВаш баланс:\n{user_btc_value[0]:.8f} Bitcoin\n{user_rub_value[0]} "
                              "Рублей", call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_exchange_btc_rub_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'exchange_btc_rub_buy' == call.data)
def callback(call):
    logging_call(call)
    try:
        commission = dbworker.get_commission_exchange() / 100
        user_rub_value = dbworker.get_rub_balance(call.message.chat.id)
        max_btc_value = user_rub_value[0] / (Decimal(
            currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close']) \
                        * \
                        Decimal(currency_price_online.get_latest_currency_price('USD').value))\
                                             /\
                                             Decimal(str(1 + commission))
        dbworker.set_state(call.message.chat.id, config.State.EXCHANGE_BTC_RUB_BUY_ENTER_AMOUNT.value)
        bot.edit_message_text(f"Пожалуйста, введите сумму от 100 до {user_rub_value[0]} RUB или от 0.000059 до "
                              f"{max_btc_value:.8f} BTC.\n\nЕсли вы хотите указать сумму в BTC, то добавьте "
                              f"тикер криптовалюты BTC (например: 0.1 BTC)", call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_back_to_exchange_btc_rub_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(
    func=lambda message: dbworker.get_state(message.chat.id) == config.State.EXCHANGE_BTC_RUB_BUY_ENTER_AMOUNT.value)
def handle(message):
    logging_message(message)

    try:
        # dbworker.cleanup_ads()
        commission = dbworker.get_commission_exchange()/100

        user_btc_value = dbworker.get_btc_balance(message.chat.id)
        user_rub_value = dbworker.get_rub_balance(message.chat.id)

        max_btc_value = user_rub_value[0] / (Decimal(
            currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close']) \
                                             * \
                                             Decimal(currency_price_online.get_latest_currency_price('USD').value))\
                                             /\
                                             Decimal(str(1 + commission))

        try:
            Decimal(message.text.replace(',', '.').replace('BTC', '').replace(' ', ''))
        except:
            bot.send_message(message.chat.id,
                             f"Пожалуйста, введите сумму от 100 до {user_rub_value[0]} RUB или от 0.000059 до "
                             f"{'{:.8f}'.format(max_btc_value)} BTC.\n\nЕсли вы хотите указать сумму в BTC, то добавьте "
                             f"тикер криптовалюты BTC (например: 0.1 BTC)")

            return



        if 'BTC' in message.text:
            dbworker.set_state(message.chat.id, config.State.ZERO.value)
            getcontext().prec = 8
            btc_value = Decimal(message.text.replace(',', '.').replace('BTC', '').replace(' ', ''))
            rub_value = btc_value * Decimal(
                currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close']) \
                        * Decimal(currency_price_online.get_latest_currency_price('USD').value) * Decimal(str(1+commission))
            comm = Decimal(str(commission)) * rub_value / Decimal(str(1+commission))
            if float(max_btc_value) >= float(btc_value) >= 0.000059:

                dbworker.create_exchange(message.chat.id, rub_value, btc_value, 'buy', comm,
                                         currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close'],
                                         currency_price_online.get_latest_currency_price('USD').value,
                                         user_btc_value[0], user_rub_value[0])
                bot.send_message(message.chat.id, f"У вас спишется {rub_value} руб, вы получите {btc_value} btc\n\n❗️"
                                                  f"Заявка действует 5 минут. Нажмите подтвердить, если хотите "
                                                  f"совершить обмен по текущему курсу.",
                                 reply_markup=buttons.get_exchange_btc_rub_buy_accept_keyboard())
            else:

                bot.send_message(message.chat.id,
                                 f"Пожалуйста, введите сумму от 100 до {user_rub_value[0]} RUB или от 0.000059 до "
                                 f"{'{:.8f}'.format(max_btc_value)} BTC.\n\nЕсли вы хотите указать сумму в BTC, то добавьте "
                                 f"тикер криптовалюты BTC (например: 0.1 BTC)")
                dbworker.set_state(message.chat.id, config.State.EXCHANGE_BTC_RUB_BUY_ENTER_AMOUNT.value)
        else:
            dbworker.set_state(message.chat.id, config.State.ZERO.value)
            getcontext().prec = 8
            rub_value = Decimal(message.text.replace(',', '.'))
            if float(user_rub_value[0]) >= float(rub_value) >= 100:

                btc_value = Decimal(1-commission)*( rub_value / (Decimal(
                    currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close'])
                            * Decimal(currency_price_online.get_latest_currency_price('USD').value)))
                comm = Decimal(str(commission)) * rub_value
                dbworker.create_exchange(message.chat.id, rub_value, btc_value, 'buy', comm,
                                         currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close'],
                                         currency_price_online.get_latest_currency_price('USD').value,
                                         user_btc_value[0], user_rub_value[0])
                bot.send_message(message.chat.id, f"У вас спишется {rub_value} руб, вы получите {btc_value} btc\n\n❗️"
                                                  f"Заявка действует 5 минут. Нажмите подтвердить, если хотите совершить"
                                                  f" обмен по текущему курсу.",
                                 reply_markup=buttons.get_exchange_btc_rub_buy_accept_keyboard())
            else:
                bot.send_message(message.chat.id,
                                 f"Пожалуйста, введите сумму от 100 до {user_rub_value[0]} RUB или от 0.000059 до "
                                 f"{'{:.8f}'.format(max_btc_value)} BTC.\n\nЕсли вы хотите указать сумму в BTC, то добавьте "
                                 f"тикер криптовалюты BTC (например: 0.1 BTC)")
                dbworker.set_state(message.chat.id, config.State.EXCHANGE_BTC_RUB_BUY_ENTER_AMOUNT.value)

    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'exchange_btc_rub_buy_accept' == call.data)
def callback(call):
    logging_call(call)

    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        exchange_id = dbworker.get_user_last_exchange(call.message.chat.id)
        exchange_amount_btc = dbworker.get_exchange_amaunt_btc(exchange_id)
        exchange_amount_rub = dbworker.get_exchange_amaunt_rub(exchange_id)
        dbworker.set_exchange_status(exchange_id, '1')
        admins = dbworker.get_admins_type('exchange')
        username = dbworker.get_username(call.message.chat.id)
        fio = dbworker.get_fio(call.message.chat.id)
        email = dbworker.get_email(call.message.chat.id)
        for admin in admins:
            try:
                admin_t_id = admin[0]
                bot_admin.send_message(admin_t_id, f'🔁 Заявка №{exchange_id}\nна покупку {exchange_amount_btc} btc '
                                                   f'за {exchange_amount_rub} rub\nID: {call.message.chat.id} '
                                                   f'username: @{username}\nДанные пользователя:\n{fio}\n{email}',
                                       reply_markup=buttons.get_exchange_admin_approve_keyboard(exchange_id))
            except telebot.apihelper.ApiException as e:
                logging.exception(e)
                continue
        bot.edit_message_text('Запрос на обмен отправлен администратору, скоро мы переведем средства',
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_back_to_exchange_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'exchange_btc_rub_sell' == call.data)
def callback(call):
    logging_call(call)

    try:
        commission = dbworker.get_commission_exchange() / 100

        user_btc_value = dbworker.get_btc_balance(call.message.chat.id)
        max_rub_value = user_btc_value[0] * (Decimal(
            currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close']) \
                        * \
                        Decimal(currency_price_online.get_latest_currency_price('USD').value)) \
                        *\
                        Decimal(str(1-commission))


        dbworker.set_state(call.message.chat.id, config.State.EXCHANGE_BTC_RUB_SELL_ENTER_AMOUNT.value)
        bot.edit_message_text(f"Пожалуйста, введите сумму от 100 до {max_rub_value:.2f} RUB или от 0.000059 до "
                              f"{user_btc_value[0]:.8f} BTC.\n\nЕсли вы хотите указать сумму в BTC, то добавьте "
                              f"тикер криптовалюты BTC (например: 0.1 BTC)", call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_back_to_exchange_btc_rub_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.message_handler(
    func=lambda message: dbworker.get_state(message.chat.id) == config.State.EXCHANGE_BTC_RUB_SELL_ENTER_AMOUNT.value)
def handle(message):
    logging_message(message)

    try:
        # dbworker.cleanup_ads()
        user_btc_value = dbworker.get_btc_balance(message.chat.id)
        user_rub_value = dbworker.get_rub_balance(message.chat.id)
        commission = dbworker.get_commission_exchange()/100

        max_rub_value = user_btc_value[0] * (Decimal(
            currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close']) \
                                             * \
                                             Decimal(currency_price_online.get_latest_currency_price('USD').value)) \
                        * \
                        Decimal(str(1 - commission))
        try:
            Decimal(message.text.replace(',', '.').replace('BTC', '').replace(' ', ''))
        except:
            bot.send_message(message.chat.id,
                             f"Пожалуйста, введите сумму от 100 до {max_rub_value:.2f} RUB или от 0.000059 до "
                             f"{user_btc_value[0]:.8f} BTC.\n\nЕсли вы хотите указать сумму в BTC, то добавьте "
                             f"тикер криптовалюты BTC (например: 0.1 BTC)")
        if 'BTC' in message.text:
            dbworker.set_state(message.chat.id, config.State.ZERO.value)
            getcontext().prec = 8
            btc_value = Decimal(message.text.replace(',', '.').replace('BTC', '').replace(' ', ''))
            if float(user_btc_value[0]) >= float(btc_value) >= 0.000059:
                rub_value = btc_value * Decimal(
                    currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close']) * Decimal(
                    currency_price_online.get_latest_currency_price('USD').value) * Decimal(str(1-commission))

                comm = btc_value * Decimal(str(commission))
                dbworker.create_exchange(message.chat.id, rub_value, btc_value, 'sell', comm,
                                         currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close'],
                                         currency_price_online.get_latest_currency_price('USD').value,
                                         user_btc_value[0], user_rub_value[0])
                bot.send_message(message.chat.id, f"Вы получите {rub_value} руб, спишется {btc_value} btc\n\n❗️"
                                                  f"Заявка действует 5 минут. Нажмите подтвердить, "
                                                  f"если хотите совершить обмен "
                                                  f"по текущему курсу.",
                                 reply_markup=buttons.get_exchange_btc_rub_sell_accept_keyboard())
            else:
                bot.send_message(message.chat.id,
                                 f"Пожалуйста, введите сумму от 100 до {max_rub_value:.2f} RUB или от 0.000059 до "
                                 f"{user_btc_value[0]:.8f} BTC.\n\nЕсли вы хотите указать сумму в BTC, то добавьте "
                                 f"тикер криптовалюты BTC (например: 0.1 BTC)")
                dbworker.set_state(message.chat.id, config.State.EXCHANGE_BTC_RUB_SELL_ENTER_AMOUNT.value)
        else:
            dbworker.set_state(message.chat.id, config.State.ZERO.value)
            getcontext().prec = 8
            rub_value = Decimal(message.text.replace(',', '.'))
            if float(max_rub_value) >= float(rub_value) >= 100:
                btc_value = rub_value / (Decimal(
                    currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close']) * Decimal(
                    currency_price_online.get_latest_currency_price('USD').value)) * Decimal(str(1-commission))
                comm = Decimal(commission) * rub_value / (Decimal(
                    currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close']) * Decimal(
                    currency_price_online.get_latest_currency_price('USD').value))

                dbworker.create_exchange(message.chat.id, rub_value, btc_value, 'sell', comm,
                                         currency_price_online.get_latest_crypto_price_usd('bitcoin')[0]['close'],
                                         currency_price_online.get_latest_currency_price('USD').value,
                                         user_btc_value[0], user_rub_value[0])
                bot.send_message(message.chat.id, f"Вы получите {rub_value} руб, спишется {btc_value} btc\n\n❗️Заявка "
                                                  f"действует 5 минут. Нажмите подтвердить, если хотите совершить обмен "
                                                  f"по текущему курсу.",
                                 reply_markup=buttons.get_exchange_btc_rub_sell_accept_keyboard())
            else:
                bot.send_message(message.chat.id,
                                 f"Пожалуйста, введите сумму от 100 до {max_rub_value:.2f} RUB или от 0.000059 до "
                                 f"{user_btc_value[0]:.8f} BTC.\n\nЕсли вы хотите указать сумму в BTC, то добавьте "
                                 f"тикер криптовалюты BTC (например: 0.1 BTC)")
                dbworker.set_state(message.chat.id, config.State.EXCHANGE_BTC_RUB_SELL_ENTER_AMOUNT.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'exchange_btc_rub_sell_accept' == call.data)
def callback(call):
    logging_call(call)
    try:
        exchange_id = dbworker.get_user_last_exchange(call.message.chat.id)
        exchange_amount_btc = dbworker.get_exchange_amaunt_btc(exchange_id)
        exchange_amount_rub = dbworker.get_exchange_amaunt_rub(exchange_id)
        dbworker.set_exchange_status(exchange_id, '1')
        admins = dbworker.get_admins_type('exchange')
        username = dbworker.get_username(call.message.chat.id)
        fio = dbworker.get_fio(call.message.chat.id)
        email = dbworker.get_email(call.message.chat.id)
        for admin in admins:
            try:
                admin_t_id = admin[0]
                bot_admin.send_message(admin_t_id, f'🔁 Заявка №{exchange_id}\nна продажу {exchange_amount_btc} btc '
                                                   f'за {exchange_amount_rub} rub\nID: {call.message.chat.id} '
                                                   f'username: @{username}\nДанные пользователя:\n{fio}\n{email}',
                                       reply_markup=buttons.get_exchange_admin_approve_keyboard(exchange_id))
            except telebot.apihelper.ApiException as e:
                logging.exception(e)
                continue
        bot.edit_message_text('Запрос на обмен отправлен администратору, скоро мы переведем средства',
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_back_to_exchange_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'history' == call.data)
def callback(call):
    logging_call(call)
    try:
        # dbworker.set_state(call.message.chat.id, config.State.SETTINGS.value)
        bot.edit_message_text("История операций", call.from_user.id,
                              call.message.message_id, reply_markup=buttons.get_history_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'in_out_history' == call.data)
def callback(call):
    logging_call(call)
    try:
        offset = 0
        in_out_operations = dbworker.get_in_out_operations(call.message.chat.id, offset)
        operations = ''
        if in_out_operations is not None:
            for operation in in_out_operations:
                operation_date = operation[0]  # 'yyyy-mm-dd'
                operation_type = 'выведено'
                if operation[3] == 'rub':
                    value = operation[1]
                else:
                    value = operation[2]
                currency = operation[3]
                operations += f'{operation_date} {operation_type} {value} {currency}\n'
        bot.edit_message_text("История операций ввода-вывода Биткоина/рубля:\n" + operations, call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_in_out_history_keyboard(call.message.chat.id, offset))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'in_out_history_offset_' == call.data[:22])
def callback(call):
    logging_call(call)
    try:
        offset = call.data[22:]
        in_out_operations = dbworker.get_in_out_operations(call.message.chat.id, offset)
        operations = ''
        for operation in in_out_operations:
            operation_date = operation[0]  # 'yyyy-mm-dd'
            operation_type = 'выведено'
            if operation[3] == 'rub':
                value = operation[1]
            else:
                value = operation[2]
            currency = operation[3]
            operations += f'{operation_date} {operation_type} {value} {currency}\n'
        bot.edit_message_text("История операций ввода-вывода Биткоина/рубля:\n" + operations,
                              call.from_user.id, call.message.message_id,
                              reply_markup=buttons.get_in_out_history_keyboard(call.message.chat.id, offset))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'exchange_history' == call.data)
def callback(call):
    logging_call(call)
    try:
        offset = 0
        exchange_operations = dbworker.get_exchange_operations(call.message.chat.id, offset)
        operations = ''
        if exchange_operations is not None:
            for operation in exchange_operations:
                operation_date = operation[0]  # 'yyyy-mm-dd'
                operation_type = 'куплено'
                if operation[3] == 'buy':
                    currency_1 = 'BTC'
                    currency_2 = 'RUB'
                    value = operation[2]
                    cost = operation[1]
                else:
                    currency_1 = 'RUB'
                    currency_2 = 'BTC'
                    value = operation[1]
                    cost = operation[2]
                operations += f'{operation_date} {operation_type} {value} {currency_1} за {cost} {currency_2}\n'
        bot.edit_message_text("История операций обмена Биткоина/рубля:\n" + operations, call.from_user.id,
                              call.message.message_id,
                              reply_markup=buttons.get_exchange_history_keyboard(call.message.chat.id, offset))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot.callback_query_handler(func=lambda call: 'exchange_history_offset_' == call.data[:24])
def callback(call):
    logging_call(call)
    try:
        offset = call.data[24:]
        exchange_operations = dbworker.get_exchange_operations(call.message.chat.id, offset)
        operations = ''
        for operation in exchange_operations:
            operation_date = operation[0]  # 'yyyy-mm-dd'
            operation_type = 'куплено'
            if operation[3] == 'buy':
                currency_1 = 'BTC'
                currency_2 = 'RUB'
                value = operation[2]
                cost = operation[1]
            else:
                currency_1 = 'RUB'
                currency_2 = 'BTC'
                value = operation[1]
                cost = operation[2]
            operations += f'{operation_date} {operation_type} {value} {currency_1} за {cost} {currency_2}\n'
        bot.edit_message_text("История операций обмена Биткоина/рубля:\n" + operations,
                              call.from_user.id, call.message.message_id,
                              reply_markup=buttons.get_exchange_history_keyboard(call.message.chat.id, offset))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


#  Polling
#bot.delete_webhook()
bot.polling()


#  Webhook

'''
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


bot.remove_webhook()

# time.sleep(7)  # Pause

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

#  nohup python3 main.py >/dev/null 2>&1 &
'''
