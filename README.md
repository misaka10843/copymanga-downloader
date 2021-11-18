# copymanga-download

copymanga网站的一个小爬虫，来使用python下载copymanga中的漫画

## 技术栈

![python](https://img.shields.io/badge/Python-3.0+-326c9c?style=for-the-badge&logo=Python&logoColor=326c9c)

## 简介

此程序使用`python`来下载copymanga中的漫画

并且支持全本下载以及范围下载(例如`10-20`话,或者是`11`话)

而且我在写的时候发现了copymanga每章的图片顺序似乎是打乱的，

但是也有个`word`数组对应着每张图片的顺序，所以就小改一下，下载完之后99%是正确顺序的qwq

（如果不是那就重新下载一遍，如果还有的话就发**issuse**吧qwq）

## 更新

### 重大更新：
2021/11/18：增加获取用户收藏的漫画并且支持下载


## 放几张截图qwq（时效性不敢保证）

这张是第一次初始化之后的qwq

![img1](./doc/img1.png)

这张是第一次初始化的qwq

![img2](./doc/img2.png)

## 如何使用

### 立即使用(仅限Windows)

1.点击[这里](https://github.com/misaka10843/copymanga-download/releases)下载最新的编译exe版本(无法保证与源代码运行方式的同步更新)

2.将此程序放入一个空文件夹（不放也没问题，就是数据会写到当前文件夹中）

3.直接双击exe即可qwq

### 编译/原代码使用(所有系统均支持)

1.点击[这里](https://github.com/misaka10843/copymanga-download/archive/refs/heads/master.zip)直接下载最新的源码包

2.解压后放入一个空文件夹（不放也没问题，就是数据会写到当前文件夹中）

3.先运行这个来安装依赖`pip install requirements.txt`(其实也就只有个`requests`需要安装，其他都是python自带的(￣▽￣))

4.然后运行`python main.py`即可

### 如何获取authorization(此为获取用户收藏漫画)
1.访问https://copymanga.com/web/person/shujia

2.按下F12后刷新页面

3.找到类似`comics?limit=12&offset=0&free_type=1&ordering=-datetime_modifier`的文件(?)后点击

4.在**请求标头**中找到`authorization: Token {各有各的不同}`，复制`Token {各有各的不同}`即可，如`Token 1293asd123s8adhh2juhsada2`

图片（[大图查看](https://i.loli.net/2021/11/18/Tv85D4a7GO9jNbn.png)）：

![图文](https://i.loli.net/2021/11/18/Tv85D4a7GO9jNbn.png)

## 注意

### 关于api

此程序所使用的所有资料获取的API均为官方API
具体使用如下

```text
漫画搜索：
https://api.copymanga.com/api/v3/search/comic?format=json&limit=18&offset=0&platform=3&q={关键词}

漫画章节获取：
https://api.copymanga.com/api/v3/comic/{漫画path_word}/group/default/chapters?limit=500&offset=0&platform=3

漫画每章图片获取：
https://api.copymanga.com/api/v3/comic/{漫画path_word}/chapter2/{章节UUID}?platform=3

用户收藏漫画获取（需要设置headers['authorization']）:
https://copymanga.com/api/v3/member/collect/comics?limit=50&offset=0&free_type=1&ordering=-datetime_modifier
```

### 关于代码

#### 关于manga_download的def

因为一下int not str,

一下srt not int 所以就一修运行一次，

然后修的有点乱，

可能以后会重新写一下吧qwq

#### 关于有时候下载会卡住

这应该是copymanga的服务器限制

绝对不是我的问题＞︿＜

如果遇见这种情况的话请`Ctrl+C`终止程序后使用`范围下载`或者`单话下载`

(其实单话下载与范围下载使用的代码是一样的，只不过就是直接将范围下载的两个参数合并成一个而已qwq)

或者可能是已经下完了，但是还没结束循环qwq

#### 关于代码注解

因为代码注解时使用了VScode的`Better Comments`插件来使注解有对应颜色来让开发者更加明了地分析代码，

所以建议您也安装此插件来获取更好的代码理解

---

更多资料还在编写中....
