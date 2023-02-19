# `class` LoginMusic163

**LoginMusic163 包含了登录 Api**

## 类实例方法

### LoginMusic163.email

邮箱登录，登录成功返回一个元组 (tuple) 包括 (Cookie, 一个使用本次登录 Cookie 的[ Music163Api 对象](/pycloudmusic/Music163Api.md))

**`async def email(self, email: str, password: str) -> tuple[str, Music163Api]:`**

> `email`: 邮箱
>
> `password`: 密码

#### Demo

```python
from pycloudmusic import LoginMusic163
import asyncio


async def main():
    login = LoginMusic163()
    # 邮箱登录
    cookie, musicapi = await login.email("you login email", "you login password")
    # 验证登录
    print(cookie, musicapi)
    print("=" * 60)
    print(await musicapi.my())

asyncio.run(main())
```

### LoginMusic163.send_captcha

发送手机验证码

**`async def send_captcha(self, phone: Union[str, int], country_code: Union[str, int] = "86") -> dict[str, Any]:`**

> `phone`: 手机号
>
> `country_code`: 国家码 (国外手机号使用)

### LoginMusic163.captcha

手机/手机验证码 登录，登录成功返回一个元组 (tuple) 包括 (Cookie, 一个使用本次登录 Cookie 的[ Music163Api 对象](/pycloudmusic/Music163Api.md))

**`async def cellphone(self, phone: Union[str, int], password: Union[str, int], captcha: bool = False, country_code: Union[str, int] = "86") -> tuple[str, Music163Api]:`**

> `phone`: 手机号
>
> `password`: 密码/手机验证码
>
> `captcha`: 是否为手机验证码登录，默认 False 密码登录
>
> `country_code`: 国家码 (国外手机号使用)

#### Demo

这里演示手机验证码登录

```python
from pycloudmusic import LoginMusic163
import asyncio


async def main():
    login = LoginMusic163()
    phone = input("you login phone: ")
    # 发送验证码
    print(await login.send_captcha(phone))
    cookie, musicapi = await login.cellphone(
        phone,
        input("you captcha code: "),
        captcha=True
    )
    # 验证登录
    print(cookie, musicapi)
    print("=" * 60)
    print(await musicapi.my())


asyncio.run(main())
```

### LoginMusic163.qr_key

获取二维码 key，用于二维码登录与生成登录二维码，成功返回一个元组 (tuple) 包括 (二维码 key, 登录二维码 url (用于生成登录二维码))

**`async def qr_key(self) -> Union[tuple[str, str], dict[str, Any]]:`**

### LoginMusic163.qr_check

查询二维码状态，成功返回一个元组 (tuple) 包括 (状态码, Cookie)

状态码:801 等待扫码 802 授权中 800 二维码不存在或已过期 803 登录成功

**`async def qr_check(self, qr_key: str) -> tuple[int, str]:`**

> `qr_key`: 二维码 key 使用 [LoginMusic163.qr_key](/pycloudmusic/LoginMusic163?id=loginmusic163qr_key) 获得二维码 key

### LoginMusic163.qr

二维码登录，使用后将堵塞线程直到登录成功或二维码过期或登录失败，登录成功返回一个元组 (tuple) 包括 (Cookie, 一个使用本次登录 Cookie 的[ Music163Api 对象](/pycloudmusic/Music163Api.md))

**`async def qr(self, qr_key: str, time_sleep: int = 3) -> tuple[str, Music163Api]:`**

> `qr_key`: 二维码 key 使用 [LoginMusic163.qr_key](/pycloudmusic/LoginMusic163?id=loginmusic163qr_key) 获得二维码 key
>
> `time_sleep`: 每隔多久查询一次二维码，默认3秒

#### Demo

```python
from pycloudmusic import LoginMusic163
import asyncio


async def main():
    login = LoginMusic163()
    # 获取二维码 key
    qr_key = await login.qr_key()
    # 去 https://cli.im/ 生成二维码或者自己生成二维码
    print(f"请使用该 url 生成二维码: {qr_key[1]}")
    # 等待扫码
    cookie, musicapi = await login.qr(qr_key[0])
    # 验证登录
    print(cookie, musicapi)
    print("=" * 60)
    print(await musicapi.my())

asyncio.run(main())
```