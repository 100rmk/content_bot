from datetime import datetime
from typing import Union

import pymongo
from pymongo.results import BulkWriteResult

from db.BaseModel import BaseDB
from etc.config import POST_COUNT_IN_WEEK  # TODO: вынести в .env


class MongoDB(BaseDB):
    def __init__(self, *, mongo_url, bot_name):
        self._db = pymongo.MongoClient(mongo_url)
        self._db_posts = self._db[bot_name].posts
        self._db_users = self._db[bot_name].users

    def get_post(self, *, message_id):
        return self._db_posts.find_one({'_id': message_id})

    def insert_post(self, *, file_id: int, id_: int, username: str, user_id: Union[int, str]):
        post = {
            '_id': id_,
            'file_id': file_id,
            'user': username,
            'user_id': user_id,
            'likes': [],
            'dislikes': [],
            'timestamp': datetime.now()
        }
        self._db_posts.insert_one(post)

    def add_user(self, *, user_id: int, username: str):
        user = self._db_users.find_one({"_id": user_id})
        if user is None:
            user = {
                '_id': user_id,
                'username': username,
                'role': 'user',
                'sugg_post_count': POST_COUNT_IN_WEEK,
                'is_banned': False
            }
            self._db_users.insert_one(user)

    def get_user(self, *, user_id):
        return self._db_users.find_one({'_id': user_id})

    def ban_user(self, *, user_id):
        self._db_users.update_one({'_id': user_id}, {'$set': {'is_banned': True}})

    def unban_user(self, *, username):
        return self._db_users.find_one_and_update({'username': username}, {'$set': {'is_banned': False}})

    def reset_post_count(self):
        self._db_users.update_many({'role': 'user'}, {'$set': {'sugg_post_count': POST_COUNT_IN_WEEK}})

    def reduce_post_count(self, *, user_id):
        self._db_users.find_one_and_update({'_id': user_id}, {'$inc': {'sugg_post_count': -1}})

    def bulk_push_reactions(self, *, reactions: list) -> BulkWriteResult:
        return self._db_posts.bulk_write(reactions)

