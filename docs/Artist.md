# `class` Artist

**歌手 (Artist) 是一个数据类 (DataObject)，支持使用 `.` 读取数据，并且支持歌手相关的 Api**

## 类实例变量

在外部使用 `.` 即可读取数据

```python
class Artist(_Artist):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        artist_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, artist_data)
        # 歌手id
        self.id = artist_data["id"]
        # 歌手
        self.name = artist_data["name"]
        # 歌手简介
        self.brief_desc_str = artist_data["briefDesc"]
        self.brief_desc = artist_data["briefDesc"].split("\n")
        # 专辑数
        self.album_size = artist_data["albumSize"]
        # 单曲数
        self.music_size = artist_data["musicSize"]
        # mv数
        self.mv_size = artist_data["mvSize"]
        # 头像
        self.cover = artist_data["cover"]
```

## 类实例方法

### Artist.song

**`async def song(self, hot: bool = True, page: int = 0, limit: int = 100) -> Generator[Music, None, None]:`**

获取该对像歌曲，返回一个 [Music 对像](/pycloudmusic/Music)生成器(Generator)

> `hot`: True 按热度排序 / False 按时间排序
>
> `page`: 页
>
> `limit`: 一页的数据量

### Artist.song_top

**`async def song_top(self) -> Generator[Music, None, None]`**

获取该对像热门50首，返回一个 [Music 对像](/pycloudmusic/Music)生成器(Generator)

### Artist.album

**`async def album(self, page: int = 0, limit: int = 30) -> Generator[Album, None, None]:`**

获取该对像专辑，返回一个 [Album 对像](/pycloudmusic/Album)生成器(Generator)

> `page`: 页
>
> `limit`: 一页的数据量

### Artist.subscribe

**`async def subscribe(self, in_: bool = True) -> dict[str, Any]:`**

对像 收藏/取消收藏

> `in_`: 收藏 / 取消收藏

### Artist.similar

**`async def similar(self) -> Any:`**

该对象的相似