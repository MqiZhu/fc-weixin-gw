# coding=utf-8
from common.redis_cli import get_redis_client
import json
from common.logger import get_logger


def get_cache_key(app_id, contact_id, msg_id):
    key = "rs:{}-{}-{}".format(contact_id, msg_id, app_id)
    return key


def store_cache(app_id, contact_id, msg_id, rsp):
    logger = get_logger()

    client = get_redis_client()
    key = get_cache_key(app_id, contact_id, msg_id)
    data = {
        "msg": rsp
    }
    client.set(key, json.dumps(data), ex=10*60)
    logger.debug("store_cache:key={}, rsp={}".format(key, rsp))


def try_get_from_cache(app_id, contact_id, msg_id):
    logger = get_logger()

    client = get_redis_client()
    key = get_cache_key(app_id, contact_id, msg_id)

    rsp = client.get(key)

    if rsp != None and len(rsp) > 0:
        logger.debug("get_cache hit,key={}, rsp={}".format(key, str(rsp)))
        data = json.loads(rsp)
        return True, data["msg"]

    return False, None
