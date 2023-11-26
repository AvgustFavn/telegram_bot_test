import datetime
import json
from pathlib import Path

import aiohttp
from sqlalchemy import *
from sqlalchemy.orm import Session, declarative_base

engine = create_engine("postgresql+psycopg2://test:Some_password@localhost/test_base")
session = Session(bind=engine)
BASE_DIR = Path(__file__).resolve().parent.parent

Base = declarative_base()

class User(Base):
    __tablename__ = 'user_bot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=True)
    time = Column(DateTime(), default=datetime.datetime.now())
    chatacter = Column(Integer, nullable=True)

class Character(Base):
    __tablename__ = 'chars_bot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    greetings = Column(String(500), nullable=False)


Base.metadata.create_all(engine)

async def send_message(id, mess):
    messages = ''
    if id == 1:
        messages = [
            {"role": "system", "content": "Ты Марио из Супер Марио, общайся с пользователем от лица этого песронажа. "
                                          "Не пиши опастные советы и сообщения"},
            {"role": "user", "content": f' {mess}'}
        ]

    elif id == 2:
        messages = [
            {"role": "system", "content": "Ты Альберт Эйнштейн, общайся с пользователем от лица этого человека. "
                                          "Не пиши опастные советы и сообщения"},
            {"role": "user", "content": f' {mess}'}
        ]

    endpoint = 'http://95.217.14.178:8080/candidates_openai/gpt'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': messages,
    }
    data = json.dumps(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, data=data) as response:
            return await response.json()


def get_user(username):
    return session.query(User).filter_by(username=username).first()

def get_char(id):
    return session.query(Character).filter_by(id=id).first()


# us = Character(name='Марио', greetings='Привет, я Марио! Я пришел, чтобы спасти принцессу и победить Купу! '
#                                        'Я люблю приключения, пиццу и своего брата Луиджи! Я всегда готов к новым '
#                                        'испытаниям! Я - супер Марио!')
# us2 = Character(name='Альберт Эйнштейн', greetings='Здравствуйте, я Альберт Эйнштейн. Я физик-теоретик, лауреат '
#                                                    'Нобелевской премии по физике за объяснение фотоэлектрического '
#                                                    'эффекта. Я также известен как создатель специальной и общей теорий '
#                                                    'относительности, которые изменили основания физики. Я родился в '
#                                                    'Германии, но жил в Швейцарии и США. Я интересуюсь философией, '
#                                                    'историей науки и общественными вопросами. ')
#
# session.add(us)
# session.add(us2)
# session.commit()