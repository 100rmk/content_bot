import logging
import ffmpeg
import urllib.request
import io


def video_convert(link, tmp_file):
    logging.info('ffmpeg starts converting video')
    in_file = ffmpeg.input(link)

    # Проверка есть ли аудио поток в видео
    audio_stream = [i for i in ffmpeg.probe(link).get('streams') if i.get('codec_type') == 'audio']
    audio = ''
    if audio_stream:
        ffmpeg.input(in_file.audio)
        audio = 'a'

    (
        ffmpeg
            .drawtext(in_file, text='t.me/vidmem', fontfile='other/font.ttf', fontsize='(h/25)',
                      fontcolor='#d2d2e0', fix_bounds=True,
                      x='if(lt(mod(t,20),10),w,W-w-10)',
                      y='if(lt(mod(t,20),10),h/2,H-h-10)')
            .output(tmp_file, map=audio)
            .run(quiet=True)
    )
    logging.info('video  converting  complete')


def img_convert(link, tmp_file):
    logging.info('ffmpeg starts converting photo')
    in_file = ffmpeg.input(link)
    (
        ffmpeg
            .drawtext(in_file, text='t.me/vidmem', fontfile='other/font.ttf', fontsize='(h/25)',
                      fontcolor='#d2d2e0', fix_bounds=True,
                      x='if(lt(mod(t,20),10),w,W-w-10)',
                      y='if(lt(mod(t,20),10),h/2,H-h-10)')
            .output(tmp_file)
            .run(quiet=True)
    )
    logging.info('photo  converting  complete')


def get_content_bytes(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        ds = io.BytesIO(resp.read())
    return ds
