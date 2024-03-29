FROM python:3.11.2-alpine

LABEL maintainer="Dmitrii Nesvit. mail: hinesqui@gmail.com"

WORKDIR /usr/src/app

ENV API_TOKEN ''
ENV WEBHOOK_URL ''
ENV WEBAPP_HOST ''
ENV WEBAPP_PORT ''

COPY . .

RUN apk add --update --no-cache \
        musl coreutils build-base nasm ca-certificates curl tar \
        openssl-dev zlib-dev yasm-dev lame-dev freetype-dev opus-dev \
        rtmpdump-dev x264-dev x265-dev xvidcore-dev libass-dev libwebp-dev \
        libvorbis-dev libogg-dev libtheora-dev libvpx-dev \
    # build and install ffmpeg
    && FFMPEG_VER=5.0 \
    && pip install --no-cache-dir -r requirements.txt \
    && curl -s http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VER}.tar.gz | tar zxvf - -C . \
    && cd ffmpeg-${FFMPEG_VER} \
    && ./configure \
        --disable-debug --enable-version3 --enable-small --enable-gpl \
        --enable-nonfree --enable-postproc --enable-openssl \
        --enable-libfreetype --enable-libmp3lame \
        --enable-libx264 --enable-libx265 --enable-libopus --enable-libass \
        --enable-libwebp --enable-librtmp --enable-libtheora \
        --enable-libvorbis --enable-libvpx --enable-libxvid \
    && make -j"$(nproc)" install \
    && cd .. \
    && rm -rf ffmpeg-${FFMPEG_VER} \
    # cleanup
    && apk del --purge \
        coreutils build-base nasm curl tar openssl-dev zlib-dev yasm-dev \
        lame-dev freetype-dev opus-dev xvidcore-dev libass-dev libwebp-dev \
        libvorbis-dev libogg-dev libtheora-dev libvpx-dev \
    && apk add --no-cache \
        zlib lame freetype faac opus xvidcore libass libwebp libvorbis libogg \
        libtheora libvpx \
    && rm -rf /var/cache/apk/*
# fix "TypeError: duplicate base class TimeoutError" exception in aioredis 2.0.1(latest) lib for python 3.11.2
# TODO: aioredis is in archive, replace with redis
RUN sed -i 's/class TimeoutError(asyncio.TimeoutError, builtins.TimeoutError, RedisError):/class TimeoutError(asyncio.TimeoutError, RedisError):/g' /usr/local/lib/python3.11/site-packages/aioredis/exceptions.py

CMD [ "python", "./main.py" ]
