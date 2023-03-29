import argparse
import datetime
import json
import os
from rich import print as print
from rich.prompt import Prompt, Confirm, IntPrompt

import requests as requests

# 全局化headers，节省空间

API_HEADER = {
    'User-Agent': '"User-Agent" to "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44"',
    'version': datetime.datetime.now().strftime("%Y.%m.%d"),
    'region': '0',
    'webp': '0',
    "platform": "1",
    "referer": "https://www.copymanga.site/"
}
PROXIES = {}
# 全局化设置
SETTINGS = None


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--MangaPath',
        help='漫画的全拼，https://copymanga.site/comic/这部分')

    parser.add_argument('--Url', help='copymanga的域名,如使用copymanga.site，那就输入site')

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

    parser.add_argument('--MangaStart', help='漫画开始下载话')

    parser.add_argument('--MangaEnd', help='漫画结束下载话(如果只想下载一话请与MangaStart相同)')

    parser.add_argument('--MangaList', help='漫画下载列表txt(每行一个漫画的全拼，具体请看Readme)')

    parser.add_argument('--Proxy', help='设置代理')

    args = parser.parse_args()

    return args


def welcome():
    Prompt.ask(
        "您是想搜索还是查看您的收藏？[italic yellow](0:导出收藏,1:搜索,2:收藏)[/italic yellow]",
        choices=["0", "1", "2"], default="1")


# 设置相关

def get_org_url():
    print("[italic yellow]正在获取CopyManga网站Url...[/italic yellow]")
    url = "https://cdn.jsdelivr.net/gh/misaka10843/copymanga-downloader@master/url.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except:
        print("[bold yellow]无法链接至jsdelivr，准备直接访问Github[/bold yellow]")
        # 更换URL
        url = "https://raw.githubusercontent.com/misaka10843/copymanga-downloader/master/url.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except:
            print("[bold red]无法链接至GitHub，请检查网络连接[/bold red]", )
            exit()


def set_settings():
    # 获取用户输入
    download_path = Prompt.ask("请输入保存路径")
    authorization = Prompt.ask("请输入账号Token")
    use_oversea_cdn_input = Confirm.ask("是否使用海外CDN？", default=False)
    use_webp_input = Confirm.ask("是否使用Webp？[italic yellow](可以节省服务器资源,下载速度也会加快)[/italic yellow]",
                                 default=True)
    proxy = Prompt.ask("请输入代理地址[italic yellow](没有的话可以直接回车跳过)[/italic yellow]")

    api_urls = get_org_url()
    for i, url in enumerate(api_urls):
        print(f"{i + 1}->{url}")
    choice = IntPrompt.ask("请输入要使用的API前面的数字")

    # input转bool
    use_oversea_cdn = False
    use_webp = False
    if use_oversea_cdn_input == "Y":
        use_oversea_cdn = True
    if use_webp_input != "N":
        use_webp = True

    # 构造settings字典
    settings = {
        "download_path": download_path,
        "authorization": authorization,
        "use_oversea_cdn": use_oversea_cdn,
        "use_webp": use_webp,
        "proxies": proxy,
        "api_url": api_urls[choice - 1]
    }

    # 写入settings.json文件
    with open(os.path.join(os.getcwd(), "copymanga-downloader.json"), "w") as f:
        json.dump(settings, f)


def load_settings():
    global SETTINGS
    # 获取用户目录的路径
    home_dir = os.path.expanduser("~")
    settings_path = os.path.join(home_dir, "copymanga-downloader.json")
    print(settings_path)
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
            return False, "copymanga-downloader.json中缺少必要字段{}".format(field)
    SETTINGS = settings


def main():
    loaded_settings = load_settings()
    if not loaded_settings[0]:
        print(f"[bold red]{loaded_settings[1]},我们将重新为您设置[/bold red]")
        set_settings()


if __name__ == '__main__':
    main()
