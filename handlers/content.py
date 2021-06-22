import logging
import os
from datetime import datetime

import ffmpeg
from aiogram import types
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from etc.config import RECIPIENT_CHAT_ID
from misc import dp, bot, db_posts


inline_kb_full = InlineKeyboardMarkup(row_width=2)
inline_btn_3 = InlineKeyboardButton(f'👍', callback_data='up')
inline_btn_4 = InlineKeyboardButton(f'👎', callback_data='down')
inline_kb_full.add(inline_btn_3, inline_btn_4)


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def file_work(message: types.Message):
    video = message.video
    file = await bot.get_file(video.file_id)

    await bot.download_file(file.file_path, destination=f'tmp/temp_video')
    tmp_vid = 'tmp/tmp_video_out.mp4'
    if os.path.isfile(tmp_vid):
        os.remove(tmp_vid)

    try:
        in_file = ffmpeg.input('tmp/temp_video')
        audio = ffmpeg.input(in_file.audio)
        (
            ffmpeg
                .drawtext(in_file, text='t.me/vidmem', fontfile='misc/font.ttf', fontsize='(h/25)',
                          fontcolor='#d2d2e0', fix_bounds=True,
                          x='if(lt(mod(t,20),10),w,W-w-10)',
                          y='if(lt(mod(t,20),10),h/2,H-h-10)')
                .output(tmp_vid, map='a')
                .run()
        )
    except Exception as e:
        logging.exception('ffmpeg error')
        return

    tg_upload = types.InputFile(tmp_vid)
    response = await bot.send_video(RECIPIENT_CHAT_ID, tg_upload, caption=message.caption, reply_markup=inline_kb_full)
    insert_post_db(message, response.message_id)
    return SendMessage(message.chat.id, f'{datetime.now()} vidos zaletel')


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def img_edit(message: types.Message):
    img = message.photo
    file = await bot.get_file(img[-1].file_id)

    await bot.download_file(file.file_path, destination=f'tmp/temp_image')
    tmp_img = 'tmp/tmp_image_out.jpg'
    if os.path.isfile(tmp_img):
        os.remove(tmp_img)

    try:
        in_file = ffmpeg.input('tmp/temp_image')
        (
            ffmpeg
                .drawtext(in_file, text='t.me/vidmem', fontfile='misc/font.ttf', fontsize='(h/25)',
                          fontcolor='#d2d2e0', fix_bounds=True,
                          x='if(lt(mod(t,20),10),w,W-w-10)',
                          y='if(lt(mod(t,20),10),h/2,H-h-10)')
                .output(tmp_img)
                .run()
        )
    except Exception as e:
        logging.exception('ffmpeg error')
        return

    tg_upload = types.InputFile(tmp_img)
    response = await bot.send_photo(RECIPIENT_CHAT_ID, tg_upload, caption=message.caption, reply_markup=inline_kb_full)
    insert_post_db(message, response.message_id)
    return SendMessage(message.chat.id, f'{datetime.now()} img zaletel')


def insert_post_db(message: types.Message, id):
    file_id = None
    if message.video:
        file_id = message.video.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id
    post = {
        '_id': id,
        'file_id': file_id,
        'user': message.from_user.username,
        'likes': [],
        'dislikes': []
    }
    db_posts.insert_one(post)
