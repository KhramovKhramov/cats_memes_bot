from base64 import b64encode
from random import choice

from pymongo import MongoClient

import settings

client = MongoClient(settings.MONGO_LINK)

db = client[settings.MONGO_DB_NAME]


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({'user_id': effective_user.id})
    if not user:
        user = {
            'user_id': effective_user.id,
            'first_name': effective_user.first_name,
            'last_name': effective_user.last_name,
            'username': effective_user.username,
            'chat_id': chat_id
        }
        db.users.insert_one(user)

    return user


def save_pic(db, file_name):
    with open(f'{file_name}', 'rb') as f:
        bynary = b64encode(f.read())
        pic = {
            'file_name': file_name,
            'bynary': bynary
        }
        db.pics.insert_one(pic)


def get_random_pic(db):
    files = db.pics.find()
    random_pic = choice(list(files))
    bynary = random_pic['bynary']
    file_name = random_pic['file_name']

    return bynary, file_name
