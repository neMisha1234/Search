from telegram import InlineKeyboardMarkup, InlineKeyboardButton


async def college_choise(query, dct):
    if query.data == 'exit':
        return
    CURRENT = int(query.data)
    college = dct[CURRENT]
    markup = [[InlineKeyboardButton("Назад", callback_data="back"),
               InlineKeyboardButton('Добавить в избранное 🔥', callback_data='add_to')]]
    message = f'{college["name"]} \n'
    message += f'Контактная информация: \n'
    message += f"Сайт: {college['url']} \nТелефон: {college['Phones']}\n"
    message += '-' * 30 + '\n'

    await query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(markup))


async def back_to_college(query, dct):
    if query.data == 'back':
        markup = [[InlineKeyboardButton('ВЕРНУТЬСЯ В МЕНЮ', callback_data=f"exit")]]
        for i in dct:
            coll = dct[i]
            markup.append([InlineKeyboardButton(coll['name'], callback_data=f"{i}")])
        await query.edit_message_text(text="Выберите ВУЗ:", reply_markup=InlineKeyboardMarkup(markup))
    else:
        return True

