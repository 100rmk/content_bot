from aiogram import types
from datetime import datetime
from misc import db_mongo
from etc.config import POST_COUNT_IN_WEEK  # TODO: вынести в .env (см. https://pypi.org/project/python-dotenv/)

_db_posts = db_mongo.tg_memvid.posts  # TODO: заменить tg_memvid на абстрактное обозначение
_db_users = db_mongo.tg_memvid.users  # TODO: тоже самое


def insert_post(message: types.Message, id, username, user_id):
    file_id = None
    if message.video:
        file_id = message.video.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id
    post = {
        '_id': id,
        'file_id': file_id,
        'user': username,
        'user_id': user_id,
        'likes': [],
        'dislikes': [],
        'timestamp': datetime.now()
    }
    _db_posts.insert_one(post)


def add_user(user_id, username):
    user = _db_users.find_one({"_id": user_id})
    if user is None:
        user = {
            '_id': user_id,
            'username': username,
            'role': 'user',
            'sugg_post_count': POST_COUNT_IN_WEEK,
            'is_banned': False
        }
        _db_users.insert_one(user)


def reduce_post_count(user_id):
    _db_users.find_one_and_update({'_id': user_id}, {'$inc': {'sugg_post_count': -1}})


def get_user(user_id):
    return _db_users.find_one({'_id': user_id})


def get_post(message_id):
    return _db_posts.find_one({'_id': message_id})


def add_user_reaction(message_id, user_id, action: str, reaction: str):
    _db_posts.find_one_and_update({'_id': message_id}, {f'${action}': {reaction: user_id}})


def ban_user(user_id):
    _db_users.update_one({'_id': user_id}, {'$set': {'is_banned': True}})


def unban_user(username):
    return _db_users.find_one_and_update({'username': username}, {'$set': {'is_banned': False}})


def reset_post_count():
    _db_users.update_many({'role': 'user'}, {'$set': {'sugg_post_count': POST_COUNT_IN_WEEK}})


def get_db_params(message_id):
    response = get_post(message_id)
    likes = response.get('likes')
    dislikes = response.get('dislikes')
    likes_count = len(likes)
    dislikes_count = len(dislikes)
    return dislikes, dislikes_count, likes, likes_count
