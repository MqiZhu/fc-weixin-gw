# coding=utf-8
from wechatpy import WeChatClient
import threading
import time
import redis_lock
import json
from common.logger import get_logger


class ZyWxClient(WeChatClient):
    def __init__(self, appname: str, appId, appKey, redis):
        super().__init__(appId, appKey)
        self.fetch_access_token_lock = threading.Lock()
        self.redis = redis
        self.lock_key = "rl:{}:accesskey:lock".format(appname)
        self.redis_key = "rl:{}:accesskey".format(appname)

    def fetch_access_token(self):
        logger = get_logger()

        with self.fetch_access_token_lock:
            access_token = self.session.get(self.access_token_key)

            if access_token:
                if not self.expires_at:
                    return access_token
                timestamp = time.time()
                if self.expires_at - timestamp > 60:
                    return access_token

            with redis_lock.Lock(self.redis, self.lock_key):
                value = self.redis.get(self.redis_key)
                try:
                    data = json.loads(value)
                    access_token = data["token"]
                    expire_at = data["expire"]

                    if expire_at - timestamp > 60:
                        self.access_token = access_token

                    expire_in = expire_at - timestamp
                    self.session.set(
                        self.access_token_key,
                        access_token, expire_in)

                    return access_token

                except:
                    logger.error("Load Access Token From redis")

                super().fetch_access_token()

                access_token = self.session.get(self.access_token_key)
                expire_at = self.expires_at

                redis_data = {
                    "token": access_token,
                    "expire":  expire_at,
                }

                self.redis.set(self.redis_key, json.dumps(redis_data))
                logger.info("set redis data", json.dumps(data))
                return access_token
