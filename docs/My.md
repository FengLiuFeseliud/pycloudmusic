# `class` My

My 支持 [User 对象](/pycloudmusic/User)的所有实例方法与实例变量， 并且可以调用与 Cookie 用户相关的 Api

## 类实例变量

在外部使用 `.` 即可读取数据

```python
class My(User):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        user_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, user_data)
        """包括 User 的所有实例变量"""
        # 登录ip
        self.login_ip = user_data["profile"]["lastLoginIP"]
        # 登录时间
        self.login_time = int(user_data["profile"]["lastLoginTime"] / 1000)
        self.login_time_str = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(self.login_time))
```

## 类实例方法

### My.sign

**`async def sign(self, type_: bool = True) -> dict[str, Any]:`**

使用该对象签到

> `type_`: True 为安卓端签到3点经验 / False 为网页签到2点经验

### My.recommend_songs

**`async def recommend_songs(self) -> Generator[Music, None, None]:`**

获取日推，返回一个 [Music 对像](/pycloudmusic/Music)生成器(Generator)

### My.recommend_resource

**`async def recommend_resource(self) -> Generator[ShortPlayList, None, None]:`**

获取每日推荐歌单，返回一个 [ShortPlayList 对像](/pycloudmusic/ShortObject?id=class-shortplaylist)生成器(Generator)

### My.playmode_intelligence

**`async def playmode_intelligence(self, music_id: Union[str, int], sid: Optional[Union[str, int]] = None, playlist_id: Optional[Union[str, int]] = None) -> Generator[Music, None, None]:`**

心动模式/智能播放 歌单，返回一个 Music 对像生成器(Generator)

> `music_id`: 歌曲 id
>
> `sid`: 可选 要开始播放的歌曲的 id
>
> `playlist_id`: 可选 歌单 id 默认使用喜欢的歌曲歌单

### My.sublist_artist

**`async def sublist_artist(self, page: int = 0, limit: int = 25) -> tuple[int, Generator[ShortArtist, None, None]]:`**

查看 cookie 用户收藏的歌手，返回一个元组 (tuple) 包含所有的歌手收藏数，一个 [ShortArtist 对像](/pycloudmusic/ShortObject?id=class-shortartist)生成器(Generator)

> `page`: 页
>
> `limit`: 一页的数据量

### My.sublist_album

**`async def sublist_album(self, page: int = 0, limit: int = 25) -> tuple[int, Generator[ShortAlbum, None, None]]:`**

查看 cookie 用户收藏的专辑，返回一个元组 (tuple) 包含所有的专辑收藏数，一个 [ShortAlbum 对像](/pycloudmusic/ShortObject?id=class-shortalbum)生成器(Generator)

> `page`: 页
>
> `limit`: 一页的数据量

### My.sublist_dj

**`async def sublist_dj(self, page: int = 0, limit: int = 25) -> tuple[int, Generator[ShortDj, None, None]]:`**

查看 cookie 用户收藏的电台，返回一个元组 (tuple) 包含所有的电台收藏数，一个 [ShortDj 对像](/pycloudmusic/ShortObject?id=class-shortdj)生成器(Generator)

> `page`: 页
>
> `limit`: 一页的数据量

### My.sublist_mv

**`async def sublist_mv(self, page: int = 0, limit: int = 25) -> tuple[int, Generator[ShortMv, None, None]]:`**

查看 cookie 用户收藏的 MV，返回一个元组 (tuple) 包含所有的 MV 收藏数，一个 [ShortMv 对像](/pycloudmusic/ShortObject?id=class-shortmv)生成器(Generator)

> `page`: 页
>
> `limit`: 一页的数据量

### My.sublist_topic

**`async def sublist_topic(self, page: int = 0, limit: int = 50) -> dict[str, Any]:`**

查看 cookie 用户收藏的专题

> `page`: 页
>
> `limit`: 一页的数据量

### My.fm

**`def fm(self) -> Fm:`**

私人 fm 实例化一个 fm 对象并返回

### My.message

**`def message(self) -> Message:`**

私信 实例化一个 message 对象并返回

### My.event

**`def event(self) -> Event:`**

动态 实例化一个 event 对象并返回

### My.cloud

**`async def cloud(self, page: int = 0, limit: int = 30) -> Cloud:`**

获取云盘数据并实例化一个 cloud 对象返回， 实例化失败时返回 Api 错误信息 (json)

> `page`: 页
>
> `limit`: 一页的数据量