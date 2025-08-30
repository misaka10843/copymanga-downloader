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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
    "authorization": SETTINGS.get('authorization'),
}

PROXIES = {}

API_COUNTER = 0
IMG_API_COUNTER = 0
IMG_CURRENT_TIME = 0

ARGS = {}
