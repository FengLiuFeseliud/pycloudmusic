# pycloudmusic

![issues](https://img.shields.io/github/issues/FengLiuFeseliud/pycloudmusic)
![forks](https://img.shields.io/github/forks/FengLiuFeseliud/pycloudmusic)
![stars](https://img.shields.io/github/stars/FengLiuFeseliud/pycloudmusic)
![license](https://img.shields.io/github/license/FengLiuFeseliud/pycloudmusic)

**优雅的异步高性能 Python 音乐 API 库**

开箱即用/简单/快速 Python >= 3.9

[基于 NeteaseCloudMusicApi 改写](https://github.com/Binaryify/NeteaseCloudMusicApi)

[项目文档 (文档不更新时请清理浏览器缓存): https://docs.sakuratools.top/pycloudmusic/](https://docs.sakuratools.top/pycloudmusic/) | [打不开时候备用: https://github.com/FengLiuFeseliud/pycloudmusic.docs](https://github.com/FengLiuFeseliud/pycloudmusic.docs)

# 快速入门

## 安装

使用 pip 即可安装 pycloudmusic

```bash
pip install pycloudmusic
```

## 输出对象

pycloudmusic 下的所有对象被打印时都会格式化输出类所有变量， 方便查看对象数据

```python
from pycloudmusic import Music163Api
import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌曲 421531
    # https://music.163.com/#/song?id=421531
    music = await musicapi.music(421531)
    # 打印歌曲信息
    print(music)
    print("=" * 50)

asyncio.run(main())
```

此处数据为打印歌单对象

![printobj.png](https://img.sakuratools.top/docs/pycloudmusic/printobj.png@0x0x0.8x80)

## 可迭代对象

pycloudmusic 下的部分对象可以被迭代使用

如下获取歌单 PlayList 对象后可以直接 for in PlayList 对象， 将迭代返回按歌单曲目生成的 Music 对象

```python
from pycloudmusic import Music163Api
import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌单 7487291782
    # https://music.163.com/#/playlist?id=7487291782
    playlist = await musicapi.playlist(7487291782)
    # 打印歌单信息
    print(playlist)
    print("=" * 50)

    # 打印歌单曲目
    for music in playlist:
        print(music.name, music.artist_str, music.id)

asyncio.run(main())
```

因此可以使用推导式快速生成 task 列表下载歌单曲目

```python
from pycloudmusic import Music163Api
import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌单 7487291782
    # https://music.163.com/#/playlist?id=7487291782
    playlist = await musicapi.playlist(7487291782)
    # 创建任务
    tasks = [asyncio.create_task(music.play()) for music in playlist]
    # 等待任务
    await asyncio.wait(tasks)

asyncio.run(main())
```

## 模拟登录

pycloudmusic 支持邮箱登录， 二维码登录， 手机密码登录， 手机验证码登录

这里可以用邮箱登录长期保持 Cookie 有效性，邮箱登录不需要人为操作

```python
from pycloudmusic import LoginMusic163
import asyncio


async def main():
    login = LoginMusic163()
    # 邮箱登录
    code, cookie, musicapi = await login.email("you login email", "you login password")
    # 验证登录
    print("=" * 60)
    print(code, cookie, musicapi)
    print("=" * 60)
    print(await musicapi.my())

asyncio.run(main())
```

## 评论

pycloudmusic 支持网易云的所有评论， 对支持评论的对象使用 Music163Comment 的方法即可

```python
"""获取歌曲评论"""

from pycloudmusic import Music163Api, Page
import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌曲
    # https://music.163.com/song?id=1902224491&userid=492346933
    music = await musicapi.music(1902224491)
    # 按时间获取评论
    async for comments in Page(music.comments, hot=False):
        for comment in comments:
            print(f"{comment.user_str}:  {comment.content}")

asyncio.run(main())
```