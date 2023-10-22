import logging
from random import choice

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create Bot instance
bot = Bot(token=os.environ.get('BOT_TOKEN'))

# Create Dispatcher instance
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Database configuration
Base = declarative_base()
engine = create_engine()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    state = Column(String)


class CoffeeMatch(Base):
    __tablename__ = 'coffee_matches'
    id = Column(Integer, primary_key=True)
    user1_id = Column(Integer)
    user2_id = Column(Integer)


class Form(StatesGroup):
    username = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    session = Session()
    user = session.query(User).filter_by(id=message.from_user.id).first()
    if user:
        await bot.send_message(message.chat.id, "Welcome back!")
    else:
        await bot.send_message(message.chat.id, "Welcome to Random Coffee Bot! Please enter your username.")
        await Form.username.set()
    session.close()


@dp.message_handler(state=Form.username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text

    session = Session()
    user = session.query(User).filter_by(id=message.from_user.id).first()

    if not user:
        new_user = User(id=message.from_user.id, username=username, state='registered')
        session.add(new_user)
    else:
        user.username = username
        user.state = 'registered'

    session.commit()
    session.close()

    await state.finish()
    await bot.send_message(message.chat.id, f"Thank you, {username}! You are now registered.")


@dp.message_handler(Command('match'))
async def match_command(message: types.Message):
    session = Session()
    current_user = session.query(User).filter_by(id=message.from_user.id).first()

    if current_user.state != 'registered':
        await bot.send_message(message.chat.id, "You need to register first!")
        return

    # Find a match for the current user
    user_pool = session.query(User).filter(User.id != current_user.id, User.state == 'registered').all()

    if not user_pool:
        await bot.send_message(message.chat.id, "No other registered users found. Please try again later.")
        return

    matched_user = choice(user_pool)

    # Create a coffee match
    coffee_match = CoffeeMatch(user1_id=current_user.id, user2_id=matched_user.id)
    session.add(coffee_match)
    session.commit()
    session.close()

    await bot.send_message(message.chat.id, f"Congratulations! You are matched with {matched_user.username}!")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    executor.start_polling(dp, skip_updates=True)