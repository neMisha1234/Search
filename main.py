import logging
from data import db_session
from data.favorites import Favorite
from geocoder_functions import find_with_city
from telegram.ext import Application, CommandHandler, filters, CallbackQueryHandler, ConversationHandler, MessageHandler, CallbackContext
from button_functions import back_to_college, college_choise
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

dct = {}
CURRENT = None


def speed(c):
    pass


BOT_TOKEN = "6996213303:AAEG96smFA4Nk0nobcrcY1FR_pAgjSLW-S8"
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def to_str(dct):
    res = ''
    for el in dct:
        res += f"{el}:{dct[el]};"
    return res[:-1]


def to_dict(st):
    res = {}
    for el in st.split(";"):
        res[el.split(":")[0]] = el.split(":")[1]
    return res


db_session.global_init("db/college.db")
db_sess = db_session.create_session()


async def start(update, context):
    await update.message.reply_text(
        "Добро пожаловать в бота, для поиска идеального ВУЗа, бот на стадии разработки. \n Текущая разработка: нахождение вузов в конкретном городе")
    await update.message.reply_text("Привет, введи команду '/find (название города)'")


async def stop(update, context):
    return ConversationHandler.END


async def get_college(update, context):
    await update.message.reply_text("Введите название города:")
    return "find_by_city"


async def find_by_city(update, context):
    global dct
    city = update.message.text
    markup = [[InlineKeyboardButton('ВЕРНУТЬСЯ В МЕНЮ', callback_data=f"exit")]]
    for college in find_with_city(city):
        markup.append([InlineKeyboardButton(college['name'], callback_data="College-" + to_str(college))])
    await update.message.reply_text("Выберите ВУЗ:", reply_markup=InlineKeyboardMarkup(markup))


async def main_menu(update, context):
    markup = [[InlineKeyboardButton("Найти ВУЗ в городе", callback_data="get_college")],
              [InlineKeyboardButton('Найти ВУЗы рядом со мной', callback_data='find_by_geo')],
              [InlineKeyboardButton('Открыть избранные ВУЗы', callback_data='open_favorite')]]
    await update.message.reply_text("Что бы вы хотели сделать?", reply_markup=InlineKeyboardMarkup(markup))
    print(context.user_data)
    if context.user_data.get("get_college", False):
        return 'get_college'


async def btn(update, context: CallbackContext):
    global CURRENT
    query = update.callback_query
    await query.answer()
    if query.data.startswith("get_college"):
        context.user_data['get_college'] = True
    if query.data.startswith("College"):
        dct = to_dict(query.data.split('-')[1])
        await college_choise(query, dct)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    c1 = CommandHandler('start', main_menu)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_menu)],
        states={
            "get_college": [MessageHandler(filters.TEXT & ~filters.COMMAND, get_college)],
            "find_by_city": [MessageHandler(filters.TEXT & ~filters.COMMAND, find_by_city)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler)
    application.add_handler(c1)
    application.add_handler(CallbackQueryHandler(btn))
    application.run_polling()


if __name__ == '__main__':
    main()
