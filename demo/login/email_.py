"""
邮箱登录
"""


from pycloudmusic import LoginMusic163
import asyncio


async def main():
    login = LoginMusic163()
    # 邮箱登录
    code, cookie, musicapi = await login.email(
        input("you login email: "),
        input("you login password: ")
    )
    # 验证登录
    print("=" * 60)
    print(code, cookie, musicapi)
    print("=" * 60)
    print(await musicapi.my())


asyncio.run(main())