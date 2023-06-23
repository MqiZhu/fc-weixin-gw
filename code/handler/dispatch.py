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
import time
import json
import sys

from mq_http_sdk.mq_exception import MQExceptionBase
from mq_http_sdk.mq_producer import *
from mq_http_sdk.mq_client import *
import time


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
            return None

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
            logger.warn("unknown msg", msg.type)
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
        return create_reply(None).render()


class MQDispatcher(Dispatcher):

    def __init__(self, url, user, passwd) -> None:
        super().__init__()
        self.url = url
        self.user = user
        self.passwd = passwd

    def DispatchMsg(self, app_id: str, msg: BaseMessage):
        logger = get_logger()
        logger.info("DispatchMsg")

        if msg.type != 'text':
            logger.warn("unknown msg", msg.type)
            return create_reply("暂时仅支持文字聊天哦！")

        t_msg: TextMessage = msg

        msg_id = msg.id
        msgType = msg.type
        source = msg.source
        target = msg.target
        content = t_msg.content

        from handler.cache import try_get_from_cache
        from apps.app_config import is_passive

        if is_passive(app_id):
            hit, rsp = try_get_from_cache(app_id, source, msg_id)
            logger.info("rsp pre result:{},{}".format(hit, rsp))
            if hit:
                return create_reply(rsp, msg).render()

        data = {
            "user_id": source,
            "app_id": app_id,
            "msg_id": msg_id,
            "to": target,
            "msg": content,
            "type": msg.type,
            "time": int(time.time())
        }

        logger.info("before sending!!!")
        if not self.send_to_queue(source, data):
            logger.warn("dispatch failed")
            return None
        logger.info("sending ok!")

        if is_passive(app_id):
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
        return create_reply(None).render()

    def send_to_queue(self, source: str, data: dict) -> bool:
        logger = get_logger()
        logger.error("not impleted")


class RocketMQDispatcher(MQDispatcher):

    def __init__(self, url, user, passwd, topic='weixin_chat_msg') -> None:
        super().__init__(url, user, passwd)
        self.topic = topic
        self.mq_client = MQClient(
            # 设置HTTP协议客户端接入点，进入云消息队列 RocketMQ 版控制台实例详情页面的接入点区域查看。
            self.url,
            self.user,
            self.passwd,
        )
        self.producer = self.mq_client.get_producer(
            "MQ_INST_1357979013296492_BYlRvnCy", topic)

    def send_to_queue(self, source: str, data: dict) -> bool:
        logger = get_logger()
        logger.info("send_to_queue")
        try:
            msg = TopicMessage(
                # 消息内容。
                json.dumps(data),
                # 消息标签。
                "tag")
            # 设置消息的自定义属性。
            msg.put_property("test", "test")
            # 设置消息的Key。
            msg.set_message_key("MessageKey")
            msg.set_sharding_key(source)
            ret_msg = self.producer.publish_message(msg)
            logger.info("ret_msg{}".format(ret_msg))
        except MQExceptionBase as e:
            if e.type == "TopicNotExist":
                logger.error("topic not exist!!, need create")
            logger.error("failed, {}".format(e))
            return False

        logger.info("send to queue from: {}".format(source))
        return True
