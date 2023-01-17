from typing import Any


class CannotConnectApi(Exception):
    """无法连接 API 时抛出"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Music163BadCode(BaseException):
    """当服务器返回代码 `code` 不为 200 时抛出"""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data
        self.code = data["code"]

    def __str__(self) -> str:
        return f'Music163BadCode({self.code}): {self.data}'


class Music163BadData(Exception):
    """当服务器返回数据 pycloudmusic 内部无法正常处理时抛出"""

    def __init__(self, data: dict[str, Any]) -> None:
        self.code = data["code"]
        self.data = data

    def __str__(self) -> str:
        return f'Music163BadData({self.data["code"]}): {self.data}'
