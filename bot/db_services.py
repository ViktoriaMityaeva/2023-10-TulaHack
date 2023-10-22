from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

Session = sessionmaker(bind=engine)
session = Session()
new_user = User(name='John Doe')
session.add(new_user)
session.commit()
all_users = session.query(User).all()
for user in all_users:
    print(user.name)
session.close()

#TODO