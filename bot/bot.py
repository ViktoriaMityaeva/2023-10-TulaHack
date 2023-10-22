import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
from random import shuffle
import db_services
import os

# Create the bot instance
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

# Create the menu keyboard
menu_keyboard = InlineKeyboardMarkup()
menu_keyboard.add(InlineKeyboardButton(text='👀 Random coffe', callback_data='Random coffe'))
menu_keyboard.add(InlineKeyboardButton(text='📊 График встреч', callback_data='График встреч'))
menu_keyboard.add(InlineKeyboardButton(text='🎈 Отключиться', callback_data='Отключиться'))
menu_keyboard.add(InlineKeyboardButton(text='👥 Отчёты прошлых встреч', callback_data='Статистика прошлых встреч'))
menu_keyboard.add(InlineKeyboardButton(text='🏠 Управление локациями', callback_data='Управление локациями'))
# Register command handlers
@bot.message_handler(commands=['register'])
def handle_register(message):
    user = db_services.get_user_by_tg_id(message.from_user.id)
    if user:
        bot.reply_to(message, "Ты уже зарегистрирован.")
    else:
        db_services.create_user(telegram_id=message.from_user.id, username=message.from_user.username,
                    first_name=message.from_user.first_name, last_name=message.from_user.last_name)
        bot.reply_to(message, "Регистрация прошла успешно!\nТы можешь начать работу с ботом, используя команду /menu.")

@bot.message_handler(commands=['pair'])
def handle_pair(message):
    users = db_services.get_all_users()
    shuffle(users)

    if len(users) % 2 != 0:
        bot.reply_to(message, "Не могу найти тебе пару.")

    else:
        for i in range(0, len(users), 2):
            db_services.add_pair(users[i].id, users[i+1].id)
        bot.reply_to(message, "Для вас создана пара :)")

@bot.message_handler(commands=['start'])
def handle_pair(message):
    bot.reply_to(message, "Привет, я Random Coffee, рад тебя видеть 🥳 Я предназначен для тех, кто ищет новые пути для общения, знакомств и обмена идеями 😼 Если ты один из нас, то давай скорей начнём 🙌\nНажми /menu")


@bot.message_handler(commands=['menu'])
def handle_pair(message):
    user = db_services.get_user_by_tg_id(message.from_user.id)
    if user:
        bot.reply_to(message, "Наше меню:",
                    reply_markup=menu_keyboard)
    else:
        bot.reply_to(message, "Ты не зарегистрирован. Напиши /register")

# Handle the menu options
@bot.callback_query_handler(func=lambda call: True)
def handle_menu_selection(call):
    user = db_services.get_user_by_tg_id(call.message.chat.id)
    print(call.message.chat.id)
    print(user)
    if user:
        option_selected = call.data
        if option_selected == 'Random coffe':
            # Handle option 1
            db_services.active_user(call.message.chat.id)
            bot.edit_message_text(call.message.chat.id,  'Ты в Random coffe, ожидай уведомления ✨', message_id=call.message.message_id)
        elif option_selected == 'График встреч':
            bot.edit_message_text(call.message.chat.id, 'График встреч: ✨', message_id=call.message.message_id,)
        elif option_selected == 'Отключиться':
            db_services.disactive_user(call.message.chat.id)
            bot.edit_message_text(call.message.chat.id, 'Вы больше не участвуете в random coffe', message_id=call.message.message_id,)
        elif option_selected == 'Отчёты прошлых встреч':
            bot.edit_message_text(call.message.chat.id, 'Пока что вы не были ни на одной встречи :(', message_id=call.message.message_id,)
    else:
        bot.reply_to(call.message, "Ты не зарегистрирован. Напиши /register")

# Start the bot
bot.polling()