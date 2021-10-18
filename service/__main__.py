import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import httpx
from flask import Flask, jsonify, request, abort
import service.config

app = Flask(__name__)
client = app.test_client()

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn',
        'password': 'python'
    }
}

def greet_user(update, context):
    text = 'Вызван /start'
    update.message.reply_text('Привет! Я помогу тебе найти водопад!\nОтправь мне водопад в формате:\n/waterfall твой водопад')

# def default_response(update, context):
#     user_text = update.message.text
#     text = f'Привет! Я помогу тебе найти водопад!\nОтправь мне водопад в формате:\n/waterfall твой водопад'
#     update.message.reply_text(text)

def get_waterfalls(update, context):
    text = update.message.text
    text = text.replace('/waterfall','')
    logging.info(text)
    waterfall = httpx.get('http://127.0.0.1:5000/api/v1/waterfalls/')
    waterfalls = waterfall.json()
    update.message.reply_text(str(waterfalls))


def main():
    mybot = Updater(service.config.TOKEN, request_kwargs=PROXY, use_context=True)
    dp = mybot.dispatcher    
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("waterfall", get_waterfalls))
    # dp.add_handler(CommandHandler(Filters.text, default_response))

    mybot.start_polling()
    mybot.idle()
if __name__ == "__main__":
    main()
