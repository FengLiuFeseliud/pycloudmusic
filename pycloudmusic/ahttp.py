import os
from typing import Any, Optional
import aiofiles, aiohttp
from pycloudmusic import MUSIC_HEADERS


__session = None
__headers = MUSIC_HEADERS


class CannotConnectApi(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def _set_cookie(cookie: str):
    global __headers
    __headers["cookie"] = f"appver=2.7.1.198277; os=pc; {cookie}"


def _get_headers():
    global __headers
    return __headers


async def _get_session():
    from pycloudmusic import LIMIT

    global __session
    if __session is None:
        conn = aiohttp.TCPConnector(limit=LIMIT)
        __session = aiohttp.ClientSession(connector=conn)
    
    return __session


async def _post_url(
    url: str, 
    data: Optional[dict[str, Any]] = None, 
    reconnection_count: int=0
) -> dict[str, Any]:
    """post 请求"""
    from pycloudmusic import RECONNECTION

    try:
        session = await _get_session()
        async with session.post(url, headers=__headers, data=data) as req:
            return await req.json(content_type=None)
    except Exception as err:
        reconnection_count =+ 1
        if reconnection_count > RECONNECTION:
            raise CannotConnectApi(f"超出重连次数 {RECONNECTION} 无法请求到 {url} err: {err}")

        return await _post_url(url, data, reconnection_count)


async def _post(
    path: str, 
    data: Optional[dict[str, Any]] = None
) -> dict[str, Any]:
    """post 请求 api 路径"""
    return await _post_url(f"https://music.163.com{path}", data)


async def _download(
    url: str, 
    file_name: str, 
    file_path: Optional[str] = None, 
    reconnection_count: int = 0
) -> str:
    """下载文件"""
    from pycloudmusic import RECONNECTION, CHUNK_SIZE

    if file_path is None:
        from pycloudmusic import DOWNLOAD_PATH
        file_path = DOWNLOAD_PATH
    
    if not os.path.isdir(file_path):
        os.makedirs(file_path)

    file_path_ = os.path.join(file_path, file_name)    
    try:
        session = await _get_session()
        async with session.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        }) as req:
            async with aiofiles.open(file_path_, "wb") as file_:
                async for chunk in req.content.iter_chunked(CHUNK_SIZE):
                    await file_.write(chunk)
                
            return file_path_

    except Exception as err:
        reconnection_count += 1
        if reconnection_count > RECONNECTION:
            raise CannotConnectApi(f"超出重连次数 {RECONNECTION} 无法请求到 {url} err: {err}")

        return await _download(url, file_name, file_path, reconnection_count)