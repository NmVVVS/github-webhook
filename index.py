# coding: utf-8
# +-------------------------------------------------------------------
# | Github Webhook
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2017
# +-------------------------------------------------------------------
# | Author:
# +-------------------------------------------------------------------


# +--------------------------------------------------------------------
# |   Github Webhook
# +--------------------------------------------------------------------

import json
import os
import hmac
from hashlib import sha256

from flask import Flask, request

app = Flask(__name__)


# +--------------------------------------------------------------------
# |   compare_signature
# |
# |   github 签名校验方法
# |
# |   @param secretkey  string 密钥
# |   @param data       string 要加密的数据
# |   @param signature  string github 签名
# +--------------------------------------------------------------------
def compare_signature(secretkey, data, signature):
    _key = secretkey.encode('utf-8')
    _data = data.encode('utf-8')
    _signature = 'sha256=' + hmac.new(_key, _data, digestmod=sha256).hexdigest()
    return _signature == signature


# +--------------------------------------------------------------------
# |   run_shell
# |
# |   执行 linux 脚本
# |
# |   @param shell_path string 脚本绝对路径
# +--------------------------------------------------------------------
def run_shell(shell_name):
    if shell_name is "":
        return False

    shell_path = './script/' + shell_name
    log_path = './logs/' + shell_name + '.log'

    if not os.path.exists(shell_path):
        log_file = open(log_path, 'a')
        log_file.writelines("脚本不存在，无法执行")
        return False

    os.system("/bin/bash {} >> {} &".format(shell_path, log_path))
    return True


# +--------------------------------------------------------------------
# |   app.post("/<key>")
# |
# |   Hook 接收方法，github 请求方法，当github
# |   发送 webhook 通知时候，执行当前方法
# |
# |   @param key string 脚本绝对路径
# +--------------------------------------------------------------------
@app.post("/<key>")
def webhook(key):
    json_file = './list.json'
    if not os.path.exists(json_file):
        return '配置文件不存在!'

    # 读取文件
    with open(json_file, encoding='utf-8') as config:
        result = json.load(config)

    # 检查 key 是否存在
    config_data = result.get(key)
    if config_data is None:
        return 'Key 不存在!'

    # 检查 配置文件 中参数是否配置成功
    secret_key = config_data.get('secret')
    shell = config_data.get('shell')
    if secret_key is None or shell is None:
        return 'Key 配置错误!'

    # 从 request 中获取原始数据
    github_signature = request.headers.get("X-Hub-Signature-256")
    post_data = request.stream.read()

    # request body 可能是bytes 转化成 string
    if type(post_data) is bytes:
        post_data = post_data.decode()

    if compare_signature(secret_key, post_data, github_signature):
        return '滚!'

    if run_shell(shell):
        return 'Success'
    else:
        return 'Fail'


@app.get("/add")
def add():
    return "<p>Hello, add!</p> "


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
