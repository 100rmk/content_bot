from aiogram import types, Dispatcher

from db.fsm import GroupState


def register_handlers(dispatcher: Dispatcher):
    _commands(dispatcher)
    _content(dispatcher)
    _callbacks(dispatcher)


def _commands(dp):
    from handlers.commands import start, unban, info, advertisement
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(info, commands=['info'])
    dp.register_message_handler(unban, commands=['unban'], is_admin=True)
    dp.register_message_handler(advertisement, commands=['ad'], is_admin=True)


def _content(dp):
    from handlers.content import suggest_posts, video_post, img_post, ad_link, ad_post, instagram_post
    dp.register_message_handler(
        suggest_posts,
        content_types=[types.ContentType.VIDEO, types.ContentType.PHOTO],
        is_admin=False,
        has_nickname=True,
    )
    dp.register_message_handler(
        video_post,
        content_types=[types.ContentType.VIDEO, types.ContentType.ANIMATION],
        is_admin=True,
        run_task=True,
    )
    dp.register_message_handler(img_post, content_types=types.ContentType.PHOTO, is_admin=True)
    dp.register_message_handler(ad_link, state=GroupState.advertising_link, is_admin=True)
    dp.register_message_handler(
        ad_post,
        state=GroupState.advertising_inline,
        content_types=types.ContentType.ANY,
        is_admin=True,
    )
    dp.register_message_handler(
        instagram_post,
        content_types=types.ContentType.TEXT,
        regexp=r'(?:(?:http|https):\/\/)?(?:www.)?(?:instagram.com|instagr.am|instagr.com)\/(\w+)',
        is_moder=True,
        run_task=True,
    )


def _callbacks(dp):
    from handlers.callback import callback_liking, callback_disliking, ban_user, remove_sugg_post, post_sugg_content
    dp.register_callback_query_handler(callback_liking, text='up')
    dp.register_callback_query_handler(callback_disliking, text='down')
    dp.register_callback_query_handler(ban_user, text='ban')
    dp.register_callback_query_handler(remove_sugg_post, text='remove')
    dp.register_callback_query_handler(post_sugg_content, text='post', run_task=True)
