import logging
import redis
import telebot

from telegram_bot import buttons
from telegram_bot import config
from telegram_bot import dbworker

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

log_file = 'support.log'
f = open(log_file, 'a')
f.close()
file_log = logging.FileHandler(log_file)
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out),
                    format=u'%(filename)s [LINE:%(lineno)s; FUNC:%(funcName)s] #%(levelname)2s  [%(asctime)s]  %('
                           u'message)s',
                    level=logging.INFO)


@bot_support.message_handler(commands=['start'])
def handle_start(message):
    t_id = message.chat.id
    r = redis.Redis(connection_pool=config.pool)
    r.set(f'connect_user_status_{t_id}', '0')
    r.set(f'connect_admin_status_{t_id}', '0')
    bot_support.send_message(t_id, 'Если хотите начать чат с оператором - нажмите кнопку ниже',
                             reply_markup=buttons.get_support_chat_keyboard())


@bot_support.message_handler(func=lambda m: m.text == 'Начать чат с оператором' and
                             redis.Redis(connection_pool=config.pool).get(f'connect_user_status_{m.chat.id}')[:8]
                                            != b'connect_')
def message(message):
    t_id = message.chat.id
    users = dbworker.get_all_users()
    bot_username = bot.get_me().username
    try:
        bot.send_chat_action(chat_id=t_id, action='typing')
    except:
        if (t_id,) in users:
            bot_support.send_message(t_id, f'Чтобы задать вопрос оператору напишите @{bot_username}')
        else:
            bot_support.send_message(t_id, f'Чтобы задать вопрос оператору разблокируйте @{bot_username}')
        return
    r = redis.Redis(connection_pool=config.pool)
    status = r.get(f'connect_user_status_{t_id}')
    if status == b'created' or status == b'connect':
        bot_support.send_message(message.chat.id, 'Запрос уже отправлен')
        return
    r.set(f'connect_user_status_{t_id}', 'created')
    admins = dbworker.get_admins()
    connect_id = dbworker.create_connection(t_id)
    for admin in admins:
        try:
            admin_t_id = admin[0]
            bot_admin.send_message(admin_t_id, f'Запрос на подключение оператора\n'
                                               f'ID подключения: {connect_id}\n'
                                               f'ID пользователя: {message.chat.id}',
                                   reply_markup=buttons.get_connect_operator_keyboard(connect_id))
        except telebot.apihelper.ApiException as e:
            logging.exception(e)
            continue
    bot_support.send_message(t_id, f'Запрос на подключение отправлен администраторам, ожидайте')


@bot_support.message_handler(func=
    lambda m: redis.Redis(connection_pool=config.pool).get(f'connect_admin_status_{m.chat.id}')[:8] == b'connect_')
def handle_start(message):
    r = redis.Redis(connection_pool=config.pool)
    connect_id = int(r.get(f'connect_admin_status_{message.chat.id}')[8:])
    admin_id = message.chat.id
    t_id = dbworker.get_connect_t_id(connect_id)
    bot_support.send_message(t_id, message.text)
    dbworker.add_support_message(t_id, admin_id, message.text, 'Админ', connect_id)


@bot_support.message_handler(func=
    lambda m: redis.Redis(connection_pool=config.pool).get(f'connect_user_status_{m.chat.id}')[:8] == b'connect_')
def handle_start(message):
    r = redis.Redis(connection_pool=config.pool)
    connect_id = int(r.get(f'connect_user_status_{message.chat.id}')[8:])
    admin_id = dbworker.get_connect_admin_id(connect_id)
    t_id = dbworker.get_connect_t_id(connect_id)
    bot_support.send_message(admin_id, message.text)
    dbworker.add_support_message(t_id, admin_id, message.text, 'Пользователь', connect_id)

#  Polling
# bot.delete_webhook()
bot_support.polling()

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
            bot_support.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


bot_support.remove_webhook()

# time.sleep(7)  # Pause

bot_support.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
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
