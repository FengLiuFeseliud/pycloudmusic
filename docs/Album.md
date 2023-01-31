# `class` Album

**专辑 (Album) 是一个数据列表类 (DataListObject)， 支持直接迭代对象将返回按专辑曲目生成的 [Music 对象](/pycloudmusic/Music)，支持使用 `.` 读取数据，并且专辑相关的 Api， Album 也支持[评论 (CommentObject)](/pycloudmusic/CommentObject)**

```python
"""迭代 Album"""
from pycloudmusic import Music163Api
import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌单 62338
    album = await musicapi.album(62338)
    # 迭代 album 打印专辑曲目
    for music in album:
        print(music.name, music.artist_str, music.id)

asyncio.run(main())
```

## 类实例变量

在外部使用 `.` 即可读取数据

```python
class Album(_Album):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        album_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, album_data)
        # 专辑id
        self.id = album_data["album"]["id"]
        # 专辑标题
        self.name = album_data["album"]["name"]
        # 专辑类型
        self.sub_type = album_data["album"]["subType"]
        # 专辑别名
        self.alias = album_data["album"]["alias"]
        self.alias_str = "/".join(self.alias)
        # 专辑主作者
        self.artist = album_data["album"]["artist"]
        # 专辑所有作者
        self.artists = album_data["album"]["artists"]
        self.artists_str = "/".join([artists_data["name"] for artists_data in self.artists])
        # 专辑曲目数
        self.size = album_data["album"]["size"]
        # 专辑简介
        self.description = album_data["album"]["description"]
        # 未知
        self.liked = album_data["album"]["info"]["liked"]
        # 专辑评论数
        self.comment_count = album_data["album"]["info"]["commentCount"]
        # 专辑分享数
        self.share_count = album_data["album"]["info"]["shareCount"]
        # 未知
        self.liked_count = album_data["album"]["info"]["likedCount"]
        # 专辑封面
        self.cover = album_data["album"]['picUrl']
        # 专辑曲目 (json)
        self.music_list = album_data["songs"]
```

## 类实例方法

### Album.subscribe

**`async def subscribe(self, in_: bool = True) -> dict[str, Any]:`**

对像 收藏/取消收藏

> `in_`: 收藏 / 取消收藏