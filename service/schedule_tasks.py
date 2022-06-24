import logging

import orjson
from pymongo import UpdateOne

from db.BaseModel import AsyncBaseCache, BaseDB


async def update_users_sugg_count(db: BaseDB):
    db.reset_post_count()
    logging.info('Posts count updated')


async def upload_cache_db(db: BaseDB, cache: AsyncBaseCache):
    bulk = []
    async for post_id in cache.redis.scan_iter('post_id:*'):
        _, id_ = post_id.split(':')
        reactions = await cache.get(key=f"post_id:{id_}")
        bulk.append(UpdateOne({"_id": int(id_)}, {"$set": orjson.loads(reactions)}), )
        await cache.delete(key=post_id)
        if len(bulk) == 500:
            logging.info('500 batch cache uploaded')
            result = db.bulk_push_reactions(reactions=bulk)
            logging.info(result.bulk_api_result)
            bulk.clear()
    if len(bulk) > 0:
        db.bulk_push_reactions(reactions=bulk)
        logging.info('cache uploaded')
