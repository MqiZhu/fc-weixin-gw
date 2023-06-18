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
        self.appId = data.get("appId", '')
        self.contactId = data.get("userId", '')
        self.msgId = data.get("msgId", '')
        self.msgType = data.get("msgType", 0)
        self.msgTime = data.get("msgTime", 0)
        self.msgContent = data.get("content", 0)
        self.meta = data["meta"]

    def toJsonDict(self) -> dict:
        data = {
            "appId": self.appId,
            "userId": self.contactId,
            "msgId": self.msgId,
            "msgTime": self.msgTime,
            "meta": self.meta,
            "content": self.msgContent,
        }
        return data

    def toJson(self) -> str:
        return json.dumps(self.toJsonDict())

    def GetContactId(self):
        return self.contactId
