## `class` Page

**`def __init__(self, api_fun: Callable, limit: Optional[int] = None, page: int = 0, **kwargs) -> None:`**

Page 对象可以按内部设置的方法来遍历绑定 Api 的页

> `api_fun`: 绑定的 Api
> 
> `limit`: 一页的数据量
>
> `page`: 遍历起点页数， 默认0 (重头开始)
>
> `**kwargs`: 绑定的 Api 其它参数

### demo

```python
from pycloudmusic import Music163Api, Page
import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌曲
    # https://music.163.com/song?id=1902224491&userid=492346933
    music = await musicapi.music(1902224491)
    """
    遍历 Page

    绑定的 Api music.comments
    绑定的 Api 参数 hot
    """
    async for comments in Page(music.comments, hot=False):
        # 遍历一页的数据
        for comment in comments:
            print(f"{comment.user_str}:  {comment.content}")

asyncio.run(main())
```

### 类实例方法

### Page.all

**`async def all(self, call_fun: Optional[Callable[[dict], int]] = None)`**

获取对象绑定 Api 的所有数据

> `call_fun`: 设置最大页数回调，接受 api 数据，返回最大页数 (int)

#### Demo

Page.all 与直接遍历对象的不同是，Page.all会一次性请求所有数据，而直接遍历对象是循环一次请求一次，按需请求

```python
from pycloudmusic import Music163Api, Page
import asyncio


async def main():
    musicapi = Music163Api()
    # https://music.163.com/song?id=1902224491&userid=492346933
    music = await musicapi.music(1902224491)
    # 一次性请求所有数据
    for count, comments in await Page(music.comments, hot=False).all():
        # 遍历一页的数据
        for comment in comments:
            print(f"{comment.user_str}:  {comment.content}")

asyncio.run(main())
```