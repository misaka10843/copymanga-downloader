import time

import config
from settings import save_settings


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


# API限制相关

def api_restriction():
    config.API_COUNTER += 1
    # 防止退出后立马再次运行
    current_time = config.OG_SETTINGS['api_time']
    time_diff = time.time() - current_time
    # 判断是否超过60秒
    if time_diff < 60 and config.API_COUNTER <= 1:
        config.API_COUNTER = config.API_COUNTER + config.OG_SETTINGS['API_COUNTER']
    if config.API_COUNTER >= 15:
        config.API_COUNTER = 0
        print("[bold yellow]您已经触发到了API请求阈值，我们将等60秒后再进行[/]")
        time.sleep(60)
    config.OG_SETTINGS['API_COUNTER'] = config.API_COUNTER
    config.OG_SETTINGS['api_time'] = time.time()
    # 将时间戳与API请求数量写入配置文件
    save_settings(config.OG_SETTINGS)


def img_api_restriction():
    config.IMG_API_COUNTER += 1
    # 防止退出后立马再次运行

    time_diff = time.time() - config.IMG_CURRENT_TIME
    # 判断是否超过60秒
    if time_diff < 60 and config.IMG_API_COUNTER >= 100:
        print("[bold yellow]您已经触发到了图片服务器API请求阈值，我们将等60秒后再进行[/]")
        time.sleep(60)
        config.IMG_CURRENT_TIME = 0
        config.IMG_API_COUNTER = 0
