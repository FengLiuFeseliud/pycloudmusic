# `class` PlayList

**歌单 (PlayList) 是一个数据列表类 (DataListObject)， 支持直接迭代对象将返回按歌单歌曲生成的 [Music 对象](/pycloudmusic/Music)，支持使用 `.` 读取数据，并且支持歌单相关的 Api， PlayList 也支持[评论 (CommentObject)](/pycloudmusic/CommentObject)**

```python
"""迭代 PlayList"""
from pycloudmusic import Music163Api
import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌单 7487291782
    playlist = await musicapi.playlist(7487291782)
    # 迭代 PlayList 打印歌单曲目
    for music in playlist:
        print(music.name, music.artist_str, music.id)

asyncio.run(main())
```

## 类实例变量

在外部使用 `.` 即可读取数据

```python
class PlayList(_PlayList):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        playlist_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, playlist_data)
        # 资源类型
        self.data_type = DATA_TYPE[2]
        # 歌单id
        self.id = playlist_data["id"]
        # 歌单标题
        self.name = playlist_data["name"]
        # 歌单封面
        self.cover = playlist_data['coverImgUrl']
        # 歌单创建者
        self.user = playlist_data['creator']
        self.user_str = playlist_data['creator']["nickname"]
        # 歌单tags
        self.tags = playlist_data['tags']
        self.tags_str = "/".join(playlist_data['tags'])
        # 歌单描述
        self.description = playlist_data["description"]
        # 歌单播放量
        self.play_count = playlist_data["playCount"]
        # 歌单收藏量
        self.subscribed_count = playlist_data["subscribedCount"]
        # 歌单创建时间
        self.create_time = playlist_data["createTime"]
        # 歌单歌曲
        self.music_list = playlist_data["tracks"]
```

## 类实例方法

### PlayList.subscribe

**`async def subscribe(self, in_: bool = True) -> dict[str, Any]:`**

对像 收藏/取消收藏

> `in_`: 收藏 / 取消收藏

### PlayList.subscribers

**`async def subscribers(self, page: int=0, limit: int=20) -> Generator[User, None, None]:`**

查看歌单收藏者， 返回一个 [User 对像](/pycloudmusic/User)生成器(Generator)

> `page`: 页
>
> `limit`: 一页的数据量

### PlayList.add

**`async def add(self, music_id: Union[str, int, list[Union[str, int]]]) -> dict[str, Any]:`**

向对像添加歌曲

> `music_id`: 歌曲 id， 支持多 id (使用列表)

### PlayList.del_

**`async def del_(self, music_id: Union[str, int, list[Union[str, int]]]) -> dict[str, Any]:`**

向对像删除歌曲

> `music_id`: 歌曲 id， 支持多 id (使用列表)