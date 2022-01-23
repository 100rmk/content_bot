from aiogram import types
from datetime import datetime
from misc import db_mongo
from etc.config import POST_COUNT_IN_WEEK

_db_posts = db_mongo.tg_memvid.posts
_db_suggest = db_mongo.tg_memvid.users


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
    user = _db_suggest.find_one({"_id": user_id})
    if user is None:
        user = {
            '_id': user_id,
            'username': username,
            'sugg_post_count': POST_COUNT_IN_WEEK,
            'is_banned': False
        }
        _db_suggest.insert_one(user)


def reduce_post_count(user_id):
    _db_suggest.find_one_and_update({'_id': user_id}, {'$inc': {'sugg_post_count': -1}})


def get_user(user_id):
    return _db_suggest.find_one({"_id": user_id})


def get_post(message_id):
    return _db_posts.find_one({"_id": message_id})


def add_user_reaction(message_id, user_id, action: str, reaction: str):
    _db_posts.find_one_and_update({'_id': message_id}, {f'${action}': {reaction: user_id}})


def ban_user(user_id):
    _db_suggest.update_one({'_id': user_id}, {'$set': {'is_banned': True}})


def unban_user(username):
    return _db_suggest.find_one_and_update({'username': username}, {'$set': {'is_banned': False}})


def reset_post_count():
    _db_suggest.update_many({}, {'$set': {'sugg_post_count': POST_COUNT_IN_WEEK}})


def get_db_params(message_id):
    response = get_post(message_id)
    likes_arr = response.get('likes')
    dislikes_arr = response.get('dislikes')
    likes_count = len(likes_arr)
    dislikes_count = len(dislikes_arr)
    return dislikes_arr, dislikes_count, likes_arr, likes_count
