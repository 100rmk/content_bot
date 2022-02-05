from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from etc.config import ADMINS, MODERS


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        return (message.from_user.id in ADMINS) == self.is_admin


class NicknameFilter(BoundFilter):
    key = 'has_nickname'

    def __init__(self, has_nickname):
        self.has_nickname = has_nickname

    async def check(self, message: types.Message):
        return (message.from_user.username != None) == self.has_nickname


class ModerFilter(BoundFilter):
    key = 'is_moder'

    def __init__(self, is_moder):
        self.is_moder = is_moder

    async def check(self, message: types.Message):
        return (message.from_user.id in MODERS) == self.is_moder
