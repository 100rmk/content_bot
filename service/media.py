import asyncio
import logging
import os

import ffmpeg
from aiogram import types

from etc.exceptions import FfmpegException
from main import bot


async def upload_img(*, img, watermark_text: str):
    file = await bot.get_file(img[-1].file_id)
    file_link = bot.get_file_url(file.file_path)
    tmp_img = 'tmp/tmp_image_out.jpg'
    if os.path.isfile(tmp_img):
        os.remove(tmp_img)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _img_convert, file_link, tmp_img, watermark_text)
    return types.InputFile(tmp_img)


async def upload_video(*, video, watermark_text: str):
    file = await bot.get_file(video.file_id)
    file_link = bot.get_file_url(file.file_path)

    tmp_vid = 'tmp/tmp_video_out.mp4'
    if os.path.isfile(tmp_vid):
        os.remove(tmp_vid)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _video_convert, file_link, tmp_vid, watermark_text)
    return types.InputFile(tmp_vid)


def _video_convert(link: str, tmp_file: str, watermark_text: str):
    logging.info('ffmpeg starts converting video')
    try:
        in_file = ffmpeg.input(link)

        # Проверка есть ли аудио поток в видео
        audio_stream = [i for i in ffmpeg.probe(link).get('streams') if i.get('codec_type') == 'audio']
        audio = ''
        if audio_stream:
            ffmpeg.input(in_file.audio)
            audio = 'a'

        ffmpeg.drawtext(
            in_file,
            text=watermark_text,
            fontfile='other/font.ttf',
            fontsize='main_w/20',
            fontcolor='white@0.2',
            bordercolor='black@0.2',
            borderw=2,
            fix_bounds=True,
            y='(mod(2*n,h+th))',
            x='(w-text_w)/2',
        ).output(tmp_file, map=audio).run(quiet=True)
        logging.info('video  converting  complete')
    except Exception as e:
        raise FfmpegException from e


def _img_convert(link: str, tmp_file: str, watermark_text: str):
    logging.info('ffmpeg starts converting photo')
    try:
        in_file = ffmpeg.input(link)
        ffmpeg.drawtext(
            in_file,
            text=watermark_text,
            fontfile='other/font.ttf',
            fontsize='main_w/7',
            fontcolor='white@0.1',
            bordercolor='black@0.1',
            borderw=2,
            fix_bounds=True,
            x='(w-text_w)/2',
            y='(h-text_h)/2'
        ).output(tmp_file).run(quiet=True)
        logging.info('photo converting  complete')
    except Exception as e:
        raise FfmpegException from e
