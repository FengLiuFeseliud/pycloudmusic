import json
import time
from typing import Generator, NoReturn, Optional, Union, Any
from pycloudmusic.ahttp import _post, _download, _post_url
from pycloudmusic.baseclass import *


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


# 动态类型
EVENT_TYPE = {
    18: '分享单曲',
    19: '分享专辑',
    17: '分享电台节目',
    28: '分享电台节目',
    22: '转发',
    39: '发布视频',
    35: '分享歌单',
    13: '分享歌单',
    24: '分享专栏文章',
    41: '分享视频',
    21: '分享视频'
}


class Music163CommentItem(CommentItemObject):

    def __init__(
        self, 
        comment_data: dict[str, Any]
    ) -> None:
        super().__init__(comment_data)
        # 评论 id
        self.id = comment_data["commentId"]
        # 资源 id 
        self.thread_id =  comment_data["threadId"]
        # 用户 id
        self.user = comment_data["user"]
        # 用户名
        self.user_str = comment_data["user"]["nickname"]
        # 评论内容
        self.content = comment_data["content"]
        # 评论时间
        self.time = comment_data["time"]
        self.time_str = comment_data["timeStr"]
        # 评论点赞数
        self.liked_count = comment_data["likedCount"]
        # 是否点赞了该评论
        self.liked = comment_data["liked"]

    async def floors(
        self, 
        page: int = 0, 
        limit: int = 20
    ) -> Union[tuple[int, Generator[CommentItemObject, None, None]], dict[str, Any]]:
        data = await _post("/api/resource/comment/floor/get", {
            "parentCommentId": self.id, 
            "threadId": self.thread_id, 
            "limit": limit,
            "offset": limit * page
        })

        if data["code"] != 200:
            return data

        return data["data"]["totalCount"], (Music163CommentItem(
            dict({"threadId": self.thread_id}, **comment_data)
        ) for comment_data in data["data"]["comments"])

    async def reply(
        self,
        content: str
    ) -> dict[str, Any]:
        return await _post("/api/resource/comments/reply", {
            "threadId": self.thread_id,
            "commentId": self.id,
            "content": content
        })

    async def like(
        self, 
        in_: bool = True
    ) -> dict[str, Any]:
        return await _post("/api/v1/comment/%s" % ('like' if in_ else 'unlike'), {
            "threadId": self.thread_id,
            "commentId": self.id
        })

    async def delete(
        self, 
    ) -> dict[str, Any]:
        return await _post("/api/resource/comments/delete", {
            "threadId": self.thread_id,
            "commentId": self.id
        })


class Music163Comment(CommentObject):

    def __init__(
        self,
        data: dict[str, Any]
    ) -> None:
        super().__init__(data)
        self.data_type: Optional[str] = None
        self.id: Optional[int] = None
        self.thread_id: Optional[str] = None

    async def comments(
        self, 
        hot: bool = True, 
        page: int = 0, 
        limit: int = 20, 
        before_time: int = 0
    ) -> Union[tuple[int, Generator["CommentItemObject", None, None]], dict[str, Any]]:
        api = "/api/v1/resource/hotcomments" if hot else "/api/v1/resource/comments"

        data = await _post("%s/%s%s" % (api, self.data_type, self.id), {
            "rid": self.id, 
            "limit": limit, 
            "offset": limit * page, 
            "beforeTime": before_time
        })

        if data["code"] != 200:
            return data

        if self.thread_id is None:
            self.thread_id = f"{self.data_type}{self.id}"

        comment_data_list = data["hotComments"] if hot else data["comments"]
        return data["total"], (Music163CommentItem(
            dict({"threadId": self.thread_id}, **comment_data)
        ) for comment_data in comment_data_list)

    async def comment_send(
        self, 
        content: str
    ) -> dict[str, Any]:
        return await _post("/api/resource/comments/add", {
            "threadId": self.thread_id,
            "content": content
        })


class _Music(DataObject, Music163Comment):

    def __init__(
        self, 
        music_data: dict[str, Any]
    ) -> None:
        super().__init__(music_data)
        self.quality: dict = {}
        self.mv_id = 0
        self.album_data: dict[str, Any] = {}
    
    async def subscribe(
        self, 
        in_: bool = True
    ) -> dict[str, Any]:
        raise TypeError("无法直接收藏 该对象不支持收藏")

    async def similar(self) -> dict[str, Any]:
        return await _post("/api/v1/discovery/simiSong", {
            "songid": self.id,
            "limit": 50, 
            "offset": 0
        })
    
    async def similar_playlist(
        self, 
        page: int = 0, 
        limit: int = 50
    ) -> Union[Generator["PlayList", None, None], dict[str, Any]]:
        """该 music 对象的相似歌单"""
        data = await _post("/api/discovery/simiPlaylist", {
            "songid": self.id, 
            "limit": limit, 
            "offset": limit * page,
        })

        if data["code"] != 200:
            return data
            
        return (PlayList(playlist_data) for playlist_data in data['playlists'])

    async def similar_user(
        self, 
        page: int = 0, 
        limit: int = 50
    ) -> Union[Generator["User", None, None], dict[str, Any]]:
        """最近5个听了这 music 对象的用户"""
        data = await _post("/api/discovery/simiUser", {
            "songid": self.id, 
            "limit": limit, 
            "offset": limit * page,
        })

        if data["code"] != 200:
            return data
            
        return (User(user_data) for user_data in data['userprofiles'])

    async def like(
        self, 
        like: bool = True
    ) -> dict[str, Any]:
        """红心该 music 对象与取消红心"""
        return await _post("/api/radio/like", {
            "alg": 'itembased', 
            "trackId": self.id, 
            "like": like, 
            "time": '3'
        })

    async def lyric(self) -> dict[str, Any]:
        """该 music 对象的歌词"""
        return await _post("/api/song/lyric", {
            "id": self.id, 
            "lv": -1, 
            "kv": -1, 
            "tv": -1,
        })

    async def _play_url(
        self, 
        br: Union[int, str] = 999000
    ) -> dict[str, Any]:
        """获取播放该 music 对象指定的歌曲文件 url"""
        return await _post_url("https://interface3.music.163.com/api/song/enhance/player/url", {
            "ids": f'[{self.id}]',
            "br": br
        })

    async def _download_url(
        self, 
        br: Union[int, str] = 999000
    ) -> dict[str, Any]:
        """获取该 music 对象指定的歌曲 url, 错误码 -105 需要会员"""
        return await _post("/api/song/enhance/download/url", {
            "id": self.id,
            "br": br
        })

    async def play(
        self, 
        br: Union[int, str] = 999000,
        download_path: str = None
    ) -> Union[str, dict[str, Any]]:
        """获取播放该 music 对象指定的歌曲文件"""
        data = await self._play_url(br)
        if data["code"] != 200:
            return data

        return await _download(data["data"][0]["url"], f"{self.id}.mp3", download_path)
    
    async def download(
        self, 
        br: Union[int, str] = 999000,
        download_path: str = None
    ) -> Union[str, dict[str, Any]]:
        """获取下载该 music 对象指定的歌曲文件"""
        data = await self._download_url(br)
        if data["code"] != 200 or data["data"]["code"] == -105:
            return data

        return await _download(data["data"]["url"], f"{self.id}.mp3", download_path)

    async def album(self) -> Union["Album", dict[str, Any]]:
        """实例化该对像专辑 album 对像并返回 album 对像"""
        from pycloudmusic.music163 import Music163Api
        
        return await Music163Api().album(self.album_data["id"])

    async def mv(self) -> Union["Mv", dict[str, Any]]:
        """获取该对像 mv 实例化 mv 对像并返回 mv 对像"""
        from pycloudmusic.music163 import Music163Api

        return await Music163Api().mv(self.mv_id)


class Music(_Music):

    def __init__(
        self,  
        music_data: dict[str, Any]
    ) -> None:
        super().__init__(music_data)
        # 资源类型
        self.data_type = DATA_TYPE[0]
        # 歌曲id
        self.id = music_data['id']
        # 标题列表 [大标题, 副标题]
        self.name = [music_data["name"], " ".join(music_data["alia"])]
        self.name_str = f"{self.name[0]} {self.name[1]}"
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
        self.quality = {
            "h": music_data["h"],
            "m": music_data["m"],
            "l": music_data["l"],
            "sq": music_data["sq"],
            "hr": music_data["hr"],
        }
        # mv id
        self.mv_id = music_data["mv"]
        # 发表时间
        if "publishTime" in music_data:
            self.publish_time = music_data["publishTime"]
        else:
            self.publish_time = None
        # 推荐理由
        self.reason = music_data["reason"] if "reason" in music_data else None


class PersonalizedMusic(_Music):

    def __init__(
        self, 
        music_data: dict[str, Any]
    ) -> None:
        super().__init__(music_data)
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


class _PlayList(DataListObject, Music163Comment):

    def __init__(
        self, 
        playlist_data: dict[str, Any]
    ) -> None:
        super().__init__(playlist_data)
        self.music_list = []

    def __next__(self) -> Music:
        return Music(super().__next__())

    async def subscribe(
        self, 
        in_: bool = True
    ) -> dict[str, Any]:
        return await _post("/api/playlist%s" % ('/subscribe' if in_ else '/unsubscribe'), {
            "id": self.id
        })
    
    async def similar(self) -> Any:
        raise TypeError("无法直接获取相似 请通过歌曲/该对象不支持获取相似")

    async def subscribers(
        self, 
        page: int=0, 
        limit: int=20
    ) -> Union[Generator["User", None, None], dict[str, Any]]:
        """
        查看歌单收藏者
        """
        data = await _post("/api/playlist/subscribers", {
            "id": self.id, "limit": limit, "offset": page * limit
        })

        if data["code"] != 200:
            return data

        return (User(user_data) for user_data in data['subscribers'])


class PlayList(_PlayList):

    def __init__(
        self, 
        playlist_data: dict[str, Any]
    ) -> None:
        super().__init__(playlist_data)
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

    async def add(
        self, 
        music_id: Union[str, int, list[Union[str, int]]]
    ) -> dict[str, Any]:
        """
        向对像添加歌曲
        """
        music_id = [str(music_id)] if type(music_id) != list else music_id
        return await _post("/api/playlist/manipulate/tracks", {
            "op": "add", 
            "pid": self.id, 
            "trackIds": str(music_id), 
            "imme": "true"
        })

    async def del_(
        self, 
        music_id: Union[str, int, list[Union[str, int]]]
    ) -> dict[str, Any]:
        """
        向对像删除歌曲
        """
        music_id = [str(music_id)] if type(music_id) != list else music_id
        return await _post("/api/playlist/manipulate/tracks", {
            "op": "del", 
            "pid": self.id, 
            "trackIds": str(music_id), 
            "imme": "true"
        })


class ShortPlayList(_PlayList):

    def __init__(
        self, 
        playlist_data: dict[str, Any]
    ) -> None:
        super().__init__(playlist_data)
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
    
    def __next__(self) -> NoReturn:
        raise TypeError("ShortPlayList 并非一个完整的 PlayList , 请用 ShortPlayList 的歌单 id 请求一个完整的 PlayList 实例, 来得到歌单曲目")


class ShorterPlayList(_PlayList):

    def __init__(
        self, 
        playlist_data: dict[str, Any]
    ) -> None:
        super().__init__(playlist_data)
        # 资源类型
        self.data_type = DATA_TYPE[2]
        # 歌单id
        self.id = playlist_data["id"]
        # 歌单标题
        self.name = playlist_data["name"]
        # 歌单封面
        self.cover = playlist_data['picUrl']
        self.track_count = playlist_data["trackCount"]
        # 推荐理由
        self.reason = playlist_data["copywriter"] if "copywriter" in playlist_data else None

    def __next__(self) -> NoReturn:
        raise TypeError("ShorterPlayList 并非一个完整的 PlayList , 请用 ShorterPlayList 的歌单 id 请求一个完整的 PlayList 实例, 来得到歌单曲目")


class User(Api):

    def __init__(
        self, 
        user_data: dict[str, Any]
    ) -> None:
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
            if type(data) == dict:
                return data
            self.like_playlist_id = next(data).id
        return self.like_playlist_id

    async def playlist(
        self, 
        page: int = 0, 
        limit: int = 30
    ) -> Union[Generator[PlayList, None, None], dict[str, Any]]:
        """获取该对象的歌单"""
        data = await _post("/api/user/playlist", {
            "uid": self.id, 
            "limit": limit, 
            "offset": limit * page, 
            "includeVideo": True
        })

        if data["code"] != 200:
            return data["code"]
        
        return (PlayList(playlist_data) for playlist_data in data['playlist'])

    async def like_music(self) -> Union[PlayList, dict[str, Any]]:
        """获取该对象喜欢的歌曲"""
        from pycloudmusic.music163 import Music163Api

        like_playlist_id = await self._get_like_playlist_id()
        return await Music163Api().playlist(like_playlist_id)

    async def record(
        self, 
        type_: bool = True
    ) -> Union[Generator[Music, None, None], dict[str, Any]]:
        """获取该对象听歌榜单"""
        data = await _post("/api/v1/play/record", {
            "uid": self.id, "type": 0 if type_ else 1
        })

        if data['code'] != 200:
            return data

        return (Music(music_data) for music_data in (data["allData"] if type_ else data["weekData"]))

    async def follow(
        self, 
        follow_in: bool=True
    ) -> dict[str, Any]:
        """关注用户"""
        follow_in_ = "follow" if follow_in else "delfollow"
        return await _post(f"/api/user/{follow_in_}/{self.id}")


class _Album(DataListObject, Music163Comment):

    def __init__(
        self, 
        album_data: dict[str, Any]
    ) -> None:
        super().__init__(album_data)
        self.data_type = DATA_TYPE[3]
        # 专辑id
        self.id = 0

    def __next__(self) -> Music:
        return Music(super().__next__())

    async def subscribe(
        self, 
        in_: bool = True
    ) -> dict[str, Any]:
        return await _post("/api/album/%s" % ("sub" if in_ else "unsub"), {
            "id": self.id
        })
    
    async def similar(self) -> Any:
        raise TypeError("无法直接获取相似 请通过歌曲/该对象不支持获取相似")

class Album(_Album):

    def __init__(
        self, 
        album_data: dict[str, Any]
    ) -> None:
        super().__init__(album_data)
        # 专辑id
        self.id = album_data["album"]["id"]
        # 专辑标题
        self.name = album_data["album"]["name"]
        # 专辑类型
        self.sub_type = album_data["album"]["subType"]
        # 专辑别名
        self.alias = album_data["album"]["alias"]
        self.alias_str = "/".join(self.alias)
        # 专辑主作者
        self.artist = album_data["album"]["artist"]
        # 专辑所有作者
        self.artists = album_data["album"]["artists"]
        self.artists_str = "/".join([artists_data["name"] for artists_data in self.artists])
        # 专辑曲目数
        self.size = album_data["album"]["size"]
        # 专辑简介
        self.description = album_data["album"]["description"]
        # 未知
        self.liked = album_data["album"]["info"]["liked"]
        # 专辑评论数
        self.comment_count = album_data["album"]["info"]["commentCount"]
        # 专辑分享数
        self.share_count = album_data["album"]["info"]["shareCount"]
        # 未知
        self.liked_count = album_data["album"]["info"]["likedCount"]
        # 专辑封面
        self.cover = album_data["album"]['picUrl']
        self.music_list = album_data["songs"]


class ShortAlbum(_Album):

    def __init__(
        self, 
        album_data: dict[str, Any]
    ) -> None:
        super().__init__(album_data)
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

    def __next__(self) -> NoReturn:
        raise TypeError("ShortAlbum 并非一个完整的 Album , 请用 ShortAlbum 的专辑 id 请求一个完整的 Album 实例, 来得到专辑曲目")


class _Mv(DataObject, Music163Comment):

    def __init__(
        self, 
        mv_data: dict[str, Any]
    ) -> None:
        super().__init__( mv_data)
        self.data_type = DATA_TYPE[1]
        self.id = 0

    async def _play_url(
        self, 
        quality: Union[str, int] = 1080
    ) -> dict[str, Any]:
        """获取播放该 mv 对象指定的视频 url"""
        return await _post("/api/song/enhance/play/mv/url", {
            "id": self.id, "r": quality
        })

    async def play(
        self, 
        download_path: Optional[str] = None, 
        quality: Union[str, int] = 1080
    ) -> Union[str, dict[str, Any]]:
        """获取播放该 mv 对象指定的视频文件"""
        data = await self._play_url(quality)

        if data["code"] != 200:
            return data

        return await _download(data["data"]["url"], f"{self.id}.mp4", download_path)

    async def subscribe(
        self, 
        in_: bool = True
    ) -> dict[str, Any]:
        return await _post("/api/mv/%s" % ("sub" if in_ else "unsub"), {
            "mvId": self.id,
            "mvIds": '["' + str(self.id) + '"]',
        })
    
    async def similar(self) -> Any:
        return await _post("/api/discovery/simiMV", {
            "mvid": self.id
        })


class Mv(_Mv):

    def __init__(
        self, 
        mv_data: dict[str, Any]
    ) -> None:
        super().__init__(mv_data)
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


class ShortMv(_Mv):

    def __init__(
        self, 
        mv_data: dict[str, Any]
    ) -> None:
        super().__init__(mv_data)
        # mv id
        self.id = mv_data["vid"]
        # mv标题
        self.name = mv_data["title"]
        # mv歌手
        self.artists = mv_data["creator"]
        self.artists_str = "/".join([artists['userName'] for artists in self.artists])
        # mv封面
        self.cover = mv_data["coverUrl"]


class _Artist(DataObject):

    def __init__(
        self, 
        artist_data: dict[str, Any]
    ) -> None:
        super().__init__(artist_data)
        self.data_type = "artist"
        self.id = 0

    async def song(
        self, 
        hot: bool = True, 
        page: int = 0, 
        limit: int = 100
    ) -> Union[Generator[Music, None, None], dict[str, Any]]:
        """获取该对像歌曲"""
        data = await _post("/api/v1/artist/songs", {
            "id": self.id,
            "order": 'hot' if hot else "time",
            "offset": limit * page,
            "limit": limit,
            "private_cloud": True,
            "work_type": 1
        })
        
        if data["code"] != 200:
            return data

        return (Music(music_data) for music_data in data['songs'])

    async def song_top(self) -> Union[Generator[Music, None, None], dict[str, Any]]:
        """获取该对像热门50首"""
        data = await _post("/api/artist/top/song", {
            "id": self.id
        })

        if data["code"] != 200:
            return data

        return (Music(music_data) for music_data in data['songs'])

    async def album(
        self, 
        page: int = 0,
        limit: int = 30
    ) -> Union[Generator[Album, None, None], dict[str, Any]]:
        """获取该对像专辑"""
        data = await _post("/api/artist/albums/%s" % self.id, {
            "limit": limit, "offset": limit * page, "total": True,
        })

        if data["code"] != 200:
            return data

        return (Album(album_data) for album_data in data["hotAlbums"])
    
    async def subscribe(
        self, 
        in_: bool = True
    ) -> dict[str, Any]:
        return await _post("/api/artist/%s" % ("sub" if in_ else "unsub"), {
            "artistId": self.id,
            "artistIds": f'["{self.id}"]'
        })
    
    async def similar(self) -> Any:
        return await _post("/api/discovery/simiArtist", {
            "artistid": self.id
        })

class Artist(_Artist):

    def __init__(
        self, 
        artist_data: dict[str, Any]
    ) -> None:
        super().__init__(artist_data)
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
        self.mv_size = artist_data.get("mvSize")
        # 头像
        self.cover = artist_data["cover"] if "cover" in artist_data else artist_data["picUrl"]


class ShortArtist(_Artist):

    def __init__(
        self, 
        artist_data: dict[str, Any]
    ) -> None:
        super().__init__(artist_data)
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
        self.mv_size = artist_data.get("mvSize")
        # 头像
        self.cover = artist_data["picUrl"]

class DjMusic(Music163Comment):

    def __init__(
        self, 
        dj_music_data: dict[str, Any]
    ) -> None:
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


class _Dj(DataListObject):

    def __init__(
        self, 
        dj_data: dict[str, Any]
    ) -> None:
        super().__init__(dj_data)
        self.data_type = DATA_TYPE[4]
        self.id = 0

    def __next__(self) -> DjMusic:
        return DjMusic(super().__next__())
    
    async def read(
        self, 
        page: int = 0, 
        limit: int= 30, 
        asc: bool = False
    ) -> dict[str, Any]:
        """获取电台节目"""
        data = await _post("/api/dj/program/byradio", {
            "radioId": self.id, "limit": limit, "offset": limit * page, "asc": asc
        })

        if data["code"] != 200:
            return data

        self.music_list = data["programs"]
        return data
    
    async def subscribe(
        self, 
        in_: bool = True
    ) -> dict[str, Any]:
        return await _post("/api/djradio/%s" % ("sub" if in_ else "unsub"), {
            "id": self.id
        })

    async def similar(self) -> Any:
        raise TypeError("无法直接获取相似 请通过歌曲/该对象不支持获取相似")

class Dj(_Dj):

    def __init__(
        self, 
        dj_data: dict[str, Any]
    ) -> None:
        super().__init__(dj_data)
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
        self.subed = dj_data["subed"] if "subed" in  dj_data else None
        # 最后上传电台节目 id
        self.last_music_id = dj_data["lastProgramId"]
        # 最后上传电台节目时间
        self.last_music_create_time = dj_data["lastProgramCreateTime"]


class ShortDj(_Dj):

    def __init__(
        self, 
        dj_data: dict[str, Any]
    ) -> None:
        super().__init__(dj_data)
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


class PersonalizedDj(_Dj):

    def __init__(
        self, 
        dj_data: dict[str, Any]
    ) -> None:
        super().__init__(dj_data)
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


class Fm(Api, ListObject):

    def __init__(
        self, 
        fm_data: dict[str, Any] = {}
    ) -> None:
        super().__init__(fm_data)

    def __next__(self) -> PersonalizedMusic:
        return PersonalizedMusic(super().__next__())

    async def read(self) -> dict[str, Any]:
        """获取fm歌曲"""
        data = await _post("/api/v1/radio/get")

        if data["code"] != 200:
            return data

        self.music_list = data["data"]
        return data

    async def write(
        self, 
        id_: Union[int, str]
    ) -> dict[str, Any]:
        """将歌曲扔进垃圾桶 (优化推荐)"""
        return await _post("/api/radio/trash/add?alg=RT&songId=%s&time=%s" % (id_, int(time.time())), {
            "songId": id_
        })


class Message(Api):

    def __init__(
        self, 
        user_id: Union[str, int]
    ) -> None:
        self.id = user_id

    async def comments(
        self, 
        before_time: int = -1, 
        limit: int = 30
    ) -> dict[str, Any]:
        """获取评论"""
        return await _post(f"/api/v1/user/comments/{self.id}", {
            "beforeTime": before_time, 
            "limit": limit, 
            "total": 'true', 
            "uid": self.id
        })

    async def forwards(
        self, 
        page: int = 0, 
        limit: int = 30
    ) -> dict[str, Any]:
        """获取@我"""
        return await _post("/api/forwards/get", {
            "offset": limit * page, 
            "limit": limit, 
            "total": 'true'
        })

    async def notices(
        self, 
        last_time: int = -1, 
        limit: int = 30
    ) -> dict[str, Any]:
        """获取通知"""
        return await _post("/api/msg/notices", {
            "limit": limit, 
            "time": last_time
        })

    async def private_new(self) -> dict[str, Any]:
        """获取最接近联系人"""
        return await _post("/api/msg/recentcontact/get")

    async def private_history(
        self, 
        id_: Union[str, int], 
        page: int = 0, 
        limit: int = 30
    ) -> dict[str, Any]:
        """获取指定用户历史私信"""
        return await _post("/api/msg/private/history", {
            "userId": id_, 
            "offset": limit * page, 
            "limit": limit, 
            "total": 'true'
        })

    async def private(
        self, 
        page: int = 0, 
        limit: int = 30
    ) -> dict[str, Any]:
        """获取私信列表"""
        return await _post("/api/msg/private/users", {
            "offset": limit * page, 
            "limit": limit, 
            "total": 'true'
        })

    def __set_to_user_id_str(
        self, 
        to_user_id: Union[int, str, list[Union[int, str]]]
    ) -> str:
        if type(to_user_id) != list:
            return str(to_user_id)

        return "[%s]" % ','.join([str(user_id) for user_id in to_user_id])

    async def send(
        self, 
        msg: str, 
        to_user_id: Union[int, str, list[Union[int, str]]]
    ) -> dict[str, Any]:
        """发送私信"""
        return await _post("/api/msg/private/send", {
            "msg": msg, 
            "type": "text", 
            "userIds": self.__set_to_user_id_str(to_user_id)
        })

    async def send_music(
        self, 
        msg: str, 
        to_user_id: Union[int, str, list[Union[int, str]]],
        id_: Union[int, str]
    ) -> dict[str, Any]:
        """发送私信 带歌曲 id_:歌曲 id"""
        return await _post("/api/msg/private/send", {
            "msg": msg, 
            "type": "song", 
            "userIds": self.__set_to_user_id_str(to_user_id),
            "id": id_
        })

    async def send_album(
        self, 
        msg: str, 
        to_user_id: Union[int, str, list[Union[int, str]]],
        id_: Union[int, str]
    ) -> dict[str, Any]:
        """发送私信 带专辑 id_:专辑 id"""
        return await _post("/api/msg/private/send", {
            "msg": msg, 
            "type": "album", 
            "userIds": self.__set_to_user_id_str(to_user_id),
            "id": id_
        })

    async def send_playlist(
        self, 
        msg: str, 
        to_user_id: Union[int, str, list[Union[int, str]]],
        id_: Union[int, str]
    ) -> dict[str, Any]:
        """发送私信 带歌单 不能发送重复的歌单 id_:歌单 id"""
        return await _post("/api/msg/private/send", {
            "msg": msg, 
            "type": "playlist", 
            "userIds": self.__set_to_user_id_str(to_user_id),
            "id": id_
        })


class EventItem(Music163Comment):

    def __init__(
        self, 
        event_data: dict[str, Any]
    ) -> None:
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
        self.type_str = EVENT_TYPE[self.type] if self.type in EVENT_TYPE else None
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

    async def forward(
        self, 
        msg: str
    ) -> dict[str, Any]:
        """指定动态转发到 cookie 用户"""
        return await _post("/api/event/forward", {
            "forwards": msg, 
            "id": self.id, 
            "eventUserId": self.user["userId"]
        })


class Event(Api, ListObject):

    def __init__(
        self, 
        even_data: dict[str, Any] = {}
    ) -> None:
        super().__init__(even_data)

    def __next__(self) -> EventItem:
        return EventItem(super().__next__())

    async def read(
        self, 
        last_time: Union[str, int] = -1, 
        limit: int = 30
    ) -> dict[str, Any]:
        """获取下一页动态"""
        data = await _post("/api/v1/event/get", {
            "pagesize": limit, 
            "lasttime": last_time
        })

        if data["code"] != 200:
            return data

        self.music_list = data['event']
        return data

    async def read_user(
        self, 
        user_id: Union[str, int], 
        last_time: Union[str, int] = -1, 
        limit: int = 30
    ) -> dict[str, Any]:
        """获取指定用户动态"""
        data = await _post(f"/api/event/get/{user_id}", {
            "limit": limit, 
            "time": last_time, 
            "getcounts": "true", 
            "total": "true"
        })

        if data["code"] != 200:
            return data

        self.music_list = data['events']
        return data

    async def del_(
        self, 
        id_: Union[str, int]
    ) -> dict[str, Any]:
        """删除 cookie 用户动态"""
        return await _post("/api/event/delete", {
            "id": id_
        })

    async def send(
        self,
        msg: str
    ) -> dict[str, Any]:
        """使用 cookie 用户发送动态"""
        return await _post("/api/share/friends/resource", {
            "msg": msg, 
            "id": "", 
            "type": "noresource"
        })

    async def send_music(
        self,
        msg: str,
        id_: Union[str, int]
    ) -> dict[str, Any]:
        """使用 cookie 用户发送动态 带歌曲 id_:歌曲 id"""
        return await _post("/api/share/friends/resource", {
            "msg": msg, 
            "id": id_, 
            "type": "song"
        })

    async def send_playlist(
        self,
        msg: str,
        id_: Union[str, int]
    ) -> dict[str, Any]:
        """使用 cookie 用户发送动态 带歌单 id_:歌单 id"""
        return await _post("/api/share/friends/resource", {
            "msg": msg, 
            "id": id_, 
            "type": "playlist"
        })

    async def send_mv(
        self,
        msg: str,
        id_: Union[str, int]
    ) -> dict[str, Any]:
        """使用 cookie 用户发送动态 带 mv id_:mv id"""
        return await _post("/api/share/friends/resource", {
            "msg": msg, 
            "id": id_, 
            "type": "mv"
        })

    async def send_dj(
        self,
        msg: str,
        id_: Union[str, int]
    ) -> dict[str, Any]:
        """使用 cookie 用户发送动态 带电台 id_:电台 id"""
        return await _post("/api/share/friends/resource", {
            "msg": msg, 
            "id": id_, 
            "type": "djprogram"
        })

    async def send_dj_music(
        self,
        msg: str,
        id_: Union[str, int]
    ) -> dict[str, Any]:
        """使用 cookie 用户发送动态 带电台节目 id_:电台节目 id"""
        return await _post("/api/share/friends/resource", {
            "msg": msg, 
            "id": id_, 
            "type": "djradio"
        })


class CloudMusic(Api):

    def __init__(
        self,
        cloud_music_data: dict[str, Any]
    ) -> None:
        # 云盘歌曲id
        self.id = cloud_music_data["simpleSong"]["id"]
        # 标题
        self.name = cloud_music_data["songName"]
        # 歌曲大小
        self.file_size = cloud_music_data["fileSize"]
        # 歌曲文件名
        self.file_name = cloud_music_data["fileName"]
        # 歌手
        self.artist = cloud_music_data["artist"]
        # 专辑
        self.album = cloud_music_data["album"]
        # 封面
        self.cover = cloud_music_data["simpleSong"]['al']["picUrl"]
        # 上传时间
        self.add_time = cloud_music_data["addTime"]


class Cloud(Api, ListObject):

    def __init__(self, cloud_data):
        # 云盘歌曲数
        self.cloud_count = cloud_data["count"]
        # 云盘最大容量
        self.max_size = cloud_data["maxSize"]
        # 云盘已用容量
        self.size = cloud_data["size"]
        # 云盘当时页歌曲数据
        self.music_list = cloud_data["data"]

    def __next__(self) -> CloudMusic:
        return CloudMusic(super().__next__())


class My(User):

    def __init__(
        self, 
        user_data: dict[str, Any]
    ) -> None:
        super().__init__(user_data)
        # 登录ip
        self.login_ip = user_data["profile"]["lastLoginIP"]
        # 登录时间
        self.login_time = int(user_data["profile"]["lastLoginTime"] / 1000)
        self.login_time_str = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(self.login_time))

    async def sign(
        self, 
        type_: bool = True
    ) -> dict[str, Any]:
        """使用该对象签到"""
        return await _post("/api/point/dailyTask", {
            "type": 0 if type_ else 1
        })

    async def recommend_songs(self) -> Union[Generator[Music, None, None], dict[str, Any]]:
        """获取日推"""
        data = await _post("/api/v3/discovery/recommend/songs")
        
        if data["code"] != 200:
            return data

        return (Music(music_data) for music_data in data["data"]["dailySongs"])

    async def recommend_resource(self) -> Union[Generator[ShortPlayList, None, None], dict[str, Any]]:
        """获取每日推荐歌单"""
        data = await _post("/api/v1/discovery/recommend/resource")
        
        if data["code"] != 200:
            return data

        return (ShortPlayList(playlist_data) for playlist_data in data["recommend"])

    async def playmode_intelligence(
        self, 
        music_id: Union[str, int], 
        sid: Optional[Union[str, int]] = None, 
        playlist_id: Optional[Union[str, int]] = None
    ) -> Union[Generator[Music, None, None], dict[str, Any]]:
        """心动模式/智能播放"""
        if playlist_id is None:
            playlist_id = await self._get_like_playlist_id()

        data = await _post("/api/playmode/intelligence/list", {
            "songId": music_id,
            "playlistId": playlist_id,
            "type": "fromPlayOne",
            "startMusicId": sid if sid is not None else music_id,
            "count": 1,
        })

        if data["code"] != 200:
            return data

        return (Music(music_data["songInfo"]) for music_data in data["data"])
    
    async def sublist_artist(
        self, 
        page: int = 0, 
        limit: int = 25
    ) -> Union[tuple[int, Generator[ShortArtist, None, None]], dict[str, Any]]:
        """查看 cookie 用户收藏的歌手"""
        data = await _post("/api/artist/sublist", {
            "limit": limit, 
            "offset": page * limit, 
            "total": "true"
        })

        if data["code"] != 200:
            return data

        return data["count"], (ShortArtist(artist_data) for artist_data in data["data"])

    async def sublist_album(
        self, 
        page: int = 0, 
        limit: int = 25
    ) -> Union[tuple[int, Generator[ShortAlbum, None, None]], dict[str, Any]]:
        """查看 cookie 用户收藏的专辑"""
        data = await _post("/api/album/sublist", {
            "limit": limit, 
            "offset": page * limit, 
            "total": "true"
        })

        if data["code"] != 200:
            return data

        return data["count"], (ShortAlbum(album_data) for album_data in data["data"])

    async def sublist_dj(
        self, 
        page: int = 0, 
        limit: int = 25
    ) -> Union[tuple[int, Generator[ShortDj, None, None]], dict[str, Any]]:
        """查看 cookie 用户收藏的电台"""
        data = await _post("/api/djradio/get/subed", {
            "limit": limit, 
            "offset": page * limit, 
            "total": "true"
        })

        if data["code"] != 200:
            return data

        return data["count"], (ShortDj(dj_data) for dj_data in data["djRadios"])
    
    async def sublist_mv(
        self, 
        page: int = 0, 
        limit: int = 25
    ) -> Union[tuple[int, Generator[ShortMv, None, None]], dict[str, Any]]:
        """查看 cookie 用户收藏的 MV"""
        data = await _post("/api/cloudvideo/allvideo/sublist", {
            "limit": limit, 
            "offset": page * limit, 
            "total": "true"
        })

        if data["code"] != 200:
            return data

        return data["count"], (ShortMv(mv_data) for mv_data in data["data"])
    
    async def sublist_topic(
        self, 
        page: int = 0, 
        limit: int = 50
    ) -> dict[str, Any]:
        """查看 cookie 用户收藏的专题"""
        data = await _post("/api/topic/sublist", {
            "limit": limit, 
            "offset": page * limit, 
            "total": "true"
        })

        if data["code"] != 200:
            return data

        return data

    def fm(self) -> Fm:
        """私人 fm 实例化一个 fm 对象并返回"""
        return Fm()

    def message(self) -> Message:
        """私信 实例化一个 message 对象并返回"""
        return Message(self.id)

    def event(self) -> Event:
        """动态 实例化一个 event 对象并返回"""
        return Event()

    async def cloud(
        self, 
        page: int = 0, 
        limit: int = 30
    ) -> Union[Cloud, dict[str, Any]]:
        """获取云盘数据并实例化一个 cloud 对象返回"""
        data = await _post("/api/v1/cloud/get", {
            'limit': limit, 'offset': page * limit
        })

        if data["code"] != 200:
            return data

        return Cloud(data)