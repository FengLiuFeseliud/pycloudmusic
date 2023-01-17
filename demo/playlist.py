"""
获取歌单
"""


from pycloudmusic.music163 import Music163Api

import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌单 7487291782
    # https://music.163.com/#/playlist?id=7487291782
    playlist = await musicapi.playlist(7487291782)
    # 打印歌单信息
    print(playlist)
    print("=" * 50)

    # 打印歌单曲目
    for music in playlist:
        print(music.name, music.artist_str, music.id)

asyncio.run(main())
