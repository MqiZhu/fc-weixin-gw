# coding=utf-8
from handler.msg import UMsg
from wechatpy.messages import BaseMessage, TextMessage
import threading
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
    def dispatch_wxmp_msg(self, app_id: str, msg: BaseMessage):
        pass

    def dispatch_data(self, app_id: str, source: str, msg_id: str, data: dict):
        pass


class MQDispatcher(Dispatcher):

    def __init__(self, url, user, passwd) -> None:
        super().__init__()
        self.url = url
        self.user = user
        self.passwd = passwd

    def dispatch_wxmp_msg(self, app_id: str, msg: BaseMessage, extra_meta={}):
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

        data = {
            "user_id": source,
            "app_id": app_id,
            "msg_id": msg_id,
            "to": target,
            "msg": content,
            "type": msg.type,
            "time": int(time.time()),
            "meta": extra_meta
        }

        return self.dispatch_data(app_id, source, msg_id, data)

    def dispatch_data(self, app_id, source, msg_id, data):
        logger = get_logger()
        from handler.cache import try_get_from_cache
        from apps.app_config import is_passive

        if is_passive(app_id):
            hit, rsp = try_get_from_cache(app_id, source, msg_id)
            logger.info("rsp pre result:{},{}".format(hit, rsp))
            if hit:
                return True, rsp

        if not self.send_to_queue(source, msg_id, data):
            logger.warn("dispatch failed")
            return False, None

        if is_passive(app_id):
            for i in range(6):
                time.sleep(1)
                hit, rsp = try_get_from_cache(app_id, source, msg_id)
                if hit:
                    logger.info("passive reply text:app_id={}, source={}, msg_id={}".format(
                        app_id, source, msg_id))
                    return True, rsp

            return False, None
        logger.info("active reply none:app_id={}, source={}, msg_id={}".format(
            app_id, source, msg_id))
        return True, None

    def send_to_queue(self, source: str, msg_id: str, data: dict) -> bool:
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

    def send_to_queue(self, source: str, msg_id: str, data: dict) -> bool:
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


class RedisDispatcher(MQDispatcher):
    def __init__(self, redis: Redis, queueCnt, prefix) -> None:
        self.redis_cli = get_redis_client()
        self.quecnt = queueCnt
        self.prefix = prefix

    def send_to_queue(self, source: str,  msg_id: str, data: dict) -> bool:

        logger = get_logger()
        ha = hash(source) % self.quecnt
        key = "{}-{}-{}".format(self.prefix, "In", ha)

        logger.info("redis publish: key={}, source={}, msgId={}".format(
            key, source, msg_id))
        self.redis_cli.publish(key, json.dumps(data))
        return True
