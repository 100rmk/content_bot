import json
from typing import Literal, Tuple, Optional

from db.BaseModel import BaseDB, AsyncBaseCache
from etc.config import Config


async def add_reaction(
        *,
        user_id: int,
        reaction_name: Literal['likes', 'dislikes'],
        post: dict,
        cache: AsyncBaseCache,
        post_id: int,
) -> Tuple[int, int]:
    main_reaction: list = post[reaction_name]
    secondary_reaction: list = post['dislikes' if reaction_name == 'likes' else 'likes']

    if all((user_id not in main_reaction, user_id not in secondary_reaction)):
        main_reaction.append(user_id)
    elif user_id in secondary_reaction:
        secondary_reaction.remove(user_id)
        main_reaction.append(user_id)
    else:
        main_reaction.remove(user_id)

    await cache.set(
        key=f'{Config.bot_name}:post_id:{post_id}',
        value=json.dumps({'likes': post['likes'], 'dislikes': post['dislikes']})
    )
    return len(main_reaction), len(secondary_reaction)


async def check_cached_post(*, message_id: int, db: BaseDB, cache: AsyncBaseCache) -> Optional[dict]:
    if not (cached_reactions := await cache.get(key=f'{Config.bot_name}:post_id:{message_id}')):
        post = db.get_post(message_id=message_id)
        if post:
            await cache.set(
                key=f'{Config.bot_name}:post_id:{message_id}',
                value=json.dumps({'likes': post['likes'], 'dislikes': post['dislikes']})
            )
            return post
        else:
            return None
    else:
        return json.loads(cached_reactions)
