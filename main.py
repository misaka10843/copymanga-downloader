import json
import os

import requests


def manga_search(manga_name):
    global get_list_name
    # *获取搜索结果
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    response = requests.get(
        'https://api.copymanga.com/api/v3/search/comic?format=json&limit=20&offset=0&platform=3&q=%s' % manga_name, headers=headers)
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
        get_list_name = manga_search_list["results"]["list"][get_list_num]["path_word"]
    else:
        # *报告远程服务器无法连接的状态码
        print("服务器似乎无法连接了qwq\n")
        print("返回的状态码是：%d" % response.status_code)


def manga_chapter_list():
    # *获取章节列表
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    response = requests.get(
        'https://api.copymanga.com/api/v3/comic/%s/group/default/chapters?limit=500&offset=0&platform=3' % get_list_name, headers=headers)
    # !简要判断是否服务器无法连接
    if requests.status_code == 200:
        # *将api解析成json
        manga_chapter_list = response.json()
        print("我们获取了%s话的内容，请问是如何下载呢？" % manga_chapter_list["results"]["total"])


if __name__ == "__main__":
    manga_name = input("请输入漫画名称:")
    manga_search(manga_name)
    manga_chapter_list()
