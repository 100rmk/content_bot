import logging
import os

from aiogram import types
from aiogram.dispatcher.webhook import AnswerCallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageNotModified

from db import db
from etc.config import RECIPIENT_CHAT_ID, id_predlojki
from handlers.content import inline_reaction
from misc import dp, bot
from utils import video_convert, img_convert

cache_time = 8
sugg_caption = 'Прислали через @VidMem_bot'


# reaction: like
@dp.callback_query_handler(text='up')
async def callback_liking(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id
    dislikes_arr, dislikes_count, likes_arr, likes_count = await get_db_params(message_id)
    like_btn = None

    if user_id in likes_arr:
        db.add_user_reaction(message_id, user_id, action='pull', reaction='likes')
        likes_count = likes_count - 1
        like_btn = InlineKeyboardButton(f'👍{likes_count}', callback_data='up')
    elif user_id in dislikes_arr:
        db.add_user_reaction(message_id, user_id, action='pull', reaction='dislikes')
        dislikes_count = dislikes_count - 1

    if like_btn is not None:
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        dislike_btn = InlineKeyboardButton(f'👎{dislikes_count}', callback_data='down')
        inline_kb_full.add(like_btn, dislike_btn)
        await edit_reply_markup(inline_kb_full, message_id)

        return AnswerCallbackQuery(callback_query.id, text='Like снят', cache_time=cache_time)

    db.add_user_reaction(message_id, user_id, action='push', reaction='likes')

    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    like_btn = InlineKeyboardButton(f'👍{likes_count + 1}', callback_data='up')
    dislike_btn = InlineKeyboardButton(f'👎{dislikes_count}', callback_data='down')
    inline_kb_full.add(like_btn, dislike_btn)
    await edit_reply_markup(inline_kb_full, message_id)

    return AnswerCallbackQuery(callback_query.id, text='Like залетел', cache_time=cache_time)


# reaction: dislike
@dp.callback_query_handler(text='down')
async def callback_disliking(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id
    dislikes_arr, dislikes_count, likes_arr, likes_count = await get_db_params(message_id)
    dislike_btn = None

    if user_id in likes_arr:
        db.add_user_reaction(message_id, user_id, action='pull', reaction='likes')
        likes_count = likes_count - 1
    elif user_id in dislikes_arr:
        db.add_user_reaction(message_id, user_id, action='pull', reaction='dislikes')
        dislikes_count = dislikes_count - 1
        dislike_btn = InlineKeyboardButton(f'👎{dislikes_count}', callback_data='down')

    if dislike_btn is not None:
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        like_btn = InlineKeyboardButton(f'👍{likes_count}', callback_data='up')
        inline_kb_full.add(like_btn, dislike_btn)
        await edit_reply_markup(inline_kb_full, message_id)

        return AnswerCallbackQuery(callback_query.id, text='Dislike снят', cache_time=cache_time)

    db.add_user_reaction(message_id, user_id, action='push', reaction='dislikes')

    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    like_btn = InlineKeyboardButton(f'👍{likes_count}', callback_data='up')
    dislike_btn = InlineKeyboardButton(f'👎{dislikes_count + 1}', callback_data='down')
    inline_kb_full.add(like_btn, dislike_btn)
    await edit_reply_markup(inline_kb_full, message_id)

    return AnswerCallbackQuery(callback_query.id, text='Dislike залетел', cache_time=cache_time)


# reaction: ban user
@dp.callback_query_handler(text='ban')
async def ban_user(callback_query: types.CallbackQuery):
    meta = callback_query.message.caption.split('|')
    username = meta[0]
    user_id = int(meta[1])
    db.ban_user(user_id)
    return AnswerCallbackQuery(callback_query.id, text=f'Пользователь {username} забанен')


# reaction: remove post
@dp.callback_query_handler(text='remove')
async def remove_sugg_post(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    try:
        await bot.delete_message(id_predlojki, message_id)
    except MessageCantBeDeleted as e:
        return AnswerCallbackQuery(callback_query.id, text='Нельзя удалить, удалите руками')
    return AnswerCallbackQuery(callback_query.id, text='Удалено')


# reaction: post sugg content
@dp.callback_query_handler(text='post')
async def post_sugg_content(callback_query: types.CallbackQuery):
    message = callback_query.message
    try:
        if message.photo:
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

            response = await bot.send_photo(RECIPIENT_CHAT_ID, tg_upload, caption=sugg_caption,
                                            reply_markup=inline_reaction)
            meta = message.caption.split('|')
            username = meta[0]
            user_id = meta[1]
            db.insert_post(message, response.message_id, username=username, user_id=user_id)

        if message.video:
            video = message.video
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

            response = await bot.send_video(RECIPIENT_CHAT_ID, tg_upload, caption=sugg_caption,
                                            reply_markup=inline_reaction)
            meta = message.caption.split('|')
            username = meta[0]
            user_id = meta[1]
            db.insert_post(message, response.message_id, username=username, user_id=user_id)

        await remove_sugg_post(callback_query)
        return AnswerCallbackQuery(callback_query.id, text='Мем запощен')
    except Exception as e:
        return AnswerCallbackQuery(callback_query.id, text='Мем нихуя не запощен')


async def edit_reply_markup(inline_kb_full, message_id):
    try:
        await bot.edit_message_reply_markup(RECIPIENT_CHAT_ID, message_id, reply_markup=inline_kb_full)
    except MessageNotModified:
        pass


async def get_db_params(message_id):
    response = db.get_post(message_id)
    likes_arr = response.get('likes')
    dislikes_arr = response.get('dislikes')
    likes_count = len(likes_arr)
    dislikes_count = len(dislikes_arr)
    return dislikes_arr, dislikes_count, likes_arr, likes_count
