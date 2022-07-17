"""
获取分层评论
"""


from pycloudmusic import Music163Api
import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌曲
    # https://music.163.com/song?id=1486983140&userid=492346933
    music = await musicapi.music(1486983140)
    # 获取热评第一条
    head_comment = (await music.comment(limit=1))["hotComments"][0]
    # 获取热评第一条分层评论
    print(await music.comment_floor(head_comment["commentId"]))

asyncio.run(main())