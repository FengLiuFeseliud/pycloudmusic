import hashlib
import asyncio
from http.cookies import SimpleCookie
from typing import Any, Generator, Optional, Union
from pycloudmusic import RECONNECTION, _id_format
from pycloudmusic.ahttp import CannotConnectApi, _get_headers, _get_session, _post, _set_cookie
from pycloudmusic.baseclass import Api
from pycloudmusic.object.music163 import *


class Music163Api:

    def __init__(
        self, 
        cookies: Optional[str] = None, 
    ) -> None:
        if not cookies is None:
            _set_cookie(cookies)

    async def my(self) -> Union[My, dict[str, Any]]:
        """获取当前cookie用户信息并实例化my对像, cookie无效返回200"""
        data = await _post("/api/w/nuser/account/get")
        if data["code"] != 200 or data["profile"] is None:
            return data

        return My(data)

    async def music(
        self, 
        ids: Union[int, str, list[Union[str, int]]]
    ) -> Union[Music, Generator[Music, None, None], dict[str, Any]]:
        """获取歌曲并实例化music对像"""
        data = await _post("/api/v3/song/detail", {
            "c": _id_format(ids, dict_str=True)
        })
        if data["code"] != 200:
            return data
        
        if len(data["songs"]) == 1:
            return Music(data["songs"][0])

        return (Music(music_data) for music_data in data["songs"])

    async def user(
        self, 
        id_: Union[int, str]
    ) -> Union[User, dict[str, Any]]:
        """获取用户并实例化user对像"""
        data = await _post(f"/api/v1/user/detail/{id_}")

        if data["code"] != 200:
            return data

        return User(data)

    async def playlist(
        self, 
        id_: Union[int, str]
    ) -> Union[PlayList, dict[str, Any]]:
        """获取歌单并实例化playlist对像"""
        data = await _post("/api/v6/playlist/detail", {
            "id": id_, 
            "n": 100000
        })

        if data["code"] != 200:
            return data

        return PlayList(data['playlist'])

    async def artist(
        self, 
        id_: Union[int, str]
    ) -> Union[Artist, dict[str, Any]]:
        """获取歌手并实例化artist对像"""
        data = await _post("/api/artist/head/info/get", {
            "id": id_
        })

        if data["code"] != 200:
            return data

        return Artist(data["data"]['artist'])

    async def album(
        self, 
        id_: Union[int, str]
    ) -> Union[Album, dict[str, Any]]:
        """实例化专辑album对像"""
        data = await _post(f"/api/v1/album/{id_}")

        if data["code"] != 200:
            return data

        return Album(data)

    async def mv(
        self, 
        id_: Union[int, str]
    ) -> Union[Mv, dict[str, Any]]:
        """获取mv并实例化mv对像"""
        data = await _post("/api/v1/mv/detail", {
            "id": id_
        })

        if data["code"] != 200:
            return data

        return Mv(data["data"])

    async def dj(
        self, 
        id_: Union[int, str]
    ) -> Union[Dj, dict[str, Any]]:
        """获取电台并实例化dj对像"""
        data = await _post("/api/djradio/v2/get", {
            "id": id_
        })

        if data["code"] != 200:
            return data

        return Dj(data["data"])

    async def _search(
        self, 
        key: str, 
        type_: Union[str, int] = 1, 
        page: int = 0, 
        limit: int = 30
    ) -> dict[str, Any]:
        """
        搜索 type_: 
        1: 单曲, 10: 专辑, 100: 歌手, 1000: 歌单, 1002: 用户
        1004: MV, 1006: 歌词, 1009: 电台, 1014: 视频
        """
        return await _post("/api/cloudsearch/pc", {
            "s": key, 
            "type": type_, 
            "limit": limit, 
            "offset": limit * page, 
            "total": True
        })
    
    async def search_music(
        self, 
        key: str, 
        page: int = 0, 
        limit: int = 30
    ) -> Union[tuple[int, Generator[Music, None, None]], dict[str, Any]]:
        """搜索单曲"""
        data = await self._search(key, "1", page, limit)

        if data["code"] != 200:
            return data

        return data["result"]["songCount"], (Music(music_data) for music_data in data["result"]['songs'])

    async def search_album(
        self, 
        key: str, 
        page: int = 0, 
        limit: int = 30
    ) -> Union[tuple[int, Generator[ShortAlbum, None, None]], dict[str, Any]]:
        """搜索专辑"""
        data = await self._search(key, "10", page, limit)
        
        if data["code"] != 200:
            return data

        return data["result"]["albumCount"], (ShortAlbum(album_data) for album_data in data["result"]['albums'])

    async def search_artist(
        self, 
        key: str, 
        page: int = 0, 
        limit: int = 30
    ) -> Union[tuple[int, Generator[ShortArtist, None, None]], dict[str, Any]]:
        """搜索歌手"""
        data = await self._search(key, "100", page, limit)

        if data["code"] != 200:
            return data

        return data["result"]["artistCount"], (ShortArtist(artist_data) for artist_data in data["result"]['artists'])

    async def search_user(
        self, 
        key: str, 
        page: int = 0, 
        limit: int = 30
    ) -> Union[tuple[int, Generator[User, None, None]], dict[str, Any]]:
        """搜索用户"""
        data = await self._search(key, "1002", page, limit)
        
        if data["code"] != 200:
            return data

        return data["result"]["userprofileCount"], (User(user_data) for user_data in data["result"]['userprofiles'])

    async def search_mv(
        self, 
        key: str, 
        page: int = 0, 
        limit: int = 30
    ) -> Union[tuple[int, Generator[Mv, None, None]], dict[str, Any]]:
        """搜索 Mv"""
        data = await self._search(key, "1004", page, limit)

        if data["code"] != 200:
            return data

        return data["result"]["mvCount"], (Mv(music_data) for music_data in data["result"]['mvs'])

    async def search_dj(
        self, 
        key: str, 
        page: int = 0, 
        limit: int = 30
    ) -> Union[tuple[int, Generator[Dj, None, None]], dict[str, Any]]:
        """搜索电台"""
        data = await self._search(key, "1009", page, limit)

        if data["code"] != 200:
            return data

        return data["result"]["djRadiosCount"], (Dj(data) for data in data["result"]["djRadios"])

    async def personalized_playlist(
        self, 
        limit: int = 30
    ) -> Union[Generator[ShorterPlayList, None, None], dict[str, Any]]:
        """推荐歌单"""
        data = await _post("/api/personalized/playlist", {
            "limit": limit, 
            "total": "true", 
            "n": 1000,
        })

        if data["code"] != 200:
            return data

        return (ShorterPlayList(playlist_data) for playlist_data in data['result'])
    
    async def personalized_new_song(
        self, 
        limit: int = 10
    ) -> Union[Generator[PersonalizedMusic, None, None], dict[str, Any]]:
        """推荐新歌"""
        data = await _post("/api/personalized/newsong", {
            "type": 'recommend', 
            "limit": limit, 
            "areaId": 0,
        })

        if data["code"] != 200:
            return data

        return (PersonalizedMusic(music_data["song"]) for music_data in data['result'])
    
    async def personalized_dj(self) -> Union[Generator[PersonalizedDj, None, None], dict[str, Any]]:
        """推荐电台"""
        data = await _post("/api/personalized/djprogram")

        if data["code"] != 200:
            return data

        return (PersonalizedDj(music_data["program"]) for music_data in data['result'])
    
    async def home_page(
        self, 
        refresh: bool = True, 
        cursor: Optional[str] = None
    ) -> dict[str, Any]:
        """首页-发现 app 主页信息"""
        return await _post("/api/homepage/block/page", {
            "refresh": refresh, 
            "cursor": cursor
        })

    async def top_artist_list(
        self, 
        type_: Union[str, int] = 1, 
        page: int = 0, 
        limit: int = 100
    ) -> Union[Generator[Artist, None, None], dict[str, Any]]:
        """歌手榜
        type_ 1: 华语, 2: 欧美, 3: 韩国, 4: 日本"""
        data = await _post("/api/toplist/artist", {
            "type": type_, 
            "limit": limit, 
            "offset": page * limit, 
            "total": "true"
        })

        if data["code"] != 200:
            return data

        return (Artist(artist_data) for artist_data in data["list"]["artists"])

    async def top_song(
        self, 
        type_: int = 0
    ) -> Union[Generator[PersonalizedMusic, None, None], dict[str, Any]]:
        """新歌速递
        全部:0 华语:7 欧美:96 日本:8 韩国:16"""
        data = await _post("/api/v1/discovery/new/songs", {
            "areaId": type_, "total": "true"
        })

        if data["code"] != 200:
            return data
            
        return (PersonalizedMusic(music_data) for music_data in data["data"])


class LoginMusic163(Api):

    def __init__(
        self, 
    ) -> None:
        # md5对象
        self.__hl = hashlib.md5()

    def _md5(
        self, 
        str_: str
    ) -> str:
        self.__hl.update(str_.encode(encoding='utf-8'))
        return self.__hl.hexdigest()
    
    def _SimpleCookieToCookieStr(
        self, 
        cookie: SimpleCookie[str]
    ) -> str:
        cookie_str = ""
        for item in dict(cookie).values():
            cookie_data = str(item).lstrip("Set-Cookie: ").split("; ", maxsplit=1)[0]
            cookie_str = f"{cookie_str}{cookie_data}; "
        
        return cookie_str

    async def _login(
        self, 
        url: str, 
        data: dict[str, Any], 
        reconnection_count: int = 0
    ) -> tuple[int, str]:
        try:
            session = await _get_session()
            async with session.post(f"https://music.163.com{url}", headers=_get_headers(), data=data) as req:
                cookies = self._SimpleCookieToCookieStr(req.cookies)
                return (await req.json(content_type=None))["code"], cookies
        except Exception as err:
            reconnection_count =+ 1
            if reconnection_count > RECONNECTION:
                raise CannotConnectApi(f"超出重连次数 {RECONNECTION} 无法请求到 {url} err: {err}")

            return await self._login(url, data, reconnection_count)
    
    async def email(
        self, 
        email: str, 
        password: str
    ) -> tuple[int, str, Music163Api]:
        """
        邮箱登录
        错误码:501 未注册 502 密码错误
        """
        code, cookies = await self._login("/api/login", {
            "username": email,
            "password": self._md5(password),
            "rememberLogin": 'true'
        })

        return code, cookies, Music163Api(cookies)

    async def send_captcha(
        self, 
        phone: Union[str, int], 
        country_code: Union[str, int] = "86"
    ) -> dict[str, Any]:
        """
        发送验证码
        """
        return await _post("/api/sms/captcha/sent", {
            "ctcode": country_code,
            "cellphone": phone
        })

    async def cellphone(
        self, 
        phone: Union[str, int], 
        password: Union[str, int], 
        captcha: bool = False, 
        country_code: Union[str, int] = "86"
    ) -> tuple[int, str, Music163Api]:
        """
        手机/验证码 登录
        错误码:400 手机号格式错误 501 未注册 502 密码错误 503 验证码错误
        """
        if not captcha:
            password = self._md5(str(password))

        code, cookies = await self._login("/api/login/cellphone", {
            "phone": phone,
            "countrycode": country_code,
            "captcha" if captcha else "password": password,
            "rememberLogin": 'true'
        })

        return code, cookies, Music163Api(cookies)

    async def qr_key(self) -> Union[tuple[str, str], dict[str, Any]]:
        """
        获取二维码key
        """
        data = await _post("/api/login/qrcode/unikey", {
            "type": 1
        })
        
        if data["code"] != 200:
            return data

        return data["unikey"], "https://music.163.com/login?codekey=%s" % data["unikey"]

    async def qr_check(
        self, 
        qr_key: str
    ) -> tuple[int, str]:
        """
        查询二维码状态
        状态码:801 等待扫码 802 授权中 800 二维码不存在或已过期 803 登录成功
        """
        return await self._login("/api/login/qrcode/client/login", {
            'key': qr_key,
            'type': 1
        })

    async def qr(
        self, 
        qr_key: str, 
        time_sleep: int = 3
    ) -> tuple[int, str, Music163Api]:
        """
        二维码登录
        """
        while True:
            code, cookie = await self.qr_check(qr_key)

            if code in [801, 802]:
                await asyncio.sleep(time_sleep)
                continue

            if code == 800:
                return code, cookie, Music163Api(cookie)
            
            return code, cookie, Music163Api(cookie)
    
    async def logout(self) -> dict[str, Any]:
        """
        退出登录
        """
        return await _post("/api/logout")