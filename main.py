# -*- coding: UTF-8 -*-
import json
import os
import platform
import sys
import time
from turtle import width
from typing import Counter

import requests
from tqdm import tqdm

# 全局化headers，节省空间
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
api_headers = {
    'User-Agent': 'Dart/2.15(dart:io)',
    'source': 'copyApp',
    'version': '1.3.1',
    'region': '1',
    'webp': '0',
}
proxies = {}


def get_url():
    # *从GitHub(首先两个为CDN，方便中国大陆用户获取)中获取url的信息
    response = requests.get(
        'https://raw.fastgit.org/misaka10843/copymanga-downloader/master/url.json',
        headers=headers)
    if response.status_code != 200:
        print("您的网络似乎不支持fastgit，我们正在切换新的请求地址")
        response = requests.get(
            'https://fastly.jsdelivr.net/gh/misaka10843/copymanga-downloader@master/url.json',
            headers=headers)
        if response.status_code != 200:
            print("您的网络似乎也不支持jsdelivr，我们只能请求GitHub原站了")
            response = requests.get(
                'https://raw.githubusercontent.com/misaka10843/copymanga-downloader/master/url.json',
                headers=headers)
            if response.status_code != 200:
                print("我们无法获取到相关信息，请检查网络后重试")
                # *直接退出
                exit()
    url_list = response.json()
    print("我们获取到copymanga有以下域名，请选择您希望使用的域名来确保连接通畅:")
    list_num = 0
    for i in url_list:
        # *循环输出url信息
        print(list_num, '->', i)
        list_num = list_num + 1
    get_url_list_num = input("您希望通过第几个域名来获取相关信息?(默认0)：")
    if len(get_url_list_num) == 0:
        get_url_list_num = 0
    # *从用户选择中获取到url信息并返回
    url = url_list[int(get_url_list_num)]
    return url


def get_settings():
    global download_path, proxies, Api_url, Authorization
    # *初始化第一次初始化的开关（默认为关）
    first_initialization = 0
    if not os.path.isfile("./settings.json"):
        file = open('./settings.json', 'w')
        file.close()
        # *打开
        first_initialization = 1
    elif os.path.getsize("./settings.json") == 0:
        # *打开
        first_initialization = 1
    # *如果为第一次初始化
    if first_initialization == 1:
        json_data = {}
        download_path = input(
            "您似乎是第一次启动此程序，请您先输入您需要下载的路径(请输入E:\\manga这种格式,不要最后一个斜杠哦qwq)：")
        # *将反斜杠转成正斜杠
        json_data["download_path"] = download_path.replace('\\', '/')
        print("\n接下来填写的是获取您的收藏漫画需要的参数，请认真填写哦qwq(如果不想获取的话也可以直接填写null)\n")
        cookies_get = input(
            "请输入您的authorization(如不会获取请看https://t.hk.uy/bdFu ("
            "此为获取用户收藏漫画,下载服务不受影响))：")
        json_data["authorization"] = cookies_get
        if input("是否使用海外CDN？(y/n)：").lower() == 'y':
            json_data["use_oversea_cdn"] = True
        else:
            json_data["use_oversea_cdn"] = False
        # *是否为了节省服务器带宽而使用webp
        if input("是否下载webp格式图片(可以节省服务器资源)？(y/n)：").lower() == 'y':
            json_data["use_webp"] = True
        else:
            json_data["use_webp"] = False
        # *获取proxies状态
        proxies_get = input(
            "您是否使用了代理？如果是，请填写代理地址(如http://127.0.0.1:8099或者socks5://127.0.0.1:8099)：")
        json_data["proxies"] = proxies_get
        # *获取最新的域名状态
        json_data["api_url"] = get_url()
        # *写入文件
        with open('./settings.json', 'w', encoding="utf-8") as fp:
            json.dump(json_data, fp, indent=2, ensure_ascii=False)

        print("恭喜您已经完成初始化啦！\n我们将立即执行主要程序，\n如果您需要修改设置的话可以直接到程序根目录的settings.json更改qwq")
    # *读取设置内容
    with open('./settings.json', 'r', encoding="utf-8") as fp:
        json_data = json.load(fp)
        #! 只要下载路径/请求地址是空，那么就直接报错
        if not json_data["download_path"] or not json_data["api_url"]:
            print("\033[1;31m 您的设置似乎出现了问题导致部分设置丢失，请您重新启动此程序后重新设置\033[37m")
            fp.close()
            os.rename("./settings.json", "./settings_old.json")
            exit()
        download_path = json_data["download_path"]
        if json_data["authorization"]:
            headers["authorization"] = json_data["authorization"]
        else:
            headers["authorization"] = "null"
            Authorization = 0
        proxies_set = json_data["proxies"]
        Api_url = json_data["api_url"]
        if json_data["use_oversea_cdn"] == True:
            api_headers["region"] = '0'
        if json_data["use_webp"] == True:
            api_headers["webp"] = '1'

    if proxies_set:
        # 如果代理不存在协议前缀，则视为http代理
        if proxies_set.find('://') == -1:
            proxies_set = 'http://' + proxies_set
        proxies = {
            'http': proxies_set,
            'https': proxies_set
        }
    # *检测是否有此目录，没有就创建
    if not os.path.exists("%s/" % download_path):
        os.mkdir("%s/" % download_path)


def manga_search(manga_name):
    global get_list_name, get_list_manga
    print("正在搜索中...\r", end="")
    # *获取搜索结果
    response = requests.get(
        'https://api.%s/api/v3/search/comic?format=json&limit=20&offset=0&platform=3&q=%s' % (
            Api_url, manga_name),
        headers=api_headers, proxies=proxies)
    print("搜索完毕啦！  \n")
    # !简要判断是否服务器无法连接
    if response.status_code == 200:
        # *将api解析成json
        manga_search_list = response.json()
        # *初始化列表的序号
        list_num = 0

        print("已搜索出以下漫画(如果没有您要找的漫画，请更换关键词即可)：")
        # *循环输出搜索列表
        for i in manga_search_list["results"]["list"]:
            print(list_num, '->', i["name"])
            list_num = list_num + 1
        get_list_num = input("您需要下载的漫画是序号几？(默认0)：")
        if len(get_list_num) == 0:
            get_list_num = 0
        get_list_name = manga_search_list["results"]["list"][int(
            get_list_num)]["path_word"]
        get_list_manga = manga_search_list["results"]["list"][int(
            get_list_num)]["name"]
    else:
        # *报告远程服务器无法连接的状态码
        print("服务器似乎\033[1;31m 无法连接\033[37m 了qwq\n")
        print("如需使用代理，可使用命令，如：set https_proxy=http://127.0.0.1:7890，或者在settings.json中设置代理")
        print("返回的状态码是：%d" % response.status_code)
        sys.exit(0)


def manga_chapter_group(Manga_pathWord):
    chapter_group = requests.get(
        'https://api.%s/api/v3/comic2/%s'
        % (Api_url, Manga_pathWord), headers=api_headers, proxies=proxies)
    chapter_group_list = chapter_group.json()
    if chapter_group.status_code == 200:
        # * 获取group值并强转list
        group_list = list(chapter_group_list["results"]["groups"].keys())
        if len(group_list) == 1:
            return "default"
        else:
            print("我们获取到了一些不同的分组，请输入需要下载的分组序号(默认为‘默認’):")
            list_num = 0
            # *循环输出
            while list_num < len(group_list):
                print(list_num, '->',
                      chapter_group_list["results"]["groups"][group_list[list_num]]["name"])
                list_num = list_num + 1
            # *获取选项
            Get_group = input()
            # *添加默认选项
            if len(Get_group) == 0:
                Get_group = 0
            else:
              Get_group = int(Get_group)
            # *将path_word传给manga_chapter_list
            return chapter_group_list["results"]["groups"][group_list[Get_group]]["path_word"]


def manga_chapter_list():
    global all_chapter, start_chapter, end_chapter, manga_chapter
    group_name = manga_chapter_group(get_list_name)
    # *获取章节列表
    manga_chapter = requests.get(
        'https://api.%s/api/v3/comic/%s/group/%s/chapters?limit=500&offset=0&platform=3'
        % (Api_url, get_list_name, group_name), headers=api_headers, proxies=proxies)
    # !简要判断是否服务器无法连接
    if manga_chapter.status_code == 200:
        # *将api解析成json
        chapter_list = manga_chapter.json()
        print("我们获取了\033[1;33m %s\033[37m 话的内容，请问是如何下载呢？" %
              chapter_list["results"]["total"])
        # *判断用户需要怎么下载
        how_download = input("1->全本下载\n2->范围下载\n3->单话下载\n您的选择是(默认全本下载)：")
        all_chapter = 0  # !防止误触发
        if len(how_download) == 0:
            how_download = 1
        if int(how_download) == 1:
            all_chapter = 1
        elif int(how_download) == 2:
            start_chapter = input("从第几话？")
            end_chapter = input("到第几话？")
        elif int(how_download) == 3:
            start_chapter = end_chapter = input("下载第几话？")
    else:
        # *报告远程服务器无法连接的状态码
        print("服务器似乎\033[1;31m 无法连接\033[37m 了qwq\n")
        print("返回的状态码是：%d" % manga_chapter.status_code)
        sys.exit(0)


def download(url: str, fname: str, img_num: str):
    # 用流stream的方式获取url的数据
    resp = requests.get(url, stream=True, verify=False)
    # 拿到文件的长度，并把total初始化为0
    total = int(resp.headers.get('content-length', 0))
    # 打开当前目录的fname文件(名字你来传入)
    # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
    with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
            bar.set_description("\r正在下载[%s]第%s张: %s" % (fname, img_num, size))


def manga_download():
    # *解析全局传输的json
    manga_chapter_list = manga_chapter.json()
    # *判断是否为全本下载
    if all_chapter == 1:
        # *开始循环
        for i in manga_chapter_list["results"]["list"]:
            # *获取每章的图片url以及顺序
            response = requests.get(
                'https://api.%s/api/v3/comic/%s/chapter2/%s?platform=3' % (
                    Api_url, get_list_name, i["uuid"]),
                headers=api_headers, proxies=proxies)
            response = response.json()
            j = 0
            # *通过获取的数量来循环
            while i["size"] > j:
                # 直接传给chapter_analysis做调用download
                chapter_analysis(response, j)
                j = j + 1
        # *试图跳出循环
        if(platform.system() == 'Windows'):
            os.system("cls")
        else:
            os.system("clear")
        print(
            "这个漫画已经全部下载完了qwq                                                     ")
        time.sleep(10)
        sys.exit(0)
    elif all_chapter == 0:
        # *通过输入的数量来循环
        startchapter = start_chapter
        while int(end_chapter) >= int(startchapter):
            # ?因为数组为0开始，所以必须减去1
            startchapter_id = int(startchapter) - 1
            # *获取每章的图片url以及顺序
            response = requests.get(
                'https://api.%s/api/v3/comic/%s/chapter2/%s?platform=3' % (
                    Api_url, get_list_name, manga_chapter_list["results"]["list"][startchapter_id]["uuid"]), headers=api_headers,
                proxies=proxies)
            response = response.json()
            j = 0
            # *通过获取的数量来循环
            while manga_chapter_list["results"]["list"][startchapter_id]["size"] > j:
                # 直接传给chapter_analysis做调用download
                chapter_analysis(response, j)
                j = j + 1
            startchapter = int(startchapter) + 1
        # *试图跳出循环
        if(platform.system() == 'Windows'):
            os.system("cls")
        else:
            os.system("clear")
        print(
            "这个漫画已经全部下载完了qwq                                                     ")
        # *返回到初始界面
        welcome()


def chapter_analysis(response, j):
    img_url = response["results"]["chapter"]["contents"][j]["url"]
    img_num = response["results"]["chapter"]["words"][j]
    chapter_index = response["results"]["chapter"]["index"] + 1
    chapter_name = response["results"]["chapter"]["name"]
    # *检测是否有此目录，没有就创建
    if not os.path.exists("%s/%s/" % (download_path, get_list_manga)):
        os.mkdir("%s/%s/" % (download_path, get_list_manga))
    if not os.path.exists("%s/%s/%.3d - %s/" % (download_path, get_list_manga, chapter_index, chapter_name)):
        os.mkdir("%s/%s/%.3d - %s/" %
                 (download_path, get_list_manga, chapter_index, chapter_name))
    # 分析图片位置以及名称
    img_ext = 'webp' if img_url.endswith('webp') else 'jpg'
    img_path = "%s/%s/%.3d - %s/%s.%s" % (
        download_path, get_list_manga, chapter_index, chapter_name, img_num, img_ext)
    download(img_url, img_path, img_num)


def manga_collection(offset):
    global get_list_name, get_list_manga
    if Authorization == 0:
        print(
            "您并未填写Authorization，请按照https://t.hk.uy/bdFu填写并添加到settings.json中的authorization字段")
        return
    manga_search_list = ""
    print("正在查询中...\r", end="")
    response = requests.get(
        'https://%s/api/v3/member/collect/comics?limit=12&offset={'
        '%s}&free_type=1&ordering=-datetime_modifier' % (Api_url, offset),
        headers=headers, proxies=proxies)
    print("查询完毕啦！  \n")
    # !简要判断是否服务器无法连接
    if response.status_code == 200:
        # *将api解析成json
        manga_search_list = response.json()
        # *初始化列表的序号
        list_num = 0

        # print("已查询出以下漫画(输入pn为下一页，pu为上一页)：")
        print("已查询出以下漫画(暂且只能查询前50个)：")
        # *循环输出搜索列表
        for i in manga_search_list["results"]["list"]:
            print(list_num, '->', i["comic"]["name"])
            list_num = list_num + 1
        get_list_num = input("您需要下载的漫画是序号几？(默认0)：")
        if len(get_list_num) == 0:
            get_list_num = 0
        # Todo：查询漫画时翻页功能
        # 因为一些原因，无法使用下列方法查询其他页数漫画
        # if get_list_num == "pn":
        #    offsetnum = offset + 12
        #    print(offsetnum)
        #    manga_collection(offsetnum)
        # elif get_list_num == "pu":
        #    if offset == "0":
        #        print("没有上一页了qwq")
        #        manga_collection()
        #    else:
        #        offsetnum = offset - 12
        #        manga_collection(offsetnum)
        # offsetnum = offset - 12
        # manga_collection(offsetnum)
        get_list_name = manga_search_list["results"]["list"][int(
            get_list_num)]["comic"]["name"]
        manga_search(get_list_name)
    else:
        # *报告远程服务器无法连接的状态码
        print("服务器似乎\033[1;31m 无法连接\033[37m 了qwq\n")
        print("返回的状态码是：%d" % response.status_code)
        sys.exit(0)


def manga_collection_backup():
    global get_list_name, get_list_manga
    if Authorization == 0:
        print(
            "您并未填写Authorization，请按照https://t.hk.uy/bdFu填写并添加到settings.json中的authorization字段")
        return
    manga_search_list = ""
    print("正在查询中...\r", end="")
    response = requests.get(
        'https://%s/api/v3/member/collect/comics?limit=500&offset=0&free_type=1&ordering=-datetime_modifier' % Api_url,
        headers=headers, proxies=proxies)
    print("查询完毕啦！  \n")
    # !简要判断是否服务器无法连接
    if response.status_code == 200:
        # *将api解析成json
        manga_search_list = response.json()
        # *初始化列表的序号
        manga_list = manga_search_list["results"]["list"]
        # 输出txt
        print("正在输出到程序目录下的backup.csv....")
        f = open("./backup.csv", "w", encoding='GBK')
        f.write('漫画名,最后更新时间\n')
        for line in manga_list:
            f.write('%s,%s\n' % (line["comic"]["name"],
                    line["comic"]["datetime_updated"]))
        f.close()
        f = open("./backup.txt", "w", encoding='utf-8')
        # 输出txt
        print("正在输出到程序目录下的backup.txt....")
        for line in manga_list:
            f.write('%s\n' % line["comic"]["name"])
        f.close()
        print("写入完成！(SCV请用Excel打开，编码为GBK)")
        welcome()
    else:
        # *报告远程服务器无法连接的状态码
        print("服务器似乎\033[1;31m 无法连接\033[37m 了qwq\n")
        print("返回的状态码是：%d" % response.status_code)
        sys.exit(0)


def welcome():
    is_search = input("您是想搜索还是查看您的收藏？(0:导出收藏,1:搜索,2:收藏  默认1):")
    if is_search == "2":
        manga_collection(0)
    elif is_search == "0":
        manga_collection_backup()
    else:
        manga_name = input("请输入漫画名称:")
        manga_search(manga_name)


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    get_settings()
    welcome()
    manga_chapter_list()
    manga_download()
