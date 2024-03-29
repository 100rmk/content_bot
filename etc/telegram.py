from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from other import text


class Buttons:
    reaction = InlineKeyboardMarkup(row_width=2)
    _like_button = InlineKeyboardButton(text.INLINE_TEXT['thumbUp'], callback_data='up')
    _dislike_button = InlineKeyboardButton(text.INLINE_TEXT['thumbDown'], callback_data='down')
    reaction.add(_like_button, _dislike_button)

    moderation = InlineKeyboardMarkup(row_width=2)
    _post_button = InlineKeyboardButton('POST', callback_data='post')
    _remove_button = InlineKeyboardButton('REMOVE', callback_data='remove')
    _ban_button = InlineKeyboardButton('BAN', callback_data='ban')
    moderation.add(_remove_button, _ban_button).add(_post_button)

    @staticmethod
    def edit_keyboard_button(*, likes_count: int, dislikes_count: int) -> InlineKeyboardMarkup:
        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        like_button = InlineKeyboardButton(f'{text.INLINE_TEXT["thumbUp"]}{likes_count}', callback_data='up')
        dislike_button = InlineKeyboardButton(f'{text.INLINE_TEXT["thumbDown"]}{dislikes_count}', callback_data='down')
        inline_keyboard.add(like_button, dislike_button)
        return inline_keyboard
