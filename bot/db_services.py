from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
import db


def create_user(telegram_id, username, first_name, last_name):
    new_user = db.User(telegram_id=telegram_id, username=username, first_name=first_name, last_name=last_name)
    session.add(new_user)
    session.commit()

def get_user_by_tg_id(telegram_id):
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    return user

def get_all_users():
    users = session.query(db.User).all()
    return users

def add_pair(user1_id, user2_id):
    new_pair = db.Pair(user1_id=user1_id, user2_id=user2_id)
    session.add(new_pair)
    session.commit()

def active_user(telegram_id):
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    user.is_active = True
    session.commit()

def disactive_user(telegram_id):
    user = session.query(db.User).filter_by(telegram_id=telegram_id).first()
    user.is_active = False
    session.commit()

Session = sessionmaker(bind=db.engine)
session = Session()