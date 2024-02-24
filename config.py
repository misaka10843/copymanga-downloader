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
    "email_smtp_address": None
}

# '''
#     "epub_and_mail_to_kindle": None,
#     "kcc_cmd": None,
#     "email_address": None,
#     "email_passwd": None,
#     "kindle_address": None,
# '''

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
    "email_smtp_address": None
}

# 全局化headers，节省空间

API_HEADER = {
    'User-Agent': '"User-Agent" to "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44"',
    'version': datetime.datetime.now().strftime("%Y.%m.%d"),
    'region': '0',
    'webp': '0',
    "platform": "1",
    "referer": "https://www.copymanga.site/"
}

PROXIES = {}

API_COUNTER = 0
IMG_API_COUNTER = 0
IMG_CURRENT_TIME = 0
