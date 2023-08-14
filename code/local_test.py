# -*- coding: utf-8 -*-
import requests
import json
import random



def request_url(method_name, config):
    url = "http://api.agentbot.greatleapai.com"  # Replace with the desired URL
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(url + method_name, data=json.dumps(config), headers=headers)
    #try:
    data = response.json()
    # Process the JSON data
    print(data)  # Print the response content
    # except json.JSONDecodeError as e:
    #     print("Error decoding JSON:", e)
    #     print("Response content:", response.content)


gameconfig = {
    "gameName": "九梦仙域_魂天",
    "gameUrl": "https://p.daimiaohudong.cn/Mobile/Promotion/code?spm=tvBACk",
    "gameBonusSummary": "开局赠送1亿元宝+300绑定仙玉+初级羽翼、法宝精华+后续各种等级材料大礼i包，每天打佧礼i包",
    "gameBonus": "①上线就给您一亿元宝、海量材料快速提升战力\n②豪华升级大礼i包+500万元宝\n③专属丰厚等级奖i励\n④后续每日一百万元宝、通用BOSS刷新card等礼福多多\n开局赠送1亿元宝+300绑定仙玉+初级羽翼、法宝精华+后续各种等级材料大礼i包，每天打佧礼i包",
    "gameFeatureSummary": "九梦仙域是一款仙侠世界多人在线的RPG游戏。",
    "gameFeature": "1.仙侠世界：九梦仙域以传统的仙侠世界为背景，游戏地图丰富多样，包括山水、城镇、副本等多种场景。\n2.职业门派：游戏中有多个职业门派可供选择，每个门派有不同的特点和技能，玩家可以根据自己的喜好选择。\n3.任务系统：游戏中有大量的任务可供完成，包括主线任务、支线任务、日常任务等，玩家可以通过完成任务获得经验、金钱和道具。\n4.社交系统：九梦仙域为玩家提供了多种社交功能，玩家可以与其他玩家组队、聊天、交易等。\n\n九梦仙域是一款多人在线游戏，玩家可以通过互联网与其他玩家互动。\n戏以虚拟角色扮演为核心玩法，玩家可以自由探索游戏世界，与NPC和其他玩家交互，完成任务和挑战副本。\n这款游戏是一款RPG游戏，有着非常丰富的故事情节和多元化的玩法，比如战斗、副本、家园建设、养成团队等等。  游戏中有着各种各样的装备、技能、坐骑和宠物，让玩家可以深度的探索游戏世界\n\n我们的游戏画质非常精美，采用了高清画面和流畅的动画效果，让玩家可以真正身临其境地感受游戏世界的美妙。同时我们也会不断优化游戏性能，保证游戏可以流畅运行在各种设备上。让玩家可以随时随地，畅玩我们的游戏.",
    "gameShotsUrl": ["http://web-zhsj-1318887924.cos.ap-guangzhou.myqcloud.com/chat/img/t-AADl.png", "http://web-zhsj-1318887924.cos.ap-guangzhou.myqcloud.com/chat/img/t-AADk.png", "http://web-zhsj-1318887924.cos.ap-guangzhou.myqcloud.com/chat/img/t-AADj.png"], 
    "gameWxUrl":"http://web-zhsj-1318887924.cos.ap-guangzhou.myqcloud.com/chat/img/t-AADm.png"
}

gameconfig1 = {
    "gameName": "独步武林",
    "gameUrl": "https://z.p6e.cn/p/cccc4Y",
    "gameBonusSummary": "0.1折福利版本，游戏内充值100块只需要1元，几十块钱就可以得到几千块钱的氪金大佬体验。",
    "gameBonus": "0.1折福利版本，游戏内充值100块只需要1元，几十块钱就可以得到几千块钱的氪金大佬体验。",
    "gameFeatureSummary": "武侠风格竖版手游，全程挂机解放双手",
    "gameFeature": "武侠风格竖版手游，全程挂机解放双手",
    "gameShotsUrl": ["http://web-zhsj-1318918231.cos.ap-guangzhou.myqcloud.com/chat/img/190_1691809531556_715.jpeg", "http://web-zhsj-1318918231.cos.ap-guangzhou.myqcloud.com/chat/img/190_1691809523102_515.jpeg"], 
    "gameWxUrl":"http://suo.im/7NaVv"
}

botconfig = {
    "token": "zhenhuaadmin",
    "botName": "徐露",
    "botSex": "女孩",
    "botAge": "21",
    "botTask": "独步武林",
    "botWxId": "yuanquan1"
}

gameconfig_check = {
    "gameName": "九梦仙域_魂天2"
}
botconfig_check = {
    "botWxId": "yuanquan5"
}

#单独配置游戏
request_url("/zhdata/adminregister", gameconfig1)

# 配置一个机器人
# request_url("/zhdata/adminregister", botconfig)

# 配置多个客服机器人
# with open('bot_list.txt', 'r') as f:
#     for line in f.readlines():
#         conf = botconfig
#         conf['botWxId'] = line.strip()
#         conf['botTask'] = "独步武林"
#         print(json.dumps(conf, ensure_ascii=False).encode('utf-8'))
#         request_url("/zhdata/adminregister", conf)


# 检查配置
# request_url("/zhdata/admincheck", gameconfig_check)
# request_url("/zhdata/admincheck", botconfig_check)
# request_url("/zhdata/admincheckallconfigs", {})