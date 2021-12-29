# coding=utf-8
import datetime
import logging
import os

import cherrypy
import redis
import telebot
from django.conf import settings

import buttons
import config
import dbworker
from django.core.mail import send_mail

from decimal import *
from decimal import Decimal

# from memory_profiler import profile
from send_email_code import send_email_code
from send_email_notification import send_email_notification

WEBHOOK_HOST = config.host_ip
WEBHOOK_PORT = config.host_port_admin
WEBHOOK_LISTEN = '0.0.0.0'  # #config.host_ip

WEBHOOK_SSL_CERT = config.ssl_cert  # Путь к сертификату
WEBHOOK_SSL_PRIV = config.ssl_priv  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % config.token_admin

bot_admin = telebot.TeleBot(config.token_admin)
bot = telebot.TeleBot(config.token)
bot_support = telebot.TeleBot(config.token_support)

log_file = 'admin.log'
f = open(log_file, 'a')
f.close()
file_log = logging.FileHandler(log_file)
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out),
                    format=u'%(filename)s [LINE:%(lineno)s; FUNC:%(funcName)s] #%(levelname)2s  [%(asctime)s]  %('
                           u'message)s',
                    level=logging.INFO)

admins = {}
withdraw_decline = {}
exchange_decline = {}
replenish_decline = {}
transactions = {}


def logging_transaction(type_transaction, profit):
    f = open('transactions.log', 'a')
    time = datetime.datetime.now()
    log_time = time.strftime("%d-%b-%y %H:%M:%S")
    f.write(f'[{log_time}]  {type_transaction}  {profit}')
    f.close()


def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None


@bot_admin.message_handler(commands=['delete'])
def handle_delete(message):
    try:
        dbworker.delete_user_admin(message.chat.id)
        bot_admin.send_message(message.chat.id, "Вы удалены из системы",
                               reply_markup=buttons.get_remove_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


# @profile
@bot_admin.message_handler(commands=['start'])
def handle_start(message):
    try:
        bot_admin.send_message(message.chat.id, 'Главное меню')
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.message_handler(commands=['disconnect'])
def message(message):
    try:
        connect_id = message.text.replace('/disconnect ', '')
        r = redis.Redis(connection_pool=config.pool)
        if dbworker.get_connect_t_id(connect_id):
            t_id = dbworker.get_connect_t_id(connect_id)
            admin_id = dbworker.get_connect_admin_id(connect_id)
            if admin_id != message.chat.id:
                return
            dbworker.set_admin_id_disconnections(connect_id)
            if r.get(f'connect_user_status_{t_id}')[:7] == b'connect':
                r.set(f'connect_admin_status_{message.chat.id}', 'disconnect')
                r.set(f'connect_user_status_{t_id}', 'disconnect')
                bot_support.send_message(t_id, 'Оператор отключился')
                bot_admin.send_message(message.chat.id, f'Вы отключены')
            else:
                bot_admin.send_message(message.chat.id, f'Админ уже отключился')
        else:
            bot_admin.send_message(message.chat.id,
                                   f'Такого id подключения нет')
    except Exception as error:
        pass


@bot_admin.message_handler(
    func=lambda message: "Изменить комиссию" == message.text)
def handle_change_commission(message):
    try:
        bot_admin.send_message(chat_id=message.chat.id,
                               text='Выберите какую коммиссию вы хотите изменить',
                               reply_markup=buttons.get_change_commission_keyboard1())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'change_commission_replenish' == call.data)
def callback(call):
    try:
        bot_admin.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text='Изменить комиссию на пополнение',
                                    reply_markup=buttons.get_change_commission_keyboard())
        dbworker.set_state(call.message.chat.id,
                           config.State.CHANGE_COMMISSION_REPLENISH.value)

    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'change_commission_exchange' == call.data)
def callback(call):
    try:
        bot_admin.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text='Изменить комиссию на обмен',
                                    reply_markup=buttons.get_change_commission_keyboard())
        dbworker.set_state(call.message.chat.id,
                           config.State.CHANGE_COMMISSION_EXCHANGE.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'change_commission_withdraw' == call.data)
def callback(call):
    try:
        bot_admin.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text='Изменить комиссию на вывод',
                                    reply_markup=buttons.get_change_commission_keyboard())
        dbworker.set_state(call.message.chat.id,
                           config.State.CHANGE_COMMISSION_WITHDRAW.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'change_commission' == call.data[4:] and
                      dbworker.get_state(
                          call.message.chat.id) == config.State.CHANGE_COMMISSION_REPLENISH.value)
def callback(call):
    try:

        commission = float(call.data[:3])
        dbworker.set_commission_replenish(commission)
        dbworker.set_state(call.message.chat.id, config.State.ZERO.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'change_commission' == call.data[4:] and
                      dbworker.get_state(
                          call.message.chat.id) == config.State.CHANGE_COMMISSION_EXCHANGE.value)
def callback(call):
    try:
        commission = float(call.data[:3])
        dbworker.set_commission_exchange(commission)
        dbworker.set_state(call.message.chat.id, config.State.ZERO.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'change_commission' == call.data[4:] and
                      dbworker.get_state(
                          call.message.chat.id) == config.State.CHANGE_COMMISSION_WITHDRAW.value)
def callback(call):
    try:
        commission = float(call.data[:3])
        dbworker.set_commission_withdraw(commission)
        dbworker.set_state(call.message.chat.id, config.State.ZERO.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: call.data == 'back_to_change_commission')
def callback(call):
    try:
        bot_admin.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text='Выберите какую коммиссию вы хотите изменить',
                                    reply_markup=buttons.get_change_commission_keyboard1())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.message_handler(func=lambda message: "54321" == message.text)
def handle(message):
    try:
        bot_admin.send_message(message.chat.id, 'Вы вошли')
        dbworker.add_admin(message.chat.id)
        admins[message.chat.id] = 'is_admin'
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.message_handler(commands=['check'])
def handle_delete(message):
    try:
        bot_admin.send_message(message.chat.id, f"ID: {str(message.chat.id)}",
                               reply_markup=buttons.get_main_menu_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.message_handler(commands=['admins'])
def handle_delete(message):
    try:
        bot_admin.send_message(message.chat.id, f"ID: {str(admins)}",
                               reply_markup=buttons.get_main_menu_keyboard())
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'withdraw_admin_decline' == call.data[:22])
def callback(call):
    try:
        dbworker.set_state(call.message.chat.id, config.State.ZERO.value)
        withdraw_id = call.data[22:]
        status = dbworker.get_withdraw_status(withdraw_id)
        if status != 1:
            bot_admin.edit_message_reply_markup(call.message.chat.id,
                                                call.message.message_id, '')
            bot_admin.answer_callback_query(call.id, 'Заявка уже обработана')
            return
        withdraw_currency = dbworker.get_withdraw_currency(withdraw_id)
        if withdraw_currency == 'btc':
            withdraw_value = dbworker.get_withdraw_amaunt_btc(withdraw_id)
        else:
            withdraw_value = dbworker.get_withdraw_amaunt_rub(withdraw_id)
        bot_admin.send_message(call.message.chat.id,
                               f'❌ Вы собираетесь отказать по заявку №{withdraw_id} на вывод {withdraw_value[0]} '
                               f'{withdraw_currency}',
                               reply_markup=buttons.get_withdraw_admin_decline_second_keyboard(
                                   withdraw_id))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'second_withdraw_admin_back' == call.data)
def callback(call):
    try:
        bot_admin.delete_message(call.from_user.id,
                                 call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'second_exchange_admin_back' == call.data[:26])
def callback(call):
    try:
        bot_admin.delete_message(call.from_user.id,
                                 call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'second_withdraw_admin_decline' == call.data[:29])
def callback(call):
    try:
        bot_admin.delete_message(call.from_user.id,
                                 call.message.message_id)
        withdraw_id = call.data[29:]
        status = dbworker.get_withdraw_status(withdraw_id)
        if status != 1:
            bot_admin.edit_message_reply_markup(call.message.chat.id,
                                                call.message.message_id, '')
            bot_admin.answer_callback_query(call.id, 'Заявка уже обработана')
            return
        withdraw_decline[call.message.chat.id] = withdraw_id
        dbworker.set_withdraw_end_dt(withdraw_id)
        dbworker.set_state(call.message.chat.id,
                           config.State.WAITING_WITHDRAW_DECLINE_REASON.value)
        bot_admin.send_message(call.message.chat.id,
                               f'Укажите причину отказа',
                               reply_markup=buttons.get_withdraw_admin_decline_second_reason_keyboard(
                                   withdraw_id))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.message_handler(
    func=lambda message: dbworker.get_state(
        message.chat.id) == config.State.WAITING_WITHDRAW_DECLINE_REASON.value)
def handle(message):
    try:
        answer = message.text
        bot_admin.delete_message(message.chat.id,
                                 message.message_id)
        bot_admin.delete_message(message.chat.id,
                                 message.message_id - 1)
        dbworker.set_state(message.chat.id, config.State.ZERO.value)
        withdraw_id = withdraw_decline[message.chat.id]
        current_admins = dbworker.get_admins()
        withdraw_currency = dbworker.get_withdraw_currency(withdraw_id)
        withdraw_user = dbworker.get_withdraw_user(withdraw_id)
        commission = dbworker.get_withdraw_commission(withdraw_id)
        if withdraw_currency == 'btc':
            withdraw_value = dbworker.get_withdraw_amaunt_btc(withdraw_id)
            balance_was = dbworker.get_withdraw_btc_balance_was(withdraw_id)
            dbworker.user_btc_plus(withdraw_user,
                                   withdraw_value[0] + commission)
            balance = dbworker.get_btc_balance(message.chat.id)[0]
            to_address = dbworker.get_withdraw_btc_payment(withdraw_id)
            comm = f'{commission:.8f} BTC'
        else:
            withdraw_value = dbworker.get_withdraw_amaunt_rub(withdraw_id)
            balance_was = dbworker.get_withdraw_rub_balance_was(withdraw_id)
            dbworker.user_rub_plus(withdraw_user,
                                   withdraw_value[0] + commission)
            balance = dbworker.get_rub_balance(message.chat.id)[0]
            to_address = dbworker.get_withdraw_rub_payment(withdraw_id)
            comm = f'{commission:.2f} RUB'
        dt = dbworker.get_withdraw_create_dt(withdraw_id)

        dbworker.add_transaction_withdraw(message.chat.id, dt, '0',
                                          f'{balance_was} {withdraw_currency}',
                                          f'{balance} {withdraw_currency}',
                                          comm, 'Отказ', answer, to_address)
        dbworker.set_withdraw_answer(withdraw_id, answer)
        dbworker.set_withdraw_status(withdraw_id, '3')
        dbworker.set_withdraw_rub_balance(withdraw_id, withdraw_user)
        dbworker.set_withdraw_btc_balance(withdraw_id, withdraw_user)
        for admin in current_admins:
            admin_t_id = admin[0]
            bot_admin.send_message(admin_t_id,
                                   f'⬆️❌ Администратор {message.chat.id} отклонил заявку №{withdraw_id} '
                                   f'на вывод {withdraw_value[0]} {withdraw_currency}. Причина: {answer}')
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'exchange_admin_decline' == call.data[:22])
def callback(call):
    try:
        exchange_id = call.data[22:]
        exchange_status = dbworker.get_exchange_status(exchange_id)
        if exchange_status != 1:
            bot_admin.edit_message_reply_markup(call.message.chat.id,
                                                call.message.message_id, '')
            bot_admin.answer_callback_query(call.id, 'Заявка уже обработана')
            return
        dbworker.set_state(call.message.chat.id, config.State.ZERO.value)

        exchange_type = dbworker.get_exchange_type(exchange_id)
        exchange_currency = ''
        if exchange_type == 'sell':
            exchange_currency = 'rub'
            exchange_value = dbworker.get_exchange_amaunt_btc(exchange_id)
        else:
            exchange_currency = 'btc'
            exchange_value = dbworker.get_exchange_amaunt_rub(exchange_id)
        bot_admin.send_message(call.message.chat.id,
                               f'❌ Вы собираетесь отказать по заявке №{exchange_id} на обмен {exchange_value} '
                               f'{exchange_currency}',
                               reply_markup=buttons.get_exchange_admin_decline_second_keyboard(
                                   exchange_id))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'second_exchange_admin_decline' == call.data[:29])
def callback(call):
    try:
        bot_admin.delete_message(call.from_user.id,
                                 call.message.message_id)
        exchange_id = call.data[29:]
        exchange_decline[call.message.chat.id] = exchange_id
        dbworker.set_state(call.message.chat.id,
                           config.State.WAITING_EXCHANGE_DECLINE_REASON.value)
        # bot_admin.send_message(call.message.chat.id, f"{exchange_decline[call.message.chat.id]}")
        bot_admin.send_message(call.message.chat.id,
                               f'Укажите причину отказа обмена',
                               reply_markup=buttons.get_exchange_admin_decline_second_reason_keyboard(
                                   exchange_id))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.message_handler(
    func=lambda message: dbworker.get_state(
        message.chat.id) == config.State.WAITING_EXCHANGE_DECLINE_REASON.value)
def handle(message):
    try:
        bot_admin.delete_message(message.chat.id,
                                 message.message_id)
        bot_admin.delete_message(message.chat.id,
                                 message.message_id - 1)
        dbworker.set_state(message.chat.id, config.State.ZERO.value)
        exchange_id = exchange_decline[message.chat.id]
        current_admins = dbworker.get_admins()
        exchange_type = dbworker.get_exchange_type(exchange_id)
        exchange_user = dbworker.get_exchange_user(exchange_id)
        dbworker.set_balance_after_exchange(exchange_id, exchange_user)
        answer = message.text
        dbworker.set_exchange_answer(exchange_id, answer)
        dbworker.set_exchange_end_dt(exchange_id)
        dbworker.set_exchange_admin_id(exchange_id, message.chat.id)
        dbworker.set_exchange_status(exchange_id, 3)

        if exchange_type == 'sell':
            exchange_currency = 'rub'
            exchange_value = dbworker.get_exchange_amaunt_rub(exchange_id)
        else:
            exchange_currency = 'btc'
            exchange_value = dbworker.get_exchange_amaunt_btc(exchange_id)

        for admin in current_admins:
            admin_t_id = admin[0]
            bot_admin.send_message(admin_t_id,
                                   f'⬆️❌ Администратор {message.chat.id} отклонил заявку №{exchange_id} '
                                   f'на обмен {exchange_value} {exchange_currency}.Причина: {message.text}')

        heading = 'Уведомление о обмене валюты!'
        html = f"""
                    <html>
                      <head></head>
                      <body>
                        <h1>Уведомление о обмене валюты!</h1>
                        <h2>Администратор отклонил заявку на обмен:
                         {exchange_value} {exchange_currency}</h2>
                        <h2>Причина: </h2>
                        <h3>{message.text}</h3>
                      </body>
                    </html>
                """
        send_email_notification(
            dbworker.get_email(message.from_user.id), heading, html
        )
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'withdraw_admin_approve' == call.data[:22])
def callback(call):
    try:
        withdraw_id = call.data[22:]
        if dbworker.get_withdraw_status(withdraw_id) != 1:
            bot_admin.answer_callback_query(call.id,
                                            'Заявка уже была обработана')
            bot_admin.edit_message_reply_markup(call.message.chat.id,
                                                call.message.message_id, '')
        else:
            withdraw_currency = dbworker.get_withdraw_currency(withdraw_id)
            if withdraw_currency == 'btc':
                withdraw_value = dbworker.get_withdraw_amaunt_btc(withdraw_id)
            else:
                withdraw_value = dbworker.get_withdraw_amaunt_rub(withdraw_id)
            bot_admin.send_message(call.message.chat.id,
                                   f'✅ Вы собираетесь одобрить заявку №{withdraw_id} на вывод '
                                   f'{withdraw_value[0]} {withdraw_currency}',
                                   reply_markup=buttons.get_withdraw_admin_approve_second_keyboard(
                                       withdraw_id))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'second_withdraw_admin_approve' == call.data[:29])
def callback(call):
    bot_admin.delete_message(call.from_user.id,
                             call.message.message_id)

    try:
        withdraw_id = call.data[29:]
        if dbworker.get_withdraw_status(withdraw_id) != 1:
            bot_admin.delete_message(call.message.chat.id,
                                     call.message.message_id)
            bot_admin.answer_callback_query(call.id,
                                            'Заявка уже была обработана')
        else:
            withdraw_user = dbworker.get_withdraw_user(withdraw_id)
            withdraw_currency = dbworker.get_withdraw_currency(withdraw_id)

            if withdraw_currency == 'btc':
                withdraw_value = dbworker.get_withdraw_amaunt_btc(withdraw_id)
                to_address = dbworker.get_withdraw_btc_payment(withdraw_id)
            else:
                withdraw_value = dbworker.get_withdraw_amaunt_rub(withdraw_id)
                to_address = dbworker.get_withdraw_rub_payment(withdraw_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    try:
        commission = dbworker.get_commission_withdraw() / 100
        profit = commission * float(withdraw_value[0]) / (1 - commission)
        dbworker.add_profit('Вывод', profit, withdraw_currency)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    try:
        dt = dbworker.get_withdraw_create_dt(withdraw_id)

        if withdraw_currency == 'btc':
            pay_system = 'кошелек'
            to_address = dbworker.get_withdraw_btc_payment(withdraw_id)
            balance_was = dbworker.get_withdraw_btc_balance_was(withdraw_id)
            balance = dbworker.get_btc_balance(withdraw_user)[0]
            comm = f'{dbworker.get_withdraw_commission(withdraw_id):.8f} BTC'
        else:
            pay_system = dbworker.get_withdraw_bank(withdraw_id)
            balance_was = dbworker.get_withdraw_rub_balance_was(withdraw_id)
            balance = dbworker.get_rub_balance(withdraw_user)[0]
            to_address = dbworker.get_withdraw_rub_payment(withdraw_id)
            comm = f'{dbworker.get_withdraw_commission(withdraw_id):.2f} RUB'
        dbworker.add_transaction_withdraw(call.message.chat.id, dt,
                                          f'{withdraw_value[0]} {withdraw_currency}',
                                          f'{balance_was} {withdraw_currency}',
                                          f'{balance} {withdraw_currency}',
                                          f'{comm}', 'Выполнено', '',
                                          to_address)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    dbworker.set_withdraw_end_dt(withdraw_id)
    current_admins = dbworker.get_admins()
    for admin in current_admins:
        try:
            admin_t_id = admin[0]
            bot_admin.send_message(admin_t_id,
                                   f'✅ Администратор {call.message.chat.id} одобрил заявку №{withdraw_id} '
                                   f'на вывод {withdraw_value[0]} {withdraw_currency} '
                                   f'На {pay_system}: {to_address} Id пользователя: {withdraw_user}')
        except telebot.apihelper.ApiException as e:
            logging.exception(e)
            continue
    try:
        user_rub_value = dbworker.get_rub_balance(withdraw_user)
        user_btc_value = dbworker.get_btc_balance(withdraw_user)
        dbworker.set_withdraw_status(withdraw_id, '2')
        dbworker.set_withdraw_btc_balance(withdraw_id, withdraw_user)
        dbworker.set_withdraw_rub_balance(withdraw_id, withdraw_user)
        bot.send_message(withdraw_user,
                         f'Вывод совершен:\nВаш баланс:\n{user_btc_value[0]:.8f} '
                         f'Bitcoin\n{user_rub_value[0]} Рублей')
        if withdraw_currency == 'btc':
            bot.send_message(withdraw_user, f'🔁✅ Введите номер Txid')
            dbworker.set_state(message.chat.id,
                               config.State.WITHDRAW_TXID_ENTER)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.message_handler(func=lambda m: dbworker.get_state(
    m.chat.id) == config.State.REPLENISH_TXID_ENTER.value)
def handle(message):
    try:
        dbworker.set_state(message.chat.id, config.State.ZERO.value)
        txid = message.text
        withdraw_id = withdraw_decline[message.chat.id]
        transaction_id = transactions[message.chat.id]
        dbworker.set_withdraw_txid(withdraw_id, txid)
        dbworker.set_replenish_txid_transaction(transaction_id, txid)
        bot_admin.send_message(message.chat.id, 'Txid введен✅')

    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'exchange_admin_approve' == call.data[:22])
def callback(call):
    try:
        exchange_id = call.data[22:]
        if dbworker.get_exchange_status(exchange_id) != 1:
            bot_admin.edit_message_reply_markup(call.message.chat.id,
                                                call.message.message_id,
                                                reply_markup='')
            bot_admin.answer_callback_query(call.id,
                                            'Заявка уже была обработана')
        else:
            exchange_type = dbworker.get_exchange_type(exchange_id)
            exchange_amount_btc = dbworker.get_exchange_amaunt_btc(exchange_id)
            exchange_amount_rub = dbworker.get_exchange_amaunt_rub(exchange_id)

            if exchange_type == 1:
                type_text = 'покупку'
            else:
                type_text = 'продажу'
            bot_admin.send_message(call.message.chat.id,
                                   f'✅ Вы собираетесь одобрить заявку №{exchange_id} '
                                   f'на {type_text} '
                                   f'{exchange_amount_btc} btc за {exchange_amount_rub} rub',
                                   reply_markup=buttons.get_exchange_admin_approve_second_keyboard(
                                       exchange_id))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'second_exchange_admin_approve' == call.data[:29])
def callback(call):
    bot_admin.delete_message(call.from_user.id,
                             call.message.message_id)
    current_admins = []
    exchange_id = 0
    exchange_user = 0

    exchange_currency = ''
    try:

        exchange_id = call.data[29:]
        if dbworker.get_exchange_status(exchange_id) != 1:
            bot_admin.edit_message_reply_markup(call.message.chat.id,
                                                call.message.message_id,
                                                reply_markup='')
            bot_admin.answer_callback_query(call.id,
                                            'Заявка уже была обработана')
        else:
            exchange_user = dbworker.get_exchange_user(exchange_id)
            exchange_type = dbworker.get_exchange_type(exchange_id)
            if exchange_type == 1:
                exchange_type = 'buy'
            else:
                exchange_type = 'sell'

            if exchange_type == 'buy':
                exchange_currency = 'btc'
                exchange_price_currency = 'rub'
                exchange_value = exchange_amount_btc = dbworker.get_exchange_amaunt_btc(
                    exchange_id)
                exchange_price = exchange_amount_rub = dbworker.get_exchange_amaunt_rub(
                    exchange_id)
                dbworker.user_btc_plus(call.message.chat.id,
                                       exchange_amount_btc)
                dbworker.user_rub_minus(call.message.chat.id,
                                        exchange_amount_rub)
            else:
                exchange_currency = 'rub'
                exchange_price_currency = 'btc'
                exchange_price = exchange_amount_btc = dbworker.get_exchange_amaunt_btc(
                    exchange_id)
                exchange_value = exchange_amount_rub = dbworker.get_exchange_amaunt_rub(
                    exchange_id)
                dbworker.user_btc_minus(call.message.chat.id,
                                        exchange_amount_btc)
                dbworker.user_rub_plus(call.message.chat.id,
                                       exchange_amount_rub)

            current_admins = dbworker.get_admins()
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    dbworker.set_balance_after_exchange(exchange_id, exchange_user)
    for admin in current_admins:
        try:
            admin_t_id = admin[0]
            bot_admin.send_message(admin_t_id,
                                   f'🔁✅ Администратор {call.message.chat.id} одобрил заявку\n'
                                   f'Заявку№{exchange_id} '
                                   f'на покупку {exchange_value} {exchange_currency} за {exchange_price}'
                                   f'{exchange_price_currency}\n'
                                   f'Id пользователя: {exchange_user}')
        except telebot.apihelper.ApiException as e:
            logging.exception(e)
            continue
    '''
    try:
        exchange_commission = dbworker.get_commission_exchange() / 100
        invited_by = dbworker.get_invited_by(exchange_user)
        if exchange_type == 'buy':
            plus = exchange_amount_rub * Decimal(str(exchange_commission)) * Decimal(str(0.05))
        else:
            plus = (exchange_amount_rub * Decimal(str(exchange_commission)) * Decimal(str(0.05))) / (1 - Decimal(str(exchange_commission)))
        dbworker.plus_bonuses(invited_by, plus)
        dbworker.user_rub_plus(invited_by, plus)
        dbworker.add_profit('Рефералка', -plus, 'rub')
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    try:
        commission = dbworker.get_commission_exchange() / 100
        if exchange_type == 'buy':
            profit = Decimal(str(commission)) * exchange_amount_rub
            currency = 'rub'
        else:
            profit = Decimal(str(commission)) * exchange_amount_btc
            currency = 'btc'
        dbworker.add_profit('Обмен', profit, currency)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    '''
    try:
        user_rub_value = dbworker.get_rub_balance(exchange_user)
        user_btc_value = dbworker.get_btc_balance(exchange_user)

        dbworker.set_exchange_status(exchange_id, '2')
        dbworker.set_exchange_end_dt(exchange_id)
        dbworker.set_exchange_admin_id(exchange_id, admin_t_id)

        bot.send_message(exchange_user, f'Средства отправлены:\n'
                                        f'Ваш баланс:\n'
                                        f'{user_btc_value[0]:.8f} Bitcoin\n'
                                        f'{user_rub_value[0]} Рублей')

        heading = 'Уведомление о обмене валюты!'
        html = f"""
            <html>
              <head></head>
              <body>
                <h1>Уведомление о обмене валюты!</h1>
                <h2>Средства отправлены:</h2>
                <h2>Ваш баланс:</h2>
                <h3>{user_btc_value[0]:.8f} Bitcoin</h3>
                <h3>{user_rub_value[0]} Рублей</h3>
              </body>
            </html>
        """
        send_email_notification(
            dbworker.get_email(call.from_user.id), heading, html
        )
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'replenish_admin_approve' == call.data[:23])
def callback(call):
    try:
        replenish_id = call.data[23:]
        if dbworker.get_replenish_status(replenish_id) != 1:
            bot_admin.answer_callback_query(call.id,
                                            'Заявка уже была обработана')
            bot_admin.edit_message_reply_markup(call.message.chat.id,
                                                call.message.message_id, '')
        else:
            replenish_currency = dbworker.get_replenish_currency(replenish_id)
            replenish_amount_btc = \
            dbworker.get_replenish_amaunt_btc(replenish_id)[0]
            bot_admin.send_message(call.message.chat.id,
                                   f'✅ Вы собираетесь одобрить заявку №{replenish_id} '
                                   f'на ввод {round(replenish_amount_btc, 8)} {replenish_currency}',
                                   reply_markup=buttons.get_replenish_admin_approve_second_keyboard(
                                       replenish_id))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'second_replenish_admin_approve' == call.data[:30])
def callback(call):
    bot_admin.delete_message(call.from_user.id,
                             call.message.message_id)

    try:
        replenish_id = call.data[30:]
        replenish_decline[call.message.chat.id] = replenish_id
        replenish_user = dbworker.get_replenish_user(replenish_id)
        balance_was = dbworker.get_btc_balance(replenish_user)[0]
        replenish_currency = dbworker.get_replenish_currency(replenish_id)
        if replenish_currency == 'btc':
            replenish_value = dbworker.get_replenish_amaunt_btc(replenish_id)
            dbworker.user_btc_plus(replenish_user, str(replenish_value[0]))
        else:
            replenish_value = dbworker.get_replenish_amaunt_rub(replenish_id)
            dbworker.user_rub_plus(replenish_user, str(replenish_value[0]))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    current_admins = dbworker.get_admins()
    comm = dbworker.get_replenish_commission(replenish_id)
    for admin in current_admins:
        try:
            admin_t_id = admin[0]
            bot_admin.send_message(admin_t_id,
                                   f'✅ Администратор {call.message.chat.id} подтвердил получение средств'
                                   f'по Заявке №{replenish_id} на пополнение'
                                   f' {replenish_value[0]} (+комиссия: {"{:0.8f}".format(comm)})'
                                   f' {replenish_currency}\n'
                                   f'Id пользователя: {replenish_user}')
        except telebot.apihelper.ApiException as e:
            logging.exception(e)
            continue
    try:
        commission = dbworker.get_commission_withdraw() / 100
        profit = commission * float(replenish_value[0]) / (1 - commission)
        dbworker.add_profit('Пополнение', profit, replenish_currency)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)

    try:
        dt = dbworker.get_replenish_create_dt(replenish_id)
        balance = dbworker.get_btc_balance(replenish_user)[0]

        transaction_id = dbworker.add_transaction_replenish(replenish_user, dt,
                                                            f'{replenish_value[0]}',
                                                            f'{balance_was} BTC',
                                                            f'{balance} BTC',
                                                            f'{"{:0.8f}".format(comm)} BTC',
                                                            'Пополнено', '')
        transactions[call.message.chat.id] = transaction_id
        to_address = dbworker.get_replenish_wallet_to(replenish_id)
        dbworker.set_replenish_to_address_transaction(transaction_id,
                                                      to_address)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    try:
        dbworker.set_state(call.message.chat.id,
                           config.State.REPLENISH_TXID_ENTER.value)
        bot_admin.send_message(call.message.chat.id, '⬇️ ✅ Введите номер Txid')
    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    try:
        user_rub_value = dbworker.get_rub_balance(replenish_user)
        user_btc_value = dbworker.get_btc_balance(replenish_user)
        dbworker.set_replenish_btc_balance(replenish_id, replenish_user)
        dbworker.set_replenish_rub_balance(replenish_id, replenish_user)
        dbworker.set_replenish_status(replenish_id, '2')
        dbworker.set_replenish_end_dt(replenish_id)
        bot.send_message(replenish_user,
                         f'Баланс пополнен:\nВаш баланс:\n{user_btc_value[0]} '
                         f'Bitcoin\n{user_rub_value[0]} Рублей')

    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.message_handler(func=lambda m: dbworker.get_state(
    m.chat.id) == config.State.REPLENISH_TXID_ENTER.value)
def handle(message):
    try:
        dbworker.set_state(message.chat.id, config.State.ZERO.value)
        txid = message.text
        replenish_id = replenish_decline[message.chat.id]
        transaction_id = transactions[message.chat.id]
        dbworker.set_replenish_txid(replenish_id, txid)
        dbworker.set_replenish_txid_transaction(transaction_id, txid)
        bot_admin.send_message(message.chat.id, 'Txid введен✅')

    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'second_replenish_admin_back' == call.data[:27])
def callback(call):
    try:
        bot_admin.delete_message(call.from_user.id,
                                 call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'replenish_admin_decline' == call.data[:23])
def callback(call):
    try:
        dbworker.set_state(call.message.chat.id, config.State.ZERO.value)
        replenish_id = call.data[23:]
        status = dbworker.get_replenish_status(replenish_id)
        if status != 1:
            bot_admin.answer_callback_query(call.id,
                                            'Заявка уже была обработана')
            bot_admin.edit_message_reply_markup(call.message.chat.id,
                                                call.message.message_id, '')
            return
        replenish_currency = dbworker.get_replenish_currency(replenish_id)
        if replenish_currency == 'btc':
            replenish_value = dbworker.get_replenish_amaunt_btc(replenish_id)
        else:
            replenish_value = dbworker.get_replenish_amaunt_rub(replenish_id)
        replenish_decline[call.message.chat.id] = replenish_id
        bot_admin.send_message(call.message.chat.id,
                               f'❌ Вы собираетесь отказать по заявке №{replenish_id} на пополнение {replenish_value[0]} '
                               f'{replenish_currency}',
                               reply_markup=buttons.get_replenish_admin_decline_second_keyboard(
                                   replenish_id))
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: 'second_replenish_admin_decline' == call.data[:30])
def callback(call):
    try:
        bot_admin.delete_message(call.message.chat.id, call.message.message_id)
        bot_admin.send_message(call.message.chat.id, 'Укажите причину отказа',
                               reply_markup=buttons.get_replenish_admin_decline_second_reason_keyboard())

        dbworker.set_state(call.message.chat.id,
                           config.State.WAITING_REPLENISH_DECLINE_REASON.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.message_handler(
    func=lambda m: dbworker.get_state(
        m.chat.id) == config.State.WAITING_REPLENISH_DECLINE_REASON.value)
def handle(message):
    current_admins = dbworker.get_admins()
    try:
        answer = message.text
        replenish_id = replenish_decline[message.chat.id]
        dbworker.set_replenish_answer(replenish_id, answer)

        replenish_currency = dbworker.get_replenish_currency(replenish_id)
        replenish_user = dbworker.get_replenish_user(replenish_id)
        dbworker.set_replenish_status(replenish_id, '3')
        dbworker.set_replenish_btc_balance(replenish_id, replenish_user)
        dbworker.set_replenish_rub_balance(replenish_id, replenish_user)
        dbworker.set_replenish_end_dt(replenish_id)
        dt = dbworker.get_replenish_create_dt(replenish_id)

        if replenish_currency == 'btc':
            replenish_value = dbworker.get_replenish_amaunt_btc(replenish_id)
            balance_was = f'{dbworker.get_replenish_btc_balance_was(replenish_id)} BTC'
            balance = f'{dbworker.get_replenish_btc_balance(replenish_id)} BTC'
            commission = f'{dbworker.get_replenish_commission(replenish_id)} BTC'
        else:
            replenish_value = dbworker.get_replenish_amaunt_rub(replenish_id)
            balance_was = f'{dbworker.get_replenish_rub_balance_was(replenish_id)} RUB'
            balance = f'{dbworker.get_replenish_rub_balance(replenish_id)} RUB'
            commission = f'{dbworker.get_replenish_commission(replenish_id)} RUB'
        transaction_id = dbworker.add_transaction_replenish(replenish_user, dt,
                                                            '0', balance_was,
                                                            balance, commission,
                                                            'Отказ', answer)
        to_address = dbworker.get_replenish_wallet_to(replenish_id)
        dbworker.set_replenish_to_address_transaction(transaction_id,
                                                      to_address)

    except telebot.apihelper.ApiException as e:
        logging.exception(e)
    for admin in current_admins:
        try:
            admin_t_id = admin[0]
            bot_admin.send_message(admin_t_id,
                                   f'⬇️❌ Администратор {admin_t_id} отклонил заявку\n'
                                   f'Заявку №{replenish_id}'
                                   f' на пополнение {replenish_value[0]} {replenish_currency}\n'
                                   f'Причина: {answer}')
        except telebot.apihelper.ApiException as e:
            logging.exception(e)
            continue

    try:
        bot.send_message(replenish_user,
                         f'Отказ в пополнении. Причина: {answer}')
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: call.data[:15] == 'answer_support_')
def call(call):
    try:
        if redis.Redis(connection_pool=config.pool).get(
                f'support_{call.message.chat.id}').decode('utf-8')[
           :8] == 'support_':
            return
    except:
        pass
    try:
        id = call.data[15:]
        t_id = call.message.chat.id
        status = dbworker.get_support_status(id)
        if status == 0:
            r = redis.Redis(connection_pool=config.pool)
            r.set(f'support_{t_id}', f'support_{id}')
            bot_admin.send_message(t_id, 'Пришлите ответ на обращение',
                                   reply_markup=buttons.get_back_to_support_main_keyboard())
            dbworker.update_support_status(id, '1')
        else:
            bot_admin.delete_message(t_id, message_id=call.message.message_id)
            bot_admin.send_message(t_id, f'На обращение №{id} уже ответили')
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.message_handler(func=lambda message:
redis.Redis(connection_pool=config.pool).get(
    f'support_{message.chat.id}') is not None)
def handle(message):
    if redis.Redis(connection_pool=config.pool).get(
            f'support_{message.chat.id}').decode('utf-8')[:8] != 'support_':
        return
    try:
        r = redis.Redis(connection_pool=config.pool)
        id = r.get(f'support_{message.chat.id}').decode('utf-8')[8:]
        answer = message.text
        dbworker.update_support_answer(id, answer)
        dbworker.set_support_admin(id, message.chat.id)

        user_id = dbworker.get_support_user_id(id)
        text = dbworker.get_support_text(id)
        bot.send_message(user_id, f'Ответ на ваш вопрос №{id}:\n'
                                  f'{answer}')
        dbworker.update_support_status(id, 2)
        r.set(f'support_{message.chat.id}', f'unsupport')
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: call.data == 'back_to_support_main' and
                      redis.Redis(connection_pool=config.pool).get(
                          f'support_{call.message.chat.id}').decode('utf-8')[
                      :8] == 'support_')
def call(call):
    try:
        r = redis.Redis(connection_pool=config.pool)
        id = r.get(f'support_{call.message.chat.id}').decode('utf-8')[8:]
        dbworker.update_support_status(id, 0)
        r.set(f'support_{call.message.chat.id}', f'unsupport')
        bot_admin.delete_message(call.message.chat.id, call.message.message_id)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: call.data[:21] == 'confirm_verification_')
def call(call):
    try:
        user_id = call.data[21:]
        admin_id = call.message.chat.id
        status = dbworker.get_status(user_id)
        if status != 0:
            bot_admin.send_message(admin_id, 'Запрос уже обработали')
            bot_admin.delete_message(admin_id, call.message.message_id)
            bot_admin.delete_message(admin_id, call.message.message_id - 1)
            bot_admin.delete_message(admin_id, call.message.message_id - 2)
        bot_admin.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id - 1)
        bot_admin.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id - 2)
        bot_admin.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text='Вы уверены что хотите подтвердить верификацию?',
                                    reply_markup=buttons.get_confirm_verification_keyboard(
                                        user_id))

        dbworker.set_status(user_id, 1)
        dbworker.set_state(admin_id,
                           config.State.ADMIN_CHECK_VERIFICATION.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: call.data[:20] == 'reject_verification_')
def call(call):
    try:
        user_id = call.data[20:]
        admin_id = call.message.chat.id
        status = dbworker.get_status(user_id)
        if status != 0:
            bot_admin.send_message(admin_id, 'Запрос уже обработали')
            bot_admin.delete_message(admin_id, call.message.message_id)
            bot_admin.delete_message(admin_id, call.message.message_id - 1)
            bot_admin.delete_message(admin_id, call.message.message_id - 2)
        bot_admin.delete_message(admin_id, call.message.message_id - 1)
        bot_admin.delete_message(admin_id, call.message.message_id - 2)
        bot_admin.edit_message_text(chat_id=admin_id,
                                    message_id=call.message.message_id,
                                    text='Вы уверены что хотите отклонить верификацию?',
                                    reply_markup=buttons.get_reject_verification_keyboard(
                                        user_id))
        dbworker.set_status(user_id, 1)
        dbworker.set_state(admin_id,
                           config.State.ADMIN_CHECK_VERIFICATION.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(
    func=lambda call: dbworker.get_state(call.message.chat.id) ==
                      config.State.ADMIN_CHECK_VERIFICATION.value)
def call(call):
    try:
        if call.data[:28] == 'second_confirm_verification_':
            user_id = call.data[28:]
            photo1 = open(f'verification/{user_id}/photo1.jpg', "rb")
            photo2 = open(f'verification/{user_id}/photo2.jpg', "rb")
            fio = dbworker.get_fio(user_id)
            date_of_birth = dbworker.get_birth_date(user_id)
            address = dbworker.get_address(user_id)
            text = f'Заявка на верификацию:\n' \
                   f'id: {user_id}\n' \
                   f'ФИО: {fio}\n' \
                   f'Дата рождения(в формате гггг-мм-дд): {date_of_birth}\n' \
                   f'Адрес: {address}'

            current_admins = dbworker.get_admins()
            for admin in current_admins:
                try:
                    bot_admin.delete_message(call.message.chat.id,
                                             call.message.message_id)
                    admin_t_id = admin[0]
                    caption = f'✅ Администратор {call.message.chat.id} отклонил верификацию:\n' + text
                    bot_admin.send_media_group(admin_t_id,
                                               [telebot.types.InputMediaPhoto(
                                                   photo1,
                                                   caption=caption),
                                                telebot.types.InputMediaPhoto(
                                                    photo2)])
                except telebot.apihelper.ApiException as e:
                    logging.exception(e)
                    continue
            dbworker.set_status(user_id, 2)
            dbworker.set_state(call.message.chat.id, config.State.ZERO.value)
            bot.send_message(chat_id=user_id,
                             text='Вам подтвердили верификацию')
        elif call.data[:33] == 'second_verification_verification_':
            user_id = call.data[28:]
            photo1 = open(f'verification/{user_id}/photo1.jpg', "rb")
            photo2 = open(f'verification/{user_id}/photo2.jpg', "rb")
            fio = dbworker.get_fio(user_id)
            date_of_birth = dbworker.get_birth_date(user_id)
            address = dbworker.get_address(user_id)
            text = f'Заявка на верификацию:\n' \
                   f'id: {user_id}\n' \
                   f'ФИО: {fio}\n' \
                   f'Дата рождения(в формате гггг-мм-дд): {date_of_birth}\n' \
                   f'Адрес: {address}'

            current_admins = dbworker.get_admins()
            for admin in current_admins:
                try:
                    bot_admin.delete_message(call.message.chat.id,
                                             call.message.message_id)
                    admin_t_id = admin[0]
                    caption = f'✅ Администратор {call.message.chat.id} отклонил верификацию:\n' + text

                    bot_admin.send_media_group(admin_t_id,
                                               [telebot.types.InputMediaPhoto(
                                                   photo1,
                                                   caption=caption),
                                                telebot.types.InputMediaPhoto(
                                                    photo2, )])
                except telebot.apihelper.ApiException as e:
                    logging.exception(e)
                    continue
            dbworker.set_state(call.message.chat.id, config.State.ZERO.value)
            bot.send_message(chat_id=user_id,
                             text='Вам отклонили верификацию. Для выяснения причины отклонения обратитесь в поддержку')
        elif call.data[:21] == 'back_to_verification_':
            user_id = call.data[21:]
            photo1 = open(f'verification/{user_id}/photo1.jpg', "rb")
            photo2 = open(f'verification/{user_id}/photo2.jpg', "rb")
            fio = dbworker.get_fio(user_id)
            date_of_birth = dbworker.get_birth_date(user_id)
            address = dbworker.get_address(user_id)
            text = f'Заявка на верификацию:\n' \
                   f'id: {user_id}\n' \
                   f'ФИО: {fio}\n' \
                   f'Дата рождения(в формате гггг-мм-дд): {date_of_birth}\n' \
                   f'Адрес: {address}'

            bot_admin.send_media_group(call.message.chat.id,
                                       [telebot.types.InputMediaPhoto(photo1,
                                                                      caption='Идентификация и проверка лица'),
                                        telebot.types.InputMediaPhoto(photo2,
                                                                      caption='Фото с документом')])

            bot_admin.send_message(call.message.chat.id, text,
                                   reply_markup=buttons.get_verification_keyboard(
                                       user_id))
            bot_admin.delete_message(call.message.chat.id,
                                     call.message.message_id)
            dbworker.set_status(user_id, 0)
            dbworker.set_state(call.message.chat.id, config.State.ZERO.value)
    except telebot.apihelper.ApiException as e:
        logging.exception(e)


@bot_admin.callback_query_handler(func=lambda call: call.data[:8] == 'connect_')
def call(call):
    r = redis.Redis(connection_pool=config.pool)
    try:
        if r.get(f'connect_admin_status_{call.message.chat.id}')[
           :8] == b'connect_':
            bot_admin.answer_callback_query(call.id,
                                            'Вы уже подключены к другому чату')
            return
    except:
        bot_admin.answer_callback_query(call.id,
                                        'Вы уже подключены к другому чату')
        return
    connect_id = call.data[8:]
    status = dbworker.get_connect_status(connect_id)
    if status != 0:
        bot_admin.delete_message(call.message.chat.id, call.message.message_id)
        bot_admin.answer_callback_query(call.id, 'Оператор уже подключен')
        return

    admin_id = call.message.chat.id
    dbworker.set_admin_id_connections(admin_id, connect_id)
    dbworker.set_state(call.message.chat.id,
                       config.State.CHAT_WITH_SUPPORT.value)
    bot_support_username = bot_support.get_me().username
    bot_admin.edit_message_text(
        f'Вы подключены - перейдите к @{bot_support_username}\n'
        f'ID подключения: {connect_id}\n'
        f'ID юзера: {dbworker.get_connect_t_id(connect_id)}',
        call.message.chat.id, call.message.message_id,
        reply_markup=buttons.get_disconnect_operator_keyboard(connect_id))
    t_id = dbworker.get_connect_t_id(connect_id)
    r = redis.Redis(connection_pool=config.pool)
    r.set(f'connect_admin_status_{call.message.chat.id}',
          f'connect_{connect_id}')
    r.set(f'connect_user_status_{t_id}', f'connect_{connect_id}')
    bot_support.send_message(t_id, 'Оператор подключился')


@bot_admin.callback_query_handler(
    func=lambda call: call.data[:11] == 'disconnect_')
def call(call):
    connect_id = call.data[11:]
    dbworker.set_admin_id_disconnections(connect_id)
    t_id = dbworker.get_connect_t_id(connect_id)
    r = redis.Redis(connection_pool=config.pool)
    r.set(f'connect_admin_status_{call.message.chat.id}', 'disconnect')
    r.set(f'connect_user_status_{t_id}', 'disconnect')
    bot_support.send_message(t_id, 'Оператор отключился')
    bot_admin.edit_message_text(f'Вы отключены',
                                call.message.chat.id, call.message.message_id)


#  Polling
bot_admin.polling()

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
            bot_admin.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


bot_admin.remove_webhook()

# time.sleep(7)  # Pause

bot_admin.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
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
