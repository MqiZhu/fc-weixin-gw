# coding:utf-8
import logging

from redis import Redis
from common.redis_cli import get_redis_client
from handler.msg import UMsg
import apps.app_config as app_config
import threading
import time
from handler.handler import Handler
from wechatpy import WeChatClient
from common.logger import init_logger, get_logger


class RedisComsumer(object):
    def __init__(self, redis_client: Redis, prefix, i: int):

        self.redis_cli = redis_client
        self.prefix = prefix
        self.i = i

    def startWorker(self):
        logger = get_logger()
        key = "{}-{}-{}".format(self.prefix, "In", self.i)
        sub = self.redis_cli.pubsub()
        sub.subscribe(key)

        logger.info("startWorkder:".format(key))
        msg_stream = sub.listen()
        for msg in msg_stream:
            try:
                umsg = UMsg()
                try:
                    umsg.parseFromJson(msg["data"])
                except:
                    logger.error("pass err")
                    continue
                handler = app_config.GetHandlerByName(umsg.appId)
                if handler == None:
                    logger.error("not handled Msg".format(umsg.appId, msg))
                    continue

                handler.Handle(msg["data"])
            except Exception as e:
                logger.error(e)


if __name__ == "__main__":

    logger = init_logger("consumer")
    logger.setLevel(logging.DEBUG)

    c = get_redis_client()
    for i in range(10):
        comsumer = RedisComsumer(c, "yuanquanlaotu", i)
        threading.Thread(target=comsumer.startWorker, daemon=True).start()

    while (True):
        time.sleep(1)
