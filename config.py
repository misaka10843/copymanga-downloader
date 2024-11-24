import datetime

SETTINGS = {
    "download_path": None,
    "authorization": None,
    "use_oversea_cdn": None,
    "use_webp": None,
    "proxies": None,
    "api_url": None,
    "HC": None,
    "CBZ": None,
    "cbz_path": None,
    "api_time": 0.0,
    "API_COUNTER": 0,
    "loginPattern": "0",
    "salt": None,
    "username": None,
    "password": None,
    "send_to_kindle": None,
    "kcc_cmd": None,
    "email_address": None,
    "email_passwd": None,
    "kindle_address": None,
    "email_smtp_address": None,
    "UA": None,
}

# 全局化设置,备份,防止命令行参数导致设置错位
OG_SETTINGS = {
    "download_path": None,
    "authorization": None,
    "use_oversea_cdn": None,
    "use_webp": None,
    "proxies": None,
    "api_url": None,
    "HC": None,
    "CBZ": None,
    "cbz_path": None,
    "api_time": 0.0,
    "API_COUNTER": 0,
    "loginPattern": "0",
    "salt": None,
    "username": None,
    "password": None,
    "send_to_kindle": None,
    "kcc_cmd": None,
    "email_address": None,
    "email_passwd": None,
    "kindle_address": None,
    "email_smtp_address": None,
    "UA": None,
}

# 全局化headers，节省空间

API_HEADER = {
    'User-Agent': 'duoTuoCartoon/3.2.4 (iPhone; iOS 18.0.1; Scale/3.00) iDOKit/1.0.0 RSSX/1.0.0',
    'version': datetime.datetime.now().strftime("%Y.%m.%d"),
    'region': '0',
    'webp': '0',
    "platform": "1",
    "referer": "https://www.copymanga.com/"
}

PROXIES = {}

API_COUNTER = 0
IMG_API_COUNTER = 0
IMG_CURRENT_TIME = 0

ARGS = {}
