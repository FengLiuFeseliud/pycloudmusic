import os
from typing import Any, Optional
import aiofiles, aiohttp
from pycloudmusic import CHUNK_SIZE, DOWNLOAD_PATH, LIMIT, RECONNECTION


# music163通用请求头
MUSIC_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://music.163.com',
    'Host': 'music.163.com',
    'cookie': "appver=2.7.1.198277; os=pc;",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

__session = None

async def get_session():
    global __session
    if __session is None:
        conn = aiohttp.TCPConnector(limit=LIMIT)
        __session = aiohttp.ClientSession(connector=conn)
    
    return __session

class CannotConnectApi(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Http:

    def __init__(self, headers: Optional[dict[str, str]]=None) -> None:
        self._headers = headers if not headers is None else MUSIC_HEADERS
    
    async def _post(self, url: str, data: dict[str, Any], reconnection_count: int=0) -> dict[str, Any]:
        try:
            session = await get_session()
            async with session.post(f"https://music.163.com{url}", headers=self._headers, data=data) as req:
                return await req.json(content_type=None)
        except Exception as err:
            reconnection_count =+ 1
            if reconnection_count > RECONNECTION:
                raise CannotConnectApi(f"超出重连次数 {RECONNECTION} 无法请求到 {url} err: {err}")

            return await self._post(url, data, reconnection_count)

    async def _download(self, url: str, file_name: str, file_path: Optional[str]=None, reconnection_count: int=0) -> str:
        if file_path is None:
            file_path = DOWNLOAD_PATH
        
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        
        try:
            session = await get_session()
            async with session.get(url, headers=self._headers) as req:
                file_path_ = os.path.join(file_path, file_name)
                async with aiofiles.open(file_path_, "wb") as file_:
                    async for chunk in req.content.iter_chunked(CHUNK_SIZE):
                        await file_.write(chunk)
                    
                return file_path_

        except Exception as err:
            reconnection_count += 1
            if reconnection_count > RECONNECTION:
                raise CannotConnectApi(f"超出重连次数 {RECONNECTION} 无法请求到 {url} err: {err}")

            return await self._download(url, file_name, file_path, reconnection_count)