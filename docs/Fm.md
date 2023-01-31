# `class` Fm

**私人 Fm (Fm) 是一个列表类 (ListObject)， 支持直接迭代对象将返回按 Fm 曲目生成的 [PersonalizedMusic 对象](/pycloudmusic/ShortObject?id=class-personalizedmusic)，并且支持私人 Fm 相关的 Api**

```python
"""迭代 Fm"""
from pycloudmusic import Music163Api
import asyncio
import time


async def mian():
    musicapi = Music163Api("你网易云的 Cookie")

    # 验证 cookie 有效性, 并返回 my 对象
    my = await musicapi.my()
    # 打印 Cookie 用户信息
    print(my)
    print("=" * 60)

    """
    每 3 秒, 获取一次 Fm 歌曲
    """

    # 返回 fm 对象
    fm = my.fm()
    while True:
        # 获取 Fm 歌曲
        await fm.read()
        # 打印 Fm 歌曲
        for music in fm:
            print(music.name, music.artist_str, music.id)
        
        # 休息 3 秒
        time.sleep(3)

asyncio.run(mian())
```

## 类实例方法

### Fm.read

**`async def read(self) -> dict[str, Any]:`**

获取 Fm 歌曲，成功后返回 Fm json 数据，并更新 Fm 对象迭代所使用的数据

### Fm.write

**`async def write(self, id_: Union[int, str]) -> dict[str, Any]:`**

将歌曲扔进垃圾桶 (优化推荐)

> `id_`: 歌曲 id