import aiogram
from aiogram import types
from aiogram.dispatcher.webhook import AnswerCallbackQuery
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageNotModified
from sentry_sdk import capture_exception

from main import bot, db, cache, logger
from etc.config import Config, sugg_post_description
from etc.telegram import Buttons
from other import text
from service.media import upload_img, upload_video
from service.reaction import check_cached_post, add_reaction

TG_CACHE_TIME = 8


# reaction: like
async def callback_liking(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id
    post = await check_cached_post(message_id=message_id, db=db, cache=cache)

    try:
        if not post:
            return AnswerCallbackQuery(callback_query.id, cache_time=TG_CACHE_TIME, text=text.LIKES_TIMEOUT)
        likes, dislikes = await add_reaction(
            user_id=user_id,
            reaction_name='likes',
            post=post, cache=cache,
            post_id=message_id
        )
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            cache_time=TG_CACHE_TIME,
            text=text.INLINE_TEXT["success"]
        )
        await edit_reply_markup(
            Buttons.edit_keyboard_button(likes_count=likes, dislikes_count=dislikes),
            message_id
        )

        return
    except aiogram.utils.exceptions.InvalidQueryID as e:
        capture_exception(e)
        return AnswerCallbackQuery(callback_query.id, cache_time=TG_CACHE_TIME, text=text.SMTH_WRONG)


# reaction: dislike
async def callback_disliking(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id
    post = await check_cached_post(message_id=message_id, db=db, cache=cache)

    try:
        if not post:
            return AnswerCallbackQuery(callback_query.id, cache_time=TG_CACHE_TIME, text=text.LIKES_TIMEOUT)

        dislikes, likes = await add_reaction(
            user_id=user_id,
            reaction_name='dislikes',
            post=post,
            cache=cache,
            post_id=message_id
        )
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            cache_time=TG_CACHE_TIME,
            text=text.INLINE_TEXT["success"]
        )
        await edit_reply_markup(
            Buttons.edit_keyboard_button(likes_count=likes, dislikes_count=dislikes),
            message_id
        )

        return
    except aiogram.utils.exceptions.InvalidQueryID as e:
        capture_exception(e)
        return AnswerCallbackQuery(callback_query.id, cache_time=TG_CACHE_TIME, text=text.SMTH_WRONG)


# reaction: ban user
async def ban_user(callback_query: types.CallbackQuery):
    meta = callback_query.message.caption.split('|')
    username = meta[0]
    user_id = int(meta[1])
    db.ban_user(user_id=user_id)
    return AnswerCallbackQuery(callback_query.id, text=f'{text.USER_BANNED} {username}')


# reaction: remove post
async def remove_sugg_post(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    try:
        await bot.delete_message(Config.suggest_group_id, message_id)
    except MessageCantBeDeleted as e:
        logger.info(e)
        return AnswerCallbackQuery(callback_query.id, text=text.DELETE_FAIL)
    return AnswerCallbackQuery(callback_query.id, text=text.DELETED)


# reaction: post sugg content
async def post_sugg_content(callback_query: types.CallbackQuery):
    message = callback_query.message
    await bot.answer_callback_query(callback_query.id, text=text.POST_SOON)
    file_id: int
    try:
        if Config.subscriber_group_id:
            await bot.copy_message(
                chat_id=Config.subscriber_group_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                caption=''
            )

        meta = message.caption.split('|')
        username = meta[0]
        user_id = meta[1]

        if photo := message.photo:
            tg_upload = await upload_img(img=photo, watermark_text=Config.watermark_text)
            response = await bot.send_photo(
                chat_id=Config.recipient_chat_id,
                photo=tg_upload,
                caption=sugg_post_description,
                reply_markup=Buttons.reaction
            )
            db.insert_post(
                file_id=photo[-1].file_id,
                id_=response.message_id,
                username=username,
                user_id=user_id,
                content_type='photo'
            )
        if video := message.video:
            tg_upload = await upload_video(video=video, watermark_text=Config.watermark_text)
            response = await bot.send_video(
                chat_id=Config.recipient_chat_id,
                video=tg_upload,
                caption=sugg_post_description,
                reply_markup=Buttons.reaction,
                height=video.height,
                width=video.width,
            )
            db.insert_post(
                file_id=video.file_id,
                id_=response.message_id,
                username=username,
                user_id=user_id,
                content_type='video'
            )

        await remove_sugg_post(callback_query)
    except (ValueError, Exception) as e:
        capture_exception(e)
        return AnswerCallbackQuery(callback_query.id, text=text.POST_FAIL)


# Необходимая процедура связанная с особенностью АПИ телеграма
async def edit_reply_markup(inline_kb_full, message_id):
    try:
        await bot.edit_message_reply_markup(
            chat_id=Config.recipient_chat_id,
            message_id=message_id,
            reply_markup=inline_kb_full
        )
    except MessageNotModified:
        logger.info('MessageNotModified, message_id: %d' % message_id)
