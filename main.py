import argparse
import datetime
import json
import os
import threading
import time

import retrying as retrying
from rich import print as print
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt

import requests as requests

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
    "api_time": 0.0,
    "API_COUNTER": 0
}

# 全局化设置,备份,防止命令行参数导致设置错位
OG_SETTINGS = {
    "download_path": None,
    "authorization": None,
    "use_oversea_cdn": None,
    "use_webp": None,
    "proxies": None,
    "api_url": None,
    "api_time": 0.0,
    "API_COUNTER": 0
}

API_COUNTER = 0


# Todo 命令行模式的话其实可以直接输入choice_manga_path_word和manga_group_path_word给manga_chapter()，
#  然后在此函数里面接收一下start与end，然后传给chapter_allocation()即可
def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--MangaPath',
        help='漫画的全拼，https://copymanga.site/comic/这部分')
    parser.add_argument(
        '--MangaGroup',
        help='漫画的分组Path_Word，默认为default',default='default')

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
    want_to = int(Prompt.ask("您是想搜索还是查看您的收藏？[italic yellow](0:导出收藏,1:搜索,2:收藏)[/]",
                             choices=["0", "1", "2"], default="1"))
    if want_to == 0:
        print()
        return
    if want_to == 1:
        choice_manga_path_word = search()

    if want_to == 2:
        choice_manga_path_word = search_on_collect()
    manga_group_path_word = manga_group(choice_manga_path_word)
    manga_chapter_json = manga_chapter(choice_manga_path_word, manga_group_path_word)
    chapter_allocation(manga_chapter_json)


# 搜索相关

def search():
    search_content = Prompt.ask("您需要搜索什么漫画呢")
    url = "https://api.%s/api/v3/search/comic?format=json&platform=3&q=%s&limit=10&offset={}" % (
        SETTINGS["api_url"], search_content)
    offset = 0
    current_page_count = 1
    while True:
        # 发送GET请求
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


# 收藏相关

def search_on_collect():
    url = "https://%s/api/v3/member/collect/comics?limit=12&offset={}&free_type=1&ordering=-datetime_modifier" % (
        SETTINGS["api_url"])
    API_HEADER['authorization'] = SETTINGS['authorization']
    offset = 0
    current_page_count = 1
    while True:
        # 发送GET请求
        response = requests.get(url.format(offset), headers=API_HEADER, proxies=PROXIES)
        # 记录API访问量
        api_restriction()
        # 解析JSON数据
        data = response.json()
        if data['code'] == 401:
            settings_dir = os.path.join(os.path.expanduser("~"), ".copymanga-downloader/settings.json")
            print(f"[bold red]请求出现问题！疑似Token问题！[{data['message']}][/]")
            print(f"[bold red]请删除{settings_dir}来重新设置！(或者也可以自行修改配置文件)[/]")
            exit()
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
    # Todo 在这里添加支持命令行参数的代码
    return_json = {
        "json": manga_chapter_json,
        "start": None,
        "end": None
    }
    # Todo 支持500+话的漫画(感觉并不太需要)
    if manga_chapter_json['results']['total'] > 500:
        print("[bold red]我们暂时不支持下载到500话以上，还请您去Github中创建Issue！[/]")
        exit()
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
        return_json["end"] = int(Prompt.ask("请输入结束下载的话数"))
        return return_json
    if want_to == 2:
        return_json["start"] = int(Prompt.ask("请输入需要下载的话数")) - 1
        return_json["end"] = return_json["start"]
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
    print(manga_chapter_list)
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
        num_images = len(img_url_contents)
        download_path = SETTINGS['download_path']
        chapter_name = manga_chapter_info_json['results']['chapter']['name']
        # 检查漫画文件夹是否存在
        if not os.path.exists(f"{download_path}/{manga_name}/"):
            os.mkdir(f"{download_path}/{manga_name}/")
        # 创建多线程
        threads = []
        with console.status(f"[bold yellow]正在下载:[{manga_name}]{chapter_name}[/]"):
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
        print(f"[bold green][:white_check_mark: ][{manga_name}]{chapter_name}下载完成！[/]")


# API限制相关

def api_restriction():
    global API_COUNTER
    API_COUNTER += 1
    # 防止退出后立马再次运行
    current_time = OG_SETTINGS['api_time']
    time_diff = current_time - time.time()
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
    home_dir = os.path.expanduser("~")
    if not os.path.exists(os.path.join(home_dir, '.copymanga-downloader/')):
        os.mkdir(os.path.join(home_dir, '.copymanga-downloader/'))
    settings_path = os.path.join(home_dir, ".copymanga-downloader/settings.json")
    # 写入settings.json文件
    with open(settings_path, "w") as f:
        json.dump(OG_SETTINGS, f)


# 下载相关

@retrying.retry(stop_max_attempt_number=3)
def download(url, filename):
    # 判断是否已经下载
    if os.path.exists(filename):
        print(f"[blue]您已经下载了{filename}，跳过下载[/]")
        return
    try:
        response = requests.get(url, headers=API_HEADER, proxies=PROXIES)
        with open(filename, "wb") as f:
            f.write(response.content)
    except:
        print(f"[bold red]无法下载{filename}，似乎是CopyManga暂时屏蔽了您的IP，请稍后重试或检查网络连接[/]")


# 设置相关

def get_org_url():
    print("[italic yellow]正在获取CopyManga网站Url...[/]")
    url = "https://cdn.jsdelivr.net/gh/misaka10843/copymanga-downloader@master/url.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except:
        print("[bold yellow]无法链接至jsdelivr，准备直接访问Github[/]")
        # 更换URL
        url = "https://raw.githubusercontent.com/misaka10843/copymanga-downloader/master/url.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except:
            print("[bold red]无法链接至GitHub，请检查网络连接[/]", )
            exit()


def set_settings():
    # 获取用户输入
    download_path = Prompt.ask("请输入保存路径")
    authorization = Prompt.ask("请输入账号Token")
    use_oversea_cdn_input = Confirm.ask("是否使用海外CDN？", default=False)
    use_webp_input = Confirm.ask("是否使用Webp？[italic yellow](可以节省服务器资源,下载速度也会加快)[/]",
                                 default=True)
    proxy = Prompt.ask("请输入代理地址[italic yellow](没有的话可以直接回车跳过)[/]")
    api_urls = get_org_url()
    for i, url in enumerate(api_urls):
        print(f"{i + 1}->{url}")
    choice = IntPrompt.ask("请输入要使用的API前面的数字")

    # input转bool
    use_oversea_cdn = "0"
    use_webp = "0"
    if use_oversea_cdn_input:
        use_oversea_cdn = "1"
    if use_webp_input:
        use_webp = "1"

    # 构造settings字典
    settings = {
        "download_path": download_path,
        "authorization": authorization,
        "use_oversea_cdn": use_oversea_cdn,
        "use_webp": use_webp,
        "proxies": proxy,
        "api_url": api_urls[choice - 1],
        "api_time": 0.0,
        "API_COUNTER": 0
    }
    home_dir = os.path.expanduser("~")
    if not os.path.exists(os.path.join(home_dir, '.copymanga-downloader/')):
        os.mkdir(os.path.join(home_dir, '.copymanga-downloader/'))
    settings_path = os.path.join(home_dir, ".copymanga-downloader/settings.json")
    # 写入settings.json文件
    with open(settings_path, "w") as f:
        json.dump(settings, f)
    print(f"[yellow]已将配置文件存放到{settings_path}中[/]")


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
        if ARGS.MangaPath and ARGS.MangaEnd and ARGS.MangaStart:
            command_mode()
            # 防止运行完成后又触发正常模式
            exit()
        else:
            print("[bold red]命令行参数中缺少必要字段,将切换到普通模式[/]")
            ARGS = None
    welcome()


if __name__ == '__main__':
    main()
