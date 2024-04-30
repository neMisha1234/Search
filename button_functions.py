from telegram import InlineKeyboardMarkup, InlineKeyboardButton


async def college_choise(update, dct, pref=None):
    markup = [[InlineKeyboardButton("Назад", callback_data=f"{pref}-back")]]
    if pref != 'favback':
        markup[0].append(InlineKeyboardButton('Добавить в избранное 🔥', callback_data=f'{pref}-add_to'))
    message = f'{dct["name"]} \n'
    message += f'Контактная информация: \n'
    message += f"Сайт: {dct['url']} \nТелефон: {dct['Phones']}\n"
    message += '-' * 30 + '\n'

    await update.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(markup))


async def back_to_college(query, dct, pref=None):
    if query.data.split('-')[-1] == 'back':
        markup = [[InlineKeyboardButton('ВЕРНУТЬСЯ В МЕНЮ', callback_data=f"{pref}-exit")]]
        for i in dct:
            coll = dct[i]
            print(coll)
            markup.append([InlineKeyboardButton(coll['name'], callback_data=f"{pref}-{i}")])
        await query.edit_message_text(text="Выберите ВУЗ:", reply_markup=InlineKeyboardMarkup(markup))
    elif query.data.split('-')[-1] == 'add_to':
        return True


async def back_to_favorite(query, dct):
    if query.data.split('-')[-1] == 'back':
        markup = [[InlineKeyboardButton('ВЕРНУТЬСЯ В МЕНЮ', callback_data=f"Fav-exit")]]
        for i in dct:
            coll = dct[i]
            markup.append([InlineKeyboardButton(coll['name'], callback_data=f"Fav-{i}")])
        await query.edit_message_text(text="Выберите ВУЗ:", reply_markup=InlineKeyboardMarkup(markup))