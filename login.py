# @Time    : 2024/1/8 22:51
# @Author  : TwoOnefour
# @blog    : https://www.pursuecode.cn
# @Email   : twoonefour@pursuecode.cn
# @File    : login.py
import requests
from rich import print as print

import config


def login(**information: dict) -> str:
    """
    登录函数，实际访问登录获取token

    :param information: dict对象，其中包含键username，password，url，salt, proxy
    :return: string类型，返回登录后的token
    """
    if information["username"]:
        try:
            res = requests.post(f"https://{information['url']}/api/kb/web/login", data={
                "username": information["username"],
                "password": information["password"],
                "salt": information["salt"]
            }, headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
            }, proxies=information["proxy"])
            res_json = res.json()
            if res_json["code"] == 200:
                return res_json["results"]["token"]
            else:
                print(res_json["message"])
        except Exception as e:
            return None
    return None


def loginhelper(username: str, password: str, url: str) -> dict:
    """
    用于登录的函数，使用用户名和密码登录获取token后返回

    :param username: （str）明文账户名
    :param password: （str）明文密码
    :param url: (str) 指定的api地址，即对应SETTINGS["api_url"]或api_urls[n]，其中n为用户选择的api地址的序号
    :return: dict对象，其中包含token和随机生成的盐和加密后的密码，形如：{"token": res, "salt": salt, "password_enc": password_enc}
    """
    from random import randint
    from base64 import b64encode
    # 随机生成盐
    salt = randint(100000, 999999)
    # 加密
    password_enc = password + f"-{salt}"
    password_enc = b64encode(password_enc.encode()).decode()
    # 登录
    res = login(**{"username": username, "password": password_enc, "url": url, "salt": salt, "proxy": config.PROXIES})
    return {"token": res, "salt": salt, "password_enc": password_enc}


def login_information_builder(username: str, password: str, url: str, salt: str, proxy: dict) -> dict:
    """
    辅助函数，构建dict对象用于登录

    :param username: string类型，明文账户名
    :param password: string类型，明文密码
    :param url: string类型，指定的api地址，即对应SETTINGS["api_url"]或api_urls[n]，其中n为用户选择的api地址的序号
    :param salt: string类型，加密所用的盐
    :param proxy: dict类型，代理
    :return: dict类型，返回构造好的dict
    """
    return {"username": username, "password": password, "url": url, "salt": salt, "proxy": proxy}
