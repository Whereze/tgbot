import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import httpx
import service.config


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
    update.message.reply_text(
        'Привет! Я помогу тебе найти водопад!\n \
        Если знаешь название водопада, отправь мне его в формате:\n \
        /name "название"\n \
        Или же давай попробуем найти водопад по описанию:\n \
        /description "то, что ты знаешь о водопаде"'
        )


def get_waterfalls_by_name(update, context):
    text = update.message.text
    text = text.replace('/name ', '')
    logging.info(text)
    title = text
    detail = None
    waterfall = httpx.get(f'http://127.0.0.1:5000/api/v1/waterfalls?detail={detail}&title={title}')
    waterfalls = waterfall.json()
    if waterfalls:
        for waterfall in waterfalls:
            update.message.reply_text(
                str(
                    f'Название: {waterfall.get("title", "")}\n \
Страна: {waterfall.get("country", "")}\n \
Регион: {waterfall.get("region", "")}\n \
Субъект РФ: {waterfall.get("RF_subject", "")}\n \
Река: {waterfall.get("river", "")}\n \
Высота: {waterfall.get("height", "")}\n \
Ширина: {waterfall.get("width", "")}\n \
{waterfall["url"]}'
                ))

    else:
        update.message.reply_text(str('Такого водопада я не знаю :('))


def get_waterfalls_by_desc(update, context):
    text = update.message.text
    text = text.replace('/description ', '')
    logging.info(text)
    title = None
    detail = text
    waterfall = httpx.get(f'http://127.0.0.1:5000/api/v1/waterfalls?detail={detail}&title={title}')
    waterfalls = waterfall.json()
    if waterfalls:
        for waterfall in waterfalls:
            update.message.reply_text(
                str(
                    f'Название: {waterfall.get("title", "")}\n \
Страна: {waterfall.get("country", "")}\n \
Регион: {waterfall.get("region", "")}\n \
Субъект РФ: {waterfall.get("RF_subject", "")}\n \
Река: {waterfall.get("river", "")}\n \
Высота: {waterfall.get("height", "")}\n \
Ширина: {waterfall.get("width", "")}\n \
{waterfall["url"]}'
                ))
    else:
        update.message.reply_text(str('Попробуй немного изменить описание :)'))


def default_response(update, context):
    update.message.reply_text(
        'Привет! Я помогу тебе найти водопад!\n \
        Если знаешь название водопада, отправь мне его в формате:\n \
        /name "название"\n \
        Или же давай попробуем найти водопад по описанию:\n \
        /description "то, что ты знаешь о водопаде"'
        )


def main():
    mybot = Updater(
                    service.config.TOKEN,
                    request_kwargs=PROXY,
                    use_context=True
                    )
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("name", get_waterfalls_by_name))
    dp.add_handler(CommandHandler("description", get_waterfalls_by_desc))
    dp.add_handler(MessageHandler(Filters.text, default_response))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
