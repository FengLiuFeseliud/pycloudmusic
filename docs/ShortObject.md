# 短对象 (ShortObject)

通常无法获取到对象详细数据的 Api 会生成短对象 (ShortObject)，如果需要获取完整的对象可以用 对象 (ShortObject) id 请求相关 Api 生成完整的对象

## `class` ShortPlayList

短歌单对象，支持所有歌单相关 Api

### 类实例变量

```python
class ShortPlayList(_PlayList):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        playlist_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, playlist_data)
        # 资源类型
        self.data_type = DATA_TYPE[2]
        # 歌单id
        self.id = playlist_data["id"]
        # 歌单标题
        self.name = playlist_data["name"]
        # 歌单封面
        self.cover = playlist_data['picUrl']
        # 歌单创建者
        self.user = playlist_data['creator']
        self.user_str = playlist_data['creator']["nickname"]
        # 歌单播放量
        self.play_count = playlist_data["playcount"]
        # 歌单创建时间
        self.create_time = playlist_data["createTime"]
        self.track_count = playlist_data["trackCount"]
        # 推荐理由
        self.reason = playlist_data["copywriter"] if "copywriter" in playlist_data else None
```

## `class` ShortArtist

短歌手对象，支持所有歌手相关 Api

### 类实例变量

```python
class ShortArtist(_Artist):

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
        # 歌手
        self.alias = artist_data["alias"]
        self.alias_str = "/".join(self.alias)
        # 专辑数
        self.album_size = artist_data["albumSize"]
        # mv数
        self.mv_size = artist_data["mvSize"]
        # 头像
        self.cover = artist_data["picUrl"]
```

## `class` ShortAlbum

短专辑对象，支持所有专辑相关 Api

### 类实例变量

```python
class ShortAlbum(_Album):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        album_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, album_data)
        # 专辑id
        self.id = album_data["id"]
        # 专辑标题
        self.name = album_data["name"]
        # 专辑别名
        self.alias = album_data["alias"]
        self.alias_str = "/".join(self.alias)
        # 专辑所有作者
        self.artists = album_data["artists"]
        self.artists_str = "/".join([artists_data["name"] for artists_data in self.artists])
        # 专辑曲目数
        self.size = album_data["size"]
        # 专辑封面
        self.cover = album_data["picUrl"]
        # 专辑收藏时间
        self.sub_time = album_data["subTime"] if "subTime" in album_data else 0
```

## `class` ShortDj

短电台对象，支持所有电台相关 Api

### 类实例变量

```python
class ShortDj(_Dj):

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
        self.rcmd_text = dj_data["rcmdtext"]
        # 电台标签
        self.tags = [
            {"id": dj_data['categoryId'], "name": dj_data['category']}
        ]
        self.tags_str = self.tags[0]["name"]
        # 电台收藏量
        self.subscribed_count = dj_data["subCount"]
        # 电台单曲数
        self.music_count = dj_data["programCount"]
        # 电台创建时间
        self.create_time = dj_data["createTime"]
        # 最后上传电台节目 id
        self.last_music_id = dj_data["lastProgramId"]
        # 最后上传电台节目时间
        self.last_music_create_time = dj_data["lastProgramCreateTime"]
        # 最后上传电台节目标题
        self.last_music_name = dj_data["lastProgramName"]

```

## `class` ShortMv

短 Mv 对象，支持所有 Mv 相关 Api

### 类实例变量

```python
class ShortMv(_Mv):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        mv_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, mv_data)
        # mv id
        self.id = mv_data["vid"]
        # mv标题
        self.name = mv_data["title"]
        # mv歌手
        self.artists = mv_data["creator"]
        self.artists_str = "/".join([artists['userName'] for artists in self.artists])
        # mv封面
        self.cover = mv_data["coverUrl"]
```

## `class` PersonalizedMusic

推荐歌曲，支持所有歌曲相关 Api

### 类实例变量

```python
class PersonalizedMusic(_Music):

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
        self.name = [music_data["name"], " ".join(music_data["alias"])]
        self.name_str = f"{self.name[0]} {self.name[1]}"
        # 作者列表 [作者, 作者, ...]
        self.artist = [{"id": artist["id"], "name": artist["name"]} for artist in music_data['artists']]
        self.artist_str = "/".join([author["name"] for author in self.artist])
        # 专辑列表
        self.album_data = music_data["album"]
        self.album_str = music_data["album"]["name"]
        # 所有音质
        self.quality = {
            "b": music_data["bMusic"],
            "h": music_data["hMusic"],
            "m": music_data["mMusic"],
            "l": music_data["lMusic"],
            "sq": music_data.get("sqMusic"),
            "hr": music_data.get("hrMusic"),
        }
        # mv id
        self.mv_id = music_data["mvid"]
        # 发表时间
        self.album_data["publishTime"]
```

## `class` PersonalizedDj

推荐电台，支持所有电台相关 Api

### 类实例变量

```python
class PersonalizedDj(_Dj):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        dj_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, dj_data)
        # 电台id
        self.id = dj_data["id"]
        # 电台标题
        self.name = dj_data["name"]
        # 电台封面
        self.cover = dj_data['coverUrl']
        # 电台创建者
        self.user = dj_data['dj']
        self.user_str = self.user["nickname"]
        # 电台标签
        self.tags = dj_data["channels"]
        # 电台描述
        self.description = dj_data["description"]
```