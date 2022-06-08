# copymanga-downloader

![Head diagram](https://s2.loli.net/2022/03/30/b4eM9gArp5q2VKu.png)

## README Language

[简体中文](https://github.com/misaka10843/copymanga-downloader)|**English**

## Remarks

This is an English README that is not officially supported, because this file is translated using a translator and is not proofread, please refer to the Chinese README!

Translated with www.DeepL.com/Translator (free version)

**Attention! Since copymanga is a Simplified/Traditional Chinese manga site, please understand that no other languages are expected to be added to this program.**

## Attention‼️

**If your issue has not been accepted by me after a few days, Please also send an email to misaka10843@outlook.jp to inform me, thank you very much!**

To prevent emails from being categorized as spam, you can also add the following contact information (you need to specify your intention)

discord `misaka10843#2282` (morning, noon and 5-6pm)

QQ `3594254539` (not always online during working hours)

## Technology Stack ⚒️

![python](https://img.shields.io/badge/Python-3.0+-326c9c?style=for-the-badge&logo=Python&logoColor=326c9c)

## Thanks 🎁

* [KILLER2017](https://github.com/KILLER2017)(Optimize download reading experience)
* [Z-fly](https://github.com/Z-fly)(Contribute and ask some questions)
* [zhongfly](https://github.com/zhongfly)(Contribute with some problem solving and optimization code)
* [zaazwm](https://github.com/zaazwm)(add other content for download)

## Introduction 🗒️

This program uses `python` to download comics from copymanga

And it supports full download as well as range download (e.g. `10-20` words, or `11` words)

And while I was writing it, I noticed that the order of the pictures in each chapter of copymanga seems to be messed up.

But there is also a `word` array corresponding to the order of each picture, so just a small change, after downloading 99% is the correct order of qwq

(If not then download it again and send **issuse** it if you still have it qwq)

If you are an Android user, then you can use the [tachiyomi](https://github.com/tachiyomiorg/tachiyomi) client to try to download (but you need to install the `copymanga` plugin)

If you need to stitch images **right to left** and in groups of two, you can try using `Image_ stitching.exe` in [this version]() to achieve this (only simple functions are provided, no optimization is made)

## Updates 🔬

### Major updates 📈

2022/6/8: Implemented support 'other' group with the help of [@zaazwm](https://github.com/zaazwm) ，Fix collection export problem and export csv

2022/5/15: Added the ability to export favorites (up to 500)

2022/3/29: Supported some features with the help of [@zhongfly](https://github.com/zhongfly), and ~~may~~ fix the problem, and also helped optimize the code by the way www

2022/3/24: temporarily support setting a function (but the probability of not being able to download, please note that if there is a problem, please add it to the [here](https://github.com/misaka10843/copymanga-downloader/issues/) to submit relevant information

2022/2/25: Fix url problem with copymanga (copymanga.com seems to have been abandoned and replaced with copymanga.net)

2022/2/13: Github automatically compiles Windows EXE files! [actions](https://github.com/misaka10843/copymanga-downloader/actions/)

2022/1/14: Github automatically compiles Linux (should) binaries! [actions](https://github.com/misaka10843/copymanga-downloader/actions/)

2021/11/18: add get user favorite comics and support download

## Put a few screenshots qwq (timeliness not guaranteed)

First initialization

![image.png](https://s2.loli.net/2022/03/31/qKhZVtbguEAwQcJ.png)

## How to use 🖥️

### Use now (Windows)

1. Click [here](https://github.com/misaka10843/copymanga-downloader/releases/latest) to download the latest version of the exe compiled from the author's computer, or download the compiled file from GitHub [actions](https:/ /github.com/misaka10843/copymanga-downloader/actions/) (stability is not guaranteed)
2. Put this program into an empty folder (no problem if you don't put it, that is, the data will be written to the current folder)
3. directly double-click the exe can be qwq

### immediately use (Linux, can not guarantee whether to run)

1. Click [actions](https://github.com/misaka10843/copymanga-downloader/actions) to select the latest compilation (100% synchronization update, but can not guarantee whether it can run)
2. Download the `copymanga-download-Linux` zip package in the `attachment`.

3.Unzip the `copymanga-download-Linux` package

4. Put this program into an empty folder (no problem if you don't put it, that is, the data will be written to the current folder)
5. Just run it qwq

### Compile / original code use (all systems are supported)

1. Click [here](https://github.com/misaka10843/copymanga-downloader/archive/refs/heads/master.zip) to directly download the latest source code package
2. unzip it and put it into an empty folder (no problem if you don't, that is, the data will be written to the current folder)
3. first run this to install the dependency `pip install requirements.txt` (in fact, there is only a `requests,tqdm and pysocks` need to install, the other are python comes with (￣▽￣))
4. Then run `python main.py` to

### how to get authorization(this is to get user collection comics) 📒

1. Visit [https://copymanga.net/web/person/shujia](https://copymanga.net/web/person/shujia)
2. Press F12 and refresh the page
3. Find a file like `comics?limit=12&offset=0&free_type=1&ordering=-datetime_modifier` and click
4. In the **request header** find `authorization: Token {each different}`, copy `Token {each different}`, e.g. `Token 1293asd123s8adhh2juhsada2`

Image ([larger view](https://i.loli.net/2021/11/18/Tv85D4a7GO9jNbn.png)).

![graphic](https://i.loli.net/2021/11/18/Tv85D4a7GO9jNbn.png)

## Note ‼️

### About api

All the APIs used by this program to obtain information are official APIs
The specific use is as follows

```text
Comic search: 
https://api.copymanga.org/api/v3/search/comic?format=json&limit=18&offset=0&platform=3&q={keyword}

Manga chapter fetching: 
https://api.copymanga.org/api/v3/comic/{comic_path_word}/group/default/chapters?limit=500&offset=0&platform=3

Comic chapter images are available at:
https://api.copymanga.org/api/v3/comic/{manga_path_word}/chapter2/{chapterUUUID}?platform=3

User favorite manga fetching (need to set headers['authorization']):
https://copymanga.org/api/v3/member/collect/comics?limit=50&offset=0&free_type=1&ordering=-datetime_modifier
```

### About the code

#### About sometimes the download gets stuck

This should be a limitation of copymanga's server

It's definitely not my problem!

If this happens, please `Ctrl+C` to terminate the program and use `range download` or `single talk download`.

(In fact, the code used for the single word download and the range download is the same, except that the two parameters of the range download are directly combined into one qwq)

Or maybe it's already done, but it hasn't ended the loop qwq

#### about code annotation

Because code annotation uses VScode's `Better Comments` plugin to make annotations with corresponding colors to allow developers to analyze code more clearly.

So it is recommended that you also install this plugin to get a better understanding of the code

---

More information is still being written at ....
