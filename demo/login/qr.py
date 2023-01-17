"""
二维码登录
"""


from pycloudmusic.music163 import LoginMusic163

import asyncio


async def main():
    login = LoginMusic163()
    # 获取二维码 key
    qr_key = await login.qr_key()
    # 去 https://cli.im/ 生成二维码
    print(f"请使用该 url 生成二维码: {qr_key[1]}")
    # 等待扫码
    cookie, musicapi = await login.qr(qr_key[0])
    # 验证登录
    print("=" * 60)
    print(cookie, musicapi)
    print("=" * 60)
    print(await musicapi.my())

asyncio.run(main())
