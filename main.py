import logging
import time

from db_functions import add_college_to_fav, get_favorite
from geocoder_functions import find_with_city, find_with_coords
from telegram.ext import Application, CommandHandler, filters, CallbackQueryHandler, ConversationHandler, \
    MessageHandler, CallbackContext, ContextTypes
from button_functions import back_to_college, college_choise, back_to_favorite
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Update, KeyboardButton

CURRENT = None

BOT_TOKEN = "6996213303:AAEG96smFA4Nk0nobcrcY1FR_pAgjSLW-S8"
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

markup = [["Найти ВУЗ в городе"],
          ['Найти ВУЗы рядом со мной'],
          ['Открыть избранные ВУЗы']]


async def open_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    favor = get_favorite(update.message.from_user.id)
    inlinemarkup = [[InlineKeyboardButton('ВЕРНУТЬСЯ В МЕНЮ', callback_data=f"Fav-exit")]]
    context.user_data['favorite'] = {}
    cnt = 0
    for fav in favor:
        cnt += 1
        dct = {}
        dct['name'] = fav.name
        dct['url'] = fav.site
        dct['Phones'] = fav.phone
        context.user_data['favorite'][cnt] = dct
        inlinemarkup.append([InlineKeyboardButton(fav.name, callback_data=f'Fav-{cnt}')])

    await update.message.reply_text("Выберите ВУЗ:", reply_markup=InlineKeyboardMarkup(inlinemarkup))
    return 'wait'


async def get_user_location(update: Update, context):
    mp = [[KeyboardButton('Да', request_location=True), KeyboardButton('Нет')]]
    await update.message.reply_text("Отправить свою геолокацию?", reply_markup=ReplyKeyboardMarkup(mp, one_time_keyboard=True))
    return "locate"


async def find_by_geo(update: Update, context):
    location = (update.message.location.to_dict())
    location = f"{location['longitude']}, {location['latitude']}"
    markup = [[InlineKeyboardButton('ВЕРНУТЬСЯ В МЕНЮ', callback_data=f"Geocollege-exit")]]
    context.user_data["college_by_geo"] = {}
    cnt = 0
    for college in find_with_coords(location):
        cnt += 1
        markup.append([InlineKeyboardButton(college['name'], callback_data=f"Geocollege-{cnt}")])
        context.user_data["college_by_geo"][cnt] = (college)
    await update.message.reply_text("Выберите ВУЗ:", reply_markup=InlineKeyboardMarkup(markup))
    return 'wait'


async def stop(update, context):
    return ConversationHandler.END


async def get_college(update, context):
    await update.message.reply_text("Введите название города:")
    return "find_by_city"


async def find_by_city(update, context: CallbackContext):
    city = update.message.text
    context.user_data.clear()
    markup = [[InlineKeyboardButton('ВЕРНУТЬСЯ В МЕНЮ', callback_data=f"College-exit")]]
    cnt = 0
    for college in find_with_city(city):
        cnt += 1
        markup.append([InlineKeyboardButton(college['name'], callback_data=f"College-{cnt}")])
        context.user_data[cnt] = (college)
    await update.message.reply_text("Выберите ВУЗ:", reply_markup=InlineKeyboardMarkup(markup))
    return 'wait'


async def main_menu(update, context):
    await update.message.reply_text("Что бы вы хотели сделать?",
                                    reply_markup=ReplyKeyboardMarkup(markup, one_time_keyboard=True))
    return 'wait'


async def wait(update, context):
    message = update.message.text
    if message == markup[0][0]:
        return await get_college(update, context)
    elif message == markup[1][0]:
        return await get_user_location(update, context)
    elif message == markup[2][0]:
        return await open_favorite(update, context)


async def exit(temp, update, context):
    if temp == 'exit':
        await update.callback_query.delete_message()
        await context.bot.send_message(update.callback_query.message.chat.id, "Что бы вы хотели сделать?",
                                       reply_markup=ReplyKeyboardMarkup(markup, one_time_keyboard=True))
        return True


async def btn(update: Update, context: CallbackContext):
    global CURRENT
    query = update.callback_query
    await query.answer()
    if query.data.startswith("College"):
        temp = query.data.split('-')[-1]
        if await exit(temp, update, context):
            return
        CURRENT = int(temp)
        dct = context.user_data[CURRENT]
        await college_choise(query, dct, pref='back')
    elif query.data.startswith('back') or query.data.startswith('geoback'):
        flag = query.data.startswith('back')
        if await back_to_college(query, context.user_data if flag else context.user_data["college_by_geo"], pref='College' if flag else 'Geocollege'):
            if flag:
                college = (context.user_data[CURRENT])
            else:
                college = context.user_data["college_by_geo"][CURRENT]
            add_college_to_fav(college, update.callback_query.from_user.id)
    elif query.data.startswith('Fav'):
        temp = query.data.split('-')[-1]
        if await exit(temp, update, context):
            return
        CURRENT = int(temp)
        dct = context.user_data['favorite'][CURRENT]
        await college_choise(query, dct, pref='favback')
    elif query.data.startswith('favback'):
        await back_to_favorite(query, context.user_data['favorite'])
    elif query.data.startswith('Geocollege'):
        temp = query.data.split('-')[-1]
        if await exit(temp, update, context):
            return
        CURRENT = int(temp)
        dct = context.user_data['college_by_geo'][CURRENT]
        await college_choise(query, dct, pref="geoback")
    else:
        print('error')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    c1 = CommandHandler('start', main_menu)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_menu)],
        states={
            "start": [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu)],
            "get_college": [MessageHandler(filters.TEXT & ~filters.COMMAND, get_college)],
            "find_by_city": [MessageHandler(filters.TEXT & ~filters.COMMAND, find_by_city)],
            'wait': [MessageHandler(filters.TEXT & ~filters.COMMAND, wait)],
            'open_favorite': [MessageHandler(filters.TEXT & ~filters.COMMAND, open_favorite)],
            'locate': [MessageHandler(filters.LOCATION, find_by_geo)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler)
    application.add_handler(c1)
    application.add_handler(CallbackQueryHandler(btn))
    application.run_polling()


if __name__ == '__main__':
    main()
