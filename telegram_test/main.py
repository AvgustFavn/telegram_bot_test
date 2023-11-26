import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ApplicationBuilder, \
    MessageHandler, filters
from back import *


loop = asyncio.get_event_loop()

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    result = await loop.run_in_executor(None, get_user, user.username)
    if not result:
        us = User(username=user.username, firstname=user.first_name, lastname=user.last_name)
        await loop.run_in_executor(None, session.add, us)
        await loop.run_in_executor(None, session.commit)

    keyboard = [
        [InlineKeyboardButton("Говорить с персонажем", callback_data='1'),
         InlineKeyboardButton("Посмотреть всех персонажей", callback_data='2')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=f'Привет, {user.first_name}, давай выберем персонажа, с которым ты хотел бы поболтать?',
                              reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = update.effective_user
    await query.answer()
    if query.data == '1':
        user = await loop.run_in_executor(None, get_user, user.username)
        char = user.chatacter
        if char:
            char = await loop.run_in_executor(None, get_char, char)
            await query.edit_message_text(text=char.greetings)
        else:
            await query.edit_message_text('Вы не выбрали персонажа :(')

    elif query.data == '2':
        keyboard = [
            [InlineKeyboardButton("Марио", callback_data='3'),
             InlineKeyboardButton("Альберт Эйнштейн", callback_data='4')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message is not None:
            await update.message.reply_text(text='Выберете персонажа: ', reply_markup=reply_markup)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Выберете персонажа: ', reply_markup=reply_markup)

    elif query.data == '3':
        user = await loop.run_in_executor(None, get_user, user.username)
        user.chatacter = 1
        await loop.run_in_executor(None, session.add, user)
        await loop.run_in_executor(None, session.commit)
        keyboard = [
            [InlineKeyboardButton("Говорить с персонажем", callback_data='1'),
             InlineKeyboardButton("Посмотреть всех персонажей", callback_data='2')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f'Вы выбрали Марио, нчаните разговор с ним сейчас!',
            reply_markup=reply_markup)

    elif query.data == '4':
        user = await loop.run_in_executor(None, get_user, user.username)
        user.chatacter = 2
        await loop.run_in_executor(None, session.add, user)
        await loop.run_in_executor(None, session.commit)
        keyboard = [
            [InlineKeyboardButton("Говорить с персонажем", callback_data='1'),
             InlineKeyboardButton("Посмотреть всех персонажей", callback_data='2')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message is not None:
            await update.message.reply_text(f'Вы выбрали Альберта, нчаните разговор с ним сейчас!',
            reply_markup=reply_markup)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(f'Вы выбрали Альберта, нчаните разговор с ним сейчас!',
            reply_markup=reply_markup)

async def conversation(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user = await loop.run_in_executor(None, get_user, user.username)
    user_message = update.message.text
    if user.chatacter:
        res = await send_message(int(user.chatacter), user_message)
        ans = res['choices'][0]['message']['content']
        await update.message.reply_text(ans)
    else:
        await update.message.reply_text('Вы не выбрали персонажа :(')


def main() -> None:
    TOKEN = '6812102011:AAFQQCNA0LL0Dvf16BWolyyWsgQQBpQ_5vc'
    # создание экземпляра бота через `ApplicationBuilder`
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    button_handler = CallbackQueryHandler(button)
    application.add_handler(start_handler)
    application.add_handler(button_handler)
    conversation_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), conversation)
    application.add_handler(conversation_handler)
    # запускаем приложение
    application.run_polling()


if __name__ == '__main__':
    main()