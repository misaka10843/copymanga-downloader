from datetime import datetime

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
    "User-Agent": "COPY/2.3.2",
    "authorization": SETTINGS.get('authorization'),
    "referer": "com.copymanga.app-2.3.2",
    "source": "copyApp",
    "version": "2.3.2",
    "region": "1",
    "device": "V417IR",
    "umstring": "b4c89ca4104ea9a97750314d791520ac",
    "platform": "3",
    "dt": datetime.now().strftime("%Y.%m.%d"),
    "deviceinfo": "24129PN74C-24129PN74C",
    "accept-encoding": "gzip",
    "webp": "1",
    "pseudoid": "KNJT34xmmyOB6A4a",
}

PROXIES = {}

API_COUNTER = 0
IMG_API_COUNTER = 0
IMG_CURRENT_TIME = 0

ARGS = {}
