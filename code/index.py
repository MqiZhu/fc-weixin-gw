# -*- coding: utf-8 -*-
import os
import json

from flask import Flask, request, abort, jsonify
from wechatpy import parse_message, create_reply
from apps.app_config import GetTokenByApp, GetAppAESKeyByName, GetAppIdByName, get_dispatcher_by_name
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
import traceback
import main
from common.logger import get_logger, init_logger
from common.zhdata_config import ZhConf
# set token or get from environments
app = main.create_app("wechat_gw")


@app.route("/")
def hello():
    return "hello"


@app.route("/zhdata/chat", methods=["GET", "POST"])
def zhchat():

    logger = get_logger()
    app_id = "zhenhuashuju_mq"
    req_data = request.get_json()
    hd = get_dispatcher_by_name(app_id)

    msg_id = req_data.get("msgId", 0)
    user_id = req_data.get("contactId", '')
    app_id = req_data.get("botWxid", '')
    req_data["app_id"] = "zhenhuashuju_mq"

    hd.dispatch_data(app_id, user_id, msg_id, req_data)

    return jsonify({
        "succ": True,
    })


@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    logger = get_logger()
    app_id = request.args.get("appid")
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    encrypt_type = request.args.get("encrypt_type", "raw")
    msg_signature = request.args.get("msg_signature", "")
    logger.info("call from app_id= {} {} ".format(app_id, signature))

    token = GetTokenByApp(app_id)
    if token == None:
        abort(403)

    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == "GET":
        echo_str = request.args.get("echostr", "")
        return echo_str

    dispath = get_dispatcher_by_name(app_id)
    # POST request
    if encrypt_type == "raw":
        # plaintext mode
        msg = parse_message(request.data)
        try:
            hit, rsp = dispath.dispatch_wxmp_msg(app_id, msg)
            if hit:
                if rsp == None:
                    return create_reply(None).render()
                return create_reply(rsp, msg).render()
            abort(400)
        except Exception as e:
            logger.error("Catch Error{}".format(e))
            traceback.print_exc()
            abort(500)

    from wechatpy.crypto import WeChatCrypto
    crypto = WeChatCrypto(token, GetAppAESKeyByName(
        app_id), GetAppIdByName(app_id))
    try:
        msg = crypto.decrypt_message(
            request.data, msg_signature, timestamp, nonce)
    except (InvalidSignatureException, InvalidAppIdException):
        abort(403)
    else:
        msg = parse_message(msg)
        hit, rsp = dispath.dispatch_wxmp_msg(app_id, msg)
        if hit:
            if rsp == None:
                return create_reply(None).render()
            return create_reply(rsp, msg).render()
        abort(400)


@app.route("/zhdata/adminregister", methods=["POST", "GET"])
def adminregister():
    logger = get_logger()
    req_data = request.get_json()
    data = {}
    rsp = ''
    zhconf = None
    if 'gameName' in req_data and req_data['gameName'] != '':
        zhconf = ZhConf(req_data['gameName'], 'game')
    elif 'botWxId' in req_data and req_data['botWxId'] != '':
        zhconf = ZhConf(req_data['botWxId'], 'bot')
    else:
        data['system_message'] = "gameName or botWxId needed"
        data["succ"] = False
        return json.dumps(data, ensure_ascii=False).encode('utf-8')
    try:
        zhconf.set_conf(req_data)
        result_conf = zhconf.get_conf()
        logger.info("call succ, add config {}".format(result_conf))
        data['config'] = result_conf
        data["succ"] = True
    except Exception as e:
        data["succ"] = False
        data["err"] = "intenal error: {}".format(e)
        logger.info(
            "config error, req={}, e={}".format(req_data, e))
    return json.dumps(data, ensure_ascii=False).encode('utf-8')

@app.route("/zhdata/admincheck", methods=["POST", "GET"])
def admincheck():
    logger = get_logger()
    req_data = request.get_json()
    data = {}
    rsp = ''
    zhconf = None
    if 'gameName' in req_data and req_data['gameName'] != '':
        zhconf = ZhConf(req_data['gameName'], 'game')
    elif 'botWxId' in req_data and req_data['botWxId'] != '':
        zhconf = ZhConf(req_data['botWxId'], 'bot')
    else:
        data['system_message'] = "gameName or botWxId needed"
        data["succ"] = False
        return json.dumps(data, ensure_ascii=False).encode('utf-8')
    try:
        result_conf = zhconf.get_conf()
        logger.info("call succ, get config {}".format(result_conf))
        data['config'] = result_conf
        data["succ"] = True
    except Exception as e:
        data["succ"] = False
        data["err"] = "intenal error: {}".format(e)
        logger.info(
            "config error, req={}, e={}".format(req_data, e))
    return json.dumps(data, ensure_ascii=False).encode('utf-8')

@app.route("/zhdata/admincheckallconfigs", methods=["POST", "GET"])
def admincheckallconfigs():
    logger = get_logger()
    data = {}
    try:
        zhconf = ZhConf(0, '')
        result_conf = zhconf.get_all_configs()
        logger.info("call succ, get all configs {}".format(result_conf))
        data['bots'] = result_conf['bots']
        data['games'] = result_conf['games']
        data["succ"] = True
    except Exception as e:
        data["succ"] = False
        data["err"] = "intenal error: {}".format(e)
        logger.info(
            "config error, e={}".format(e))
    return json.dumps(data, ensure_ascii=False).encode('utf-8')

if __name__ == "__main__":
    init_logger("", debug=True)

    app.run(host="0.0.0.0", port=8000, debug=True)
