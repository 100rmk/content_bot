from sqlalchemy import Column, String, Integer, Date, BigInteger
from sqlalchemy.dialects.postgresql import ARRAY

from db.models.base import BaseTable, Base


class Post(Base, BaseTable):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    content_type = Column(String(16))
    likes = Column(ARRAY(BigInteger))
    dislikes = Column(ARRAY(BigInteger))
    file_id = Column(String(255))
    timestamp = Column(Date)
    username = Column(String(255))
    user_id = Column(BigInteger)
