# copymanga-download

copymanga网站的一个小爬虫，来使用python下载copymanga中的漫画

## 技术栈

![python](https://img.shields.io/badge/Python-3.0+-326c9c?style=for-the-badge&logo=Python&logoColor=326c9c)

## 简介

此程序使用`python`来下载copymanga中的漫画

并且支持全本下载以及范围下载(例如`10-20`话,或者是`11`话)

## 注意

此程序所使用的所有资料获取的API均为官方API
具体使用如下

```text
漫画搜索：
https://api.copymanga.com/api/v3/search/comic?format=json&limit=18&offset=0&platform=3&q={关键词}

漫画章节获取：
https://api.copymanga.com/api/v3/comic/{漫画path_word}/group/default/chapters?limit=500&offset=0&platform=3

漫画每章图片获取：
https://api.copymanga.com/api/v3/comic/{漫画path_word}/chapter2/{章节UUID}?platform=3
```

---

更多资料还在编写中....
