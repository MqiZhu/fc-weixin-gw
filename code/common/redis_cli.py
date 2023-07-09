# coding=utf-8

import redis
import json

redis_cli = redis.Redis("r-bp1br74bgybp3csnhf.redis.rds.aliyuncs.com",
                        6379, username='r-bp1br74bgybp3csnhf', password='Redis_Bot')
#redis_cli = redis.Redis("127.0.0.1", 6379, username='', password='')



def get_redis_client():
    return redis_cli
