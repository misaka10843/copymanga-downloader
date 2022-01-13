# -*- coding: UTF-8 -*-
import sys
import os
import json
import requests
import time


def get_settings():
    global download_path, authorization
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
        download_path = input(
            "您似乎是第一次启动此程序，请您先输入您需要下载的路径(请输入E:\manga这种格式,不要最后一个斜杠哦qwq)：")
        # *将反斜杠转成正斜杠
        download_path = download_path.replace('\\', '/')
        print("\n接下来填写的是获取您的收藏漫画需要的参数，请认真填写哦qwq(如果不想获取的话也可以直接填写null)\n")
        cookies_get = input(
            "请输入您的authorization(如不会获取请看https://github.com/misaka10843/copymanga-download#如何获取authorization(此为获取用户收藏漫画))：")
        # *写入文件
        with open('./settings.json', 'wb')as fp:
            jsonsrt = '{"download_path" : "%s","authorization":"%s"}' % (
                download_path, cookies_get)
            fp.write(jsonsrt.encode())
        print("恭喜您已经完成初始化啦！\n我们将立即执行主要程序，\n如果您需要修改路径的话可以直接到程序根目录的settings.json更改qwq")
    with open('./settings.json', 'rb')as fp:
        json_data = json.load(fp)
        download_path = json_data["download_path"]
        authorization = json_data["authorization"]
    # *检测是否有此目录，没有就创建
    if not os.path.exists("%s/" % (download_path)):
        os.mkdir("%s/" % (download_path))


def manga_search(manga_name):
    global get_list_name, get_list_manga
    print("正在搜索中...\r", end="")
    # *获取搜索结果
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    response = requests.get(
        'https://api.copymanga.com/api/v3/search/comic?format=json&limit=20&offset=0&platform=3&q=%s' % manga_name, headers=headers)
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
        get_list_num = input("您需要下载的漫画是序号几？：")
        get_list_name = manga_search_list["results"]["list"][int(
            get_list_num)]["path_word"]
        get_list_manga = manga_search_list["results"]["list"][int(
            get_list_num)]["name"]
    else:
        # *报告远程服务器无法连接的状态码
        print("服务器似乎\033[1;31m 无法连接\033[37m 了qwq\n")
        print("如需使用代理，可使用命令，如：set https_proxy=http://127.0.0.1:7890")
        print("返回的状态码是：%d" % response.status_code)
        sys.exit(0)


def manga_chapter_list():
    global all_chapter, start_chapter, end_chapter, manga_chapter
    # *获取章节列表
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    manga_chapter = requests.get(
        'https://api.copymanga.com/api/v3/comic/%s/group/default/chapters?limit=500&offset=0&platform=3' % get_list_name, headers=headers)
    # !简要判断是否服务器无法连接
    if manga_chapter.status_code == 200:
        # *将api解析成json
        manga_chapter_list = manga_chapter.json()
        print("我们获取了\033[1;33m %s\033[37m 话的内容，请问是如何下载呢？" %
              manga_chapter_list["results"]["total"])
        # *判断用户需要怎么下载
        how_downlaod = input("1->全本下载\n2->范围下载\n3->单话下载\n您的选择是：")
        all_chapter = 0   # !防止误触发
        if int(how_downlaod) == 1:
            all_chapter = 1
        elif int(how_downlaod) == 2:
            start_chapter = input("从第几话？")
            end_chapter = input("到第几话？")
        elif int(how_downlaod) == 3:
            start_chapter = end_chapter = input("下载第几话？")
    else:
        # *报告远程服务器无法连接的状态码
        print("服务器似乎\033[1;31m 无法连接\033[37m 了qwq\n")
        print("返回的状态码是：%d" % manga_chapter.status_code)
        sys.exit(0)

# TODO 下面一个def中，因为一下int not str,一下srt not int 所以就一修运行一次，然后修的有点乱，可能以后会重新写一下吧qwq


def manga_download():
    # *解析全局传输的json
    manga_chapter_list = manga_chapter.json()
    # *判断是否为全本下载
    if all_chapter == 1:
        # *开始循环
        for i in manga_chapter_list["results"]["list"]:
            # *获取每章的图片url以及顺序
            headers = {}
            headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
            response = requests.get(
                'https://api.copymanga.com/api/v3/comic/%s/chapter2/%s?platform=3' % (get_list_name, i["uuid"]), headers=headers)
            response = response.json()
            j = 0
            # *通过获取的数量来循环
            while i["size"] > j:
                img_url = response["results"]["chapter"]["contents"][j]["url"]
                img_path = response["results"]["chapter"]["words"][j]
                r = requests.get(img_url)
                print("正在写入%s/%s/%s/%s.jpg\r" % (download_path, get_list_manga,
                      response["results"]["chapter"]["name"], img_path), end="")
                # *检测是否有此目录，没有就创建
                if not os.path.exists("%s/%s/" % (download_path, get_list_manga)):
                    os.mkdir("%s/%s/" % (download_path, get_list_manga))
                if not os.path.exists("%s/%s/%s/" % (download_path, get_list_manga, response["results"]["chapter"]["name"])):
                    os.mkdir("%s/%s/%s/" % (download_path, get_list_manga,
                             response["results"]["chapter"]["name"]))
                # !请保证目录没有此文件，不然可能会重写

                with open("%s/%s/%s/%s.jpg" % (download_path, get_list_manga, response["results"]["chapter"]["name"], img_path), "wb") as code:
                    code.write(r.content)
                j = j + 1
        # *试图跳出循环
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
            headers = {}
            headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
            response = requests.get(
                'https://api.copymanga.com/api/v3/comic/%s/chapter2/%s?platform=3' % (get_list_name, manga_chapter_list["results"]["list"][startchapter_id]["uuid"]), headers=headers)
            response = response.json()
            j = 0
            # *通过获取的数量来循环
            while manga_chapter_list["results"]["list"][startchapter_id]["size"] > j:
                img_url = response["results"]["chapter"]["contents"][j]["url"]
                img_path = response["results"]["chapter"]["words"][j]
                r = requests.get(img_url)
                print("正在写入%s/%s/%s/%s.jpg\r" % (download_path, get_list_manga,
                      response["results"]["chapter"]["name"], img_path), end="")
                # *检测是否有此目录，没有就创建
                if not os.path.exists("%s/%s/" % (download_path, get_list_manga)):
                    os.mkdir("%s/%s/" % (download_path, get_list_manga))
                if not os.path.exists("%s/%s/%s/" % (download_path, get_list_manga, response["results"]["chapter"]["name"])):
                    os.mkdir("%s/%s/%s/" % (download_path, get_list_manga,
                             response["results"]["chapter"]["name"]))
                # !请保证目录没有此文件，不然可能会重写
                with open("%s/%s/%s/%s.jpg" % (download_path, get_list_manga, response["results"]["chapter"]["name"], img_path), "wb") as code:
                    code.write(r.content)
                j = j + 1
            startchapter = int(startchapter) + 1
        # *试图跳出循环
        print(
            "这个漫画已经全部下载完了qwq                                                     ")
        # *返回到初始界面
        welcome()


def manga_collection(offset):
    global get_list_name, get_list_manga
    manga_search_list = ""
    print("正在查询中...\r", end="")
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    headers['authorization'] = authorization
    response = requests.get(
        'https://copymanga.com/api/v3/member/collect/comics?limit=50&offset={%s}&free_type=1&ordering=-datetime_modifier' % offset, headers=headers)
    print("搜索完毕啦！  \n")
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
        get_list_num = input("您需要下载的漫画是序号几？：")
        #if get_list_num == "pn":
        #    offsetnum = offset + 12
        #    print(offsetnum)
        #    manga_collection(offsetnum)
        #elif get_list_num == "pu":
        #    if offset == "0":
        #        print("没有上一页了qwq")
        #        manga_collection()
        #    else:
        #        offsetnum = offset - 12
        #        manga_collection(offsetnum)
        offsetnum = offset - 12
        manga_collection(offsetnum)
        get_list_name = manga_search_list["results"]["list"][int(
            get_list_num)]["comic"]["path_word"]
        get_list_manga = manga_search_list["results"]["list"][int(
            get_list_num)]["comic"]["name"]
    else:
        # *报告远程服务器无法连接的状态码
        print("服务器似乎\033[1;31m 无法连接\033[37m 了qwq\n")
        print("返回的状态码是：%d" % response.status_code)
        sys.exit(0)


def welcome():
    issearch = input("您是想搜索还是查看您的收藏？(1:搜索，2:收藏  默认1):")
    if issearch == "2":
        manga_collection(0)
    else:
        manga_name = input("请输入漫画名称:")
        manga_search(manga_name)


if __name__ == "__main__":
    get_settings()
    welcome()
    manga_chapter_list()
    manga_download()


# !防止用户CTRL+C导致程序报错
try:
    while 1:
        pass
except KeyboardInterrupt:
    pass
