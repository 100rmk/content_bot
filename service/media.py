import logging
import os

import ffmpeg
from aiogram import types

from etc.exceptions import FfmpegException
from main import bot


async def upload_img(*, img):
    file = await bot.get_file(img[-1].file_id)
    file_link = bot.get_file_url(file.file_path)
    tmp_img = 'tmp/tmp_image_out.jpg'
    if os.path.isfile(tmp_img):
        os.remove(tmp_img)

    img_convert(link=file_link, tmp_file=tmp_img)
    return types.InputFile(tmp_img)


async def upload_video(*, video):
    file = await bot.get_file(video.file_id)
    file_link = bot.get_file_url(file.file_path)

    tmp_vid = 'tmp/tmp_video_out.mp4'
    if os.path.isfile(tmp_vid):
        os.remove(tmp_vid)

    video_convert(link=file_link, tmp_file=tmp_vid)
    return types.InputFile(tmp_vid)


def video_convert(*, link, tmp_file):
    logging.info('ffmpeg starts converting video')
    try:
        in_file = ffmpeg.input(link)

        # Проверка есть ли аудио поток в видео
        audio_stream = [i for i in ffmpeg.probe(link).get('streams') if i.get('codec_type') == 'audio']
        audio = ''
        if audio_stream:
            ffmpeg.input(in_file.audio)
            audio = 'a'

        (
            ffmpeg.drawtext(in_file,
                            text='t.me/vidmem',  # TODO: в text вынести в .env
                            fontfile='other/font.ttf',
                            fontsize='(h/25)',
                            fontcolor='#d2d2e0',
                            fix_bounds=True,
                            x='if(lt(mod(t,20),10),w,W-w-10)',
                            y='if(lt(mod(t,20),10),h/2,H-h-10)').output(tmp_file, map=audio).run(quiet=True)
        )
        logging.info('video  converting  complete')
    except Exception as e:
        raise FfmpegException from e


def img_convert(*, link, tmp_file):
    logging.info('ffmpeg starts converting photo')
    try:
        in_file = ffmpeg.input(link)
        (
            ffmpeg.drawtext(in_file,
                            text='t.me/vidmem',
                            fontfile='other/font.ttf',
                            fontsize='(h/25)',
                            fontcolor='#d2d2e0',
                            fix_bounds=True,
                            x='if(lt(mod(t,20),10),w,W-w-10)',
                            y='if(lt(mod(t,20),10),h/2,H-h-10)').output(tmp_file).run(quiet=True)
        )
        logging.info('photo  converting  complete')
    except Exception as e:
        raise FfmpegException from e
