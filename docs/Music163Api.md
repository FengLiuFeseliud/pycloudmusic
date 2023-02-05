# `class` Music163Api

**Music163Api 类用于生成其他数据类 (DataObject/DataListObject)， 或者调用网易云独立的 Api**

## 类实例方法

### Music163Api.my

**`async def my(self) -> Union[My, dict[str, Any]]:`**

获取当前 cookie 用户信息并实例化 [my 对像](/pycloudmusic/My)，cookie 无效返回 200

###  Music163Api.music

**`async def music(self, ids: Union[int, str, list[Union[str, int]]]) -> Generator[Music, None, None]:`**

获取歌曲并实例化 [music 对像](/pycloudmusic/Music)

> `ids`: 歌曲 id，支持多 id (使用列表)，多 id 时将返回生成 music 对像的生成器 (Generator)

### Music163Api.user

获取用户并实例化 [user 对像](/pycloudmusic/User)

**`async def user(self, id_: Union[int, str]) -> User:`**

> `id_`: 用户 id

### Music163Api.playlist

获取歌单并实例化 [playlist 对像](/pycloudmusic/PlayList)

**`async def playlist(self, id_: Union[int, str]) -> PlayList:`**

> `id_`: 歌单 id

### Music163Api.artist

获取歌手并实例化 [artist 对像](/pycloudmusic/Artist)

**`async def artist(self, id_: Union[int, str]) -> Artist:`**

> `id_`: 歌手 id

### Music163Api.album

实例化专辑 [album 对像](/pycloudmusic/Album)

**`async def album(self, id_: Union[int, str]) -> Album:`**

> `id_`: 专辑 id

### Music163Api.mv

获取 mv 并实例化 [mv 对像](/pycloudmusic/Mv)

**`async def mv(self, id_: Union[int, str]) -> Mv:`**

> `id_`: mv id

### Music163Api.dj

获取电台并实例化 [dj 对像](/pycloudmusic/Dj))

**`async def dj(self, id_: Union[int, str]) -> Dj:`**

> `id_`: 电台 id


### Music163Api.search_music

搜索歌曲，返回一个元组 (tuple) 包含所有的匹配数，一个 [Music 对像](/pycloudmusic/Music)生成器(Generator)

**`async def search_music(self, key: str, page: int = 0, limit: int = 30) -> tuple[int,Generator[Music, None, None]]:`**

> `key`: 搜索内容
>
> `page`: 页
>
> `limit`: 一页的数据量

### Music163Api.search_playlist

搜索歌曲，返回一个元组 (tuple) 包含所有的匹配数，一个 [ShortPlaylist 对像](/pycloudmusic/ShortObject?id=class-shortplaylist)生成器(Generator)

**`async def search_playlist(self, key: str, page: int = 0, limit: int = 30) -> tuple[int,Generator[ShortPlaylist, None, None]]:`**

> `key`: 搜索内容
>
> `page`: 页
>
> `limit`: 一页的数据量

### Music163Api.search_album

搜索专辑，返回一个元组 (tuple) 包含所有的匹配数，一个 [ShortAlbum 对像](/pycloudmusic/ShortObject?id=class-shortalbum)生成器(Generator)

**`async def search_album(self, key: str, page: int = 0, limit: int = 30) -> tuple[int,Generator[ShortAlbum, None, None]]:`**

> `key`: 搜索内容
>
> `page`: 页
>
> `limit`: 一页的数据量

### Music163Api.search_artist

搜索歌手，返回一个元组 (tuple) 包含所有的匹配数，一个 [ShortArtist 对像](/pycloudmusic/ShortObject?id=class-shortartist)生成器(Generator)

**`async def search_artist(self, key: str, page: int = 0, limit: int = 30) -> tuple[int,Generator[ShortArtist, None, None]]:`**

> `key`: 搜索内容
>
> `page`: 页
>
> `limit`: 一页的数据量

### Music163Api.search_user

搜索用户，返回一个元组 (tuple) 包含所有的匹配数，一个 [User 对像](/pycloudmusic/User)生成器(Generator)

**`async def search_user(self, key: str, page: int = 0, limit: int = 30) -> tuple[int,Generator[User, None, None]]:`**

> `key`: 搜索内容
>
> `page`: 页
>
> `limit`: 一页的数据量

### Music163Api.search_mv

搜索 Mv，返回一个元组 (tuple) 包含所有的匹配数，一个 [Mv 对像](/pycloudmusic/Mv)生成器(Generator)

**`async def search_mv(self, key: str, page: int = 0, limit: int = 30) -> tuple[int,   Generator[Mv, None, None]]:`**

> `key`: 搜索内容
>
> `page`: 页
>
> `limit`: 一页的数据量


### Music163Api.search_dj

搜索电台，返回一个元组 (tuple) 包含所有的匹配数，一个 [Dj 对像](/pycloudmusic/Dj)生成器(Generator)

**`async def search_dj(self, key: str, page: int = 0, limit: int = 30) -> tuple[int, Generator[Dj, None, None]]:`**

> `key`: 搜索内容
>
> `page`: 页
>
> `limit`: 一页的数据量

### Music163Api._search

搜索

> `key`: 搜索内容
>
> `type_`: 1: 单曲, 10: 专辑, 100: 歌手, 1000: 歌单, 1002: 用户, 1004: MV, 1006: 歌词, 1009: 电台, 1014: 视频
>
> `page`: 页
>
> `limit`: 一页的数据量

### Music163Api.personalized_playlist

推荐歌单，一个 [ShorterPlayList 对像](/pycloudmusic/ShortObject?id=class-shortplaylist)生成器(Generator)

**`async def personalized_playlist(self, limit: int = 30) -> Generator[ShorterPlayList, None, None]:`**

> `limit`: 一页的数据量

### Music163Api.personalized_new_song

推荐新歌，一个 [PersonalizedMusic 对像](/pycloudmusic/ShortObject?id=class-personalizedmusic)生成器(Generator)

**`async def personalized_new_song(self, limit: int = 30) -> Generator[PersonalizedMusic, None, None]:`**

> `limit`: 一页的数据量

### Music163Api.personalized_dj

推荐电台，一个 [PersonalizedDj 对像](/pycloudmusic/ShortObject?id=class-personalizeddj)生成器(Generator)

**`async def personalized_dj(self) -> UGenerator[PersonalizedDj, None, None]:`**

> `limit`: 一页的数据量

### Music163Api.home_page

首页-发现 app 主页信息

### Music163Api.top_artist_list

歌手榜，一个 [Artist 对像](/pycloudmusic/Artist)生成器(Generator)

**`async def top_artist_list(self, type_: Union[str, int] = 1, page: int = 0, limit: int = 100) -> Generator[Artist, None, None]:`**

> `type_`: 1: 华语, 2: 欧美, 3: 韩国, 4: 日本
>
> `page`: 页
>
> `limit`: 一页的数据量

### Music163Api.top_song

新歌速递，一个 [PersonalizedMusic 对像](/pycloudmusic/ShortObject?id=class-personalizedmusic)生成器(Generator)
**`async def top_song(self, type_: int = 0) -> Generator[PersonalizedMusic, None, None]:`**

> `type_`: 全部:0 华语:7 欧美:96 日本:8 韩国:16
>
> `page`: 页
>
> `limit`: 一页的数据量