import datetime

import psycopg2
from psycopg2.extras import NamedTupleCursor
# import telebot
import redis

import config

def get_admins_type(type):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor(cursor_factory = NamedTupleCursor)
    cursor.execute("SELECT * FROM admins")
    admins = cursor.fetchall()

    connect.commit()
    connect.close()
    exchange_admins = []
    replenish_admins = []
    withdraw_admins = []
    support_admins = []
    verifications_admins = []
    for admin in admins:
        if 'обмен' in admin.permissions:
            exchange_admins.append([admin.t_id])
        if 'вывод' in admin.permissions:
            withdraw_admins.append([admin.t_id])
        if 'пополнение' in admin.permissions:
            replenish_admins.append([admin.t_id])
        if 'техподдержка' in admin.permissions:
            support_admins.append([admin.t_id])
        if 'верификация' in admin.permissions:
            verifications_admins.append([admin.t_id])
    result = {
        'exchange': exchange_admins,
        'replenish': replenish_admins,
        'withdraw': withdraw_admins,
        'support': support_admins,
        'verification': verifications_admins
    }
    return result[type]
def get_all_users():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT t_id FROM users")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    return result



def add_user(t_id, username, invited_by):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT t_id FROM users WHERE t_id=" + str(t_id))
    result = cursor.fetchall()
    if result:
        connect.commit()
        connect.close()
        return False
    else:
        exec_str = "INSERT INTO users" \
                   "(t_id, username, rub_value, btc_value, invited_by, status, bonuses)" \
                   "VALUES" \
                   "(%s, '%s', 0, 0, %s, 0, 0)"
        exec_str = exec_str % (str(t_id), str(username), invited_by)
        cursor.execute(exec_str)
        connect.commit()
        connect.close()
        return True


def plus_bonuses(t_id, plus_bonuses):
    if t_id == None:
        return
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT bonuses FROM users WHERE t_id = {t_id}""")
    bonuses = float(cursor.fetchone()[0]) + plus_bonuses
    cursor.execute(
        f"UPDATE users SET bonuses= {bonuses} WHERE t_id=" + str(t_id))

    connect.commit()
    connect.close()


def get_bonuses(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT bonuses FROM users WHERE t_id=" + str(t_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_invited_by(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT invited_by FROM users WHERE t_id=" + str(t_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def set_fio(t_id, fio):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE users SET fio='" + str(fio) + "' WHERE t_id=" + str(t_id))

    connect.commit()
    connect.close()


def set_birth_date(t_id, date_of_birth):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE users SET birth_date= '{date_of_birth}' WHERE t_id = {t_id}")
    connect.commit()
    connect.close()

def set_address(t_id, address):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE users SET address= '{address}' WHERE t_id = {t_id}")
    connect.commit()
    connect.close()


def set_photo1(t_id, photo):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE users SET photo1 = '{photo}' WHERE t_id = {t_id}")
    connect.commit()
    connect.close()


def set_photo2(t_id, photo):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE users SET photo2 = '{photo}' WHERE t_id = {t_id}")
    connect.commit()
    connect.close()


def get_birth_date(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT birth_date FROM users WHERE t_id=" + str(t_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_address(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT address FROM users WHERE t_id=" + str(t_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_status(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT status FROM users WHERE t_id=" + str(t_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def set_status(t_id, status):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE users SET status = {status} WHERE t_id = {t_id}")
    connect.commit()
    connect.close()


def get_state(user_id):
    r = redis.Redis(connection_pool=config.pool)
    try:
        return str(r.get(config.db_name + '_' + str(user_id)).decode('utf-8'))
    except KeyError:
        return config.State.MAIN_MENU.value
    except AttributeError:
        return config.State.MAIN_MENU.value


def set_state(user_id, value):
    r = redis.Redis(connection_pool=config.pool)
    try:
        r.set(config.db_name + '_' + str(user_id), str(value).encode('utf-8'))
        return True
    except:
        return False
    # r.set(config.db_name + '_' + str(user_id), str(value).encode('utf-8'))


def check_code(code):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT status FROM codes WHERE code='" + str(code) + "'")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 'not found'
    if result[0] == 1:
        return 'active'
    elif result[0] == 2:
        return 'expired'


def add_1000_rub(t_id):
    t_id = str(t_id)
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("UPDATE users SET rub_value=rub_value + 1000::float8::numeric(16,2) WHERE t_id=" + t_id)
    connect.commit()
    connect.close()


def add_1000_btc(t_id):
    t_id = str(t_id)
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("UPDATE users SET btc_value=btc_value + 1000::float8::numeric(24,8) WHERE t_id="
                   + t_id)
    connect.commit()
    connect.close()


def remove_1000_rub(t_id):
    t_id = str(t_id)
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("UPDATE users SET rub_value=rub_value - 1000.0::float8::numeric(16,2) WHERE t_id="
                   + t_id)
    connect.commit()
    connect.close()


def remove_1000_btc(t_id):
    t_id = str(t_id)
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("UPDATE users SET btc_value=btc_value - 1000::float8::numeric(24,8) WHERE t_id="
                   + t_id)
    connect.commit()
    connect.close()


def set_email(t_id, email):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE users SET email='" + str(email) + "' WHERE t_id=" + str(t_id))
    connect.commit()
    connect.close()


def set_phone_number(t_id, phone_number):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE users SET phone_number='" + str(phone_number) + "' WHERE t_id=" + str(t_id))
    connect.commit()
    connect.close()


def get_rub_balance(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT rub_value FROM users WHERE t_id=" + str(t_id) + "")
    result = cursor.fetchone()
    if not result:
        return 0
    connect.commit()
    connect.close()
    return result

def get_count_referals(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT count(*) FROM users WHERE invited_by=" + str(t_id) + "")
    result = cursor.fetchone()
    if not result:
        return 0
    connect.commit()
    connect.close()
    return result


def get_btc_balance(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT btc_value FROM users WHERE t_id=" + str(t_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def get_blocked_user():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT t_id FROM users WHERE block = 'Заблокирован'")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    return result


def delete_user(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "delete from users WHERE t_id=" + str(t_id))
    connect.commit()
    connect.close()


def delete_user_admin(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "delete from admins WHERE t_id=" + str(t_id))
    connect.commit()
    connect.close()


def create_withdraw(t_id, currency, value):
    if currency == 'rub':
        rub_value = value
        btc_value = 0
    else:
        rub_value = 0
        btc_value = value
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO withdraw (t_id, create_dt, currency, btc_value, rub_value, status) "
                   f"VALUES ('{t_id}', NOW(), '{currency}', {btc_value}, {rub_value}, 0) RETURNING id")
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result

def get_admins():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT distinct t_id FROM admins")
    result = cursor.fetchall()
    if not result:
        return []
    connect.commit()
    connect.close()
    return result


def get_user_last_withdraw(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM withdraw WHERE status not in (1, 2) and "
                   "t_id=" + str(t_id) + "order by id desc limit 1")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_withdraw_amaunt_btc(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT btc_value FROM withdraw WHERE id=" + str(withdraw_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def get_withdraw_amaunt_rub(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT rub_value FROM withdraw WHERE id=" + str(withdraw_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def get_fio(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT fio FROM users WHERE t_id=" + str(t_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def set_withdraw_status(withdraw_id, status):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE withdraw SET status='" + str(status) + "' WHERE id=" + str(withdraw_id))
    connect.commit()
    connect.close()


def set_replenish_status(replenish_id, status):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE replenish SET status='" + str(status) + "' WHERE id=" + str(replenish_id))
    connect.commit()
    connect.close()


def create_exchange(t_id, rub_value, btc_value, currency, commission, currency_btc, currency_usd, balance_btc_was,
                    balance_rub_was):
    t_id = str(t_id)
    if currency == 'buy':
        type_exchange = 1
    else:
        type_exchange = 0
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO exchange (t_id, create_dt, type, btc_value, rub_value, status, "
                   "commission,currency_btc, currency_usd, balance_btc_was, balance_rub_was) "
                   "VALUES ('" + t_id + "', NOW(), '" + str(type_exchange) + "', " + str(btc_value) + ", "
                   + str(rub_value) + f", 0, {commission}, {currency_btc}, {currency_usd}, {balance_btc_was},"
                                      f" {balance_rub_was})")
    connect.commit()
    connect.close()


def set_exchange_status(exchange_id, status):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE exchange SET status='" + str(status) + "' WHERE id=" + str(exchange_id))
    connect.commit()
    connect.close()

def set_exchange_end_dt(exchange_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE exchange SET end_dt = NOW() WHERE id=" + str(exchange_id))
    connect.commit()
    connect.close()


def set_exchange_admin_id(exchange_id, admin_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE exchange SET admin_id = {admin_id} WHERE id=" + str(exchange_id))
    connect.commit()
    connect.close()


def add_admin(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM admins WHERE t_id={t_id} ")
    admin = cursor.fetchone()
    if admin is None:
        cursor.execute("INSERT INTO admins (t_id, login_dt) "
                   "VALUES (" + str(t_id) + ", NOW())")
    connect.commit()
    connect.close()


def get_withdraw_user(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT t_id FROM withdraw WHERE id=" + str(withdraw_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]

def get_replenish_user(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT t_id FROM replenish WHERE id=" + str(replenish_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_user_last_exchange(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM exchange WHERE t_id=" + str(t_id) + "order by id desc limit 1")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_withdraw_currency(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT currency FROM withdraw WHERE id=" + str(withdraw_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_replenish_currency(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT currency FROM replenish WHERE id=" + str(replenish_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_withdraw_status(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT status FROM withdraw WHERE id=" + str(withdraw_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_exchange_amaunt_rub(exchange_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT rub_value FROM exchange WHERE id=" + str(exchange_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_replenish_amaunt_rub(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT rub_value FROM replenish WHERE id=" + str(replenish_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_exchange_amaunt_btc(exchange_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT btc_value FROM exchange WHERE id=" + str(exchange_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def user_btc_plus(t_id, btc_value):
    t_id = str(t_id)
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users SET btc_value=btc_value + {str(btc_value)}::float8::numeric(24,8) WHERE t_id="
                   + t_id)
    connect.commit()
    connect.close()


def user_btc_minus(t_id, btc_value):
    t_id = str(t_id)
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users SET btc_value=btc_value - {str(btc_value)}::float8::numeric(24,8) WHERE t_id="
                   + t_id)
    connect.commit()
    connect.close()


def user_rub_minus(t_id, rub_value):
    t_id = str(t_id)
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users SET rub_value=rub_value - {str(rub_value)}::float8::numeric(16,2) WHERE t_id="
                   + t_id)
    connect.commit()
    connect.close()


def user_rub_plus(t_id, rub_value):
    if t_id == None:
        return
    t_id = str(t_id)
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users SET rub_value=rub_value + {str(rub_value)}::float8::numeric(16,2) WHERE t_id="
                   + t_id)
    connect.commit()
    connect.close()


def get_in_out_operations(t_id, offset):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"SELECT create_dt, rub_value, btc_value, currency FROM withdraw WHERE status=2 and "
                   f"t_id={str(t_id)} "
                   f"ORDER BY create_dt desc "
                   f"OFFSET {offset}")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    if not result:
        return None
    return result


def get_in_out_count(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT count(*) FROM withdraw WHERE status=2 and t_id=" + str(t_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_exchange_operations(t_id, offset):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"SELECT create_dt, rub_value, btc_value, type FROM exchange WHERE status=2 and "
                   f"t_id={str(t_id)} "
                   f"ORDER BY create_dt desc "
                   f"OFFSET {offset}")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    if not result:
        return None
    return result


def get_exchange_count(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT count(*) FROM exchange WHERE status=2 and t_id=" + str(t_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def create_replenish(t_id, currency, value, commission, wallet):
    if currency == 'rub':
        rub_value = value
        btc_value = 0
    else:
        rub_value = 0
        btc_value = value
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO replenish (t_id, create_dt, currency, btc_value, rub_value, status, commission, wallet_to) "
                   "VALUES ('" + str(t_id) + "', NOW(), '" + str(currency) + "', " + str(btc_value) + ", "
                   + str(rub_value) + f", 0, {commission}, '{wallet}')")
    connect.commit()
    connect.close()


def get_user_last_replenish(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM replenish WHERE status not in (1, 2) and "
                   "t_id=" + str(t_id) + "order by id desc limit 1")
    result = cursor.fetchone()
    if not result:
        return 0
    connect.commit()
    connect.close()
    return result[0]


def get_replenish_amaunt_btc(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT btc_value FROM replenish WHERE id=" + str(replenish_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def add_replenish_country(replenish_id, country):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE replenish SET country='" + str(country) + "' WHERE id=" + str(replenish_id))
    connect.commit()
    connect.close()


def create_code(t_id, currency, value):
    if currency == 'rub':
        rub_value = value
        btc_value = 0
    else:
        rub_value = 0
        btc_value = value
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO codes (t_id, create_dt, currency, btc_value, rub_value, status) "
                   "VALUES ('" + str(t_id) + "', NOW(), '" + str(currency) + "', " + str(btc_value) + ", "
                   + str(rub_value) + ", 0)")
    connect.commit()
    connect.close()


def get_email(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"SELECT email FROM users WHERE t_id= {t_id}")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_username(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT username FROM users WHERE t_id=" + str(t_id))
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_exchange_status(exchange_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT status FROM exchange WHERE id=" + str(exchange_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_replenish_status(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT status FROM replenish WHERE id = " + str(replenish_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_exchange_user(exchange_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT t_id FROM exchange WHERE id=" + str(exchange_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_exchange_type(exchange_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT type FROM exchange WHERE id=" + str(exchange_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]



def get_user_last_code(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM codes WHERE status=0 and "
                   "t_id=" + str(t_id) + "order by id desc limit 1")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_code_currency(code_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT currency FROM codes WHERE id=" + str(code_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_code_amount_btc(code_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT btc_value FROM codes WHERE id=" + str(code_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_code_amount_rub(code_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT rub_value FROM codes WHERE id=" + str(code_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_code(code_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT code FROM codes WHERE id=" + str(code_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def set_code(code_id, code):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE codes SET code='" + str(code) + "' WHERE id=" + str(code_id))
    connect.commit()
    connect.close()


def set_code_amount_btc(code_id, value):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE codes SET btc_value=" + str(value) + " WHERE id=" + str(code_id))
    connect.commit()
    connect.close()


def set_code_amount_rub(code_id, value):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE codes SET rub_value=" + str(value) + " WHERE id=" + str(code_id))
    connect.commit()
    connect.close()


def get_code_id(text):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM codes WHERE code='" + str(text) + "'")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def set_code_status(code_id, value):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE codes SET status='" + str(value) + "' WHERE id=" + str(code_id))
    connect.commit()
    connect.close()


def set_code_used_by_user(code_id, t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE codes SET used_by_id='" + str(t_id) + "' WHERE id=" + str(code_id))
    connect.commit()
    connect.close()


def set_withdraw_btc_payment(withdraw_id, text):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE withdraw SET btc_payment='" + str(text) + "' WHERE id=" + str(withdraw_id))
    connect.commit()
    connect.close()


def set_withdraw_rub_payment(withdraw_id, text, bank):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE withdraw SET rub_payment='" + str(text) + "' WHERE id=" + str(withdraw_id))
    cursor.execute(
        "UPDATE withdraw SET bank='" + str(bank) + "' WHERE id=" + str(withdraw_id))
    connect.commit()
    connect.close()


def get_withdraw_rub_payment(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT rub_payment FROM withdraw WHERE id=" + str(withdraw_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_withdraw_btc_payment(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("SELECT btc_payment FROM withdraw WHERE id=" + str(withdraw_id) + "")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_commission_replenish():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("""SELECT replenish FROM commission WHERE id = 1""")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def set_commission_replenish(commission):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE commission SET replenish={commission} WHERE id = 1")
    connect.commit()
    connect.close()


def get_commission_exchange():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("""SELECT exchange FROM commission WHERE id = 1""")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def set_commission_exchange(commission):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE commission SET exchange = {commission} WHERE id = 1")
    connect.commit()
    connect.close()


def get_commission_withdraw():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    #cursor.execute("""SELECT withdraw FROM commission WHERE id = 1""")
    #result = cursor.fetchone()
    connect.commit()
    connect.close()
    result = 1
    if not result:
        return 0
    return result[0]


def get_commission_withdraw_sber():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("""SELECT withdraw_sber FROM commission WHERE id = 1""")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_commission_withdraw_tink():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute("""SELECT withdraw_tink FROM commission WHERE id = 1""")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def set_commission_withdraw(commission):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE commission SET withdraw = {commission} WHERE id = 1")
    connect.commit()
    connect.close()


def create_support(t_id, text, message_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""INSERT INTO support (t_id, time, text, status, message_id) VALUES 
                       ({t_id}, NOW(), '{text}', 0, {message_id})""")
    connect.commit()
    connect.close()


def get_support_message_id(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT message_id FROM support WHERE t_id = {t_id}""")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def get_support_id(t_id, message_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT id FROM support WHERE t_id = {t_id} AND message_id = {message_id}""")
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def update_support_text(t_id, message_id, text):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""UPDATE support SET text = '{text}' WHERE t_id = {t_id} AND message_id = {message_id}""")
    connect.commit()
    connect.close()

def get_support_user_id(id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT t_id FROM support WHERE id = {id}""")
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result

def get_support_status(id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT status FROM support WHERE id = {id}""")
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result

def update_support_status(id, status):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""UPDATE support SET status = {status} WHERE id = {id}""")
    connect.commit()
    connect.close()

def update_support_answer(id, answer):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""UPDATE support SET answer = '{answer}' WHERE id = {id}""")
    connect.commit()
    connect.close()


def set_support_admin(id, admin_t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""UPDATE support SET admin_t_id = {admin_t_id} WHERE id = {id}""")
    connect.commit()
    connect.close()


def get_support_text(id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT text FROM support WHERE id = {id}""")
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def add_profit(type, profit, currency):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""INSERT INTO profit (id, time, type, profit, currency)
                       VALUES 
                       (DEFAULT ,NOW() , '{type}', {profit}, '{currency}')""")
    connect.commit()
    connect.close()

def get_all_exchange():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor(cursor_factory=NamedTupleCursor)
    cursor.execute(f"""SELECT * FROM exchange""")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def set_replenish_wallet_from(replenish_id, wallet_from):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE replenish SET wallet_from='" + str(wallet_from) + "' WHERE id=" + str(replenish_id))
    connect.commit()
    connect.close()


def set_replenish_btc_balance(replenish_id, t_id):
    btc_balance = get_btc_balance(t_id)[0]
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE replenish SET btc_balance= {btc_balance} WHERE id=" + str(replenish_id))
    connect.commit()
    connect.close()


def set_replenish_rub_balance(replenish_id, t_id):
    rub_balance = get_rub_balance(t_id)[0]
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE replenish SET rub_balance= {rub_balance} WHERE id=" + str(replenish_id))
    connect.commit()
    connect.close()


def get_btc_wallet():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT wallet FROM wallets WHERE currency = 'BTC'""")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def add_wallet():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""INSERT INTO wallets (id, wallet) VALUES (DEFAULT ,'1')""")
    result = cursor.fetchall()
    connect.commit()
    connect.close()


def set_replenish_end_dt(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE replenish SET end_dt = NOW() WHERE id=" + str(replenish_id))
    connect.commit()
    connect.close()


def set_replenish_answer(replenish_id, answer):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE replenish SET answer = '{answer}' WHERE id=" + str(replenish_id))
    connect.commit()
    connect.close()

def get_replenish_commission(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT commission FROM replenish WHERE id = {replenish_id}""")
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def set_replenish_txid(replenish_id, txid):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE replenish SET Txid = '{txid}' WHERE id=" + str(replenish_id))
    connect.commit()
    connect.close()


def get_replenish_answer(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT answer FROM replenish WHERE id = {replenish_id}""")
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def get_all_replenish():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT * FROM replenish""")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def set_withdraw_answer(withdraw_id, answer):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE withdraw SET answer = '{answer}' WHERE id=" + str(withdraw_id))
    connect.commit()
    connect.close()


def get_withdraw_answer(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT answer FROM withdraw WHERE id = {withdraw_id}""")
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def set_withdraw_end_dt(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE withdraw SET end_dt = NOW() WHERE id=" + str(withdraw_id))
    connect.commit()
    connect.close()


def set_withdraw_commission(withdraw_id, commission):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE withdraw SET commission = {commission} WHERE id=" + str(withdraw_id))
    connect.commit()
    connect.close()


def get_withdraw_commission(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT commission FROM withdraw WHERE id = {withdraw_id}""")
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def set_withdraw_btc_balance(withdraw_id, t_id):
    btc_balance = get_btc_balance(t_id)[0]
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE withdraw SET btc_balance= {btc_balance} WHERE id=" + str(withdraw_id))
    connect.commit()
    connect.close()


def set_withdraw_rub_balance(withdraw_id, t_id):
    rub_balance = get_rub_balance(t_id)[0]
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE withdraw SET rub_balance= {rub_balance} WHERE id=" + str(withdraw_id))
    connect.commit()
    connect.close()


def set_withdraw_txid(withdraw_id, txid):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE withdraw SET txid = {txid} WHERE id=" + str(withdraw_id))
    connect.commit()
    connect.close()


def get_all_withdraw():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT * FROM withdraw""")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result



def set_code_end_dt(code_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE codes SET end_dt = NOW() WHERE id=" + str(code_id))
    connect.commit()
    connect.close()


def get_all_support():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor(cursor_factory=NamedTupleCursor)
    cursor.execute(f"""SELECT * FROM support""")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def get_all_codes():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor(cursor_factory=NamedTupleCursor)
    cursor.execute(f"""SELECT * FROM codes""")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def create_chat(dt, t_id, type, text):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""INSERT INTO chat (dt, t_id, type, text)
                      VALUES
                      ('{dt}', {t_id}, '{type}', '{text}')""")
    connect.commit()
    connect.close()


def get_all_chat():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor(cursor_factory=NamedTupleCursor)
    cursor.execute(f"""SELECT * FROM chat""")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result


def create_connection(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""INSERT INTO connections (t_id, status) 
                      VALUES
                      ({t_id}, 0)""")
    cursor.execute(f"""SELECT id FROM connections""")
    ids = cursor.fetchall()
    connect.commit()
    connect.close()
    return max(ids)[0]


def set_admin_id_connections(admin_id, connect_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE connections SET admin_id = {admin_id} WHERE id = {connect_id}")
    cursor.execute(
        f"UPDATE connections SET connect_time = NOW() WHERE id = {connect_id}")
    cursor.execute(
        f"UPDATE connections SET status = 1 WHERE id = {connect_id}")
    connect.commit()
    connect.close()


def get_connect_status(id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT status FROM connections WHERE id = {id}""")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_connect_admins(id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT status FROM connections WHERE id = {id}""")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def set_admin_id_disconnections(connect_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE connections SET disconnect_time = NOW() WHERE id = {connect_id}")
    cursor.execute(
        f"UPDATE connections SET status = 2 WHERE id = {connect_id}")
    connect.commit()
    connect.close()


def get_connect_t_id(connect_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT t_id FROM connections WHERE id = {connect_id}""")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def get_connect_admin_id(connect_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT admin_id FROM connections WHERE id = {connect_id}""")
    result = cursor.fetchone()
    connect.commit()
    connect.close()
    if not result:
        return 0
    return result[0]


def add_support_message(t_id, admin_id, message, from_who, connect_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(f"""INSERT INTO support (time, t_id, admin_id, message, from_who, connect_id) 
                      VALUES
                      (NOW(), {t_id}, {admin_id}, '{message}', '{from_who}', {connect_id})""")
    connect.commit()
    connect.close()


def set_balance_after_exchange(exchange_id, t_id):
    btc_balance = get_btc_balance(t_id)[0]
    rub_balance = get_rub_balance(t_id)[0]
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE exchange SET balance_rub = {rub_balance} WHERE id = {exchange_id}")
    cursor.execute(
        f"UPDATE exchange SET balance_btc = {btc_balance} WHERE id = {exchange_id}")
    connect.commit()
    connect.close()


def set_balance_was_creator_code(code_id, t_id):
    btc_balance = get_btc_balance(t_id)[0]
    rub_balance = get_rub_balance(t_id)[0]
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE codes SET rub_balance_was_creator = {rub_balance} WHERE id = {code_id}")
    cursor.execute(
        f"UPDATE codes SET btc_balance_was_creator = {btc_balance} WHERE id = {code_id}")
    connect.commit()
    connect.close()


def set_balance_creator_code(code_id, t_id):
    btc_balance = get_btc_balance(t_id)[0]
    rub_balance = get_rub_balance(t_id)[0]
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE codes SET rub_balance_creator = {rub_balance} WHERE id = {code_id}")
    cursor.execute(
        f"UPDATE codes SET btc_balance_creator = {btc_balance} WHERE id = {code_id}")
    connect.commit()
    connect.close()


def set_balance_was_activator_code(code_id, t_id):
    btc_balance = get_btc_balance(t_id)[0]
    rub_balance = get_rub_balance(t_id)[0]
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE codes SET rub_balance_was_activator = {rub_balance} WHERE id = {code_id}")
    cursor.execute(
        f"UPDATE codes SET btc_balance_was_activator = {btc_balance} WHERE id = {code_id}")
    connect.commit()
    connect.close()


def set_balance_activator_code(code_id, t_id):
    btc_balance = get_btc_balance(t_id)[0]
    rub_balance = get_rub_balance(t_id)[0]
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"UPDATE codes SET rub_balance_activator = {rub_balance} WHERE id = {code_id}")
    cursor.execute(
        f"UPDATE codes SET btc_balance_activator = {btc_balance} WHERE id = {code_id}")
    connect.commit()
    connect.close()

def get_code_create_dt(code_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""SELECT create_dt FROM codes WHERE id = {code_id}"""
    )
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result

def add_transaction_code(t_id, dt, got, balance_was, balance, status):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""INSERT INTO transactions (t_id, dt, got, balance_was, balance, type, info, status, end_dt) 
            VALUES
            ({t_id}, '{dt}', '{got}', '{balance_was}', '{balance}', 'ВВОД', 'КОД КЛИЕНТАЛА BTC', '{status}', NOW())"""
    )
    connect.commit()
    connect.close()


def add_transaction_replenish(t_id, dt, got, balance_was, balance, commission, status, answer):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""INSERT INTO transactions (t_id, dt, got, balance_was, balance, type, commission, status, end_dt, answer) 
            VALUES
            ({t_id}, '{dt}', '{got}', '{balance_was}', '{balance}', 'ВВОД', '{commission}', '{status}', NOW(),
             '{answer}') RETURNING id"""
    )
    id = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return id


def get_replenish_create_dt(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""SELECT create_dt FROM replenish WHERE id = {replenish_id}"""
    )
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result


def set_replenish_txid_transaction(transaction_id, txid):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""UPDATE transactions SET txid = '{txid}' WHERE id = {transaction_id}"""
    )
    connect.commit()
    connect.close()


def add_transaction_withdraw(t_id, dt, sent, balance_was, balance, commission, status, answer, to_address):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""INSERT INTO transactions (t_id, dt, sent, balance_was, balance, type, commission, status, end_dt, answer,
                                      to_address) 
            VALUES
            ({t_id}, '{dt}', '{sent}', '{balance_was}', '{balance}', 'ВЫВОД', '{commission}', '{status}', NOW(),
             '{answer}', '{to_address}')"""
    )
    connect.commit()
    connect.close()


def get_withdraw_create_dt(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""SELECT create_dt FROM withdraw WHERE id = {withdraw_id}"""
    )
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result


def get_withdraw_btc_balance_was(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""SELECT btc_balance_was FROM withdraw WHERE id = {withdraw_id}"""
    )
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result


def get_withdraw_rub_balance_was(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""SELECT rub_balance_was FROM withdraw WHERE id = {withdraw_id}"""
    )
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result


def set_withdraw_btc_balance_was(withdraw_id, btc_balance_was):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""UPDATE withdraw SET btc_balance_was = {btc_balance_was} WHERE id = {withdraw_id}"""
    )
    connect.commit()
    connect.close()


def set_withdraw_rub_balance_was(withdraw_id, rub_balance_was):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""UPDATE withdraw SET rub_balance_was = {rub_balance_was} WHERE id = {withdraw_id}"""
    )
    connect.commit()
    connect.close()


def set_exchange_answer(exchange_id, answer):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""UPDATE exchange SET answer = '{answer}' WHERE id = {exchange_id}"""
    )
    connect.commit()
    connect.close()


def get_replenish_btc_balance_was(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""SELECT btc_balance_was FROM replenish WHERE id = {replenish_id}"""
    )
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result


def get_replenish_rub_balance_was(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""SELECT rub_balance_was FROM replenish WHERE id = {replenish_id}"""
    )
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result


def get_replenish_btc_balance(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""SELECT btc_balance FROM replenish WHERE id = {replenish_id}"""
    )
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result


def get_replenish_rub_balance(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""SELECT rub_balance FROM replenish WHERE id = {replenish_id}"""
    )
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result


def set_replenish_btc_balance_was(replenish_id, btc_balance_was):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""UPDATE replenish SET btc_balance_was = {btc_balance_was} WHERE id = {replenish_id}"""
    )
    connect.commit()
    connect.close()


def set_replenish_rub_balance_was(replenish_id, rub_balance_was):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""UPDATE replenish SET rub_balance_was = {rub_balance_was} WHERE id = {replenish_id}"""
    )
    connect.commit()
    connect.close()


def set_replenish_to_address_transaction(transaction_id, to_address):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""UPDATE transactions SET to_address = '{to_address}' WHERE id = {transaction_id}"""
    )
    connect.commit()
    connect.close()


def get_replenish_wallet_to(replenish_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""SELECT wallet_to FROM replenish WHERE id = {replenish_id}"""
    )
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result


def get_all_transactions():
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor(cursor_factory = NamedTupleCursor)
    cursor.execute(
        f"""SELECT * FROM transactions"""
    )
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    return result


def add_email_code(t_id, code, email):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""INSERT INTO email_codes (t_id, create_dt, status, code, email)
            VALUES
            ({t_id}, NOW(), 'Создан', '{code}', '{email}')""")
    connect.commit()
    connect.close()


def get_active_email_code(t_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor(cursor_factory=NamedTupleCursor)
    cursor.execute(
        f"""SELECT * FROM email_codes WHERE t_id = {t_id}""")
    results = cursor.fetchall()
    connect.commit()
    connect.close()
    ids = []
    for result in results:
        if result.status == 'Создан':
           ids.append(result.id)
    return ids



def set_email_code_status(id, status):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor(cursor_factory=NamedTupleCursor)
    cursor.execute(
        f"""UPDATE email_codes SET status = '{status}' WHERE id = {id}""")
    connect.commit()
    connect.close()


def set_email_end_dt(id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor(cursor_factory=NamedTupleCursor)
    cursor.execute(
        f"""UPDATE email_codes SET end_dt = NOW() WHERE id = {id}""")
    connect.commit()
    connect.close()


def get_email_code(code):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor(cursor_factory=NamedTupleCursor)
    cursor.execute(
        f"""SELECT * FROM email_codes WHERE code = '{code}'""")
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    return result


def add_email_history(t_id, email):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor(cursor_factory=NamedTupleCursor)
    cursor.execute(
        f"""SELECT history_email FROM users WHERE t_id = '{t_id}'""")
    history = cursor.fetchone()[0] + f'{email}=>'
    cursor.execute(
        f"""UPDATE users SET history_email = '{history}' WHERE t_id = {t_id}"""
    )
    connect.commit()
    connect.close()


def get_withdraw_bank(withdraw_id):
    connect = psycopg2.connect(
        "dbname='" + config.db_name + "' user='" + config.db_user + "' password='"
        + config.db_pass + "' host='" + config.db_host + "'")
    connect.set_client_encoding('UTF8')
    cursor = connect.cursor()
    cursor.execute(
        f"""SELECT bank FROM withdraw WHERE id = {withdraw_id}""")
    result = cursor.fetchone()[0]
    connect.commit()
    connect.close()
    return result
