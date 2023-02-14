from datetime import datetime, timedelta
from typing import Union, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.BaseModel import BaseDB
from db.models.posts import Post
from db.models.user import SuggestionUser
from etc.config import Config


class PostgresDB(BaseDB):
    def __init__(self, *, pg_url: str):
        engine = create_engine(pg_url)
        self.session = sessionmaker(bind=engine)

    def get_post(self, *, message_id: int) -> dict:
        with self.session() as session:
            return session.query(Post).filter_by(id=message_id).one().as_dict()

    def insert_post(self, *, file_id: int, id_: int, username: str, user_id: Union[int, str], content_type: str):
        post = Post(
            id=id_,
            content_type=content_type,
            likes=[],
            dislikes=[],
            file_id=file_id,
            timestamp=datetime.utcnow() + timedelta(hours=Config.tz),
            username=username,
            user_id=user_id
        )
        with self.session() as session:
            session.add(post)
            session.commit()

    def add_user(self, *, user_id: int, username: str):
        with self.session() as session:
            user = session.query(SuggestionUser).filter_by(id=user_id).one()
            if user is None:
                user = SuggestionUser(
                    id=user_id,
                    username=username,
                    role='user',
                    anonymized=False,
                    banned=False,
                    suggestions_count=Config.post_count_in_week
                )
                session.add(user)
                session.commit()

    def get_user(self, *, user_id: int) -> dict:
        with self.session() as session:
            return session.query(SuggestionUser).filter_by(id=user_id).one().as_dict()

    def ban_user(self, *, user_id: int):
        with self.session() as session:
            user = session.query(SuggestionUser).filter_by(id=user_id).one()
            user.banned = True
            session.commit()

    def unban_user(self, *, username: str) -> Optional[bool]:
        with self.session() as session:
            user = session.query(SuggestionUser).filter_by(username=username).one()
            if user:
                user.banned = False
                session.commit()
                return True
            else:
                return None

    def reset_post_count(self):
        with self.session() as session:
            session.query(SuggestionUser).filter().update({SuggestionUser.suggestions_count: Config.post_count_in_week})
            session.commit()

    def reduce_post_count(self, *, user_id: int):
        with self.session() as session:
            user = session.query(SuggestionUser).filter_by(id=user_id).one()
            user.suggestions_count -= 1
            session.commit()

    def bulk_push_reactions(self, *, reactions: list):
        with self.session() as session:
            session.bulk_update_mappings(Post, reactions)
            session.commit()
