# coding=utf-8
import telebot

from telebot import types

try:
    from telegram_bot import dbworker
except ImportError:
    import dbworker


def get_remove_keyboard():
    return telebot.types.ReplyKeyboardRemove()


def get_main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row('Управление активами')
    keyboard.row('Личный кабинет')
    return keyboard


def get_lk_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Настройки', callback_data='settings'))
    keyboard.row(types.InlineKeyboardButton(text='Реферальная программа', callback_data='ref_program'))
    keyboard.row(types.InlineKeyboardButton(text='Комиссия', callback_data='commission'))
    keyboard.row(types.InlineKeyboardButton(text='Help', callback_data='help'))
    keyboard.row(types.InlineKeyboardButton(text='Верификация', callback_data='verification'))
    keyboard.row(types.InlineKeyboardButton(text='Промокод', callback_data='promo'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_start'))
    return keyboard


def get_settings_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Язык', callback_data='language'))
    keyboard.row(types.InlineKeyboardButton(text='2FA', callback_data='2fa'))
    keyboard.row(types.InlineKeyboardButton(text='e-mail', callback_data='email'))
    keyboard.row(types.InlineKeyboardButton(text='Относительный курс', callback_data='relative_rate'))
    keyboard.row(types.InlineKeyboardButton(text='Реквизиты для вывода', callback_data='withdrawal_requisites'))
    keyboard.row(types.InlineKeyboardButton(text='Автоконвертация', callback_data='autoconv'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_lk'))
    return keyboard

def get_ref_program_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Получить ссылку', callback_data='get_ref_link'))
    return keyboard

def get_assets_managment_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Пополнить', callback_data='replenish'))
    keyboard.row(types.InlineKeyboardButton(text='Вывести', callback_data='withdraw'))
    keyboard.row(types.InlineKeyboardButton(text='Обмен', callback_data='exchange'))
    keyboard.row(types.InlineKeyboardButton(text='История', callback_data='history'))
    keyboard.row(types.InlineKeyboardButton(text='Гарант', callback_data='garant'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_start'))
    return keyboard


def get_replenish_currency_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Bitcoin', callback_data='replenish_btc'))
    keyboard.row(types.InlineKeyboardButton(text='Рубль', callback_data='replenish_rub'))
    keyboard.row(types.InlineKeyboardButton(text='Код', callback_data='replenish_сode'))
    keyboard.row(types.InlineKeyboardButton(text='Иное', callback_data='chat_with_operator'))
    # keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_back_to_replenish_currency_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='replenish'))
    return keyboard


def get_back_to_replenish_rub_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='replenish_rub'))
    return keyboard


def get_withdraw_btc_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Код', callback_data='withdraw_code_btc'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_replenish_btc_wallets_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='<название кошелька 1>', callback_data='replenish_btc_wallet_1'))
    keyboard.row(types.InlineKeyboardButton(text='<название кошелька 2>', callback_data='replenish_btc_wallet_2'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_payment_replenish_btc_done_keyboard(replenish_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Перевод совершен',
                                            callback_data=f'replenish_btc_success_{replenish_id}'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_replenish_rub_banks_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Банки', callback_data='replenish_rub_banks'))
    # keyboard.row(types.InlineKeyboardButton(text='Qiwi', callback_data='replenish_rub_bank_qiwi'))
    keyboard.row(types.InlineKeyboardButton(text='Наличное пополнение', callback_data='replenish_rub_cash'))
    # keyboard.row(types.InlineKeyboardButton(text='Yandex.Money', callback_data='replenish_rub_bank_yandex_money'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_replenish_rub_wallets_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='<название кошелька 1>', callback_data='replenish_rub_wallet_1'))
    keyboard.row(types.InlineKeyboardButton(text='<название кошелька 2>', callback_data='replenish_rub_wallet_2'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_payment_replenish_rub_done_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Перевод совершен', callback_data='replenish_rub_success'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_withdraw_currency_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Bitcoin', callback_data='withdraw_btc'))
    keyboard.row(types.InlineKeyboardButton(text='Рубль', callback_data='withdraw_rub'))
    keyboard.row(types.InlineKeyboardButton(text='Иное', callback_data='chat_with_operator'))
    # keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_withdraw_rub_banks_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Тинькофф', callback_data='withdraw_rub_bank_tink'))
    keyboard.row(types.InlineKeyboardButton(text='Сбербанк', callback_data='withdraw_rub_bank_sber'))
    #keyboard.row(types.InlineKeyboardButton(text='Qiwi', callback_data='withdraw_rub_bank_qiwi'))
    keyboard.row(types.InlineKeyboardButton(text='Вывод наличными', callback_data='withdraw_rub_cash'))
    #keyboard.row(types.InlineKeyboardButton(text='Yandex.Money', callback_data='withdraw_rub_bank_yandex_money'))
    keyboard.row(types.InlineKeyboardButton(text='Код', callback_data='withdraw_code_rub'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_commission_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Бонусная программа', callback_data='bonus_program'))
    keyboard.row(types.InlineKeyboardButton(text='Сколько смогли сэкономить', callback_data='how_much_economy'))
    return keyboard


def get_help_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Чат с оператором', callback_data='chat_with_operator'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_lk'))
    return keyboard


def get_email_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Изменить e-mail', callback_data='change_email'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='settings'))
    return keyboard


def get_enter_email_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='email'))
    return keyboard


def get_first_add_btc_wallet():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    row = [
        types.InlineKeyboardButton(text='Да', callback_data='first_add_btc_wallet_yes'),
        types.InlineKeyboardButton(text='Нет', callback_data='first_add_btc_wallet_no')
    ]
    keyboard.row(*row)
    return keyboard


def get_first_add_rub_wallet():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    row = [
        types.InlineKeyboardButton(text='Да', callback_data='first_add_rub_wallet_yes'),
        types.InlineKeyboardButton(text='Нет', callback_data='first_add_rub_wallet_no')
    ]
    keyboard.row(*row)
    return keyboard


def get_exchange_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='BTC/РУБ', callback_data='exchange_btc_rub'))
    keyboard.row(types.InlineKeyboardButton(text='иное', callback_data='chat_with_operator'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_exchange_btc_rub_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Купить BTC', callback_data='exchange_btc_rub_buy'))
    keyboard.row(types.InlineKeyboardButton(text='Продать BTC', callback_data='exchange_btc_rub_sell'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='exchange'))
    return keyboard


def get_back_to_exchange_btc_rub_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='exchange_btc_rub'))
    return keyboard


def get_exchange_btc_rub_buy_accept_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Подтвердить', callback_data='exchange_btc_rub_buy_accept'))
    keyboard.row(types.InlineKeyboardButton(text='Отменить', callback_data='exchange_btc_rub_buy'))
    return keyboard


def get_exchange_btc_rub_sell_accept_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Подтвердить', callback_data='exchange_btc_rub_sell_accept'))
    keyboard.row(types.InlineKeyboardButton(text='Отменить', callback_data='exchange_btc_rub_sell'))
    return keyboard


def get_back_to_withdraw_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='withdraw'))
    return keyboard


def get_withdraw_rub_requisites_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='<реквизиты1>', callback_data='requisites_1'))
    keyboard.row(types.InlineKeyboardButton(text='<реквизиты2>', callback_data='requisites_2'))
    keyboard.row(types.InlineKeyboardButton(text='<реквизиты3>', callback_data='requisites_3'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='withdraw_rub'))
    return keyboard


def get_history_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Ввод-Вывод', callback_data='in_out_history'))
    keyboard.row(types.InlineKeyboardButton(text='Обмен', callback_data='exchange_history'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_in_out_history_keyboard(t_id, offset):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    in_out_cnt = dbworker.get_in_out_count(t_id)
    offset = int(offset)
    in_out_cnt = int(in_out_cnt)
    if offset == 0 and not (in_out_cnt < 10):
        row = [
            types.InlineKeyboardButton('Следующие 10 >', callback_data=f"in_out_history_offset_{offset+10}")
        ]
        keyboard.row(*row)
        keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='history'))
    elif offset + 10 > in_out_cnt and offset != 0:
        row = [
            types.InlineKeyboardButton("< Предыдущие 10", callback_data=f"in_out_history_offset_{offset-10}"),
        ]
        keyboard.row(*row)
        keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='history'))
    elif in_out_cnt < 10:
        keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='history'))
    else:
        row = [
            types.InlineKeyboardButton("< Предыдущие 10", callback_data=f"in_out_history_offset_{offset-10}"),
            types.InlineKeyboardButton('Следующие 10 >', callback_data=f"in_out_history_offset_{offset+10}")
        ]
        keyboard.row(*row)
        keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='history'))
    return keyboard


def get_exchange_history_keyboard(t_id, offset):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    exchange_cnt = dbworker.get_exchange_count(t_id)
    offset = int(offset)
    exchange_cnt = int(exchange_cnt)
    print(exchange_cnt)
    if offset == 0 and not (exchange_cnt < 10):
        row = [
            types.InlineKeyboardButton('Следующие 10 >', callback_data=f"exchange_history_offset_{offset + 10}")
        ]
        keyboard.row(*row)
        keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='history'))
    elif offset + 10 > exchange_cnt and offset != 0:
        row = [
            types.InlineKeyboardButton("< Предыдущие 10", callback_data=f"exchange_history_offset_{offset - 10}"),
        ]
        keyboard.row(*row)
        keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='history'))
    elif exchange_cnt < 10:
        keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='history'))
    else:
        row = [
            types.InlineKeyboardButton("< Предыдущие 10", callback_data=f"exchange_history_offset_{offset - 10}"),
            types.InlineKeyboardButton('Следующие 10 >', callback_data=f"exchange_history_offset_{offset + 10}")
        ]
        keyboard.row(*row)
        keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='history'))
    return keyboard


def get_withdraw_btc_wallets_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='<название кошелька 1>', callback_data='withdraw_btc_wallet_1'))
    keyboard.row(types.InlineKeyboardButton(text='<название кошелька 2>', callback_data='withdraw_btc_wallet_2'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_back_to_assets_managment_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_replenish_rub_select_bank_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Тинькофф', callback_data='replenish_rub_select_tink'))
    keyboard.row(types.InlineKeyboardButton(text='Сбербанк', callback_data='replenish_rub_select_sber'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_replenish_rub_payment_done_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Перевод совершен', callback_data='replenish_rub_payment_done'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_replenish_cash_country_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Россия', callback_data='replenish_cash_country_russia'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_replenish_cash_city_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Москва', callback_data='replenish_cash_city_moscow'))
    keyboard.row(types.InlineKeyboardButton(text='Санкт-Петербург',
                                            callback_data='replenish_cash_city_saint_petersburg'))
    keyboard.row(types.InlineKeyboardButton(text='Сочи', callback_data='replenish_cash_city_sochi'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='back_to_assets_managment'))
    return keyboard


def get_create_code_keyboard(code_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='выпустить код', callback_data=f'create_code_{code_id}'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='withdraw'))
    return keyboard


def get_main_admin_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row(types.KeyboardButton(text = 'Изменить комиссию'))
    return keyboard

def get_change_commission_keyboard1():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Пополнение', callback_data='change_commission_replenish'))
    keyboard.row(types.InlineKeyboardButton(text='Обмен', callback_data='change_commission_exchange'))
    keyboard.row(types.InlineKeyboardButton(text='Вывод', callback_data='change_commission_withdraw'))
    return keyboard

def get_change_commission_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.row(types.InlineKeyboardButton(text='0%', callback_data='0.0_change_commission'))
    row1 = [
        types.InlineKeyboardButton(text='0.5%', callback_data='0.5_change_commission'),
        types.InlineKeyboardButton(text='1%', callback_data='1.0_change_commission'),
        types.InlineKeyboardButton(text='2%', callback_data='2.0_change_commission')
    ]
    keyboard.row(*row1)

    row2 = [
        types.InlineKeyboardButton(text='3%', callback_data='3.0_change_commission'),
        types.InlineKeyboardButton(text='4%', callback_data='4.0_change_commission'),
        types.InlineKeyboardButton(text='5%', callback_data='5.0_change_commission')
    ]
    keyboard.row(*row2)

    keyboard.row(types.InlineKeyboardButton(text='Назад', callback_data='back_to_change_commission'))
    return keyboard


def get_replenish_admin_approve_keyboard(replenish_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Одобрить', callback_data="replenish_admin_approve" + str(replenish_id)),
        types.InlineKeyboardButton('Отказать', callback_data="replenish_admin_decline" + str(replenish_id))
    ]
    keyboard.row(*row)
    return keyboard


def get_replenish_admin_approve_second_keyboard(replenish_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Подтвердить', callback_data="second_replenish_admin_approve" + str(replenish_id)),
        types.InlineKeyboardButton('Вернуться', callback_data="second_replenish_admin_back" + str(replenish_id))
    ]
    keyboard.row(*row)
    return keyboard



def get_withdraw_admin_approve_second_keyboard(withdraw_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Подтвердить', callback_data="second_withdraw_admin_approve" + str(withdraw_id)),
        types.InlineKeyboardButton('Вернуться', callback_data="second_withdraw_admin_back")
    ]
    keyboard.row(*row)
    return keyboard


def get_withdraw_admin_approve_keyboard(withdraw_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Одобрить', callback_data="withdraw_admin_approve" + str(withdraw_id)),
        types.InlineKeyboardButton('Отказать', callback_data="withdraw_admin_decline" + str(withdraw_id))
    ]
    keyboard.row(*row)
    return keyboard


def get_exchange_admin_approve_keyboard(exchange_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Одобрить', callback_data="exchange_admin_approve" + str(exchange_id)),
        types.InlineKeyboardButton('Отказать', callback_data="exchange_admin_decline" + str(exchange_id))
    ]
    keyboard.row(*row)
    return keyboard


def get_exchange_admin_approve_second_keyboard(exchange_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Подтвердить', callback_data="second_exchange_admin_approve" + str(exchange_id)),
        types.InlineKeyboardButton('Вернуться', callback_data="second_exchange_admin_back" + str(exchange_id))
    ]
    keyboard.row(*row)
    return keyboard


def get_back_to_exchange_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='exchange'))
    return keyboard


def get_exchange_admin_decline_second_keyboard(exchange_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Да, отказать', callback_data="second_exchange_admin_decline" + str(exchange_id)),
        types.InlineKeyboardButton('Вернуться', callback_data="second_exchange_admin_back" + str(exchange_id))
    ]
    keyboard.row(*row)
    return keyboard


def get_exchange_admin_decline_second_reason_keyboard(exchange_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Вернуться', callback_data="second_exchange_admin_back" + str(exchange_id))
    ]
    keyboard.row(*row)
    return keyboard


def get_withdraw_admin_decline_second_keyboard(withdraw_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Да, отказать', callback_data="second_withdraw_admin_decline" + str(withdraw_id)),
        types.InlineKeyboardButton('Вернуться', callback_data="second_withdraw_admin_back")
    ]
    keyboard.row(*row)
    return keyboard


def get_replenish_admin_decline_second_keyboard(replenish_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Да, отказать', callback_data="second_replenish_admin_decline" + str(replenish_id)),
        types.InlineKeyboardButton('Вернуться', callback_data="second_replenish_admin_back")
    ]
    keyboard.row(*row)
    return keyboard


def get_replenish_admin_decline_second_reason_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Вернуться', callback_data="second_withdraw_admin_back")
    ]
    keyboard.row(*row)
    return keyboard


def get_withdraw_admin_decline_second_reason_keyboard(withdraw_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    row = [
        types.InlineKeyboardButton('Вернуться', callback_data="second_withdraw_admin_back" + str(withdraw_id))
    ]
    keyboard.row(*row)
    return keyboard


def get_not_enough_money_code_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.row(types.InlineKeyboardButton(text='Пополнить', callback_data='replenish'))
    keyboard.row(types.InlineKeyboardButton(text='назад', callback_data='withdraw'))
    return keyboard


def get_answer_support_question_keyboard(id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Ответить', callback_data=f'answer_support_{id}'))
    return keyboard

def get_back_to_support_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Вернуться', callback_data=f'back_to_support_main'))
    return keyboard


def get_verification_keyboard(t_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Потдвердить', callback_data=f'confirm_verification_{t_id}'))
    keyboard.row(types.InlineKeyboardButton(text='Отклонить', callback_data=f'reject_verification_{t_id}'))
    return keyboard


def get_confirm_verification_keyboard(t_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Да, хочу подтвердить верификацию',
                                            callback_data=f'second_confirm_verification_{t_id}'))
    keyboard.row(types.InlineKeyboardButton(text='Вернуться', callback_data=f'back_to_verification_{t_id}'))
    return keyboard


def get_reject_verification_keyboard(t_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Да, хочу отклонить верификацию',
                                            callback_data=f'second_verification_verification_{t_id}'))
    keyboard.row(types.InlineKeyboardButton(text='Вернуться', callback_data=f'back_to_verification_{t_id}'))
    return keyboard


def get_support_chat_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row(types.KeyboardButton(text='Начать чат с оператором'))
    return keyboard


def get_connect_operator_keyboard(connect_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Подключиться',
                                            callback_data=f'connect_{connect_id}'))
    return keyboard


def get_disconnect_operator_keyboard(connect_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton(text='Отключиться',
                                            callback_data=f'disconnect_{connect_id}'))
    return keyboard