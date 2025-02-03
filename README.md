> [!WARNING]
> **为了您能够更好的更新以及使用程序，建议直接运行`pip install copymanga-downloader`安装pip包后直接运行`copymanga-dl`来启动程序**
> 
> 我们十分十分建议直接通过pip进行安装，因为在Windows中可能会被WD等杀毒软件误杀

> [!NOTE]
> **请注意，在提交ISSUE前，请确保@misaka10843，以防止长时间未查看！**
>
> **因为尽可能缓解copymanga服务器压力，此程序限制了每分钟只能访问15次API，还请理解！**
>
> **我并不希望此工具影响copymanga的正常运行，要是把copymanga的服务器下崩了或者怎么样那你还能在哪里看到收录这么全的网站？？？如果可以还请多多访问官网点点广告支持一下他们，对于使用绝大部份的第三方小网站的下载器都是同理，服务器流量真的很贵，如果为了用户体验可能还会套上cdn会更贵，如果爬虫泛滥可能还会用Cloudflare等手段阻止爬虫。**

# copymanga-downloader

![Head diagram](https://s2.loli.net/2022/03/30/b4eM9gArp5q2VKu.png)

<p align="center">
  <a href="https://pypi.org/project/copymanga-downloader/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/copymanga-downloader?style=for-the-badge&logo=PyPI"></a>
  <a href="https://github.com/misaka10843/copymanga-downloader/graphs/contributors" target="_blank"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/misaka10843/copymanga-downloader?style=for-the-badge&logo=github"></a>
  <a href="https://github.com/misaka10843/copymanga-downloader/stargazers" target="_blank"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/misaka10843/copymanga-downloader?style=for-the-badge&label=%E2%AD%90STAR"></a>
</p>



## 前言💭

推荐在模拟器/WSA/安卓手机中安装[tachiyomi](https://github.com/tachiyomiorg/tachiyomi)
与[Copymanga插件](https://github.com/stevenyomi/copymanga)并使用tachiyomi下载！

因为这样可以尽可能的保证下载稳定与订阅系统正常

此程序只是方便下载，而不是进行订阅操作(下载与订阅系统不稳定)

**我们已经正式基本支持命令行参数下载并且完全重构啦！**

请看[命令行参数](https://github.com/misaka10843/copymanga-downloader#%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%8F%82%E6%95%B0%EF%B8%8F)
与[重大更新](https://github.com/misaka10843/copymanga-downloader#%E9%87%8D%E5%A4%A7%E6%9B%B4%E6%96%B0-)的部分！

## Q&A🗯️
> Q1: 为什么没有支持评论下载？
> 
> A1: 因为本来就没有必要，在我前期设计的时候就没有考虑进去

> Q2: 为什么我提了issue这么长时间没有看/没有修复？
> 
> A2: 因为本人现在并不经常使用，因为之前是因为没有一个比较好的**批量**下载的工具才制作的，现在基本上已经不需要批量下载了
> （毕竟下载下来没有好看的阅读器有什么用？而我使用的阅读器就有插件可以下载和在线浏览，所以就并没有用了）

> Q3: 为什么没有GUI
> 
> A3: 如Q1一样，而且本仓库还是在我自学py的时候编写的，现在的代码有点过于💩山，并且如Q2一样已经不怎么用此工具了，而且GUI做出来有什么用呢？（要做GUI那还不如在基础之上设计一个阅读器还差不多）

> Q4: 为什么我一下载就API限制？
> 
> A4: **我并不希望此工具影响copymanga的正常运行，要是把copymanga的服务器下崩了或者怎么样那你还能在哪里看到收录这么全的网站？？？如果可以还请多多访问官网点点广告支持一下他们**

> Q5: 我看见xy/tb/pdd在卖此仓库/使用此仓库提供功能
> 
> A5：如果情况属实的话我会立即归档/删除仓库，我和其他贡献者写出来的东西不是为这些zazong提供赚钱的，反正这些电商平台举报了也没啥用还不如直接不维护算了

> Q6: 我想支持其他漫画平台可以吗？
>
> A6: 此仓库仅支持copymanga，也不会考虑支持其他任何网站

> Q7: 我希望提供我的代码，我该怎么办？
>
> A7: 在提供之前请先查看是否与现有功能冲突，添加之后是否会出现问题，代码是否清晰，如果没有问题我会在看见之后测试成功就合并

> Q8: 为什么更新了这么多却不在releases升级版本号？
>
> A8: 因为懒（不是），感觉没有更新什么实质性内容所以就没有更新，如果需要的话请在[Actions](https://github.com/misaka10843/copymanga-downloader/actions)中下载

## 声明 📢

我们制作此工具是纯粹因为PC端无法下载漫画，我们并不希望个人用户一直依靠此工具并且长时间/多文件下载来增加服务器负担

在使用此工具时理应是小范围/短时间下载，而不是大范围/长时间下载，如果因此出现了问题我们是不会受理的

**请尽量使用官方网站！**

## 如何配置kindle推送📚

详细请看[copymanga-downloader自动推送到kindle的使用教程](https://www.voidval.com/archives/1705162565893)

请注意，在实现转换为epub时使用了第三方库[KCC](https://github.com/ciromattia/kcc/)
，您需要自行在[kcc/releases](https://github.com/ciromattia/kcc/releases)下载对应平台的执行程序

(windows平台需要下载`kcc_c2e_{版本号}.exe`)

然后根据上方的使用教程进行配置

## 命令行参数🖥️

```bash
> copymanga-dl -h
usage: copymanga-dl [-h] [--MangaPath MANGAPATH] [--MangaGroup MANGAGROUP] [--Url URL] [--Output OUTPUT]
                    [--subscribe SUBSCRIBE] [--UseWebp USEWEBP] [--UseOSCdn USEOSCDN] [--MangaStart MANGASTART]
                    [--MangaEnd MANGAEND] [--Proxy PROXY]

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

**（注意！虽然说是下载全话，其实就是将范围定在了1话-最新话，所以如果下载其他漫画的全话请参考漫画更新到多少话了，然后再替换38）
**

## 放几张截图qwq（时效性不敢保证）

更改设置

![image](https://github.com/misaka10843/copymanga-downloader/assets/69132853/c3c97f7c-7202-4f17-acf3-6b06edd556b8)

下载进度条

![image](https://github.com/misaka10843/copymanga-downloader/assets/69132853/f618f9cc-58d6-4bc8-a86d-1a67ff37b2ec)

漫画搜索

![image](https://github.com/misaka10843/copymanga-downloader/assets/69132853/583b0d12-9017-4115-b210-2a13d7fc7027)

## 如何使用 🖥️

### 立即使用(Windows)

1.点击[这里](https://github.com/misaka10843/copymanga-downloader/releases/latest)
下载最新的从作者电脑中编译的exe版本，或者下载GitHub中的编译文件[actions](https://github.com/misaka10843/copymanga-downloader/actions/)(
稳定无法保证)

2.将此程序放入一个空文件夹（不放也没问题，就是数据会写到当前文件夹中）

3.直接双击exe即可qwq

### 立即使用(Linux,无法保证能否运行)

1.点击[actions](https://github.com/misaka10843/copymanga-downloader/actions)选择最新的编译(
100%同步更新，但不能保障是否能运行)

2.下载 `附件`中的 `copymanga-download-Linux`压缩包

3.解压 `copymanga-download-Linux`压缩包

4.将此程序放入一个空文件夹（不放也没问题，就是数据会写到当前文件夹中）

5.运行即可qwq

### 如何获取authorization(此为获取用户收藏漫画) 📒

1.访问[https://copymanga.org/web/person/shujia](https://copymanga.org/web/person/shujia)

2.按下F12后刷新页面

3.找到类似 `comics?limit=12&offset=0&free_type=1&ordering=-datetime_modifier`的文件(?)后点击

4.在**请求标头**中找到 `authorization: Token {各有各的不同}`，复制 `Token {各有各的不同}`
即可，如 `Token 1293asd123s8adhh2juhsada2`

图片（[大图查看](https://i.loli.net/2021/11/18/Tv85D4a7GO9jNbn.png)）：

![图文](https://i.loli.net/2021/11/18/Tv85D4a7GO9jNbn.png)

---

更多资料还在编写中....
