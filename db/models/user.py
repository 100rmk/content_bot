from sqlalchemy import Column, String, Integer, Boolean, SmallInteger

from db.models.base import BaseTable, Base


class SuggestionUser(Base, BaseTable):
    __tablename__ = 'suggestion_users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    banned = Column(Boolean, default=False)
    anonymized = Column(Boolean, default=False)
    role = Column(String(16))
    suggestions_count = Column(SmallInteger)
