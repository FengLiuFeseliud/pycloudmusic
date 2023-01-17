"""
发送评论
"""


from pycloudmusic.music163 import Music163Api

import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌曲
    # https://music.163.com/song?id=1486983140&userid=492346933
    music = await musicapi.music(1486983140)
    # 发送评论
    print(await music.comment_send("ohhhhhh!!!"))

asyncio.run(main())
