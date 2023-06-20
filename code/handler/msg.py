# coding=utf-8
import json


class UMsg(object):

    def __init__(self, appId: str = '', userId="", target="", msgid="", msgtype="", content="", msgTime="", meta: dict = None) -> None:
        self.appId = appId
        self.contactId = userId
        self.msgId = msgid
        self.msgType = msgtype
        self.msgContent = content
        self.msgTime = msgTime
        self.meta = meta or {}
        self.target = target

    # todo error handling
    def parseFromJson(self, _json: str):
        data: map = json.loads(_json)
        self.appId = data.get("app_id", '')
        self.contactId = data.get("user_id", '')
        self.msgId = data.get("msg_id", '')
        self.msgType = data.get("type", 0)
        self.msgTime = data.get("time", 0)
        self.msgContent = data.get("msg", 0)
        self.meta = data.get("meta", 0)

    def toJsonDict(self) -> dict:
        data = {
            "app_id": self.appId,
            "user_id": self.contactId,
            "msg_id": self.msgId,
            "time": self.msgTime,
            "meta": self.meta,
            "msg": self.msgContent,
        }
        return data

    def toJson(self) -> str:
        return json.dumps(self.toJsonDict())

    def GetContactId(self):
        return self.contactId
