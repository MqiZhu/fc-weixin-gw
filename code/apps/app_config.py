# coding=utf-8
from handler.dispatch import RocketMQDispatcher, RedisDispatcher, Dispatcher
from common.redis_cli import get_redis_client
_apps = {
    "yuanquanlaotu": {
        "TOKEN": "1234567",
        "AES_KEY": "",
        "APP_ID": "wx22ce550ecb8bb312",
        "dispatcher": RedisDispatcher(get_redis_client, 10, "yuanquanlaotu"),
        "passive": True
    },
    "yuanquanlaotu_mq": {
        "TOKEN": "1234567",
        "AES_KEY": "",
        "APP_ID": "wx22ce550ecb8bb312",
        "dispatcher": RocketMQDispatcher("http://1357979013296492.mqrest.cn-hangzhou-internal.aliyuncs.com",
                                         "LTAI5tKwQQiKjzuXDRSP3hF5", "PPQgvhBhuIahji8zh01v0d3vMsoq5q"),
        "passive": True
    },
    "zhenhuashuju_mq": {
        "passive": True,
        "dispatcher": RocketMQDispatcher("http://1357979013296492.mqrest.cn-hangzhou-internal.aliyuncs.com",
                                         "LTAI5tKwQQiKjzuXDRSP3hF5", "PPQgvhBhuIahji8zh01v0d3vMsoq5q"),
    },
    "test_qa": {
        "TOKEN": "1234567",
        "AES_KEY": "",
        "APP_ID": "wx22ce550ecb8bb312",
        "dispatcher": RedisDispatcher(get_redis_client, 10, "yuanquanlaotu"),
        "passive": False
    },
    "greatleapaiKL": {
        "TOKEN": "wearegreatleapai",
        "AES_KEY": "",
        "APP_ID": "wx3a90ccc2d789c942",
        "dispatcher": RedisDispatcher(get_redis_client, 10, "yuanquanlaotu"),
        "passive": True
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


def get_dispatcher_by_name(name: str) -> Dispatcher:
    return _apps[name]["dispatcher"]


def GetAppAndSecretByName(name: str):
    appC = _apps.get(name)
    if appC == None:
        return "", ""

    return appC["APP_ID"], appC["APP_SECRET"]
