# `class` Event

**动态 (Event) 是一个列表类 (ListObject)， 支持直接迭代对象将返回按动态生成的 [EventItem 对象](/pycloudmusic/Event?id=class-eventitem)，并且支持动态相关的 Api**

```python
"""迭代 Event"""
from pycloudmusic import Music163Api
import asyncio


async def mian():
    musicapi = Music163Api("你网易云的 Cookie")
    
    # 验证 cookie 有效性, 并返回 my 对象
    my = await musicapi.my()
    # 打印 Cookie 用户信息
    print(my)
    print("=" * 60)
    
    # 初始化
    event, last_time, count = my.event(), -1, 0
    while True:
        try:
            # 获取动态并重设 last_time
            # https://music.163.com/#/user/home?id=1452176465
            last_time = (await event.read_user(1452176465, last_time))["lasttime"]
        except KeyError:
            # 没有动态时不会有 lasttime 会发生 KeyError, 依赖这个判断跳出循环
            break
        
        # 打印动态
        for event_item in event:
            print(event_item.user_str, event_item.msg["msg"], event_item.id)
            count += 1

    # 打印总动态数
    print(f"总动态数: {count}")

asyncio.run(mian())
```

## 类实例方法

### Event.read

**`async def read(self, last_time: Union[str, int] = -1, limit: int = 30) -> dict[str, Any]:`**

获取下一页动态，成功后返回动态 json 数据，并更新 Event 对象迭代所使用的数据

> `last_time`: 传入上一次返回结果的 time,将会返回下一页的数据
>
> `limit`: 一页获取量

### Event.read_user

**`async def read_user(self, user_id: Union[str, int], last_time: Union[str, int] = -1, limit: int = 30) -> dict[str, Any]:`**

获取指定用户动态，成功后返回动态 json 数据，并更新 Event 对象迭代所使用的数据

> `user_id`: 用户 id
>
> `last_time`: 传入上一次返回结果的 time,将会返回下一页的数据
>
> `limit`: 一页获取量

### Event.del_

**`async def del_(self, id_: Union[str, int]) -> dict[str, Any]:`**

删除 cookie 用户动态

> `id_`: 动态 id

### Event.send

**`async def send(self, msg: str) -> dict[str, Any]:`**

使用 cookie 用户发送动态

> `msg`: 内容，140 字限制，支持 emoji，@用户名

### Event.send_music

**`async def send_music(self, msg: str, id_: Union[str, int]) -> dict[str, Any]:`**

使用 cookie 用户发送动态 带歌曲

> `msg`: 内容，140 字限制，支持 emoji，@用户名
>
> `id_`: 歌曲 id

### Event.send_playlist

**`async def send_playlist(self, msg: str, id_: Union[str, int]) -> dict[str, Any]:`**

使用 cookie 用户发送动态 带歌单

> `msg`: 内容，140 字限制，支持 emoji，@用户名
>
> `id_`: 歌单 id

### Event.send_mv

**`async def send_mv(self, msg: str, id_: Union[str, int]) -> dict[str, Any]:`**

使用 cookie 用户发送动态 带 mv

> `msg`: 内容，140 字限制，支持 emoji，@用户名
>
> `id_`: mv id

### Event.send_dj

**`async def send_dj(self, msg: str, id_: Union[str, int]) -> dict[str, Any]:`**

使用 cookie 用户发送动态 带电台

> `msg`: 内容，140 字限制，支持 emoji，@用户名
>
> `id_`: 电台 id

### Event.send_dj_music

**`async def send_dj_music(self, msg: str, id_: Union[str, int]) -> dict[str, Any]:`**

使用 cookie 用户发送动态 带电台节目

> `msg`: 内容，140 字限制，支持 emoji，@用户名
>
> `id_`: 电台节目 id

# `class` EventItem

**单动态 EventItem 支持使用 `.` 读取数据，并且支持单动态相关的 Api， EventItem 也支持[评论 (CommentObject)](/pycloudmusic/CommentObject)**

## 类实例变量

在外部使用 `.` 即可读取数据

```python
class EventItem(Music163Comment):

    def __init__(
        self, 
        headers: dict[str, str],
        event_data: dict[str, Any]
    ) -> None:
        super().__init__(headers)
        self.data_type = DATA_TYPE[6]
        # 动态发布用户
        self.user = event_data["user"]
        self.user_str = self.user["nickname"]
        # 动态内容
        self.msg = json.loads(event_data["json"])
        # 动态图片
        self.pics = event_data["pics"]
        # 动态话题
        self.act_name = event_data["actName"]
        # 动态类型
        self.type = event_data["type"]
        self.type_str = EVENT_TYPE[self.type]
        # 动态 id
        self.id = event_data['id']
        # 动态 id
        self.ev_id = "%s_%s" % (self.id, self.user["userId"])
        # 动态分享数
        self.share_count = event_data["info"]["shareCount"]
        # 动态评论数
        self.comment_count = event_data["info"]["commentCount"]
        # 动态点赞数
        self.like_count = event_data["info"]["likedCount"]
        # 动态时间
        self.event_time = event_data["eventTime"]
```

## 类实例方法

### EventItem.forward

**`async def forward(self, msg: str) -> dict[str, Any]:`**

转发到 cookie 用户

> `msg`: 转发消息内容