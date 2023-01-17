"""
邮箱登录
"""


from pycloudmusic.music163 import LoginMusic163

import asyncio


async def main():
    login = LoginMusic163()
    # 邮箱登录
    cookie, musicapi = await login.email(
        input("you login email: "),
        input("you login password: ")
    )
    # 验证登录
    print("=" * 60)
    print(cookie, musicapi)
    print("=" * 60)
    print(await musicapi.my())


asyncio.run(main())
