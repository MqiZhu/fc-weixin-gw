# coding=utf-8
from handler.msg import UMsg
from wechatpy.messages import BaseMessage, TextMessage
import threading
from handler.handler import EchoHandler
from redis import Redis
from wechatpy import WeChatClient, create_reply
import queue
from common.redis_cli import get_redis_client
from common.logger import get_logger


class Dispatcher(object):
    def DispatchMsg(self, appName: str, msg: BaseMessage):
        pass

    def createWorker(self, i):
        pass


class MemoryDispatcher(Dispatcher):

    def __init__(self, queueCnt: int) -> None:
        self.queCnt = queueCnt
        self.ques = []
        for i in range(0, queueCnt):
            self.ques.append(queue.Queue(10000))
            self.createWorker(i)
        self.handler = EchoHandler(WeChatClient(
            "wx22ce550ecb8bb312", "5393aa38f70ce352bcf99b0e9031a0f2"))

    def createWorker(self, i):
        logger = get_logger()

        def func():
            q = self.ques[i]
            logger.info("Worker Started:", i)
            while True:
                msg = q.get()
                msgId = msg.id
                msgType = msg.type
                source = msg.source
                target = msg.target
                logger.info("Queue Get:", i, msgId, msgType, source, target)

                if self.handler != None:
                    self.handler.Handle(msg)
                    logger.debug("Queue handle:", i, msgId,
                                 msgType, source, target)

        threading.Thread(target=func, daemon=True).start()

    def DispatchMsg(self, appName: str, msg: BaseMessage):
        logger = get_logger()
        if msgType != 'text':
            logger.warn("unknown msg", msgType)
            return

        m: TextMessage = msg
        msgId = m.id
        msgType = m.type
        source = m.source
        target = m.target

        from handler.cache import try_get_from_cache
        from apps.app_config import is_passive

        if is_passive(appName):
            hit, rsp = try_get_from_cache(appName, source, msgId)
            if hit:
                return create_reply(rsp).render()

        ha = hash(source) % self.queCnt
        logger.debug("EnQueue:", ha, msgId, msgType, source, target)

        u = UMsg(appName, source, target, msgId, msgType, m.content)
        self.ques[ha].put(msg)

        if is_passive(appName):
            import time
            time.sleep(1)
            hit, rsp = try_get_from_cache(appName, source, msgId)
            if hit:
                return create_reply(rsp).render()
            return None

        return create_reply(None).render()


class RedisDispatcher(Dispatcher):
    def __init__(self, redis: Redis, queueCnt, prefix) -> None:
        self.redis_cli = get_redis_client()
        self.quecnt = queueCnt
        self.prefix = prefix

    def DispatchMsg(self, app_id: str, msg: BaseMessage):
        logger = get_logger()
        if msg.type != 'text':
            logger.warn("unknown msg", msgType)
            return

        tMsg: TextMessage = msg
        msg_id = msg.id
        msgType = msg.type
        source = msg.source
        target = msg.target
        content = tMsg.content

        from handler.cache import try_get_from_cache
        from apps.app_config import is_passive

        if is_passive(app_id):
            hit, rsp = try_get_from_cache(app_id, source, msg_id)
            logger.info("rsp pre result:{},{}".format(hit, rsp))
            if hit:
                return create_reply(rsp, msg).render()

        ha = hash(source) % self.quecnt

        key = "{}-{}-{}".format(self.prefix, "In", ha)
        u = UMsg(app_id, source, target, msg_id, msgType, content)

        logger.info("redis publish: key={}, source={}, msgId={}".format(
            key, source, msg_id))
        self.redis_cli.publish(key, u.toJson())

        if is_passive(app_id):
            import time
            for i in range(6):
                time.sleep(1)
                hit, rsp = try_get_from_cache(app_id, source, msg_id)
                if hit:
                    logger.info("passive reply text:app_id={}, source={}, msg_id={}".format(
                        app_id, source, msg_id))
                    return create_reply(rsp, msg).render()

            return None
        logger.info("active reply none:app_id={}, source={}, msg_id={}".format(
            app_id, source, msg_id))
        return create_reply("思考中..稍等", msg).render()
