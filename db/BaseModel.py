from abc import ABC, abstractmethod
from typing import Union, Any


class BaseDB(ABC):
    @abstractmethod
    def get_post(self, *, message_id) -> dict:
        pass

    @abstractmethod
    def insert_post(self, *, file_id: int, id_: int, username: str, user_id: Union[int, str]):
        pass

    @abstractmethod
    def add_user(self, *, user_id: int, username: str):
        pass

    @abstractmethod
    def get_user(self, *, user_id: int):
        pass

    @abstractmethod
    def ban_user(self, *, user_id: int):
        pass

    @abstractmethod
    def unban_user(self, *, username: str):
        pass

    @abstractmethod
    def reset_post_count(self):
        pass

    @abstractmethod
    def reduce_post_count(self, *, user_id: int):
        pass

    @abstractmethod
    def bulk_push_reactions(self, *, reactions: list):
        pass


class AsyncBaseCache(ABC):
    @abstractmethod
    async def get(self, key: Any):
        pass

    @abstractmethod
    async def set(self, key: Any, value: Union[str, bytes, int, float]) -> Any:
        pass

    @abstractmethod
    async def delete(self, key: Any):
        pass
