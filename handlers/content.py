from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sentry_sdk import capture_exception

from db.fsm import GroupState
from etc.config import Config
from etc.telegram import Buttons
from main import bot, db
from other import text
from service.media import upload_video, upload_img


# Предложка
async def suggest_posts(message: types.Message):
    db.add_user(user_id=message.from_user.id, username=message.from_user.username)
    user = db.get_user(user_id=message.from_user.id)
    posts_count = user.get('suggestions_count')

    if user.get('banned'):
        return SendMessage(chat_id=message.chat.id, text=text.MESSAGE_FOR_BANNED_USER)
    if posts_count == 0:
        return SendMessage(chat_id=message.chat.id, text=text.LIMIT_EXCEEDED)

    await bot.copy_message(
        chat_id=Config.suggest_group_id,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        disable_notification=True,
        caption=f'@{message.from_user.username}|{message.from_user.id}',
        reply_markup=Buttons.moderation
    )
    db.reduce_post_count(user_id=message.from_user.id)
    return SendMessage(chat_id=message.chat.id, text=f'{text.POST_ACCEPTED} {posts_count - 1}')


async def video_post(message: types.Message):
    video = message.video or message.animation
    wait_message = await bot.send_message(message.chat.id, text.PROCESSING)
    try:
        if Config.subscriber_group_id:
            await bot.copy_message(
                chat_id=Config.subscriber_group_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                caption=message.caption
            )

        uploaded = await upload_video(video=video, watermark_text=Config.watermark_text)
        await bot.delete_message(message.chat.id, wait_message.message_id)
        response = await bot.send_video(
            chat_id=Config.recipient_chat_id,
            video=uploaded,
            caption=message.caption,
            reply_markup=Buttons.reaction,
            height=video.height,
            width=video.width,
        )
        db.insert_post(
            file_id=video.file_id,
            id_=response.message_id,
            username=message.from_user.username,
            user_id=message.from_user.id,
            content_type='video'
        )
        return SendMessage(chat_id=message.chat.id, text='vidos zaletel')
    except (ValueError, Exception) as e:
        capture_exception(e)
        return SendMessage(chat_id=message.chat.id, text='something going wrong, look stacktrace')


async def img_post(message: types.Message):
    img = message.photo
    wait_message = await bot.send_message(message.chat.id, text.PROCESSING)
    try:
        if Config.subscriber_group_id:
            await bot.copy_message(
                chat_id=Config.subscriber_group_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                caption=message.caption
            )

        uploaded = await upload_img(img=img, watermark_text=Config.watermark_text)
        await bot.delete_message(message.chat.id, wait_message.message_id)
        response = await bot.send_photo(
            chat_id=Config.recipient_chat_id,
            photo=uploaded,
            caption=message.caption,
            reply_markup=Buttons.reaction
        )
        db.insert_post(
            file_id=img[-1].file_id,
            id_=response.message_id,
            username=message.from_user.username,
            user_id=message.from_user.id,
            content_type='photo'
        )

        return SendMessage(chat_id=message.chat.id, text='img zaletel')
    except (ValueError, Exception) as e:
        capture_exception(e)
        return SendMessage(chat_id=message.chat.id, text='something going wrong, look stacktrace')


async def ad_link(message: types.Message, state: FSMContext):  # TODO: проверку на ссылку
    url = message.text
    await state.update_data(ad_url=url)
    await message.answer(text.SEND_AD_POST)
    await GroupState.advertising_inline.set()


async def ad_post(message: types.Message, state: FSMContext):
    try:
        state_data = await state.get_data()
        inline_link = InlineKeyboardMarkup(row_width=1)
        # TODO: Добавить еще один стэйт для имени кнопки
        like_button = InlineKeyboardButton(text.AD_GOTO, url=state_data['ad_url'])
        inline_link.add(like_button)
        await bot.copy_message(
            chat_id=Config.recipient_chat_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            disable_notification=True,
            reply_markup=inline_link
        )
        await state.finish()
        return SendMessage(chat_id=message.chat.id, text=text.AD_POST_SENT)
    except (ValueError, Exception) as e:
        await state.finish()
        capture_exception(e)
        return SendMessage(chat_id=message.chat.id, text='something going wrong, look stacktrace')
