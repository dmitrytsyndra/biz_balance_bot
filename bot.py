import telebot
import requests
from guest_request import iiko_token
import logging
import logging.config
import re
from config import token

logging.basicConfig(filename="biz.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logging.info("Running Urban Planning")

logger = logging.getLogger('urbanGUI')


user_dict = {'id' : ''}

headers = {
    "Authorization": f'Bearer {iiko_token}',
}

def guest_id(phone):
    params2 = {
            "phone": phone,
            "type": "phone",
            "organizationId": "64f45e6f-f38a-4d58-8c62-cc7fa3cb499a"
        }
    guest_resp = requests.post('https://api-ru.iiko.services/api/1/loyalty/iiko/customer/info', headers=headers, json=params2)

    ja = guest_resp.json()
    user_dict['id'] = ja["id"]

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start','new'])

def hello(message):
    try:
        msg = bot.send_message(message.chat.id, 'Введите номер в формате 79999999999', parse_mode='Markdown')
        bot.register_next_step_handler(msg, phone_id)
    except:
        logger.exception("Exception in hello-handler")

@bot.message_handler(content_types=["text"])

def phone_id(message):
    try:
        phone = f'{message.text}'
        logger.info(f'Введен номер {phone}')
        guest_id(phone)
        msg = bot.send_message(message.chat.id, 'Введите сумму баланса', parse_mode='Markdown')
        bot.register_next_step_handler(msg, sum_step)
    except:
        logger.exception("Exception in phone_id-handler")

def sum_step(message):
    try:
        sum = message.text
        logger.info(f'Начислено {sum} рублей')
        bot.send_message(message.chat.id, 'Баланс зачислен. Для нового пополнения нажмите /start', parse_mode='Markdown')
        
        params3 = {
            "customerId": user_dict["id"],
            "walletId": "ccfb9e91-4eb4-11e8-80cd-d8d385655247", #const
            "sum": sum,
            "comment": "Начислено через бота",
            "organizationId": "64f45e6f-f38a-4d58-8c62-cc7fa3cb499a"  #const  
        }

        requests.post('https://api-ru.iiko.services/api/1/loyalty/iiko/customer/wallet/topup', headers=headers, json=params3)
    except:
        logger.exception("Exception in balance-handler")

bot.infinity_polling()