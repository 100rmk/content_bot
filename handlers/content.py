from misc import dp, bot
from aiogram import types
from aiogram.dispatcher.webhook import SendMessage
import os
import ffmpeg
from etc.config import CHAT_ID
from datetime import datetime


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def file_work(message: types.Message):
    video = message.video
    file = await bot.get_file(video.file_id)

    await bot.download_file(file.file_path, destination=f'tmp/temp_video')
    tmp_vid = 'tmp/tmp_video_out.mp4'
    if os.path.isfile(tmp_vid):
        os.remove(tmp_vid)

    in_file = ffmpeg.input('tmp/temp_video')
    audio = ffmpeg.input(in_file.audio)

    (
        ffmpeg
            .drawtext(in_file, text='t.me/vidmem', fontfile='misc/font.ttf', fontsize='(h/30)',
                      fontcolor='#d2d2e0', fix_bounds=True,
                      x='if(lt(mod(t,20),10),w,W-w-10)',
                      y='if(lt(mod(t,20),10),h,H-h-10)')
            .output(tmp_vid, map='a')
            .run()
    )

    tg_upload = types.InputFile(tmp_vid)
    await bot.send_video(CHAT_ID, tg_upload, caption=message.caption)
    return SendMessage(message.chat.id, f'{datetime.now()} vidos zaletel')


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def img_edit(message: types.Message):
    img = message.photo
    file = await bot.get_file(img[-1].file_id)

    await bot.download_file(file.file_path, destination=f'tmp/temp_image')
    tmp_img = 'tmp/tmp_image_out.jpg'
    if os.path.isfile(tmp_img):
        os.remove(tmp_img)

    in_file = ffmpeg.input('tmp/temp_image')

    (
        ffmpeg
            .drawtext(in_file, text='t.me/vidmem', fontfile='misc/font.ttf', fontsize='(h/30)',
                      fontcolor='#d2d2e0', fix_bounds=True,
                      x='if(lt(mod(t,20),10),w,W-w-10)',
                      y='if(lt(mod(t,20),10),h,H-h-10)')
            .output(tmp_img)
            .run()
    )
    tg_upload = types.InputFile(tmp_img)
    await bot.send_photo(CHAT_ID, tg_upload, caption=message.caption)  # , reply_markup=inline_kb_full)

    return SendMessage(message.chat.id, f'{datetime.now()} img zaletel')
