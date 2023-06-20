# -*- coding: utf-8 -*-
import os

from flask import Flask, request, abort
from wechatpy import parse_message
from apps.app_config import GetTokenByApp, GetAppAESKeyByName, GetAppIdByName, GetDispatcherByName
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
import main
from common.logger import get_logger
# set token or get from environments
app = main.create_app("wechat_gw")


@app.route("/")
def hello():
    return "hello"


@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    logger = get_logger()
    appName = request.args.get("appid")
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    encrypt_type = request.args.get("encrypt_type", "raw")
    msg_signature = request.args.get("msg_signature", "")

    token = GetTokenByApp(appName)
    if token == None:
        abort(403)

    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == "GET":
        echo_str = request.args.get("echostr", "")
        return echo_str

    dispath = GetDispatcherByName(appName)
    # POST request
    if encrypt_type == "raw":
        # plaintext mode
        msg = parse_message(request.data)
        try:
            ret = dispath.DispatchMsg(appName, msg)
            if ret == None:
                abort(400)
            return ret
        except:
            logger.error("Catch Error")
            abort(500)

    from wechatpy.crypto import WeChatCrypto
    crypto = WeChatCrypto(token, GetAppAESKeyByName(
        appName), GetAppIdByName(appName))
    try:
        msg = crypto.decrypt_message(
            request.data, msg_signature, timestamp, nonce)
    except (InvalidSignatureException, InvalidAppIdException):
        abort(403)
    else:
        msg = parse_message(msg)
        ret = dispath.DispatchMsg(appName, msg)
        if ret == None:
            abort(400)
        return ret


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
