from typing import Any
# 最大并行请求数
LIMIT: int = 8
# 下载目录
DOWNLOAD_PATH: str = "./download"
# 下载文件最大缓存大小 (KB)
CHUNK_SIZE: int = 1024
# 重连次数
RECONNECTION: int = 3
# 不输出 NOT_PRINT_OBJECT_DICT 中指定的列表详细
NOT_PRINT_OBJECT_DICT: list[str] = ["music_list"]
# music163 通用请求头
MUSIC_HEADERS: dict[str, str] = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://music.163.com',
    'Host': 'music.163.com',
    'cookie': "appver=2.7.1.198277; os=pc;",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}


def set_config(config: dict[str, Any]):
    """设定配置"""
    if "NOT_PRINT_OBJECT_DICT" in config:
        global NOT_PRINT_OBJECT_DICT
        NOT_PRINT_OBJECT_DICT = config["NOT_PRINT_OBJECT_DICT"]

    if "DOWNLOAD_PATH" in config:
        global DOWNLOAD_PATH
        DOWNLOAD_PATH = config["DOWNLOAD_PATH"]

    if "LIMIT" in config:
        global LIMIT
        LIMIT = config["LIMIT"]

    if "CHUNK_SIZE" in config:
        global CHUNK_SIZE
        CHUNK_SIZE = config["CHUNK_SIZE"]

    if "RECONNECTION" in config:
        global RECONNECTION
        RECONNECTION = config["RECONNECTION"]


def _id_format(id_, dict_str=False):
    if type(id_) == str or type(id_) == int:
        format_str = str([{"id": id_}]) if dict_str else str([id_])
    elif type(id_) == list and dict_str:
        list_ = []
        for data in id_:
            list_.append({"id": data})
        format_str = str(list_)
    else:
        format_str = str(id_)

    return format_str

from pycloudmusic.music163 import LoginMusic163, Music163Api
from pycloudmusic.tools import *