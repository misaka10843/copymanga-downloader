# @Time    : 2024/1/8 22:51
# @Author  : TwoOnefour
# @blog    : https://www.pursuecode.cn
# @Email   : twoonefour@pursuecode.cn
# @File    : login.py
import requests


def login(**information: dict[{"username": None, "password": None, "url": None, "salt": None, "proxy": None}]) -> str:
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
