# coding=utf-8

import redis

redis_cli = redis.Redis("r-bp1br74bgybp3csnhf.redis.rds.aliyuncs.com",
                        6379, username='r-bp1br74bgybp3csnhf', password='Redis_Bot')


def get_redis_client():
    return redis_cli
