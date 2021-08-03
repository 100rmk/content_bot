import logging
import os
from datetime import datetime

from aiogram import types
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import db
from etc.config import RECIPIENT_CHAT_ID, id_predlojki
from filters import AdminFilter, NicknameFilter
from misc import dp, bot
from utils import *

inline_reaction = InlineKeyboardMarkup(row_width=2)
like_btn = InlineKeyboardButton('👍', callback_data='up')
dislike_btn = InlineKeyboardButton('👎', callback_data='down')
inline_reaction.add(like_btn, dislike_btn)

inline_moderation = InlineKeyboardMarkup(row_width=2)
post_btn = InlineKeyboardButton('POST', callback_data='post')
remove_btn = InlineKeyboardButton('REMOVE', callback_data='remove')
ban_btn = InlineKeyboardButton('BAN', callback_data='ban')
inline_moderation.add(post_btn).add(remove_btn, ban_btn)

dp.filters_factory.bind(AdminFilter)
dp.filters_factory.bind(NicknameFilter)


@dp.message_handler(is_admin=False, has_nickname=True, content_types=[types.ContentType.VIDEO, types.ContentType.PHOTO])
async def suggest_posts(message: types.Message):
    db.add_user(user_id=message.from_user.id, username=message.from_user.username)
    user = db.get_user(message.from_user.id)
    posts_count = user.get('sugg_post_count')
    if user.get('is_banned') is True:
        return SendMessage(message.chat.id,
                           'Извините, но вы в бане, видимо вы запостили контент противоречащий нашим нормам морали. '
                           'Если это не так и вы попали в бан ошибочно, напишите @wtfout')
    if posts_count == 0:
        return SendMessage(message.chat.id, f'Лимит мемов исчерпан. Счетчик обновится в пятницу')
    await bot.copy_message(chat_id=id_predlojki, from_chat_id=message.chat.id, message_id=message.message_id,
                           disable_notification=True, caption=f'@{message.from_user.username}|{message.from_user.id}',
                           reply_markup=inline_moderation)
    db.reduce_post_count(user_id=message.from_user.id)
    return SendMessage(message.chat.id, f'Мем принят, на этой неделе вы можете скинуть мемов: {posts_count - 1}')


@dp.message_handler(is_admin=True, content_types=types.ContentType.VIDEO)
async def video_post(message: types.Message):
    video = message.video
    try:
        file = await bot.get_file(video.file_id)

        await bot.download_file(file.file_path, destination=f'tmp/temp_video')
        tmp_vid = 'tmp/tmp_video_out.mp4'
        if os.path.isfile(tmp_vid):
            os.remove(tmp_vid)

        try:
            await video_convert(tmp_vid)
        except Exception as e:
            logging.exception('ffmpeg error')
            return

        tg_upload = types.InputFile(tmp_vid)

        if message.caption is None:
            caption = '@VidMem'
        else:
            caption = message.caption + '\n\n@VidMem'

        response = await bot.send_video(RECIPIENT_CHAT_ID, tg_upload, caption=caption, reply_markup=inline_reaction)
        db.insert_post(message, response.message_id, message.from_user.username, user_id=message.from_user.id)
        return SendMessage(message.chat.id, f'{datetime.now()} vidos zaletel')
    except Exception as e:
        return SendMessage(message.chat.id, str(e))


@dp.message_handler(is_admin=True, content_types=types.ContentType.PHOTO)
async def img_post(message: types.Message):
    try:
        img = message.photo
        file = await bot.get_file(img[-1].file_id)

        await bot.download_file(file.file_path, destination=f'tmp/temp_image')
        tmp_img = 'tmp/tmp_image_out.jpg'
        if os.path.isfile(tmp_img):
            os.remove(tmp_img)

        try:
            await img_convert(tmp_img)
        except Exception as e:
            logging.exception('ffmpeg error')
            return

        tg_upload = types.InputFile(tmp_img)

        if message.caption is None:
            caption = '@VidMem'
        else:
            caption = message.caption + '\n\n@VidMem'

        response = await bot.send_photo(RECIPIENT_CHAT_ID, tg_upload, caption=caption, reply_markup=inline_reaction)
        db.insert_post(message, response.message_id, message.from_user.username, user_id=message.from_user.id)

        return SendMessage(message.chat.id, f'{datetime.now()} img zaletel')
    except Exception as e:
        return SendMessage(message.chat.id, str(e))
