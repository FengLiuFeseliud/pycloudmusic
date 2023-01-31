# `class` Dj

**电台 (Dj) 是一个数据列表类 (DataListObject)， 支持直接迭代对象将返回按电台曲目生成的 [DjMusic 对象](/pycloudmusic/Dj?id=class-djmusic)，支持使用 `.` 读取数据，并且支持电台相关的 Api， Dj 也支持[评论 (CommentObject)](/pycloudmusic/CommentObject)**

```python
"""迭代 Dj"""
from pycloudmusic import Music163Api
import asyncio


async def mian():
    musicapi = Music163Api()
    # 获取电台
    # https://music.163.com/#/djradio?id=342290050
    dj = await musicapi.dj(342290050)

    # 计算电台页数
    dj_music_page = int(dj.music_count / 30)
    while dj_music_page > 0:
        # 获取电台节目
        await dj.read(dj_music_page, asc=True)
        # 打印电台节目
        for music in dj:
            print(music.name, music.id)
        
        dj_music_page -= 1

asyncio.run(mian())
```

## 类实例变量

在外部使用 `.` 即可读取数据

```python
class Dj(_Dj):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        dj_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, dj_data)
        # 电台标题
        self.name = dj_data["name"]
        # 电台id
        self.id = dj_data["id"]
        # 电台封面
        self.cover = dj_data['picUrl']
        # 电台创建者
        self.user = dj_data['dj']
        self.user_str = self.user["nickname"]
        # 电台描述
        self.description = dj_data["desc"]
        # 电台小描述
        self.rcmd_text = dj_data["rcmdText"]
        # 电台标签
        self.tags = [
            {"id": dj_data['categoryId'], "name": dj_data['category']},
            {"id": dj_data['secondCategoryId'], "name": dj_data['secondCategory']},
        ]
        self.tags_str = "/".join([tag["name"] for tag in self.tags])
        # 电台分享量
        self.share_count = dj_data["shareCount"]
        # 电台收藏量
        self.subscribed_count = dj_data["subCount"]
        # 电台单曲数
        self.music_count = dj_data["programCount"]
        # 电台评论数
        self.count = dj_data["commentCount"]
        # 电台创建时间
        self.create_time = dj_data["createTime"]
        # 是否收藏了电台
        self.subed =  dj_data["subed"]
        # 最后上传电台节目 id
        self.last_music_id = dj_data["lastProgramId"]
        # 最后上传电台节目时间
        self.last_music_create_time = dj_data["lastProgramCreateTime"]
```

## 类实例方法

### Dj.subscribe

**`async def subscribe(self, in_: bool = True) -> dict[str, Any]:`**

对像 收藏/取消收藏

> `in_`: 收藏 / 取消收藏

### Dj.read

**`async def read(self, page: int = 0, limit: int= 30, asc: bool = False) -> dict[str, Any]:`**

获取电台节目，成功后返回电台节目 json 数据，并更新 Dj 对象迭代所使用的数据

> `page`: 页
>
> `limit`: 一页的数据量
>
> `asc`: False 时间正序获取 \ True 时间倒序获取

# `class` DjMusic

**电台节目 DjMusic 支持使用 `.` 读取数据，并且支持电台节目相关的 Api， DjMusic 也支持[评论 (CommentObject)](/pycloudmusic/CommentObject)**

## 类实例变量

在外部使用 `.` 即可读取数据

```python
class DjMusic(Music163Comment):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        dj_music_data: dict[str, Any]
    ) -> None:
        super().__init__(headers)
        self.data_type = DATA_TYPE[4]
        # 电台节目id
        self.id = dj_music_data["id"]
        # 电台节目标题
        self.name = dj_music_data["name"]
        # 电台节目简介
        self.description = dj_music_data["description"]
        # 电台节目封面
        self.cover = dj_music_data["coverUrl"]
        # 电台节目创建时间
        self.create_time = dj_music_data["createTime"]
        # 电台节目播放量
        self.play_count = dj_music_data["listenerCount"]
        # 电台节目点赞量
        self.like_count = dj_music_data["likedCount"]
        # 电台节目评论量
        self.comment_count = dj_music_data["commentCount"]
```