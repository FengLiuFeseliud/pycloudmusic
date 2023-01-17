"""
下载歌单所有曲目
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

    # 创建任务
    tasks = [asyncio.create_task(music.play()) for music in playlist]
    # 等待任务
    await asyncio.wait(tasks)

asyncio.run(main())
