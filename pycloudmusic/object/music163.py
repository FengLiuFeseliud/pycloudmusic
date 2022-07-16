import time
from typing import Optional, Union, Any
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


class Music(DataObject, Music163Comment):

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

    async def subscribe(self, in_: bool = True) -> dict[str, Any]:
        raise TypeError("无法直接收藏 该对象不支持收藏")

    async def similar(self) -> Any:
        return await self._post("/api/v1/discovery/simiSong", {
            "songid": self.id,
            "limit": 50, 
            "offset": 0
        })


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


class My(User):

    def __init__(self, headers: Optional[dict[str, str]], user_data: dict[str, Any]) -> None:
        super().__init__(headers, user_data)
        # 登录ip
        self.login_ip = user_data["profile"]["lastLoginIP"]
        # 登录时间
        self.login_time = int(user_data["profile"]["lastLoginTime"] / 1000)
        self.login_time_str = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(self.login_time))