# `class` User

用户 (User) 支持调用与该用户相关的 Api

## 类实例变量

在外部使用 `.` 即可读取数据

```python
class User(Api):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        user_data: dict[str, Any]
    ) -> None:
        super().__init__(headers)
        _user_data = user_data["profile"] if "profile" in user_data else user_data
        # 用户uid
        self.id = _user_data["userId"]
        # 用户名称
        self.name = _user_data["nickname"]
        # 用户签名
        self.signature = _user_data["signature"]
        # 用户等级
        self.level = user_data["level"] if "level" in user_data else None
        # 头像
        self.cover = _user_data['avatarUrl']
        # 会员 0 无
        self.vip = _user_data["vipType"]
        self.like_playlist_id = None
```

## 类实例方法

### User.playlist

**`async def playlist(self, page: int = 0, limit: int = 30) -> Generator[PlayList, None, None]:`**

获取该对象的歌单， 返回一个 [PlayList 对像](/pycloudmusic/PlayList)生成器(Generator)

> `page`: 页
>
> `limit`: 一页的数据量

### User.like_music

**`async def like_music(self) -> PlayList:`**

获取该对象喜欢的歌曲， 返回一个 [PlayList 对像](/pycloudmusic/PlayList)

### User.record

**`async def record(self, type_: bool = True) -> Generator[Music, None, None]:`**

获取该对象听歌榜单， 返回一个 [Music 对像](/pycloudmusic/Music)生成器(Generator)

> `type_`: True 所有时间 / False 最近一周

### User.follow

**`async def follow(self, follow_in: bool=True) -> dict[str, Any]:`**

关注用户

> `follow_in`: 关注 / 取消关注