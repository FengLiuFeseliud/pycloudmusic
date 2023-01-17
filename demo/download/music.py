"""
下载歌曲
"""


from pycloudmusic.music163 import Music163Api

import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌曲 421531
    # https://music.163.com/#/song?id=421531
    music = await musicapi.music(421531)
    # 打印歌曲信息
    print(music)
    print("=" * 50)

    # 下载歌曲
    await music.play()

asyncio.run(main())
