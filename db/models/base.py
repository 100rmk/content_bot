from sqlalchemy.ext.declarative import declarative_base

from etc.config import Config

Base = declarative_base()


class BaseTable:
    __table_args__ = {'schema': Config.bot_name}

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
