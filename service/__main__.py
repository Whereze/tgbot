import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import service.config
from service.client import BackendClient as Client
from service.json_tgbot import convert_to_messages, greet
from telegram import ParseMode

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
    update.message.reply_text(greet())


def search_by_name(update, context):
    if context.args:
        client = Client()
        text = update.message.text
        title = text.replace('/name ', '')
        detail = None
        response = client.search(detail, title)
        tm_messages = convert_to_messages(response)
        if not tm_messages:
            update.message.reply_text('Такого водопада я не знаю!')
        for msg in tm_messages:
            update.message.reply_text(text=msg, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(
            'Напиши мне какой водопад ты хочешь найти!',
        )


def search_by_desc(update, context):

    client = Client()
    detail = update.message.text
    title = update.message.text
    response = client.search(detail, title)
    tm_messages = convert_to_messages(response)
    if not tm_messages:
        update.message.reply_text('Такого водопада я не знаю!')
    for msg in tm_messages:
        update.message.reply_text(text=msg, parse_mode=ParseMode.HTML)


def main():
    mybot = Updater(
                    service.config.TOKEN,
                    request_kwargs=PROXY,
                    use_context=True
                    )
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("name", search_by_name))
    dp.add_handler(MessageHandler(Filters.text, search_by_desc))

    mybot.start_polling(timeout=600)
    mybot.idle()


if __name__ == "__main__":
    main()
