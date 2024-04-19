import logging
from data import db_session
from data.favorites import Favorite
from geocoder_functions import find_with_city
from telegram.ext import Application, CommandHandler, filters, CallbackQueryHandler
from button_functions import college_choise, back_to_college
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

dct = {}
CURRENT, CUR_MESSAGE = None, ''
flag1, flag2, menu, get_text = False, False, True, False
BOT_TOKEN = "6996213303:AAEG96smFA4Nk0nobcrcY1FR_pAgjSLW-S8"
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

db_session.global_init("db/college.db")
db_sess = db_session.create_session()


async def start(update, context):
    await update.message.reply_text(
        "Добро пожаловать в бота, для поиска идеального ВУЗа, бот на стадии разработки. \n Текущая разработка: нахождение вузов в конкретном городе")
    await update.message.reply_text("Привет, введи команду '/find (название города)'")


async def find_by_city(update, context):
    global dct
    global flag1
    flag1 = True
    city = update.message.text
    markup = [[InlineKeyboardButton('ВЕРНУТЬСЯ В МЕНЮ', callback_data=f"exit")]]
    cnt = 0
    for college in find_with_city(city):
        dct[cnt] = college
        markup.append([InlineKeyboardButton(college['name'], callback_data=f"{cnt}")])
        cnt += 1
    await update.message.reply_text("Выберите ВУЗ:", reply_markup=InlineKeyboardMarkup(markup))


async def main_menu(update, context):
    global menu
    markup = [[InlineKeyboardButton("Найти ВУЗ в городе", callback_data="find_by_city")],
              [InlineKeyboardButton('Найти ВУЗы рядом со мной', callback_data='find_by_geo')],
              [InlineKeyboardButton('Открыть избранные ВУЗы', callback_data='open_favorite')]]
    menu = True
    await update.message.reply_text("Что бы вы хотели сделать?", reply_markup=InlineKeyboardMarkup(markup))


async def btn(update, context):
    global flag1
    global flag2
    global CURRENT
    query = update.callback_query

    await query.answer()

    if menu:
        if query.data == "find_by_city":
            pass

    elif flag1:
        await college_choise(query, dct)
        flag1, flag2 = False, True
    elif flag2:
        if not await back_to_college(query, dct):
            flag1, flag2 = True, False

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    c1 = CommandHandler('start', main_menu)
    application.add_handler(c1)
    application.add_handler(CommandHandler('find', find_by_city))
    application.add_handler(CallbackQueryHandler(btn))
    application.run_polling()


if __name__ == '__main__':
    main()
