import telebot
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
from random import shuffle
import db_services
import os

# Create the bot instance
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

# Register command handlers
@bot.message_handler(commands=['register'])
def handle_register(message):
    user = db_services.get_user_by_tg_id(message.from_user.id)
    if user:
        bot.reply_to(message, "You are already registered.")
    else:
        db_services.create_user(telegram_id=message.from_user.id, username=message.from_user.username,
                    first_name=message.from_user.first_name, last_name=message.from_user.last_name)
        bot.reply_to(message, "You have been registered.")

@bot.message_handler(commands=['pair'])
def handle_pair(message):
    users = db_services.get_all_users
    shuffle(users)

    if len(users) % 2 != 0:
        bot.reply_to(message, "Cannot pair users. Odd number of users.")

    else:
        for i in range(0, len(users), 2):
            db_services.add_pair(users[i].id, users[i+1].id)
        bot.reply_to(message, "Pairs have been created.")

# Start the bot
bot.polling()