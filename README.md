**请注意，在提交ISSUE前，请确保@misaka10843，以防止长时间未查看！**

**因为尽可能缓解copymanga服务器压力，此程序限制了每分钟只能访问15次API，还请理解！**

# copymanga-downloader

![Head diagram](https://s2.loli.net/2022/03/30/b4eM9gArp5q2VKu.png)

## 前言💭

推荐在模拟器/WSA/安卓手机中安装[tachiyomi](https://github.com/tachiyomiorg/tachiyomi)，与[Copymanga插件](https://github.com/stevenyomi/copymanga)，并使用tachiyomi下载！

因为这样可以尽可能的保证下载稳定与订阅系统正常

此程序只是方便下载，而不是进行订阅操作(下载与订阅系统不稳定)


**我们已经正式基本支持命令行参数下载并且完全重构啦！**

请看[命令行参数](https://github.com/misaka10843/copymanga-downloader#%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%8F%82%E6%95%B0%EF%B8%8F)与[重大更新](https://github.com/misaka10843/copymanga-downloader#%E9%87%8D%E5%A4%A7%E6%9B%B4%E6%96%B0-)的部分！

## 下载

[pypi(稳定)](https://pypi.org/project/copymanga-dl)

[releases(稳定)](https://github.com/misaka10843/copymanga-downloader/releases)

[actions(测试)](https://github.com/misaka10843/copymanga-downloader/actions/workflows/python-app.yml)

or

`git clone https://github.com/misaka10843/copymanga-downloader.git && cd copymanga-downloader && python setup.py install`

`git clone https://github.com/misaka10843/copymanga-downloader.git && cd copymanga-downloader && pip install -r requirements.txt && python main.py`

## README 语言🌐

**简体中文**|[English](https://github.com/misaka10843/copymanga-downloader/blob/master/README-EN.md)

## 声明 📢

我们制作此工具是纯粹因为PC端无法下载漫画，我们并不希望个人用户一直依靠此工具并且长时间/多文件下载来增加服务器负担

在使用此工具时理应是小范围/短时间下载，而不是大范围/长时间下载，如果因此出现了问题我们是不会受理的

**请尽量使用官方网站！**

## 注意！ ‼️

**如果您的issue已经过了几天还没有被我受理，还请您发送邮件到misaka10843@outlook.jp来通知我，十分感谢！**

为了防止邮箱归类邮件为垃圾邮件，您也可以添加下方联系方式（需要注明来意）

discord `misaka10843#2282`（早上，中午以及下午5-6点）

QQ `3594254539`（不常工作时间上线）

因为copymanga为简体/繁体中文的漫画网站，所以此程序预计不会添加其他语言，还请谅解

为了尽可能的防止对服务器增加过大负担，我们将API请求限制为15次每分钟，还请谅解！（因为将API请求的时间与次数保存在设置中，您就算重新打开程序都会被限制的！）

![image](https://user-images.githubusercontent.com/69132853/229278511-3b2fe97b-5e01-4df0-9a23-d276de440472.png)


## 技术栈 ⚒️

![python](https://img.shields.io/badge/Python-3.0+-326c9c?style=for-the-badge&logo=Python&logoColor=326c9c)

## Thanks 🎁

* [KILLER2017](https://github.com/KILLER2017)(优化下载阅读体验)
* [Z-fly](https://github.com/Z-fly)(贡献与提出一些问题)
* [zhongfly](https://github.com/zhongfly)(贡献与提供一些问题解决方法和优化代码)
* [zaazwm](https://github.com/zaazwm)(添加其他内容的下载)
* [blacklein](https://github.com/blacklein)(添加setup.py与发布到pypi)

## 简介 🗒️

此程序使用 `python`来下载copymanga中的漫画

并且支持全本下载以及范围下载(例如 `10-20`话,或者是 `11`话)

而且我在写的时候发现了copymanga每章的图片顺序似乎是打乱的，

但是也有个 `word`数组对应着每张图片的顺序，所以就小改一下，下载完之后99%是正确顺序的qwq

（如果不是那就重新下载一遍，如果还有的话就发**issuse**吧qwq）

如果您是安卓用户，那么您可以使用[tachiyomi](https://github.com/tachiyomiorg/tachiyomi)客户端尝试下载（但是需要安装 `copymanga`的插件）

如果您需要**从右到左**的拼接图片，并且两张为一组的话，您可以尝试使用[这个版本](https://github.com/misaka10843/copymanga-downloader/releases/tag/v2.2)中的 `Image_stitching.exe`来实现(只提供简单功能，并未做出优化)

如果发现无法获取/下载的时候，请多试几次，如果不行的话请删除下图中标明的字段，触发设置缺损备份旧设置并重新初始化(**请不要删除双引号！**)

![image.png](https://s2.loli.net/2022/07/05/iXJTlowxnO2GCfc.png)


## 命令行参数🖥️

您可以在命令行中输入 `{copymanga-downloader的文件名} -h`查看现在所支持的参数

```bash
usage: main.py [-h] [--MangaPath MANGAPATH] [--MangaGroup MANGAGROUP] [--Url URL] [--Output OUTPUT] [--subscribe SUBSCRIBE] [--UseWebp USEWEBP] [--UseOSCdn USEOSCDN] [--MangaStart MANGASTART] [--MangaEnd MANGAEND] [--Proxy PROXY]

options:
  -h, --help            show this help message and exit
  --MangaPath MANGAPATH
                        漫画的全拼，https://copymanga.site/comic/这部分
  --MangaGroup MANGAGROUP
                        漫画的分组Path_Word，默认为default
  --Url URL             copymanga的域名,如使用copymanga.site，那就输入site(默认为site)
  --Output OUTPUT       输出文件夹
  --subscribe SUBSCRIBE
                        是否切换到自动更新订阅模式(1/0，默认关闭(0))
  --UseWebp USEWEBP     是否使用Webp(1/0，默认开启(1))
  --UseOSCdn USEOSCDN   是否使用海外cdn(1/0，默认关闭(0))
  --MangaStart MANGASTART
                        漫画开始下载话(如果想全部下载请输入0)
  --MangaEnd MANGAEND   漫画结束下载话(如果只想下载一话请与MangaStart相同,如果想全部下载请输入0)
  --Proxy PROXY         设置代理

```

其中，`MangaPath/MangaStart/MangaEnd`三个参数是**必填项**

而且，`MangaPath`是 `https://{copymanga域名}/comic/{这一部分}`

比如我想下载*別哭啊魔王醬*

那么我应该像图中一样复制红框中选择的字母

[高清图片链接](https://s2.loli.net/2023/01/06/FWklObHX6523CYs.png)

![img](https://s2.loli.net/2023/01/06/FWklObHX6523CYs.png)


### 命令示例

#### 如果我想下载*別哭啊魔王醬*的第一话

我可以这样输入

`python main.py --Url site --MangaPath biekuamowangjiang --MangaStart 1 --MangaEnd 1 --Proxy http://127.0.0.1:10809 --UseOSCdn 1`

或者输入精简版

`python main.py --MangaPath biekuamowangjiang --MangaStart 1 --MangaEnd 1`

#### 如果我想下载*星靈感應*的全话

我可以这样输入

`python main.py --Url site --MangaPath xinglingganying --MangaStart 1 --MangaEnd 38 --Proxy http://127.0.0.1:10809 --UseOSCdn 1`

或者输入精简版

`python main.py --MangaPath xinglingganying --MangaStart 1 --MangaEnd 38`

**（注意！虽然说是下载全话，其实就是将范围定在了1话-最新话，所以如果下载其他漫画的全话请参考漫画更新到多少话了，然后再替换38）**

## 更新 🔬

### 重大更新 📈

2023/3/31(重大):完全重构程序，添加多线程+自动更新等众多功能

2023/1/6(重大):添加直接使用命令参数进行下载，并且使用命令参数进行下载时不会出现任何输入框，优化download，修复download中并未使用代理以及headers

2022/12/5: 添加命令行支持（下载setup.py后python setup.py install）感谢[@blacklein](https://github.com/blacklein)提供的文件！

2022/7/26: HotFix分组输入数字导致报错(str未转int)

2022/7/5: 修复漫画分组只显示“默认”与“其他”的问题，添加从GitHub中获取copymanga的url列表，添加设置缺损后报错并备份老设置文件后重新进入初始化

2022/6/8: 在[@zaazwm](https://github.com/zaazwm)帮助下实现了“其他”内容的下载，修复收藏导出问题与导出csv

2022/5/15: 新增收藏导出功能（最高支持500个）

2022/3/29: 在 [@zhongfly](https://github.com/zhongfly) 帮助下支持了一些功能，并~~可能~~修复了问题，而且还顺便帮忙优化了下代码www

2022/3/24: 暂时支持设置一个功能(但是大概率无法下载，请注意，如果出现问题请在[这里](https://github.com/misaka10843/copymanga-downloader/issues/)提交相关信息

2022/2/25: 修复copymanga的url问题（copymanga.com似乎已经被弃用，已更换到copymanga.net）

2022/2/13: Github自动编译Windows EXE文件！[actions](https://github.com/misaka10843/copymanga-downloader/actions/)

2022/1/14: Github自动编译Linux(应该)二进制文件！[actions](https://github.com/misaka10843/copymanga-downloader/actions/)

2021/11/18: 增加获取用户收藏的漫画并且支持下载

## 放几张截图qwq（时效性不敢保证）

第一次初始化

![图片.png](https://s2.loli.net/2022/03/31/qKhZVtbguEAwQcJ.png)

## 如何使用 🖥️

### 立即使用(Windows)

1.点击[这里](https://github.com/misaka10843/copymanga-downloader/releases/latest)下载最新的从作者电脑中编译的exe版本，或者下载GitHub中的编译文件[actions](https://github.com/misaka10843/copymanga-downloader/actions/)(稳定无法保证)

2.将此程序放入一个空文件夹（不放也没问题，就是数据会写到当前文件夹中）

3.直接双击exe即可qwq

### 立即使用(Linux,无法保证能否运行)

1.点击[actions](https://github.com/misaka10843/copymanga-downloader/actions)选择最新的编译(100%同步更新，但不能保障是否能运行)

2.下载 `附件`中的 `copymanga-download-Linux`压缩包

3.解压 `copymanga-download-Linux`压缩包

4.将此程序放入一个空文件夹（不放也没问题，就是数据会写到当前文件夹中）

5.运行即可qwq

### 编译/原代码使用(所有系统均支持)

⭐️ 建议pip安装（如果有本地有多个Python版本，建议用pipx安装）
```bash
# macOS安装pipx
brew install pipx
pipx ensurepath

# Linux安装pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Windows安装pipx
python -m pip install --user pipx

# 从远程仓库安装copymanga-dl
pip install git+https://github.com/misaka10843/copymanga-downloader.git
或
pipx install git+https://github.com/misaka10843/copymanga-downloader.git

# 通过镜像站从远程仓库安装copymanga-dl
pip install git+https://ghproxy.com/https://github.com/misaka10843/copymanga-downloader.git
或
pipx install git+https://ghproxy.com/https://github.com/misaka10843/copymanga-downloader.git
```

1.点击[这里](https://github.com/misaka10843/copymanga-downloader/archive/refs/heads/master.zip)直接下载最新的源码包

2.解压后放入一个空文件夹（不放也没问题，就是数据会写到当前文件夹中）

3.先运行这个来安装依赖 `pip install requirements.txt`(其实也就只有个 `requests`需要安装，其他都是python自带的(￣▽￣))

4.然后运行 `python main.py`即可

### 命令行使用(beta)

1.下载仓库中的 `setup.py`

2.切换到下载目录中运行 `python setup.py install`

3.输入 `copymanga-dl`即可

### 如何获取authorization(此为获取用户收藏漫画) 📒

1.访问[https://copymanga.org/web/person/shujia](https://copymanga.org/web/person/shujia)

2.按下F12后刷新页面

3.找到类似 `comics?limit=12&offset=0&free_type=1&ordering=-datetime_modifier`的文件(?)后点击

4.在**请求标头**中找到 `authorization: Token {各有各的不同}`，复制 `Token {各有各的不同}`即可，如 `Token 1293asd123s8adhh2juhsada2`

图片（[大图查看](https://i.loli.net/2021/11/18/Tv85D4a7GO9jNbn.png)）：

![图文](https://i.loli.net/2021/11/18/Tv85D4a7GO9jNbn.png)

## 注意 ‼️

### 关于api

此程序所使用的所有资料获取的API均为官方API
具体使用如下

```text
漫画搜索：
https://api.copymanga.org/api/v3/search/comic?format=json&limit=18&offset=0&platform=3&q={关键词}

漫画章节获取：
https://api.copymanga.org/api/v3/comic/{漫画path_word}/group/default/chapters?limit=500&offset=0&platform=3

漫画每章图片获取：
https://api.copymanga.org/api/v3/comic/{漫画path_word}/chapter2/{章节UUID}?platform=3

用户收藏漫画获取（需要设置headers['authorization']）:
https://copymanga.org/api/v3/member/collect/comics?limit=50&offset=0&free_type=1&ordering=-datetime_modifier
```

### 关于代码

#### 关于有时候下载会卡住

这应该是copymanga的服务器限制

绝对不是我的问题＞︿＜

如果遇见这种情况的话请 `Ctrl+C`终止程序后使用 `范围下载`或者 `单话下载`

(其实单话下载与范围下载使用的代码是一样的，只不过就是直接将范围下载的两个参数合并成一个而已qwq)

或者可能是已经下完了，但是还没结束循环qwq

#### 关于代码注解

因为代码注解时使用了VScode的 `Better Comments`插件来使注解有对应颜色来让开发者更加明了地分析代码，

所以建议您也安装此插件来获取更好的代码理解

---

更多资料还在编写中....
