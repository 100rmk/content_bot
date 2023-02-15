from aiogram import types, Dispatcher

from db.fsm import GroupState
from etc.config import Commands


def register_handlers(dispatcher: Dispatcher):
    _commands(dispatcher)
    _content(dispatcher)
    _callbacks(dispatcher)


def _commands(dispatcher: Dispatcher):
    from handlers.commands import start, unban, info, advertisement, commands
    dispatcher.register_message_handler(start, commands=['start'])
    Commands.default.append(('/start', start.__doc__))
    dispatcher.register_message_handler(info, commands=['info'])
    Commands.default.append(('/info', info.__doc__))
    dispatcher.register_message_handler(commands, commands=['commands'])
    Commands.default.append(('/commands', commands.__doc__))

    dispatcher.register_message_handler(unban, commands=['unban'], is_admin=True)
    Commands.admins.append(('/unban', unban.__doc__))
    dispatcher.register_message_handler(advertisement, commands=['ad'], is_admin=True)
    Commands.admins.append(('/ad', advertisement.__doc__))

    Commands.init_roles()


def _content(dispatcher):
    from handlers.content import suggest_posts, video_post, img_post, ad_link, ad_post
    dispatcher.register_message_handler(
        suggest_posts,
        content_types=[types.ContentType.VIDEO, types.ContentType.PHOTO],
        is_admin=False,
        has_nickname=True,
    )
    dispatcher.register_message_handler(
        video_post,
        content_types=[types.ContentType.VIDEO, types.ContentType.ANIMATION],
        is_admin=True,
        run_task=True,
    )
    dispatcher.register_message_handler(img_post, content_types=types.ContentType.PHOTO, is_admin=True)
    dispatcher.register_message_handler(ad_link, state=GroupState.advertising_link, is_admin=True)
    dispatcher.register_message_handler(
        ad_post,
        state=GroupState.advertising_inline,
        content_types=types.ContentType.ANY,
        is_admin=True,
    )


def _callbacks(dispatcher):
    from handlers.callback import callback_liking, callback_disliking, ban_user, remove_sugg_post, post_sugg_content
    dispatcher.register_callback_query_handler(callback_liking, text='up')
    dispatcher.register_callback_query_handler(callback_disliking, text='down')
    dispatcher.register_callback_query_handler(ban_user, text='ban')
    dispatcher.register_callback_query_handler(remove_sugg_post, text='remove')
    dispatcher.register_callback_query_handler(post_sugg_content, text='post', run_task=True)
