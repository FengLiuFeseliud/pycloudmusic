"""
获取评论
"""


from pycloudmusic import Music163Api, Page
import asyncio


async def main():
    musicapi = Music163Api()
    # 获取歌曲
    # https://music.163.com/song?id=1902224491&userid=492346933
    music = await musicapi.music(1902224491)
    # 按时间获取评论
    async for comments in Page(music.comments, hot=False):
        for comment in comments:
            print(f"{comment.user_str}:  {comment.content}")

asyncio.run(main())
