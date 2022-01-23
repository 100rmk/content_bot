import asyncio
import logging
import os
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import db
from db.fsm import GroupState
from etc.config import RECIPIENT_CHAT_ID, suggest_id
from filters import AdminFilter, NicknameFilter
from misc import dp, bot
from utils import *
from other import text

inline_reaction = InlineKeyboardMarkup(row_width=2)
like_btn = InlineKeyboardButton(text.INLINE_TEXT['thumbUp'], callback_data='up')
dislike_btn = InlineKeyboardButton(text.INLINE_TEXT['thumbDown'], callback_data='down')
inline_reaction.add(like_btn, dislike_btn)

inline_moderation = InlineKeyboardMarkup(row_width=2)
post_btn = InlineKeyboardButton('POST', callback_data='post')
remove_btn = InlineKeyboardButton('REMOVE', callback_data='remove')
ban_btn = InlineKeyboardButton('BAN', callback_data='ban')
inline_moderation.add(post_btn).add(remove_btn, ban_btn)

dp.filters_factory.bind(AdminFilter)
dp.filters_factory.bind(NicknameFilter)


# Предложка
@dp.message_handler(is_admin=False, has_nickname=True, content_types=[types.ContentType.VIDEO, types.ContentType.PHOTO])
async def suggest_posts(message: types.Message):
    db.add_user(user_id=message.from_user.id, username=message.from_user.username)
    user = db.get_user(message.from_user.id)
    posts_count = user.get('sugg_post_count')
    if user.get('is_banned') is True:
        return SendMessage(message.chat.id, text.MESSAGE_FOR_BANNED_USER)
    if posts_count == 0:
        return SendMessage(message.chat.id, text.LIMIT_EXCEEDED)
    await bot.copy_message(chat_id=suggest_id, from_chat_id=message.chat.id, message_id=message.message_id,
                           disable_notification=True, caption=f'@{message.from_user.username}|{message.from_user.id}',
                           reply_markup=inline_moderation)
    db.reduce_post_count(user_id=message.from_user.id)
    return SendMessage(message.chat.id, f'{text.POST_ACCEPTED} {posts_count - 1}')


@dp.message_handler(is_admin=True, content_types=types.ContentType.VIDEO, run_task=True)
async def video_post(message: types.Message):
    video = message.video
    try:
        wait_message = await bot.send_message(message.chat.id, text.PROCESSING)

        file = await bot.get_file(video.file_id)
        file_link = bot.get_file_url(file.file_path)

        tmp_vid = 'tmp/tmp_video_out.mp4'
        if os.path.isfile(tmp_vid):
            os.remove(tmp_vid)

        try:
            await video_convert(file_link, tmp_vid)
        except Exception as e:
            await bot.delete_message(message.chat.id, wait_message.message_id)
            logging.exception('ffmpeg error')
            return

        tg_upload = types.InputFile(tmp_vid)
        await bot.delete_message(message.chat.id, wait_message.message_id)
        response = await bot.send_video(RECIPIENT_CHAT_ID, tg_upload, caption=message.caption,
                                        reply_markup=inline_reaction)
        db.insert_post(message, response.message_id, message.from_user.username, user_id=message.from_user.id)
        return SendMessage(message.chat.id, f'{datetime.now()} vidos zaletel')
    except Exception as e:
        return SendMessage(message.chat.id, str(e))


@dp.message_handler(is_admin=True, content_types=types.ContentType.PHOTO)
async def img_post(message: types.Message):
    img = message.photo
    try:
        wait_message = await bot.send_message(message.chat.id, text.PROCESSING)
        file = await bot.get_file(img[-1].file_id)
        file_link = bot.get_file_url(file.file_path)

        tmp_img = 'tmp/tmp_image_out.jpg'
        if os.path.isfile(tmp_img):
            os.remove(tmp_img)

        try:
            await img_convert(file_link, tmp_img)
        except Exception as e:
            await bot.delete_message(message.chat.id, wait_message.message_id)
            logging.exception('ffmpeg error')
            return

        tg_upload = types.InputFile(tmp_img)
        await bot.delete_message(message.chat.id, wait_message.message_id)
        response = await bot.send_photo(RECIPIENT_CHAT_ID, tg_upload, caption=message.caption,
                                        reply_markup=inline_reaction)
        db.insert_post(message, response.message_id, message.from_user.username, user_id=message.from_user.id)

        return SendMessage(message.chat.id, f'{datetime.now()} img zaletel')  # TODO: исправить логирование
    except Exception as e:
        return SendMessage(message.chat.id, str(e))


@dp.message_handler(is_admin=True, state=GroupState.advertising_link)  # TODO: проверку на ссылку
async def ad_link(message: types.Message, state: FSMContext):
    url = message.text
    await state.update_data(ad_url=url)
    await message.answer(text.SEND_AD_POST)
    await GroupState.advertising_inline.set()


@dp.message_handler(is_admin=True, state=GroupState.advertising_inline,
                    content_types=types.ContentType.ANY)
async def ad_post(message: types.Message, state: FSMContext):
    try:
        state_data = await state.get_data()
        inline_link = InlineKeyboardMarkup(row_width=1)
        link_btn = InlineKeyboardButton(text.AD_GOTO,
                                        url=state_data['ad_url'])  # TODO: Добавить еще один стэйт для имени кнопки
        inline_link.add(link_btn)
        await bot.copy_message(chat_id=RECIPIENT_CHAT_ID, from_chat_id=message.chat.id, message_id=message.message_id,
                               disable_notification=True, reply_markup=inline_link)
        await state.finish()
        return SendMessage(message.chat.id, text.AD_POST_SENT)
    except Exception as e:
        await state.finish()
        return SendMessage(message.chat.id, str(e))
