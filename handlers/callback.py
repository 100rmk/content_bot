from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from etc.config import RECIPIENT_CHAT_ID
from misc import dp, db_posts, bot

import asyncio


@dp.callback_query_handler(text='up')
async def callback_query_handler(callback_query: types.CallbackQuery):
    request = db_posts.find_one({"_id": callback_query.message.message_id})
    likes_arr = request.get('likes')
    dislikes_arr = request.get('dislikes')
    user_id = callback_query.from_user.id
    likes_count = len(likes_arr)
    dislikes_count = len(dislikes_arr)
    inline_btn_3 = None

    if user_id in likes_arr:
        db_posts.update_one({'_id': callback_query.message.message_id},
                            {'$pull': {'likes': callback_query.from_user.id}})
        likes_count = likes_count - 1
        inline_btn_3 = InlineKeyboardButton(f'👍{likes_count}', callback_data='up')
    elif user_id in dislikes_arr:
        db_posts.update_one({'_id': callback_query.message.message_id},
                            {'$pull': {'dislikes': callback_query.from_user.id}})
        dislikes_count = dislikes_count - 1

    if inline_btn_3 is not None:
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        inline_btn_4 = InlineKeyboardButton(f'👎{dislikes_count}', callback_data='down')
        inline_kb_full.add(inline_btn_3, inline_btn_4)
        await bot.edit_message_reply_markup(RECIPIENT_CHAT_ID, callback_query.message.message_id,
                                            reply_markup=inline_kb_full)
        await asyncio.sleep(5)
        return

    db_posts.update_one({'_id': callback_query.message.message_id},
                        {'$push': {'likes': callback_query.from_user.id}})

    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_3 = InlineKeyboardButton(f'👍{likes_count + 1}', callback_data='up')
    inline_btn_4 = InlineKeyboardButton(f'👎{dislikes_count}', callback_data='down')
    inline_kb_full.add(inline_btn_3, inline_btn_4)
    await bot.edit_message_reply_markup(RECIPIENT_CHAT_ID, callback_query.message.message_id,
                                        reply_markup=inline_kb_full)

    await asyncio.sleep(5)
    return


@dp.callback_query_handler(text='down')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await asyncio.sleep(1)
    request = db_posts.find_one({"_id": callback_query.message.message_id})
    likes_arr = request.get('likes')
    dislikes_arr = request.get('dislikes')
    user_id = callback_query.from_user.id
    likes_count = len(likes_arr)
    dislikes_count = len(dislikes_arr)
    inline_btn_4 = None

    if user_id in likes_arr:
        db_posts.update_one({'_id': callback_query.message.message_id},
                            {'$pull': {'likes': callback_query.from_user.id}})
        likes_count = likes_count - 1
    elif user_id in dislikes_arr:
        db_posts.update_one({'_id': callback_query.message.message_id},
                            {'$pull': {'dislikes': callback_query.from_user.id}})
        dislikes_count = dislikes_count - 1
        inline_btn_4 = InlineKeyboardButton(f'👎{dislikes_count}', callback_data='down')

    if inline_btn_4 is not None:
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        inline_btn_3 = InlineKeyboardButton(f'👍{likes_count}', callback_data='up')
        inline_kb_full.add(inline_btn_3, inline_btn_4)
        await bot.edit_message_reply_markup(RECIPIENT_CHAT_ID, callback_query.message.message_id,
                                            reply_markup=inline_kb_full)
        await asyncio.sleep(5)
        return

    db_posts.update_one({'_id': callback_query.message.message_id},
                        {'$push': {'dislikes': callback_query.from_user.id}})

    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_btn_3 = InlineKeyboardButton(f'👍{likes_count}', callback_data='up')
    inline_btn_4 = InlineKeyboardButton(f'👎{dislikes_count + 1}', callback_data='down')
    inline_kb_full.add(inline_btn_3, inline_btn_4)
    await bot.edit_message_reply_markup(RECIPIENT_CHAT_ID, callback_query.message.message_id,
                                        reply_markup=inline_kb_full)

    await asyncio.sleep(5)
    return
