"""
获取分层评论
"""


from pycloudmusic.music163 import Music163Api

import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌曲
    # https://music.163.com/song?id=1486983140&userid=492346933
    music = await musicapi.music(1486983140)
    # 获取热评第一条
    count, head_comment = await music.comments(limit=1)
    # 获取热评第一条分层评论
    count, comments = await list(head_comment)[0].floors()
    for comment in comments:
        print(f"{comment.user_str}:  {comment.content}")

asyncio.run(main())
