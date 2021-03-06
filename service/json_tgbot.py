import logging
from service.serializers import WaterfallModel
from jinja2 import Environment, PackageLoader, select_autoescape

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

env = Environment(
    loader=PackageLoader("service"),
    autoescape=select_autoescape()
)

message = env.get_template("message.html")

GREET_TEPMPLATE = """
Привет!
Я помогу тебе найти водопад :)
Опиши водопад, который хочешь найти!
А если знаешь название водопада, отправь мне его в формате:
/name "название водопада"
"""


def greet():
    msg = GREET_TEPMPLATE
    return msg


def convert_to_messages(response: dict) -> list[str]:
    tm_messages = []
    limit = 10
    for result_num, waterfall_str in enumerate(response, start=1):
        waterfall = WaterfallModel(**waterfall_str)
        msg = message.render(
            title=waterfall.title,
            country=waterfall.country,
            region=waterfall.region,
            RF_subject=waterfall.RF_subject,
            river=waterfall.river,
            height=waterfall.height,
            width=waterfall.width,
            url=waterfall.url,
            )
        # msg = MESSAGE_TEMPLATE.(
        #     waterfall.title,
        #     waterfall.country,
        #     waterfall.region,
        #     waterfall.RF_subject,
        #     waterfall.river,
        #     waterfall.height,
        #     waterfall.width,
        #     waterfall.url
        # )
        tm_messages.append(msg)
        if result_num == limit:
            break
    return tm_messages

