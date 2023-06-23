# coding=utf-8
from handler.handler import ToWxApiHandler, Handler
from handler.dispatch import RocketMQDispatcher, RedisDispatcher, Dispatcher
from apps.client_manager import ZyWxClient
from common.redis_cli import get_redis_client
_apps = {
    "yuanquanlaotu": {
        "TOKEN": "1234567",
        "AES_KEY": "",
        "APP_ID": "wx22ce550ecb8bb312",
        "APP_SECRET": "5393aa38f70ce352bcf99b0e9031a0f2",
        "dispatcher": RedisDispatcher(get_redis_client, 10, "yuanquanlaotu"),
        "passive": True
    },
    "yuanquanlaotu_mq": {
        "TOKEN": "1234567",
        "AES_KEY": "",
        "APP_ID": "wx22ce550ecb8bb312",
        "APP_SECRET": "5393aa38f70ce352bcf99b0e9031a0f2",
        "dispatcher": RocketMQDispatcher("http://1357979013296492.mqrest.cn-hangzhou.aliyuncs.com",
                                         "LTAI5tQnLUQgZSY9xy7rz2fL", "eIVPKw6R7eSv2Mt2EJ6ZJJ9Rh3HKqJ"),
        "passive": True
    },
    "test_qa": {
        "TOKEN": "1234567",
        "AES_KEY": "",
        "APP_ID": "wx22ce550ecb8bb312",
        "APP_SECRET": "5393aa38f70ce352bcf99b0e9031a0f2",
        "dispatcher": RedisDispatcher(get_redis_client, 10, "yuanquanlaotu"),
        "passive": False
    }
}


def is_passive(name: str) -> bool:
    appC = _apps.get(name, {})
    passive = appC.get("passive", False)
    return passive


def GetTokenByApp(name: str) -> str:

    appC = _apps.get(name)
    if appC == None:
        return "xxxxxx1"

    return appC["TOKEN"]


def GetAppAESKeyByName(name: str) -> str:
    appC = _apps.get(name)
    if appC == None:
        return "xxxxxx1"

    return appC["AES_KEY"]


def GetAppIdByName(name: str) -> str:

    appC = _apps.get(name)
    if appC == None:
        return "xxxxxx1"

    return appC["APP_ID"]


def GetDispatcherByName(name: str) -> Dispatcher:
    return _apps[name]["dispatcher"]


def GetAppAndSecretByName(name: str):
    appC = _apps.get(name)
    if appC == None:
        return "", ""

    return appC["APP_ID"], appC["APP_SECRET"]


def GetHandlerByName(name: str) -> Handler:
    appC = _apps.get(name)
    if appC == None:
        return None

    return appC["msgHandler"]
