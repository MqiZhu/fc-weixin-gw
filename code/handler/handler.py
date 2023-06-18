# coding=utf-8
from apps.client_manager import ZyWxClient
from handler.msg import UMsg
import requests

from common.logger import get_logger


class Handler(object):
    def __init__(self) -> None:
        pass

    def handle_user_msg(self, wxMsg):
        pass

    def handle_push_msg(self, wxMsg):
        pass


class EchoHandler(Handler):
    def __init__(self, client: ZyWxClient) -> None:
        super().__init__()
        self.client = client

    def Handle(self, msg):
        self.client.message.send_text(msg.source, "hello world!")
        print("hello world!")


class ToWxApiHandler(Handler):

    def __init__(self, url, client: ZyWxClient):
        self.url = url
        self.client = client

    def Handle(self, msg):
        logger = get_logger()

        umsg = UMsg()
        umsg.parseFromJson(msg)

        logger.info("Call Login:url={}, umsg={}".format(
            self.url, umsg.toJson()))
        rsp = requests.post(self.url, json=umsg.toJsonDict())

        from handler.cache import store_cache
        store_cache(umsg.appId, umsg.contactId, umsg.msgId, rsp.text)
        # dosomething
        self.client.message.send_text(umsg.contactId, rsp.text)
