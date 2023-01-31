# `class` Music

**Music 是一个数据类 (DataObject)，支持使用 `.` 读取数据，并且支持歌曲相关的 Api， Music 也支持[评论 (CommentObject)](/pycloudmusic/CommentObject)**

## 类实例变量

在外部使用 `.` 即可读取数据

```python
class Music(_Music):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        music_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, music_data)
        # 资源类型
        self.data_type = DATA_TYPE[0]
        # 歌曲id
        self.id = music_data['id']
        # 标题列表 [大标题, 副标题]
        self.name = [music_data['name'], music_data["alia"][0] if music_data["alia"] != [] else ""]
        self.name_str = self.name[0] + self.name[1]
        # 作者列表 [作者, 作者, ...]
        self.artist = [{"id": artist["id"], "name": artist["name"]} for artist in music_data['ar']]
        self.artist_str = "/".join([author["name"] for author in self.artist])
        # 专辑列表
        self.album_data = music_data["al"]
        self.album_str = self.album_data["name"]
        # 所有音质
        self.quality = {
            "h": music_data["h"],
            "m": music_data["m"],
            "l": music_data["l"],
            "sq": music_data["sq"],
            "hr": music_data["hr"],
        }
        # mv id
        self.mv_id = music_data["mv"]
        self.publish_time = music_data["publishTime"]
        # 推荐理由
        self.reason = music_data["reason"] if "reason" in music_data else None
```

## 类实例方法

### Music.similar

**`async def similar(self) -> dict[str, Any]:`**

获取该对象的相似

### Music.similar_playlist

**`async def similar_playlist(self, page: int = 0, limit: int = 50) -> Generator[PlayList, None, None]:`**

获取该对象的相似歌单， 返回一个 [PlayList 对像](/pycloudmusic/PlayList)生成器(Generator)

> `page`: 页
>
> `limit`: 一页的数据量

### Music.similar_user

**`async def similar_user(self, page: int = 0, limit: int = 50 ) -> Generator[User, None, None]:`**

获取最近听了这 music 对象的用户， 返回一个 [User 对像](/pycloudmusic/User)生成器(Generator)

> `page`: 页
>
> `limit`: 一页的数据量

### Music.like

**`async def like(self, like: bool = True) -> dict[str, Any]:`**

红心该 music 对象与取消红心

> `like`: 喜欢 / 取消喜欢

### Music.lyric

**`async def lyric(self) -> dict[str, Any]:`**

该 music 对象的歌词

### Music.play

**`async def play(self, br = None, download_path: str = None) -> str:`**

获取播放该 music 对象指定的歌曲文件， 下载成功后返回文件路径

> `br`: 音质
>
> `download_path`: 下载路径

### Music.download

**`async def download(self, br = None, download_path: str = None) -> str:`**

获取下载该 music 对象指定的歌曲文件 (客户端下点击下载时候的 Api)

错误码 -105 需要会员， 下载成功后返回文件路径

> `br`: 音质
>
> `download_path`: 下载路径

### Music.mv

**`async def mv(self) -> "Mv":`**

获取该对像 mv 实例化 mv 对像并返回 mv 对像

### Music._play_url

**`async def _play_url(self, br = None) -> dict[str, Any]:`**

获取播放该 music 对象指定的歌曲文件 url

> `br`: 音质

### Music._download_url

**`async def _download_url(self, br = None) -> dict[str, Any]:`**

获取该 music 对象指定的歌曲 url, 错误码 -105 需要会员

> `br`: 音质
