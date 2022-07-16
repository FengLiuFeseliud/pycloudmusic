import time
from typing import Generator, Optional, Union, Any
from pycloudmusic.metaclass import *


# 数据类型
DATA_TYPE = [
    "R_SO_4_",  # 歌曲
    "R_MV_5_",  # mv
    "A_PL_0_",  # 歌单
    "R_AL_3_",  # 专辑
    "A_DJ_1_",  # 电台
    "R_VI_62_",  # 视频
    "A_EV_2_",  # 动态
]


class Music163Comment(CommentObject):

    def __init__(self, headers: Optional[dict[str, str]] = None) -> None:
        super().__init__(headers)
        self.data_type: Optional[str] = None
        self.id: Optional[int] = None

    async def comment(self, hot: bool = True, page: int = 0, limit: int = 20, before_time: int = 0) -> dict[str, Any]:
        api = "/api/v1/resource/hotcomments" if hot else "/api/v1/resource/comments"
        return await self._post("%s/%s%s" % (api, self.data_type, self.id), {
            "rid": self.id, 
            "limit": limit, 
            "offset": limit * page, 
            "beforeTime": before_time
        })
    
    async def comment_floor(self, comment_id: Union[str, int], page: int = 0, limit: int = 20) -> dict[str, Any]:
        return await self._post("/api/resource/comment/floor/get", {
            "parentCommentId": comment_id, 
            "threadId": "%s%s" % (self.data_type, self.id), 
            "limit": limit,
            "offset": limit * page
        })

    async def comment_like(self, comment_id: Union[str, int], in_: bool) -> dict[str, Any]:
        return await self._post("/api/v1/comment%s" % '/like' if in_ else '/unlike', {
            "threadId": "%s%s" % (self.data_type, self.id),
            "commentId": comment_id
        })

    async def comment_add(self, content: str) -> dict[str, Any]:
        return await self._post("/api/resource/comments/add", {
            "threadId": "%s%s" % (self.data_type, self.id),
            "content": content
        })
    
    async def comment_delete(self, comment_id: Union[str, int]) -> dict[str, Any]:
        return await self._post("/api/resource/comments/delete", {
            "threadId": "%s%s" % (self.data_type, self.id),
            "commentId": comment_id
        })
    
    async def comment_reply(self, comment_id: Union[str, int], content: str) -> dict[str, Any]:
        return await self._post("/api/resource/comments/reply", {
            "threadId": "%s%s" % (self.data_type, self.id),
            "commentId": comment_id,
            "content": content
        })


class _Music(DataObject, Music163Comment):

    def __init__(self, headers: Optional[dict[str, str]], music_data: dict[str, Any]) -> None:
        super().__init__(headers, music_data)
    
    async def subscribe(self, in_: bool = True) -> dict[str, Any]:
        raise TypeError("无法直接收藏 该对象不支持收藏")

    async def similar(self) -> Any:
        return await self._post("/api/v1/discovery/simiSong", {
            "songid": self.id,
            "limit": 50, 
            "offset": 0
        })


class Music(_Music):

    def __init__(self, headers: Optional[dict[str, str]], music_data: dict[str, Any]) -> None:
        super().__init__(headers, music_data)
        # 资源类型
        self.data_type = DATA_TYPE[0]
        # 歌曲id
        self.id = music_data['id']
        # 标题列表 [大标题, 副标题]
        self.name = [music_data['name'], music_data["alia"][0] if music_data["alia"] != [] else ""]
        self.name_str = self.name[0] + self.name[1]
        # 作者列表 [作者, 作者, ...]
        self.artist = [{"id": artist["id"], "name": artist["name"]} for artist in music_data['ar']]
        self.artist_str = "/".join([author["name"] for author in self.artist])
        # 专辑列表
        self.album_data = music_data["al"]
        if "tns" in self.album_data:
            self.album_str = self.album_data["name"] + " " + (
                self.album_data["tns"][0] if self.album_data["tns"] != [] else "")
        else:
            self.album_str = self.album_data["name"]
        # 所有音质
        self.quality = {3: music_data["h"], 2: music_data["m"], 1: music_data["l"]}
        # mv id
        self.mv_id = music_data["mv"]
        # 发表时间
        if "publishTime" in music_data:
            self.publish_time = music_data["publishTime"]
        else:
            self.publish_time = None

        # True时获取完成资源链接后直接返回(不进行下载)
        self.not_download = False


class PlayList(DataListObject, Music163Comment):

    def __init__(self, headers: Optional[dict[str, str]], playlist_data: dict[str, Any]) -> None:
        super().__init__(headers, playlist_data)
        # 资源类型
        self.data_type = DATA_TYPE[2]
        # 歌单id
        self.id = playlist_data["id"]
        # 歌单标题
        self.name = playlist_data["name"]
        # 歌单封面
        self.cover = playlist_data['coverImgUrl']
        # 歌单创建者
        self.user = playlist_data['creator']
        self.user_str = playlist_data['creator']["nickname"]
        # 歌单tags
        self.tags = playlist_data['tags']
        self.tags_str = "/".join(playlist_data['tags'])
        # 歌单描述
        self.description = playlist_data["description"]
        # 歌单播放量
        self.play_count = playlist_data["playCount"]
        # 歌单收藏量
        self.subscribed_count = playlist_data["subscribedCount"]
        # 歌单创建时间
        self.create_time = playlist_data["createTime"]
        # 歌单歌曲
        self.music_list = playlist_data["tracks"]

    def __next__(self) -> Music:
        return Music(self._headers, super().__next__())

    async def subscribe(self, in_: bool = True) -> dict[str, Any]:
        return await self._post("/api/playlist%s" % '/subscribe' if in_ else '/unsubscribe', {
            "id": self.id
        })
    
    async def similar(self) -> Any:
        raise TypeError("无法直接获取相似 请通过歌曲/该对象不支持获取相似")


class User(Api):

    def __init__(self, headers: Optional[dict[str, str]], user_data: dict[str, Any]) -> None:
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

    async def _get_like_playlist_id(self):
        if self.like_playlist_id is None:
            data = await self.playlist(limit=1)
            if type(data) == int:
                return data
            self.like_playlist_id = next(data).id
        return self.like_playlist_id

    async def playlist(self, page: int=0, limit: int=30) -> Union[Generator[PlayList, None, None], dict[str, Any]]:
        """
        获取该对象的歌单
        """
        data = await self._post("/api/user/playlist", {
            "uid": self.id, 
            "limit": limit, 
            "offset": limit * page, 
            "includeVideo": True
        })

        if data["code"] != 200:
            return data["code"]
        
        return (PlayList(self._headers, PlayList) for PlayList in data['playlist'])

    async def like_music(self) -> Union[PlayList, dict[str, Any]]:
        """
        获取该对象喜欢的歌曲
        """
        from pycloudmusic.music163 import Music163Api

        like_playlist_id = await self._get_like_playlist_id()
        return await Music163Api(self._headers["cookie"]).playlist(like_playlist_id)

    async def record(self, type_: bool=True) -> Union[Generator[Music, None, None], dict[str, Any]]:
        """
        获取该对象听歌榜单
        """
        data = await self._post("/api/v1/play/record", {
            "uid": self.id, "type": 0 if type_ else 1
        })

        if data['code'] != 200:
            return data

        return (Music(self._headers, music_data) for music_data in (data["allData"] if type_ else data["weekData"]))

    async def follow(self, follow_in: bool=True):
        """
        关注用户
        """
        follow_in_ = "follow" if follow_in else "delfollow"
        return await self._post(f"/api/user/{follow_in_}/{self.id}")


class Album(DataListObject, Music163Comment):

    def __init__(self, headers: Optional[dict[str, str]], album_data: dict[str, Any]) -> None:
        super().__init__(headers, album_data)
        self.data_type = DATA_TYPE[3]
        # 专辑id
        self.id = album_data["id"]
        # 专辑标题
        self.name = album_data["name"]
        # 专辑封面
        self.cover = album_data['picUrl']
        self.music_list = album_data["songs"]

    async def subscribe(self, in_: bool = True) -> dict[str, Any]:
        return await self._post("/api/album%s" % "/sub" if in_ else "/unsub", {
            "id": self.id
        })
    
    async def similar(self) -> Any:
        raise TypeError("无法直接获取相似 请通过歌曲/该对象不支持获取相似")

    def __next__(self) -> Music:
        return Music(self._headers, super().__next__())


class Mv(DataObject, Music163Comment):

    def __init__(self, headers: Optional[dict[str, str]], mv_data: dict[str, Any]) -> None:
        super().__init__(headers, mv_data)
        self.data_type = DATA_TYPE[1]
        # mv id
        self.id = mv_data['data']["id"]
        # mv标题
        self.name = mv_data['data']["name"]
        # mv介绍
        self.desc = mv_data["data"]["desc"]
        # mv歌手
        self.artists = mv_data["data"]["artists"]
        self.artists_str = "/".join([artists['name'] for artists in self.artists])
        # mv tags
        self.tags = mv_data["data"]["videoGroup"]
        self.tags_str = "/".join([tags['name'] for tags in self.tags])
        # mv封面
        self.cover = mv_data["data"]["cover"]
        # mv播放数
        self.play_count = mv_data["data"]["playCount"]
        # mv收藏数
        self.subscribe_count = mv_data["data"]["subCount"]
        # mv评论数
        self.comment_count = mv_data["data"]["commentCount"]
        # mv分享数
        self.share_count = mv_data["data"]["shareCount"]
        # mv质量
        self.quality = mv_data["data"]["brs"]
        # 发布时间
        self.publish_time = mv_data["data"]["publishTime"]
        # True时获取完成资源链接后直接返回(不进行下载)
        self.not_download = False

    async def play(self, download_path, quality=1080):
        """
        获取播放该mv对象指定的视频文件
        """
        data = await self._post("/api/song/enhance/play/mv/url", {
            "id": self.id, "r": quality
        })

        if data["code"] != 200:
            return data

        url = data["data"]["url"]
        if self.not_download:
            return url

        return await self._download(url, f"{self.name}.mp4", download_path)

    async def subscribe(self, in_: bool = True) -> dict[str, Any]:
        return await self._post("/api/mv%s" % "/sub" if in_ else "/unsub", {
            "mvId": self.id,
            "mvIds": '["' + str(self.id) + '"]',
        })
    
    async def similar(self) -> Any:
        return await self._post("/api/discovery/simiMV", {
            "mvid": self.id
        })


class Artist(DataObject):

    def __init__(self, headers: Optional[dict[str, str]], artist_data: dict[str, Any]) -> None:
        super().__init__(headers, artist_data)
        self.data_type = "artist"
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

    async def song(self, hot: bool=True, page: int=0, limit: int=100) -> Union[Generator[Music, None, None], dict[str, Any]]:
        """
        获取该对像歌曲
        """
        data = await self._post("/api/v1/artist/songs", {
            "id": self.id,
            "order": 'hot' if hot else "time",
            "offset": limit * page,
            "limit": limit,
            "private_cloud": True,
            "work_type": 1
        })
        
        if data["code"] != 200:
            return data

        return (Music(self._headers, music_data) for music_data in data['songs'])

    async def song_top(self) -> Union[Generator[Music, None, None], dict[str, Any]]:
        """
        获取该对像热门50首
        """
        data = await self._post("/api/artist/top/song", {
            "id": self.id
        })

        if data["code"] != 200:
            return data

        return (Music(self._headers, music_data) for music_data in data['songs'])

    async def album(self, page: int=0, limit: int=30) -> Union[Generator[Album, None, None], dict[str, Any]]:
        """
        获取该对像专辑
        """
        data = await self._post("/api/artist/albums/%s" % self.id, {
            "limit": limit, "offset": limit * page, "total": True,
        })

        if data["code"] != 200:
            return data

        return (Album(self._headers, album_data) for album_data in data["hotAlbums"])
    
    async def subscribe(self, in_: bool = True) -> dict[str, Any]:
        return await self._post("/api/artist%s" % "/sub" if in_ else "/unsub", {
            "artistId": self.id,
            "artistIds": '["' + str(self.id) + '"]'
        })
    
    async def similar(self) -> Any:
        return await self._post("/api/discovery/simiArtist", {
            "artistid": self.id
        })


class DjMusic(Music163Comment):

    def __init__(self, headers, dj_music_data):
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


class Dj(DataListObject):

    def __init__(self, headers: Optional[dict[str, str]], dj_data: dict[str, Any]) -> None:
        super().__init__(headers, dj_data)
        self.data_type = DATA_TYPE[4]
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
        # 电台tags
        self.tags = dj_data['category']
        # self.tags_str = self.set_list_str(playlist_data['tags'])
        # 电台分享量
        self.share_count = dj_data["shareCount"]
        # 电台收藏量
        self.subscribed_count = dj_data["subCount"]
        # 电台单曲数
        self.music_count = dj_data["programCount"]
        # 电台创建时间
        self.create_time = dj_data["createTime"]
    
    async def read(self, page=0, limit=30, asc=False):
        """
        获取电台节目
        """
        data = await self._post("/api/dj/program/byradio", {
            "radioId": self.id, "limit": limit, "offset": limit * page, "asc": asc
        })

        if data["code"] != 200:
            return data

        self.music_list = data["programs"]
        return data
    
    async def subscribe(self, in_: bool = True) -> dict[str, Any]:
        return await self._post("/api/djradio%s" % "/sub" if in_ else "/unsub", {
            "id": self.id
        })

    async def similar(self) -> Any:
        raise TypeError("无法直接获取相似 请通过歌曲/该对象不支持获取相似")

    def __next__(self) -> DjMusic:
        return DjMusic(self._headers, super().__next__())


class FmMusic(_Music):

    def __init__(self, headers: Optional[dict[str, str]], music_data: dict[str, Any]) -> None:
        super().__init__(headers, music_data)
        # 资源类型
        self.data_type = DATA_TYPE[0]
        # 歌曲id
        self.id = music_data['id']
        # 标题列表 [大标题, 副标题]
        self.name = music_data["name"]
        # 作者列表 [作者, 作者, ...]
        self.artist = [{"id": artist["id"], "name": artist["name"]} for artist in music_data['artists']]
        self.artist_str = "/".join([author["name"] for author in self.artist])
        # 专辑列表
        self.album_data = music_data["album"]
        self.album_str = music_data["album"]["name"]
        # mv id
        self.mv_id = music_data["mvid"]
        # 发表时间
        self.album_data["publishTime"]
        # True时获取完成资源链接后直接返回(不进行下载)
        self.not_download = False


class Fm(Api, ListObject):

    def __init__(self, headers: Optional[dict[str, str]] = None) -> None:
        super().__init__(headers)

    async def read(self):
        """
        获取fm歌曲
        """
        data = await self._post("/api/v1/radio/get")

        if data["code"] != 200:
            return data

        self.music_list = data["data"]
        return data

    async def write(self, id_: Union[int, str]):
        """
        将歌曲扔进垃圾桶 (优化推荐)
        """
        return await self._post("/api/radio/trash/add?alg=RT&songId=%s&time=%s" % (id_, int(time.time())), {
            "songId": id_
        })

    def __next__(self) -> FmMusic:
        return FmMusic(self._headers, super().__next__())


class My(User):

    def __init__(self, headers: Optional[dict[str, str]], user_data: dict[str, Any]) -> None:
        super().__init__(headers, user_data)
        # 登录ip
        self.login_ip = user_data["profile"]["lastLoginIP"]
        # 登录时间
        self.login_time = int(user_data["profile"]["lastLoginTime"] / 1000)
        self.login_time_str = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(self.login_time))

    def fm(self):
        """
        私人fm 实例化一个fm对象 并返回
        """
        return Fm(self._headers)