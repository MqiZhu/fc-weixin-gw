# coding=utf-8

import redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)


def get_redis_client():
    return r
