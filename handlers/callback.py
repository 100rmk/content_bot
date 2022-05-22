import logging
import os

import aiogram
from aiogram import types
from aiogram.dispatcher.webhook import AnswerCallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageNotModified

from db import db
from etc.config import RECIPIENT_CHAT_ID, SUGGEST_ID, sugg_post_description
from handlers.content import inline_reaction
from misc import dp, bot
from other import text
from utils import video_convert, img_convert

cache_time = 8


# TODO: у callback_liking и callback_disliking есть общие логика работы

# reaction: like
@dp.callback_query_handler(text='up')
async def callback_liking(callback_query: types.CallbackQuery):
    try:
        message_id = callback_query.message.message_id
        user_id = callback_query.from_user.id
        try:
            dislikes, dislikes_count, likes, likes_count = db.get_db_params(message_id)
        except Exception:
            return AnswerCallbackQuery(callback_query.id, cache_time=cache_time, text=text.LIKES_TIMEOUT)

        like_button = None

        # Если пользователь лайкнувший пост повторно нажал на лайк
        if user_id in likes:
            db.add_user_reaction(message_id, user_id, action='pull', reaction='likes')
            likes_count = likes_count - 1
            like_button = InlineKeyboardButton(f'{text.INLINE_TEXT["thumbUp"]}{likes_count}', callback_data='up')
            await bot.answer_callback_query(callback_query.id, cache_time=cache_time,
                                            text=f'{text.INLINE_TEXT["thumbUp"]} {text.INLINE_TEXT["fail"]}')
        elif user_id in dislikes:
            db.add_user_reaction(message_id, user_id, action='pull', reaction='dislikes')
            dislikes_count = dislikes_count - 1
            await bot.answer_callback_query(callback_query.id, cache_time=cache_time,
                                            text=f'{text.INLINE_TEXT["thumbUp"]} {text.INLINE_TEXT["success"]}')

        if like_button is not None:
            inline_keyboard = InlineKeyboardMarkup(row_width=2)
            dislike_button = InlineKeyboardButton(f'{text.INLINE_TEXT["thumbDown"]}{dislikes_count}',
                                                  callback_data='down')
            inline_keyboard.add(like_button, dislike_button)
            await edit_reply_markup(inline_keyboard, message_id)

            return AnswerCallbackQuery(callback_query.id, cache_time=cache_time,
                                       text=f'{text.INLINE_TEXT["thumbUp"]} {text.INLINE_TEXT["fail"]}')

        db.add_user_reaction(message_id, user_id, action='push', reaction='likes')

        await bot.answer_callback_query(callback_query.id, cache_time=cache_time,
                                        text=f'{text.INLINE_TEXT["thumbUp"]} {text.INLINE_TEXT["success"]}')
        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        like_button = InlineKeyboardButton(f'{text.INLINE_TEXT["thumbUp"]}{likes_count + 1}', callback_data='up')
        dislike_button = InlineKeyboardButton(f'{text.INLINE_TEXT["thumbDown"]}{dislikes_count}', callback_data='down')
        inline_keyboard.add(like_button, dislike_button)
        await edit_reply_markup(inline_keyboard, message_id)

        return
    except aiogram.utils.exceptions.InvalidQueryID:
        return AnswerCallbackQuery(callback_query.id, cache_time=cache_time, text=text.SMTH_WRONG)


# reaction: dislike
@dp.callback_query_handler(text='down', run_task=True)
async def callback_disliking(callback_query: types.CallbackQuery):
    try:
        message_id = callback_query.message.message_id
        user_id = callback_query.from_user.id
        try:
            dislikes, dislikes_count, likes, likes_count = db.get_db_params(message_id)
        except Exception:
            return AnswerCallbackQuery(callback_query.id, cache_time=cache_time, text=text.LIKES_TIMEOUT)
        dislike_button = None

        if user_id in likes:
            db.add_user_reaction(message_id, user_id, action='pull', reaction='likes')
            likes_count = likes_count - 1
            await bot.answer_callback_query(callback_query.id, cache_time=cache_time,
                                            text=f'{text.INLINE_TEXT["thumbDown"]} {text.INLINE_TEXT["success"]}')
        elif user_id in dislikes:
            db.add_user_reaction(message_id, user_id, action='pull', reaction='dislikes')
            dislikes_count = dislikes_count - 1
            dislike_button = InlineKeyboardButton(f'{text.INLINE_TEXT["thumbDown"]}{dislikes_count}',
                                                  callback_data='down')
            await bot.answer_callback_query(callback_query.id, cache_time=cache_time,
                                            text=f'{text.INLINE_TEXT["thumbDown"]} {text.INLINE_TEXT["fail"]}')

        if dislike_button is not None:
            inline_keyboard = InlineKeyboardMarkup(row_width=2)
            like_button = InlineKeyboardButton(f'{text.INLINE_TEXT["thumbUp"]}{likes_count}', callback_data='up')
            inline_keyboard.add(like_button, dislike_button)
            await edit_reply_markup(inline_keyboard, message_id)

            return AnswerCallbackQuery(callback_query.id, cache_time=cache_time,
                                       text=f'{text.INLINE_TEXT["thumbDown"]} {text.INLINE_TEXT["fail"]}')

        db.add_user_reaction(message_id, user_id, action='push', reaction='dislikes')
        await bot.answer_callback_query(callback_query.id, cache_time=cache_time,
                                        text=f'{text.INLINE_TEXT["thumbDown"]} {text.INLINE_TEXT["success"]}')
        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        like_button = InlineKeyboardButton(f'{text.INLINE_TEXT["thumbUp"]}{likes_count}', callback_data='up')
        dislike_button = InlineKeyboardButton(f'{text.INLINE_TEXT["thumbDown"]}{dislikes_count + 1}',
                                              callback_data='down')
        inline_keyboard.add(like_button, dislike_button)
        await edit_reply_markup(inline_keyboard, message_id)

        return
    except aiogram.utils.exceptions.InvalidQueryID:
        return AnswerCallbackQuery(callback_query.id, cache_time=cache_time, text=text.SMTH_WRONG)


# reaction: ban user
@dp.callback_query_handler(text='ban')
async def ban_user(callback_query: types.CallbackQuery):
    meta = callback_query.message.caption.split('|')
    username = meta[0]
    user_id = int(meta[1])
    db.ban_user(user_id)
    return AnswerCallbackQuery(callback_query.id, text=f'{text.USER_BANNED} {username}')


# reaction: remove post
@dp.callback_query_handler(text='remove')
async def remove_sugg_post(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    try:
        await bot.delete_message(SUGGEST_ID, message_id)
    except MessageCantBeDeleted as e:
        return AnswerCallbackQuery(callback_query.id, text=text.DELETE_FAIL)
    return AnswerCallbackQuery(callback_query.id, text=text.DELETED)


# reaction: post sugg content
@dp.callback_query_handler(text='post', run_task=True)  # TODO: подумать над рефакторингом
async def post_sugg_content(callback_query: types.CallbackQuery):
    message = callback_query.message
    try:
        if message.photo:
            img = message.photo
            file = await bot.get_file(img[-1].file_id)
            await bot.answer_callback_query(callback_query.id, text=text.POST_SOON)
            file_link = bot.get_file_url(file.file_path)
            tmp_img = 'tmp/tmp_image_out.jpg'
            if os.path.isfile(tmp_img):
                os.remove(tmp_img)

            try:
                img_convert(file_link, tmp_img)
            except Exception as e:
                logging.exception('ffmpeg error')
                return

            tg_upload = types.InputFile(tmp_img)

            response = await bot.send_photo(RECIPIENT_CHAT_ID, tg_upload, caption=sugg_post_description,
                                            reply_markup=inline_reaction)
            meta = message.caption.split('|')
            username = meta[0]
            user_id = meta[1]
            db.insert_post(message, response.message_id, username=username, user_id=user_id)

        if message.video:
            video = message.video
            file = await bot.get_file(video.file_id)
            await bot.answer_callback_query(callback_query.id, text=text.POST_SOON)
            file_link = bot.get_file_url(file.file_path)
            tmp_vid = 'tmp/tmp_video_out.mp4'
            if os.path.isfile(tmp_vid):
                os.remove(tmp_vid)

            try:
                video_convert(file_link, tmp_vid)
            except Exception as e:
                logging.exception('ffmpeg error')
                return

            tg_upload = types.InputFile(tmp_vid)

            response = await bot.send_video(RECIPIENT_CHAT_ID, tg_upload, caption=sugg_post_description,
                                            reply_markup=inline_reaction)
            meta = message.caption.split('|')
            username = meta[0]
            user_id = meta[1]
            db.insert_post(message, response.message_id, username=username, user_id=user_id)

        await remove_sugg_post(callback_query)
    except Exception as e:
        return AnswerCallbackQuery(callback_query.id, text=text.POST_FAIL)


# Необходимая процедура связанная с особенностью АПИ телеграма
async def edit_reply_markup(inline_kb_full, message_id):
    try:
        await bot.edit_message_reply_markup(RECIPIENT_CHAT_ID, message_id, reply_markup=inline_kb_full)
    except MessageNotModified:
        pass
