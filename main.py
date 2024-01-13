import argparse
import csv
import datetime
import json
import os
import random
import smtplib
import sys
import threading
import time
import zipfile
import string
from xpinyin import Pinyin
import subprocess
import retrying as retrying
from rich import print as print
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from login import login
import requests as requests
import platform
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

console = Console(color_system='256', style=None)
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
# 全局化设置
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

UPDATE_LIST = []

# API限制相关
API_COUNTER = 0
IMG_API_COUNTER = 0
IMG_CURRENT_TIME = 0


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--MangaPath',
        help='漫画的全拼，https://copymanga.site/comic/这部分')
    parser.add_argument(
        '--MangaGroup',
        help='漫画的分组Path_Word，默认为default', default='default')

    parser.add_argument('--Url', help='copymanga的域名,如使用copymanga.site，那就输入site(默认为site)', default="site")

    parser.add_argument('--Output', help='输出文件夹')

    # todo 此功能暂时不在开发维护列表内，以后会随缘更新此功能
    parser.add_argument(
        '--subscribe',
        help='是否切换到自动更新订阅模式(1/0，默认关闭(0))',
        default="0")

    parser.add_argument(
        '--UseWebp',
        help='是否使用Webp(1/0，默认开启(1))',
        default="1")

    parser.add_argument(
        '--UseOSCdn',
        help='是否使用海外cdn(1/0，默认关闭(0))',
        default="0")

    parser.add_argument('--MangaStart', help='漫画开始下载话(如果想全部下载请输入0)')

    parser.add_argument('--MangaEnd', help='漫画结束下载话(如果只想下载一话请与MangaStart相同,如果想全部下载请输入0)')

    parser.add_argument('--Proxy', help='设置代理')

    return parser.parse_args()


# 命令行参数全局化

ARGS = parse_args()


# 命令行模式
def command_mode():
    global SETTINGS, PROXIES, API_HEADER
    # 将命令行参数赋值到SETTINGS等相关全局变量
    if ARGS.UseOSCdn or ARGS.UseWebp:
        API_HEADER['use_oversea_cdn'] = ARGS.UseOSCdn
        API_HEADER['use_webp'] = ARGS.UseWebp
    if ARGS.Proxy:
        PROXIES = {
            "http": ARGS.Proxy,
            "https": ARGS.Proxy
        }
    if ARGS.Output:
        SETTINGS['download_path'] = ARGS.Output
    manga_chapter_json = manga_chapter(ARGS.MangaPath, ARGS.MangaGroup)
    chapter_allocation(manga_chapter_json)
    print(f"[bold green][:white_check_mark: ]漫画已经下载完成！[/]")


# 正常模式

def welcome():
    choice_manga_path_word = None
    want_to = int(Prompt.ask(
        "您是想搜索还是查看您的收藏？[italic yellow](0:导出收藏,1:搜索,2:收藏,3:添加半自动更新,9:修改设置)[/]",
        choices=["0", "1", "2", "3", "9"], default="1"))
    if want_to == 0:
        collect_expect()
        return
    if want_to == 9:
        change_settings()
        return
    if want_to == 3:
        updates()
        return
    if want_to == 1:
        choice_manga_path_word = search()
    if want_to == 2:
        choice_manga_path_word = search_on_collect()
    manga_group_path_word = manga_group(choice_manga_path_word)
    manga_chapter_json = manga_chapter(choice_manga_path_word, manga_group_path_word)
    chapter_allocation(manga_chapter_json)


# 自动更新相关
def updates():
    update_want_to = 0
    have_list = load_updates()
    if have_list:
        update_list()
        update_want_to = int(Prompt.ask("您是想添加漫画还是删除漫画？[italic yellow](0:添加,1:删除)[/]",
                                        choices=["0", "1"], default="0"))
    if update_want_to == 0:
        new_update = add_updates()
        response = requests.get(
        f"https://api.{SETTINGS['api_url']}/api/v3/comic/{new_update[0]}/group/{new_update[1]}/chapters?limit=500"
        f"&offset=0&platform=3",
        headers=API_HEADER, proxies=PROXIES)
        # 记录API访问量
        api_restriction()
        response.raise_for_status()
        manga_chapter_json = response.json()
        manga_now=int(Prompt.ask(f"当前漫画有{manga_chapter_json['results']['total']}话的内容，请问您目前看到多少话了"))
        save_updates(new_update[0], new_update[1], new_update[2], manga_now, False)
    else:
        del_manga_int = int(Prompt.ask("请输入想要删除的漫画前面的序号"))
        save_updates(UPDATE_LIST[del_manga_int - 1]['manga_path_word'],
                     UPDATE_LIST[del_manga_int - 1]['manga_group_path_word'],
                     UPDATE_LIST[del_manga_int - 1]['manga_name'], 0, True)


def add_updates():
    search_content = Prompt.ask("您需要搜索添加什么漫画呢")
    url = "https://api.%s/api/v3/search/comic?format=json&platform=3&q=%s&limit=10&offset={}" % (
        SETTINGS["api_url"], search_content)
    offset = 0
    current_page_count = 1
    while True:
        # 发送GET请求
        selection = search_list(url, offset, current_page_count)
        data = selection[1]
        selection = selection[0]
        if selection.upper() == "Q":
            break
        try:
            # 将用户输入的字符串转换为整数
            index = int(selection) - 1
            # 获取用户选择的comic的名称并输出
            print("你选择了：{}".format(data["results"]["list"][index]["name"]))
            # 让用户选择分组
            manga_group_path_word = manga_group(data["results"]["list"][index]["path_word"])
            # 返回两个pathWord与漫画名称
            return data["results"]["list"][index]["path_word"], manga_group_path_word, data["results"]["list"][index][
                "name"]

        except (ValueError, IndexError):
            offset = page_turning(selection, offset, data, current_page_count)
            current_page_count = offset[1]
            offset = offset[0]


def load_updates():
    global UPDATE_LIST
    # 获取用户目录的路径
    home_dir = os.path.expanduser("~")
    updates_path = os.path.join(home_dir, ".copymanga-downloader/update.json")
    # 检查是否有文件
    if not os.path.exists(updates_path):
        print("[yellow]update.json文件不存在,请添加需要更新的漫画[/]")
        return False
    # 读取json配置文件
    with open(updates_path, 'r') as f:
        UPDATE_LIST = json.load(f)
    if len(UPDATE_LIST) <= 0:
        print("[yellow]update.json文件为空,请添加需要更新的漫画[/]")
        return False
    return True


def update_list():
    for i, comic in enumerate(UPDATE_LIST):
        print("[{}] {}".format(i + 1, comic["manga_name"]))


def save_updates(manga_path_word, manga_group_path_word, manga_name, now_chapter, will_del):
    global UPDATE_LIST
    home_dir = os.path.expanduser("~")
    if not os.path.exists(os.path.join(home_dir, '.copymanga-downloader/')):
        os.mkdir(os.path.join(home_dir, '.copymanga-downloader/'))
    updates_path = os.path.join(home_dir, ".copymanga-downloader/update.json")
    # 是否删除漫画
    if will_del:
        for i, item in enumerate(UPDATE_LIST):
            if item.get('manga_name') == manga_name:
                del UPDATE_LIST[i]
                break
        print(f"[yellow]已将{manga_name}从自动更新列表中删除[/]")
    else:
        # 将新的漫画添加到LIST中
        new_update = {
            "manga_name": manga_name,
            "manga_path_word": manga_path_word,
            "manga_group_path_word": manga_group_path_word,
            "now_chapter": now_chapter
        }
        UPDATE_LIST.append(new_update)
        print(f"[yellow]已将{manga_name}添加到自动更新列表中,请使用命令行参数‘--subscribe 1’进行自动更新[/]")
    # 写入update.json文件
    with open(updates_path, "w") as f:
        json.dump(UPDATE_LIST, f)


# 判断是否已经有了，此函数是为了追踪用户下载到哪一话
def save_new_update(manga_path_word, now_chapter):
    global UPDATE_LIST
    home_dir = os.path.expanduser("~")
    if not os.path.exists(os.path.join(home_dir, '.copymanga-downloader/')):
        os.mkdir(os.path.join(home_dir, '.copymanga-downloader/'))
    updates_path = os.path.join(home_dir, ".copymanga-downloader/update.json")
    for item in UPDATE_LIST:
        if item['manga_path_word'] == manga_path_word:
            item['now_chapter'] = now_chapter
            with open(updates_path, "w") as f:
                json.dump(UPDATE_LIST, f)
            return


def update_download():
    load_settings()
    if not load_updates():
        print("[bold red]update.json并没有内容，请使用正常模式添加！[/]")
        sys.exit()
    for comic in UPDATE_LIST:
        print(f"[yellow]正在准备下载{comic['manga_name']}[/]")
        manga_chapter_json = update_get_chapter(comic['manga_path_word'],
                                                comic['manga_group_path_word'],
                                                comic['now_chapter'])
        if manga_chapter_json != 0:
            chapter_allocation(manga_chapter_json)


def update_get_chapter(manga_path_word, manga_group_path_word, now_chapter):
    # 因为将偏移设置到最后下载的章节，所以可以直接下载全本
    response = requests.get(
        f"https://api.{SETTINGS['api_url']}/api/v3/comic/{manga_path_word}/group/{manga_group_path_word}/chapters"
        f"?limit=500&offset={now_chapter}&platform=3",
        headers=API_HEADER, proxies=PROXIES)
    # 记录API访问量
    api_restriction()
    response.raise_for_status()
    manga_chapter_json = response.json()
    # Todo 创建传输的json,并且之后会将此json保存为temp.json修复这个问题https://github.com/misaka10843/copymanga-downloader/issues/35
    return_json = {
        "json": manga_chapter_json,
        "start": -1,
        "end": -1
    }
    # Todo 支持500+话的漫画(感觉并不太需要)
    if not manga_chapter_json['results']['list']:
        print(f"[bold blue]此漫画并未有新的章节，我们将跳过此漫画[/]")
        return 0
    if manga_chapter_json['results']['total'] > 500:
        print("[bold red]我们暂时不支持下载到500话以上，还请您去Github中创建Issue！[/]")
        sys.exit()
    return return_json


# 搜索相关

def search_list(url, offset, current_page_count):
    response = requests.get(url.format(offset), headers=API_HEADER, proxies=PROXIES)
    # 记录API访问量
    api_restriction()
    # 解析JSON数据
    data = response.json()

    console.rule(f"[bold blue]当前为第{current_page_count}页")
    # 输出每个comic的名称和对应的序号
    for i, comic in enumerate(data["results"]["list"]):
        print("[{}] {}".format(i + 1, comic["name"]))

    # 让用户输入数字来选择comic
    selection = Prompt.ask("请选择一个漫画[italic yellow]（输入Q退出,U为上一页,D为下一页）[/]")
    return selection, data


def page_turning(selection, offset, data, current_page_count):
    # 判断是否是输入的U/D
    # 根据用户输入更新offset
    if selection.upper() == "U":
        offset -= data["results"]["limit"]
        if offset < 0:
            offset = 0
        else:
            current_page_count -= 1
    elif selection.upper() == "D":
        offset += data["results"]["limit"]
        if offset > data["results"]["total"]:
            offset = data["results"]["total"] - data["results"]["limit"]
        else:
            current_page_count += 1
    else:
        # 处理输入错误的情况
        print("[italic red]无效的选择！[/]")
    return offset, current_page_count


def search():
    search_content = Prompt.ask("您需要搜索什么漫画呢")
    url = "https://api.%s/api/v3/search/comic?format=json&platform=3&q=%s&limit=10&offset={}" % (
        SETTINGS["api_url"], search_content)
    offset = 0
    current_page_count = 1
    while True:
        # 发送GET请求
        selection = search_list(url, offset, current_page_count)
        data = selection[1]
        selection = selection[0]
        if selection.upper() == "Q":
            break
        try:
            # 将用户输入的字符串转换为整数
            index = int(selection) - 1
            # 获取用户选择的comic的名称并输出
            print("你选择了：{}".format(data["results"]["list"][index]["name"]))
            # 返回pathWord
            return data["results"]["list"][index]["path_word"]

        except (ValueError, IndexError):
            offset = page_turning(selection, offset, data, current_page_count)
            current_page_count = offset[1]
            offset = offset[0]


# 收藏相关

def search_on_collect():
    url = "https://%s/api/v3/member/collect/comics?limit=12&offset={}&free_type=1&ordering=-datetime_modifier" % (
        SETTINGS["api_url"])
    API_HEADER['authorization'] = SETTINGS['authorization']
    offset = 0
    current_page_count = 1
    retry_count = 0
    while True:
        # 发送GET请求
        response = requests.get(url.format(offset), headers=API_HEADER, proxies=PROXIES)
        # 记录API访问量
        api_restriction()
        # 解析JSON数据
        data = response.json()
        if data['code'] == 401:
            settings_dir = os.path.join(os.path.expanduser("~"), ".copymanga-downloader/settings.json")
            if SETTINGS["loginPattern"] == "1":
                print(f"[bold red]请求出现问题！疑似Token问题！[{data['message']}][/]")
                print(f"[bold red]请删除{settings_dir}来重新设置！(或者也可以自行修改配置文件)[/]")
                sys.exit()
            else:
                res = login(**loginInformationBuilder(SETTINGS["username"], SETTINGS["password"], SETTINGS["api_url"], SETTINGS["salt"]))
                if res:
                    API_HEADER['authorization'] = res
                    continue
                time.sleep(2 ** retry_count)  # 重试时间指数
                retry_count += 1

        console.rule(f"[bold blue]当前为第{current_page_count}页")
        # 输出每个comic的名称和对应的序号
        for i, comic in enumerate(data["results"]["list"]):
            print("[{}] {}".format(i + 1, comic['comic']["name"]))

        # 让用户输入数字来选择comic
        selection = Prompt.ask("请选择一个漫画[italic yellow]（输入Q退出,U为上一页,D为下一页）[/]")
        if selection.upper() == "Q":
            break
        try:
            # 将用户输入的字符串转换为整数
            index = int(selection) - 1
            # 获取用户选择的comic的名称并输出
            print("你选择了：{}".format(data["results"]["list"][index]['comic']["name"]))
            # 返回pathWord
            return data["results"]["list"][index]['comic']["path_word"]

        except (ValueError, IndexError):
            offset = page_turning(selection, offset, data, current_page_count)
            current_page_count = offset[1]
            offset = offset[0]


def collect_expect():
    url = f"https://api.{SETTINGS['api_url']}/api/v3/member/collect/comics"
    params = {
        "limit": 12,
        "offset": 0
    }
    data = []
    want_to = int(Prompt.ask(f"请问是输出json格式还是csv格式？"
                             f"[italic yellow](0:json,1:csv)[/]",
                             choices=["0", "1"], default="1"))
    while True:
        API_HEADER['authorization'] = SETTINGS['authorization']
        res = requests.get(url, params=params, headers=API_HEADER)
        res_json = json.loads(res.text)
        if res_json["code"] != 200:
            print(f"[bold red]无法获取到相关信息，请检查相关设置。Error:{res_json['message']}")
            return
        for item in res_json['results']['list']:
            comic = item['comic']
            data.append([comic['name'], comic['path_word'], comic['datetime_updated'], comic['last_chapter_name']])

        if len(data) >= res_json['results']['total']:
            break
        else:
            params['offset'] += 12
    if want_to == 0:
        # 输出到test.json
        with open('collect.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("[green]已将您的收藏输出到运行目录下的collect.json中[/]")
    else:
        with open('collect.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Path Word', 'Update Time', 'Last Chapter'])
            writer.writerows(data)
        print("[green]已将您的收藏输出到运行目录下的collect.csv中[/]")


# 漫画详细相关

def manga_group(manga_path_word):
    response = requests.get(f"https://api.{SETTINGS['api_url']}/api/v3/comic2/{manga_path_word}",
                            headers=API_HEADER, proxies=PROXIES)
    # 记录API访问量
    api_restriction()
    response.raise_for_status()
    manga_group_json = response.json()
    # 判断是否只有默认组
    if len(manga_group_json["results"]["groups"]) == 1:
        return "default"

    manga_group_path_word_list = []
    # 获取group值并强转list
    for i, manga_group_list in enumerate(manga_group_json["results"]["groups"]):
        print(f"{i + 1}->{manga_group_json['results']['groups'][manga_group_list]['name']}")
        # 将分组的path_word添加到数组中
        manga_group_path_word_list.append(manga_group_json['results']['groups'][manga_group_list]['path_word'])
    choice = IntPrompt.ask("请输入要下载的分组前面的数字")
    return manga_group_path_word_list[choice - 1]


def manga_chapter(manga_path_word, group_path_word):
    response = requests.get(
        f"https://api.{SETTINGS['api_url']}/api/v3/comic/{manga_path_word}/group/{group_path_word}/chapters?limit=500"
        f"&offset=0&platform=3",
        headers=API_HEADER, proxies=PROXIES)
    # 记录API访问量
    api_restriction()
    response.raise_for_status()

    manga_chapter_json = response.json()
    # Todo 创建传输的json,并且之后会将此json保存为temp.json修复这个问题https://github.com/misaka10843/copymanga-downloader/issues/35
    return_json = {
        "json": manga_chapter_json,
        "start": None,
        "end": None
    }
    # Todo 支持500+话的漫画(感觉并不太需要)
    if manga_chapter_json['results']['total'] > 500:
        print("[bold red]我们暂时不支持下载到500话以上，还请您去Github中创建Issue！[/]")
        sys.exit()
    # 询问应该如何下载
    # 如果是命令行参数就直接返回对应
    if ARGS:
        return_json["start"] = int(ARGS.MangaStart) - 1
        return_json["end"] = int(ARGS.MangaEnd)
        return return_json
    want_to = int(Prompt.ask(f"获取到{manga_chapter_json['results']['total']}话内容，请问如何下载?"
                             f"[italic yellow](0:全本下载,1:范围下载,2:单话下载)[/]",
                             choices=["0", "1", "2"], default="0"))
    if want_to == 0:
        return_json["start"] = -1
        return_json["end"] = -1
        return return_json
    print(
        "[italic yellow]请注意！此话数包含了其他比如特别篇的话数，比如”第一话，特别篇，第二话“，那么第二话就是3，而不2[/]")
    if want_to == 1:
        return_json["start"] = int(Prompt.ask("请输入开始下载的话数")) - 1
        print(f"[italic blue]您选择从[yellow]{manga_chapter_json['results']['list'][return_json['start']]['name']}"
              f"[/yellow]开始下载[/]")
        return_json["end"] = int(Prompt.ask("请输入结束下载的话数")) - 1
        print(f"[italic blue]您选择在[yellow]{manga_chapter_json['results']['list'][return_json['end']]['name']}"
              f"[/yellow]结束下载[/]")
        return return_json
    if want_to == 2:
        return_json["start"] = int(Prompt.ask("请输入需要下载的话数")) - 1
        return_json["end"] = return_json["start"]
        print(f"[italic blue]您选择下载[yellow]{manga_chapter_json['results']['list'][return_json['end']]['name']}[/]")
        return return_json


def chapter_allocation(manga_chapter_json):
    if manga_chapter_json['start'] < 0:
        manga_chapter_list = manga_chapter_json['json']['results']['list']
    elif manga_chapter_json['start'] == manga_chapter_json['end']:
        # 转换为一个只包含一个元素的数组
        manga_chapter_list = [manga_chapter_json['json']['results']['list'][manga_chapter_json['start']]]
    else:
        manga_chapter_list = manga_chapter_json['json']['results']['list'][
                             manga_chapter_json['start']:manga_chapter_json['end']]
    # 准备分配章节下载
    for manga_chapter_info in manga_chapter_list:
        response = requests.get(
            f"https://api.{SETTINGS['api_url']}/api/v3/comic/{manga_chapter_info['comic_path_word']}"
            f"/chapter2/{manga_chapter_info['uuid']}?platform=3",
            headers=API_HEADER, proxies=PROXIES)
        # 记录API访问量
        api_restriction()
        response.raise_for_status()
        manga_chapter_info_json = response.json()

        img_url_contents = manga_chapter_info_json['results']['chapter']['contents']
        img_words = manga_chapter_info_json['results']['chapter']['words']
        manga_name = manga_chapter_info_json['results']['comic']['name']
        special_chars = string.punctuation + ' '
        manga_name = ''.join(c for c in manga_name if c not in special_chars)
        num_images = len(img_url_contents)
        download_path = SETTINGS['download_path']
        chapter_name = manga_chapter_info_json['results']['chapter']['name']
        # 检查漫画文件夹是否存在

        if not os.path.exists(f"{download_path}/{manga_name}/"):
            os.mkdir(f"{download_path}/{manga_name}/")
        # 创建多线程
        threads = []
        with console.status(f"[bold yellow]正在下载:[{manga_name}]{chapter_name}(索引ID:"
                            f"{int(manga_chapter_info_json['results']['chapter']['index']) + 1})[/]"):
            for i in range(num_images):
                url = img_url_contents[i]['url']
                # 检查章节文件夹是否存在
                if not os.path.exists(f"{download_path}/{manga_name}/{chapter_name}/"):
                    os.mkdir(f"{download_path}/{manga_name}/{chapter_name}/")
                # 组成下载路径
                filename = f"{download_path}/{manga_name}/{chapter_name}/{str(img_words[i] + 1).zfill(3)}.jpg"
                t = threading.Thread(target=download, args=(url, filename))
                # 开始线程
                threads.append(t)
                # 限制线程数量(十分不建议修改，不然很可能会被禁止访问)
                if len(threads) == 4 or i == num_images - 1:
                    for t in threads:
                        # 添加一点延迟，错峰请求
                        time.sleep(0.5)
                        t.start()
                    for t in threads:
                        time.sleep(0.5)
                        t.join()
                    threads.clear()
        # 实施添加下载进度
        if ARGS and ARGS.subscribe == "1":
            save_new_update(manga_chapter_info_json['results']['chapter']['comic_path_word'],
                            manga_chapter_info_json['results']['chapter']['index'] + 1)

        print(f"[bold green][:white_check_mark:][{manga_name}]{chapter_name}下载完成！[/]")
        epubTransformerhelper(download_path, manga_name, chapter_name)
        if SETTINGS['CBZ']:
            with console.status(f"[bold yellow]正在保存CBZ存档:[{manga_name}]{chapter_name}[/]"):
                create_cbz(str(int(manga_chapter_info_json['results']['chapter']['index']) + 1), chapter_name,
                           manga_name, f"{manga_name}/{chapter_name}/", SETTINGS['cbz_path'])
            print(f"[bold green][:white_check_mark:]已将[{manga_name}]{chapter_name}保存为CBZ存档[/]")


# 下载相关

@retrying.retry(stop_max_attempt_number=3)
def download(url, filename):
    # 判断是否已经下载
    if os.path.exists(filename):
        print(f"[blue]您已经下载了{filename}，跳过下载[/]")
        return
    try:
        img_api_restriction()
        if SETTINGS['HC'] == "1":
            url = url.replace("c800x.jpg", "c1500x.jpg")
        response = requests.get(url, headers=API_HEADER, proxies=PROXIES)
        with open(filename, "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(
            f"[bold red]无法下载{filename}，似乎是CopyManga暂时屏蔽了您的IP，请稍后手动下载对应章节(章节话数为每话下载输出的索引ID),ErrMsg:{e}[/]")


# API限制相关

def api_restriction():
    global API_COUNTER, IMG_API_COUNTER
    API_COUNTER += 1
    # 防止退出后立马再次运行
    current_time = OG_SETTINGS['api_time']
    time_diff = time.time() - current_time
    # 判断是否超过60秒
    if time_diff < 60 and API_COUNTER <= 1:
        API_COUNTER = API_COUNTER + OG_SETTINGS['API_COUNTER']
    if API_COUNTER >= 15:
        API_COUNTER = 0
        print("[bold yellow]您已经触发到了API请求阈值，我们将等60秒后再进行[/]")
        time.sleep(60)
    OG_SETTINGS['API_COUNTER'] = API_COUNTER
    OG_SETTINGS['api_time'] = time.time()
    # 将时间戳与API请求数量写入配置文件
    save_settings(OG_SETTINGS)


def img_api_restriction():
    global IMG_API_COUNTER, IMG_CURRENT_TIME
    IMG_API_COUNTER += 1
    # 防止退出后立马再次运行

    time_diff = time.time() - IMG_CURRENT_TIME
    # 判断是否超过60秒
    if time_diff < 60 and IMG_API_COUNTER >= 100:
        print("[bold yellow]您已经触发到了图片服务器API请求阈值，我们将等60秒后再进行[/]")
        time.sleep(60)
        IMG_CURRENT_TIME = 0
        IMG_API_COUNTER = 0


# 设置相关

def get_org_url():
    print("[italic yellow]正在获取CopyManga网站Url...[/]")
    url = "https://cdn.jsdelivr.net/gh/misaka10843/copymanga-downloader@master/url.json"
    try:
        response = requests.get(url, proxies=PROXIES)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("[bold yellow]无法链接至jsdelivr，准备直接访问Github[/]")
        # 更换URL
        url = "https://raw.githubusercontent.com/misaka10843/copymanga-downloader/master/url.json"
        try:
            response = requests.get(url, proxies=PROXIES)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[bold red]无法链接至GitHub，请检查网络连接,ErrMsg:{e}[/]", )
            sys.exit()


#检查字符串是否包含中文
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def set_settings():
    global PROXIES
    # 获取用户输入
    download_path = Prompt.ask("请输入保存路径[italic yellow](最后一个字符不能为斜杠)[/]", default=os.path.split(os.path.realpath(__file__))[0])
    use_oversea_cdn_input = Confirm.ask("是否使用海外CDN？", default=False)
    use_webp_input = Confirm.ask("是否使用Webp？[italic yellow](可以节省服务器资源,下载速度也会加快)[/]",
                                 default=True)
    proxy = Prompt.ask("请输入代理地址[italic yellow](没有的话可以直接回车跳过)[/]")
    hc_input = Confirm.ask("是否下载高分辨率图片[italic yellow](不选择可以节省服务器资源,下载速度也会加快)[/]",
                           default=False)
    cbz = Confirm.ask("是否下载后打包成CBZ？", default=False)
    send_to_kindle = Confirm.ask("是否启用半自动更新自动发送至kindle功能[italic yellow][/]", default=False)
    if cbz:
        while (True):
            cbz_path = Prompt.ask("请输入CBZ文件的保存路径[italic yellow](最后一个字符不能为斜杠)[/]")
            if (is_contains_chinese(cbz_path)):
                print("路径请不要包含中文")
            else:
                break
    else:
        cbz_path = None
    if proxy:
        PROXIES = {
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
    loginPattern = Prompt.ask("请输入登陆方式(1为token登录，2为账号密码持久登录)", default="1")
    if loginPattern == "1":
        authorization = Prompt.ask("请输入token")
    elif loginPattern == "2":
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
        "loginPattern": loginPattern,
        "salt": salt if loginPattern == "2" else None,
        "username": username if loginPattern == "2" else None,
        "password": password if loginPattern == "2" else None,
        "send_to_kindle": send_to_kindle,
        "kcc_cmd": SETTINGS["kcc_cmd"],
        "email_address": SETTINGS["email_address"],
        "email_passwd": SETTINGS["email_passwd"],
        "email_smtp_address": SETTINGS["email_smtp_address"],
        "kindle_address": SETTINGS["kindle_address"]
    }
    home_dir = os.path.expanduser("~")
    settings_path = os.path.join(home_dir, ".copymanga-downloader/settings.json")
    save_settings(settings)
    print(f"[yellow]已将配置文件存放到{settings_path}中[/]")


def change_settings():
    global PROXIES
    # 获取用户输入
    download_path = Prompt.ask("请输入保存路径[italic yellow](最后一个字符不能为斜杠)[/]",
                               default=SETTINGS['download_path'])

    use_oversea_cdn = True
    use_webp = True
    if SETTINGS['use_oversea_cdn'] == "0":
        use_oversea_cdn = False
    if SETTINGS['use_webp'] == "0":
        use_webp = False
    use_oversea_cdn_input = Confirm.ask("是否使用海外CDN？", default=use_oversea_cdn)
    use_webp_input = Confirm.ask("是否使用Webp？[italic yellow](可以节省服务器资源,下载速度也会加快)[/]",
                                 default=use_webp)
    proxy = Prompt.ask("请输入代理地址[italic yellow](如果需要清除请输入0)[/]", default=SETTINGS['proxies'])
    if SETTINGS.get('HC') is None:
        hc_input = Confirm.ask("是否下载高分辨率图片[italic yellow](不选择可以节省服务器资源,下载速度也会加快)[/]",
                               default=False)
    else:
        hc_c = True
        if SETTINGS['HC'] == "0":
            hc_c = False
        hc_input = Confirm.ask("是否下载高分辨率图片[italic yellow](不选择可以节省服务器资源,下载速度也会加快)[/]",
                               default=hc_c)
    if SETTINGS.get('CBZ') is None or not SETTINGS.get("CBZ"):
        cbz = Confirm.ask("是否下载后打包成CBZ？", default=False)
    else:
        cbz = True
        hc_input = Confirm.ask("是否下载后打包成CBZ？",
                               default=cbz)
    send_to_kindle_modify = Confirm.ask("是否需要修改kindle自动推送相关设置？[italic yellow][/]", default=False)
    if cbz:
        if SETTINGS.get('cbz_path') is None:
            SETTINGS['cbz_path'] = None

        while (True):
            cbz_path = Prompt.ask("请输入CBZ文件的保存路径[italic yellow](最后一个字符不能为斜杠)[/]",
                              default=SETTINGS['cbz_path'])
            if (is_contains_chinese(cbz_path)):
                print("路径请不要包含中文")
            else:
                break
    else:
        cbz_path = None
    if proxy != SETTINGS['proxies'] and proxy != "0":
        PROXIES = {
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
        SETTINGS["send_to_kindle"] = Confirm.ask("是否继续使用kindle推送？[italic yellow][/]", default=True)
        if SETTINGS["send_to_kindle"]:
            set_kindle_config()

    # 构造settings字典


    login_change = Confirm.ask("是否要修改登陆方式？", default=False)
    if login_change:
        loginPattern = Prompt.ask("请输入登陆方式(1为token登录，2为账号密码持久登录)", default=SETTINGS["loginPattern"])
        if loginPattern == "1":
            authorization = Prompt.ask("请输入token")
        elif loginPattern == "2":
            while True:
                username = Prompt.ask("请输入账号").strip()
                password = Prompt.ask("请输入密码").strip()
                if username == "" or password == "":
                    print("请输入账号密码")
                    continue
                else:
                    res = loginhelper(username, password, api_urls[choice - 1])
                    if res["token"]:
                        SETTINGS["username"] = f"Token {res['token']}"
                        SETTINGS["salt"] = res["salt"]
                        SETTINGS["password"] = res["password_enc"]
                        break
    else:
        loginPattern = SETTINGS["loginPattern"]
        authorization = SETTINGS["authorization"]
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
        "loginPattern": loginPattern,
        "salt": SETTINGS["salt"] if loginPattern == "2" else None,
        "username": SETTINGS["username"] if loginPattern == "2" else None,
        "password": SETTINGS["password"] if loginPattern == "2" else None,
        "send_to_kindle": SETTINGS["send_to_kindle"],
        "kcc_cmd": SETTINGS["kcc_cmd"] if SETTINGS["send_to_kindle"] else None,
        "email_address": SETTINGS["email_address"] if SETTINGS["send_to_kindle"] else None,
        "email_passwd": SETTINGS["email_passwd"] if SETTINGS["send_to_kindle"] else None,
        "email_smtp_address": SETTINGS["email_smtp_address"] if SETTINGS["send_to_kindle"] else None,
        "kindle_address": SETTINGS["kindle_address"] if SETTINGS["send_to_kindle"] else None
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
    global SETTINGS, PROXIES, OG_SETTINGS, API_HEADER
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
    necessary_fields = ["download_path", "authorization", "use_oversea_cdn", "use_webp", "proxies", "api_url"]
    for field in necessary_fields:
        if field not in settings:
            return False, "settings.json中缺少必要字段{}".format(field)
    SETTINGS = settings
    if "HC" not in settings:
        SETTINGS['HC'] = None
        print("[bold yellow]我们更新了设置，请您按照需求重新设置一下，还请谅解[/]")
        change_settings()
        print("[bold yellow]感谢您的支持，重新启动本程序后新的设置将会生效[/]")
        exit(0)
    OG_SETTINGS = settings
    # 设置请求头
    API_HEADER['use_oversea_cdn'] = settings['use_oversea_cdn']
    API_HEADER['use_webp'] = settings['use_webp']
    # 设置代理
    if settings["proxies"]:
        PROXIES = {
            "http": settings["proxies"],
            "https": settings["proxies"]
        }
    return True, None


def main():
    global ARGS
    loaded_settings = load_settings()
    if not loaded_settings[0]:
        print(f"[bold red]{loaded_settings[1]},我们将重新为您设置[/]")
        set_settings()
    parse_args()
    if ARGS:
        if ARGS.subscribe == "1":
            print(
                "[bold purple]请注意！此模式下可能会导致部分img下载失败，如果遇见报错还请您自行删除更新列表然后重新添加后运行，此程序会重新下载并跳过已下载内容[/]")
            update_download()
            sys.exit()
        if ARGS.MangaPath and ARGS.MangaEnd and ARGS.MangaStart:
            command_mode()
            # 防止运行完成后又触发正常模式
            sys.exit()
        else:
            print("[bold red]命令行参数中缺少必要字段,将切换到普通模式[/]")
            ARGS = None
    welcome()


# cbz格式转换

def create_cbz(index, title, manga_name, save_dir, cbz_dir):
    pinyin = Pinyin()
    xml_data = f"<?xml version=\"1.0\"?>\n<ComicInfo xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" " \
               f"xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n  " \
               f"<Title>{pinyin.get_pinyin(title)}</Title>\n  " \
               f"<Series>{pinyin.get_pinyin(manga_name)}</Series>\n  " \
               f"<Number>{pinyin.get_pinyin(index)}</Number>\n" \
               f"</ComicInfo>"
    with open(os.path.join(os.path.join(SETTINGS['download_path'], save_dir), "ComicInfo.xml"), "w") as file:
        file.write(xml_data)

    start_dir = os.path.join(SETTINGS['download_path'], save_dir)
    file_name = f"{save_dir}/{pinyin.get_pinyin(manga_name)}/{manga_name}{title}.cbz"
    file_path = os.path.join(cbz_dir, file_name)

    # 只添加指定类型的文件到zip文件中
    allowed_ext = ['.xml', '.jpg', '.png', '.jpeg', '.webp']
    with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for dir_path, dir_names, filenames in os.walk(start_dir):
            fpath = dir_path.replace(start_dir, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                ext = os.path.splitext(filename)[1].lower()
                if ext in allowed_ext:
                    zip_file.write(os.path.join(dir_path, filename), fpath + filename)


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
    res = login(**{"username": username, "password": password_enc, "url": url, "salt": salt, "proxy": PROXIES})
    return {"token": res, "salt": salt, "password_enc": password_enc}


def loginInformationBuilder(username: str, password: str, url: str, salt: str, proxy: dict) -> dict:
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


def epubTransformer(path: str, name: str, chapter: str) -> None:
    """
    将下载好的图片转化为epub待发送

    :param path: 漫画存放的根地址
    :param name: 漫画的名称
    :param chapter: 漫画的章节
    :return: 空
    """
    global SETTINGS
    # 定义命令和参数
    # command = SETTINGS["kcc_cmd"]
    arguments = ["-o", f'{path}/{name}/{chapter}/{name} {chapter}.epub', "-t", f"{name} {chapter}", f'{path}/{name}/{chapter}']
    command = SETTINGS["kcc_cmd"].split(" ") + arguments
    subprocess.run(command, shell=True, capture_output=True, text=True)



def mailtest(sender: str, passwd: str, receiver: str, smtp_address: str, message: str) -> bool:
    """
    用于测试邮件是否可用

    :param sender:
    :param passwd:
    :param receiver:
    :param smtp_address:
    :param message:
    :return: 发送成功返回 True, 如果发送失败会返回 False
    """
    try:
        my_sender = sender
        my_pass = passwd
        my_user = receiver

        msg = MIMEMultipart()

        msg['From'] = sender

        file = MIMEBase('application', 'octet-stream')
        file.add_header('Content-Disposition', 'attachment', filename=f"{message}.txt")
        file.set_payload(message.encode())
        encoders.encode_base64(file)
        msg.attach(file)
        msg['From'] = Header(my_sender)

        server = smtplib.SMTP_SSL(smtp_address, 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, my_user, msg.as_string())
        server.quit()

    except Exception as e:
        return False
    return True


def mail(fd) -> bool:
    """
    发送邮件函数

    :param fd: io文件句柄
    :return: 发送成功为真，否则为假
    """
    global SETTINGS
    try:
        message = MIMEMultipart()
        file = MIMEBase('application', 'octet-stream')
        file.add_header('Content-Disposition', 'attachment', filename=fd.name.split("/")[-1])
        file.set_payload(fd.read())
        encoders.encode_base64(file)
        message.attach(file)
        message['From'] = Header(SETTINGS["email_address"])

        server = smtplib.SMTP_SSL(SETTINGS["email_smtp_address"], 465)
        server.login(SETTINGS["email_address"], SETTINGS["email_passwd"])
        server.sendmail(SETTINGS["email_address"], SETTINGS["kindle_address"], message.as_string())
        server.quit()

    except Exception as e:
        return False
    return True


def set_kindle_config() -> None:
    """
    发送到kindle的设置

    :return: 空
    """
    global SETTINGS
    system = platform.system()
    path = os.path.split(os.path.realpath(__file__))[0]
    while not SETTINGS['kcc_cmd']:
        if system == "Windows":
            tmp = Prompt.ask("请输入kcc_c2e路径[italic yellow](建议先查看配置教程 https://www.pursuecode.cn/archives/1705162565893，默认为copymanga-downloader目录)[/]",
                             default=path) + "/kcc_c2e.exe"
        else:
            tmp = Prompt.ask("请输入kcc_c2e路径[italic yellow](建议先查看配置教程 https://www.pursuecode.cn/archives/1705162565893,默认为copymanga-downloader目录)[/]",
                             default=path) + "/kcc_c2e"
        if is_contains_chinese(tmp):
            print("kcc_c2e路径请不要包含中文")
            continue

        if os.path.exists(tmp):
            devices = "K1, K2, K34, K578, KDX, KPW, KPW5, KV, KO, K11, KS, KoMT, KoG, KoGHD, KoA, KoAHD, KoAH2O, KoAO, KoN, KoC, KoL, KoF, KoS, KoE"
            deviceset = set(devices.split(", "))
            while True:
                device = Prompt.ask(f"请输入kcc设备参数, 支持的设备有{devices}[italic yellow][/]", default=False)
                device = device.strip()
                if device not in deviceset:
                    print("设备不存在，请重新输入")
                else:
                    break
            SETTINGS["kcc_cmd"] = f"{tmp} -p {device} -f EPUB"
            break
        else:
            print("kcc_c2e不存在，请确认程序名称是否为kcc_c2e或是否安装kcc_c2e并且路径不含中文")

    check = Confirm.ask("是否需要发送验证码到kindle验证[italic yellow][/]", default=False)
    while True:
        email_address = Prompt.ask("请输入邮箱smtp账号[italic yellow](建议查看配置教程)[/]")
        email_passwd = Prompt.ask("请输入邮箱smtp密码[italic yellow][/]")
        email_smtp_address = Prompt.ask("请输入邮箱smtp的地址[italic yellow][/]")
        kindle_address = Prompt.ask("请输入kindle推送邮件地址[italic yellow](如twoonefour_ABCDQA@kindle.com，具体请查看amazon设置)[/]")
        # email_address = "489643427@qq.com"
        # email_passwd = "xulsahtupltibjbh"
        # email_smtp_address = "smtp.qq.com"
        # kindle_address = "lys214412_uoeyap@kindle.com"
        if check:
            code = str(random.randint(100000, 999999))
            if mailtest(email_address, email_passwd, kindle_address, email_smtp_address, code):
                if code == Prompt.ask("请输入kindle上显示的验证码[italic yellow][/]"):
                    print("验证码正确，验证成功")
                    break
                else:
                    print("验证码错误，请重新输入配置")
        else:
            break
    SETTINGS["email_address"] = email_address
    SETTINGS["email_passwd"] = email_passwd
    SETTINGS["kindle_address"] = kindle_address
    SETTINGS["email_smtp_address"] = email_smtp_address


def epubTransformerhelper(download_path, manga_name, chapter_name) -> None:
    """
    辅助函数，用于转换epub

    :param download_path:
    :param manga_name:
    :param chapter_name:
    :return:
    """
    global SETTINGS
    if SETTINGS["send_to_kindle"]:
        if not os.path.exists(f'{download_path}/{manga_name}/{chapter_name}/{manga_name} {chapter_name}.epub'):
            epubTransformer(path=download_path, name=manga_name, chapter=chapter_name)
        with open(f'{download_path}/{manga_name}/{chapter_name}/{manga_name} {chapter_name}.epub', "rb") as f:
            mail(f)


if __name__ == '__main__':
    main()
