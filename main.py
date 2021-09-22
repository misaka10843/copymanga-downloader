# -*- coding: UTF-8 -*-

import os
import json
import requests


def get_settings():
    global download_path
    first_initialization = 0
    if not os.path.isfile("./settings.json"):
        first_initialization = 1
    elif os.path.getsize("./settings.json") == 0:
        first_initialization = 1
    if first_initialization == 1:
        download_path = input(
            "您似乎是第一次启动此程序，请您先输入您需要下载的路径(请输入E:\manga这种格式,不要最后一个斜杠哦qwq)：")
        download_path = download_path.replace('\\', '/')
        with open('./settings.json', 'wb', encoding='utf8')as fp:
            fp.write('{"download_path" : "%s"}' % download_path)
    with open('./settings.json', 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
        download_path = json_data["download_path"]


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
        print("服务器似乎无法连接了qwq\n")
        print("返回的状态码是：%d" % response.status_code)


def manga_chapter_list():
    global alldownload, startdownload, enddownload, manga_chapter
    # *获取章节列表
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    manga_chapter = requests.get(
        'https://api.copymanga.com/api/v3/comic/%s/group/default/chapters?limit=500&offset=0&platform=3' % get_list_name, headers=headers)
    # !简要判断是否服务器无法连接
    if manga_chapter.status_code == 200:
        # *将api解析成json
        manga_chapter_list = manga_chapter.json()
        print("我们获取了%s话的内容，请问是如何下载呢？" % manga_chapter_list["results"]["total"])
        # *判断用户需要怎么下载
        how_downlaod = input("1->全本下载\n2->范围下载\n3->单话下载\n您的选择是：")
        alldownload = 0   # !防止误触发
        if int(how_downlaod) == 1:
            alldownload = 1
        elif int(how_downlaod) == 2:
            startdownload = input("从第几话？")
            enddownload = input("到第几话？")
        elif int(how_downlaod) == 3:
            startdownload = enddownload = input("下载第几话？")


def manga_download():
    # *判断是否为全本下载
    if alldownload == 1:
        # *解析全局传输的json
        manga_chapter_list = manga_chapter.json()
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
                print("正在写入%s/%s/%s/%s.jpg" % (download_path, get_list_manga,
                      response["results"]["chapter"]["name"], img_path))
                with open("%s/%s/%s/%s.jpg" % (download_path, get_list_manga, response["results"]["chapter"]["name"], img_path), "wb") as code:
                    code.write(r.content)
                j = j + 1
    elif alldownload == 0:
        while int(enddownload) >= int(startdownload):
            headers = {}
            headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
            response = requests.get(
                'https://api.copymanga.com/api/v3/comic/%s/chapter2/%s?platform=3' % (get_list_name, startdownload), headers=headers)
            response = response.json()
            img_url = response["results"]["chapter"]["contents"][startdownload]["url"]
            img_path = response["results"]["chapter"]["words"][startdownload]
            r = requests.get(img_url)
            print("正在写入,s/,s/,s/,s.jpg" % (download_path, get_list_manga,
                  response["results"]["chapter"]["name"], img_path))
            with open("%s/%s/%s/%s.jpg" % (download_path, get_list_manga, response["results"]["chapter"]["name"], img_path), "wb") as code:
                code.write(r.content)
            startdownload = startdownload + 1


if __name__ == "__main__":
    get_settings()
    manga_name = input("请输入漫画名称:")
    manga_search(manga_name)
    manga_chapter_list()
    manga_download()


# !防止用户CTRL+C导致程序报错
try:
    while 1:
        pass
except KeyboardInterrupt:
    pass
