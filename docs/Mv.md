# `class` Mv

**Mv 是一个数据类 (DataObject)，支持使用 `.` 读取数据，并且支持 Mv 相关的 Api， Mv 也支持[评论 (CommentObject)](/pycloudmusic/CommentObject)**

## 类实例变量

在外部使用 `.` 即可读取数据

```python
class Mv(_Mv):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        mv_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, mv_data)
        # mv id
        self.id = mv_data["id"]
        # mv标题
        self.name = mv_data["name"]
        # mv介绍
        self.desc = mv_data["desc"]
        # mv歌手
        self.artists = mv_data["artists"]
        self.artists_str = "/".join([artists['name'] for artists in self.artists])
        # mv tags
        self.tags = mv_data["videoGroup"]
        self.tags_str = "/".join([tags['name'] for tags in self.tags])
        # mv封面
        self.cover = mv_data["cover"]
        # mv播放数
        self.play_count = mv_data["playCount"]
        # mv收藏数
        self.subscribe_count = mv_data["subCount"]
        # mv评论数
        self.comment_count = mv_data["commentCount"]
        # mv分享数
        self.share_count = mv_data["shareCount"]
        # mv质量
        self.quality = mv_data["brs"]
        # 发布时间
        self.publish_time = mv_data["publishTime"]
```

## 类实例方法

### Mv.subscribe

**`async def subscribe(self, in_: bool = True) -> dict[str, Any]:`**

对像 收藏/取消收藏

> `in_`: 收藏 / 取消收藏

### Mv.play

**`async def play(self, download_path: Optional[str] = None, quality: Union[str, int] = 1080) -> str:`**

获取播放该 mv 对象指定的视频文件

> `download_path`: 下载路径
>
> `quality` mv 画质

### Mv._play_url

**`async def _play_url(self, quality: Union[str, int] = 1080) -> dict[str, Any]:`**

获取播放该 mv 对象指定的视频 url

> `quality` mv 画质