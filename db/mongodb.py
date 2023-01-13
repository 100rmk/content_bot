from datetime import datetime, timedelta
from typing import Union

import pymongo
from pymongo.results import BulkWriteResult

from db.BaseModel import BaseDB
from etc.config import Config


class MongoDB(BaseDB):
    def __init__(self, *, mongo_url: str, bot_name: str):
        self._db = pymongo.MongoClient(mongo_url)
        self._db_posts = self._db[bot_name].posts
        self._db_users = self._db[bot_name].users

    def get_post(self, *, message_id: int):
        return self._db_posts.find_one({'_id': message_id})

    def insert_post(self, *, file_id: int, id_: int, username: str, user_id: Union[int, str]):
        post = {
            '_id': id_,
            'file_id': file_id,
            'user': username,
            'user_id': user_id,
            'likes': [],
            'dislikes': [],
            'timestamp': datetime.now() + timedelta(hours=Config.tz)
        }
        self._db_posts.insert_one(post)

    def add_user(self, *, user_id: int, username: str):
        user = self._db_users.find_one({"_id": user_id})
        if user is None:
            user = {
                '_id': user_id,
                'username': username,
                'role': 'user',
                'sugg_post_count': Config.post_count_in_week,
                'is_banned': False
            }
            self._db_users.insert_one(user)

    def get_user(self, *, user_id: int):
        return self._db_users.find_one({'_id': user_id})

    def ban_user(self, *, user_id: int):
        self._db_users.update_one({'_id': user_id}, {'$set': {'is_banned': True}})

    def unban_user(self, *, username: str):
        return self._db_users.find_one_and_update({'username': username}, {'$set': {'is_banned': False}})

    def reset_post_count(self):
        self._db_users.update_many({'role': 'user'}, {'$set': {'sugg_post_count': Config.post_count_in_week}})

    def reduce_post_count(self, *, user_id: int):
        self._db_users.find_one_and_update({'_id': user_id}, {'$inc': {'sugg_post_count': -1}})

    def bulk_push_reactions(self, *, reactions: list) -> BulkWriteResult:
        return self._db_posts.bulk_write(reactions)
