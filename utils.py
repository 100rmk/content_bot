import ffmpeg


async def video_convert(tmp_vid):
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


async def img_convert(tmp_img):
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
