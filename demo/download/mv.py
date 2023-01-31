"""
下载 mv
"""


from pycloudmusic.music163 import Music163Api

import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌曲
    # https://music.163.com/song?id=1486983140&userid=492346933
    music = await musicapi.music(1486983140)
    # 打印 music 信息
    print(music)
    print("=" * 50)

    # 获取歌曲 mv
    mv = await music.mv()
    # 打印 music 信息
    print(mv)
    print("=" * 50)

    print(await mv.play())

    """
    直接下载 mv

    # mv id
    # https://music.163.com/mv/?id=10944214&userid=492346933
    mv = await musicapi.mv(10944214)
    # 打印 mv 信息
    print(mv)
    print("=" * 50)

    #下载 mv
    print(await mv.play())
    """

asyncio.run(main())
