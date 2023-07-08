import json
from common.redis_cli import get_redis_client
from common.logger import get_logger

redis_cli = get_redis_client()
logger = get_logger()

default_bot = {
    "botName": "王露璐",
    "botSex": "女孩",
    "botAge": "23",
    "botTask": "九梦仙域_魂天",
    "botWxId": "yuanquan"
}
default_game = {
    "gameName": "九梦仙域_魂天",
    "gameUrl": "https://p.daimiaohudong.cn/Mobile/Promotion/code?spm=tvBACk",
    "gameBonus": "开局赠送1亿元宝+300绑定仙玉+初级羽翼、法宝精华+后续各种等级材料大礼i包，每天打佧礼i包",
    "gameFeature": "九梦仙域是一款多人在线游戏，玩家可以通过互联网与其他玩家互动。游戏以虚拟角色扮演为核心玩法，玩家可以自由探索游戏世界，与NPC和其他玩家交互，完成任务和挑战副本。",
    "gameShotsUrl": "",
    "gameWxUrl": ""
}

default_config = {
    'bot': default_bot,
    'game': default_game
}


#只取new_conf里面的指定字段
def update_config(default_conf, conf):
    new_conf = default_conf
    logger.info('ccc')
    for k in default_conf.keys():
        logger.info('key: {}, {}'.format(k, default_conf[k]))
        if k in conf and conf[k] != '':
            logger.info('key: {}, {}'.format(k, conf[k]))
            new_conf[k] = conf[k]
    return new_conf

class ZhConf(object):
    def __init__(self, id, type='bot'):
        self.type = type
        self.id = id
        self.rs_key = 'rs_zhdata_config_{}_{}'.format(type, id)
        if type in default_config:
            self.default_config = default_config[type]
        else:
            self.default_config = {}
    
    def get_conf(self):
        if not redis_cli.exists(self.rs_key):
            redis_conf = {}
            logger.warning("{} Id = {} not configured, use default".format(self.type, self.id))
        else:
            redis_conf = json.loads(redis_cli.get(self.rs_key))
        return redis_conf

    def set_conf(self, conf):
       redis_conf = update_config(self.default_config, conf)
       redis_cli.set(self.rs_key, json.dumps(redis_conf))
       return 
       
        


            
