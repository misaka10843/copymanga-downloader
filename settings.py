import json
import os
import sys

import requests
from rich import print as print
from rich.prompt import Prompt, Confirm, IntPrompt

import config
from epub import set_kindle_config
from login import loginhelper


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def get_org_url():
    print("[italic yellow]正在获取CopyManga网站Url...[/]")
    url = "https://ghproxy.net/https://raw.githubusercontent.com/misaka10843/copymanga-downloader/master/url.json"
    try:
        response = requests.get(url, proxies=config.PROXIES)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("[bold yellow]无法链接至ghproxy.net，准备直接访问Github[/]")
        # 更换URL
        url = "https://raw.githubusercontent.com/misaka10843/copymanga-downloader/master/url.json"
        try:
            response = requests.get(url, proxies=config.PROXIES)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[bold red]无法链接至GitHub，请检查网络连接,ErrMsg:{e}[/]", )
            sys.exit()


def set_settings():
    # 获取用户输入
    download_path = Prompt.ask("请输入保存路径[italic yellow](最后一个字符不能为斜杠)[/]",
                               default=os.path.split(os.path.realpath(__file__))[0])
    use_oversea_cdn_input = Confirm.ask("是否使用海外CDN？", default=False)
    use_webp_input = Confirm.ask("是否使用Webp？[italic yellow](可以节省服务器资源,下载速度也会加快)[/]",
                                 default=True)
    proxy = Prompt.ask("请输入代理地址[italic yellow](没有的话可以直接回车跳过，包括协议头)[/]")
    hc_input = Confirm.ask("是否下载高分辨率图片[italic yellow](不选择可以节省服务器资源,下载速度也会加快)[/]",
                           default=False)
    cbz = Confirm.ask("是否下载后打包成CBZ？", default=False)
    send_to_kindle = Confirm.ask("是否启用半自动更新自动发送至kindle功能[italic yellow][/]", default=False)
    if cbz:
        while True:
            cbz_path = Prompt.ask("请输入CBZ文件的保存路径[italic yellow](最后一个字符不能为斜杠)[/]")
            if is_contains_chinese(cbz_path):
                print("路径请不要包含中文")
            else:
                break
    else:
        cbz_path = None
    if proxy:
        config.PROXIES = {
            "http": proxy,
            "https": proxy
        }
    if send_to_kindle:
        set_kindle_config()

    api_urls = get_org_url()
    for i, url in enumerate(api_urls):
        print(f"{i + 1}->{url}")
    choice = IntPrompt.ask("请输入要使用的API前面的数字")

    # input转bool
    use_oversea_cdn = "0"
    use_webp = "0"
    hc = "0"
    if use_oversea_cdn_input:
        use_oversea_cdn = "1"
    if use_webp_input:
        use_webp = "1"
    if hc_input:
        hc = "1"
    # 构造settings字典
    login_pattern = Prompt.ask("请输入登陆方式(1为token登录，2为账号密码持久登录，3为不登录)", default="1")
    # 先申明变量
    authorization = None
    salt = None
    username = None
    password = None
    if login_pattern == "1":
        authorization = Prompt.ask("请输入token")
    elif login_pattern == "2":
        while True:
            username = Prompt.ask("请输入账号").strip()
            password = Prompt.ask("请输入密码").strip()
            if username == "" or password == "":
                print("请输入账号密码")
                continue
            else:
                res = loginhelper(username, password, api_urls[choice - 1])
                if res["token"]:
                    authorization = f"Token {res['token']}"
                    salt = res["salt"]
                    password = res["password_enc"]
                    break
    else:
        authorization = None
        login_pattern = "3"
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    settings = {
        "download_path": download_path,
        "authorization": authorization,
        "use_oversea_cdn": use_oversea_cdn,
        "use_webp": use_webp,
        "proxies": proxy,
        "api_url": api_urls[choice - 1],
        "HC": hc,
        "CBZ": cbz,
        "cbz_path": cbz_path,
        "api_time": 0.0,
        "API_COUNTER": 0,
        "loginPattern": login_pattern,
        "salt": salt if login_pattern == "2" else None,
        "username": username if login_pattern == "2" else None,
        "password": password if login_pattern == "2" else None,
        "send_to_kindle": send_to_kindle,
        "kcc_cmd": config.SETTINGS["kcc_cmd"],
        "email_address": config.SETTINGS["email_address"],
        "email_passwd": config.SETTINGS["email_passwd"],
        "email_smtp_address": config.SETTINGS["email_smtp_address"],
        "kindle_address": config.SETTINGS["kindle_address"]
    }
    home_dir = os.path.expanduser("~")
    settings_path = os.path.join(home_dir, ".copymanga-downloader/settings.json")
    save_settings(settings)
    print(f"[yellow]已将配置文件存放到{settings_path}中[/]")


def change_settings():
    # 获取用户输入
    download_path = Prompt.ask("请输入保存路径[italic yellow](最后一个字符不能为斜杠)[/]",
                               default=config.SETTINGS['download_path'])

    use_oversea_cdn = True
    use_webp = True
    if config.SETTINGS['use_oversea_cdn'] == "0":
        use_oversea_cdn = False
    if config.SETTINGS['use_webp'] == "0":
        use_webp = False
    use_oversea_cdn_input = Confirm.ask("是否使用海外CDN？", default=use_oversea_cdn)
    use_webp_input = Confirm.ask("是否使用Webp？[italic yellow](可以节省服务器资源,下载速度也会加快)[/]",
                                 default=use_webp)
    proxy = Prompt.ask("请输入代理地址[italic yellow](如果需要清除请输入0,输入时需包括协议头)[/]",
                       default=config.SETTINGS['proxies'])
    if config.SETTINGS.get('HC') is None:
        hc_input = Confirm.ask("是否下载高分辨率图片[italic yellow](不选择可以节省服务器资源,下载速度也会加快)[/]",
                               default=False)
    else:
        hc_c = True
        if config.SETTINGS['HC'] == "0":
            hc_c = False
        hc_input = Confirm.ask("是否下载高分辨率图片[italic yellow](不选择可以节省服务器资源,下载速度也会加快)[/]",
                               default=hc_c)
    if config.SETTINGS.get('CBZ') is None or not config.SETTINGS.get("CBZ"):
        cbz = Confirm.ask("是否下载后打包成CBZ？", default=False)
    else:
        cbz = True
        hc_input = Confirm.ask("是否下载后打包成CBZ？",
                               default=cbz)
    send_to_kindle_modify = Confirm.ask("是否需要修改kindle自动推送相关设置？[italic yellow][/]", default=False)
    if cbz:
        if config.SETTINGS.get('cbz_path') is None:
            config.SETTINGS['cbz_path'] = None

        while True:
            cbz_path = Prompt.ask("请输入CBZ文件的保存路径[italic yellow](最后一个字符不能为斜杠)[/]",
                                  default=config.SETTINGS['cbz_path'])
            if is_contains_chinese(cbz_path):
                print("路径请不要包含中文")
            else:
                break
    else:
        cbz_path = None
    if proxy != config.SETTINGS['proxies'] and proxy != "0":
        config.PROXIES = {
            "http": proxy,
            "https": proxy
        }
    if proxy == "0":
        proxy = ""
    api_urls = get_org_url()
    for i, url in enumerate(api_urls):
        print(f"{i + 1}->{url}")
    choice = IntPrompt.ask("请输入要使用的API前面的数字")
    if send_to_kindle_modify:
        config.SETTINGS["send_to_kindle"] = Confirm.ask("是否继续使用kindle推送？[italic yellow][/]", default=True)
        if config.SETTINGS["send_to_kindle"]:
            set_kindle_config()

    # 构造settings字典

    login_change = Confirm.ask("是否要修改登陆方式？", default=False)
    authorization = config.SETTINGS["authorization"]
    if login_change:
        login_pattern = Prompt.ask("请输入登陆方式(1为token登录，2为账号密码持久登录，或者直接输入其他数字跳过)",
                                   default=config.SETTINGS["loginPattern"])
        if login_pattern == "1":
            authorization = Prompt.ask("请输入token")
        elif login_pattern == "2":
            while True:
                username = Prompt.ask("请输入账号").strip()
                password = Prompt.ask("请输入密码").strip()
                if username == "" or password == "":
                    print("请输入账号密码")
                    continue
                else:
                    res = loginhelper(username, password, api_urls[choice - 1])
                    if res["token"]:
                        config.SETTINGS["authorization"] = f"Token {res['token']}"
                        config.SETTINGS["username"] = username
                        config.SETTINGS["salt"] = res["salt"]
                        config.SETTINGS["password"] = res["password_enc"]
                        break
    else:
        login_pattern = config.SETTINGS["loginPattern"]
        authorization = config.SETTINGS["authorization"]
    print(f"[yellow]我们正在更改您的设置中，请稍后[/]")
    # input转bool
    use_oversea_cdn = "0"
    use_webp = "0"
    hc = "0"
    if use_oversea_cdn_input:
        use_oversea_cdn = "1"
    if use_webp_input:
        use_webp = "1"
    if hc_input:
        hc = "1"
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    settings = {
        "download_path": download_path,
        "authorization": authorization,
        "use_oversea_cdn": use_oversea_cdn,
        "use_webp": use_webp,
        "proxies": proxy,
        "api_url": api_urls[choice - 1],
        "HC": hc,
        "CBZ": cbz,
        "cbz_path": cbz_path,
        "api_time": 0.0,
        "API_COUNTER": 0,
        "loginPattern": login_pattern,
        "salt": config.SETTINGS["salt"] if login_pattern == "2" else None,
        "username": config.SETTINGS["username"] if login_pattern == "2" else None,
        "password": config.SETTINGS["password"] if login_pattern == "2" else None,
        "send_to_kindle": config.SETTINGS["send_to_kindle"],
        "kcc_cmd": config.SETTINGS["kcc_cmd"] if config.SETTINGS["send_to_kindle"] else None,
        "email_address": config.SETTINGS["email_address"] if config.SETTINGS["send_to_kindle"] else None,
        "email_passwd": config.SETTINGS["email_passwd"] if config.SETTINGS["send_to_kindle"] else None,
        "email_smtp_address": config.SETTINGS["email_smtp_address"] if config.SETTINGS["send_to_kindle"] else None,
        "kindle_address": config.SETTINGS["kindle_address"] if config.SETTINGS["send_to_kindle"] else None
    }
    home_dir = os.path.expanduser("~")
    settings_path = os.path.join(home_dir, ".copymanga-downloader/settings.json")
    save_settings(settings)
    print(f"[yellow]已将重新修改配置文件并存放到{settings_path}中[/]")


def save_settings(settings):
    home_dir = os.path.expanduser("~")
    if not os.path.exists(os.path.join(home_dir, '.copymanga-downloader/')):
        os.mkdir(os.path.join(home_dir, '.copymanga-downloader/'))
    settings_path = os.path.join(home_dir, ".copymanga-downloader/settings.json")
    # 写入settings.json文件
    with open(settings_path, "w") as f:
        json.dump(settings, f)


def load_settings():
    # 获取用户目录的路径
    home_dir = os.path.expanduser("~")
    settings_path = os.path.join(home_dir, ".copymanga-downloader/settings.json")
    # 检查是否有文件
    if not os.path.exists(settings_path):
        return False, "settings.json文件不存在"
    # 读取json配置文件
    with open(settings_path, 'r') as f:
        settings = json.load(f)

    # 判断必要的字段是否存在
    necessary_fields = ["download_path", "authorization", "use_oversea_cdn", "use_webp", "proxies", "api_url",
                        "loginPattern"]
    for field in necessary_fields:
        if field not in settings:
            return False, "settings.json中缺少必要字段{}".format(field)
    config.SETTINGS = settings
    if "HC" not in settings:
        config.SETTINGS['HC'] = None
        print("[bold yellow]我们更新了设置，请您按照需求重新设置一下，还请谅解[/]")
        change_settings()
        print("[bold yellow]感谢您的支持，重新启动本程序后新的设置将会生效[/]")
        exit(0)
    config.OG_SETTINGS = settings
    # 设置请求头
    config.API_HEADER['use_oversea_cdn'] = settings['use_oversea_cdn']
    config.API_HEADER['use_webp'] = settings['use_webp']
    if 'UA' in settings:
        config.API_HEADER['User-Agent'] = settings['UA']
    # 设置代理
    if settings["proxies"]:
        config.PROXIES = {
            "http": settings["proxies"],
            "https": settings["proxies"]
        }
    return True, None
