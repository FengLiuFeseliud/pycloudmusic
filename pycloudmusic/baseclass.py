from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Union, Generator
import json


class Api(metaclass=ABCMeta):
    """Api"""

    def __init__(self, data: dict[str, Any]) -> None:
        pass

    def __str__(self) -> str:
        """格式化输出类属性"""
        from pycloudmusic import NOT_PRINT_OBJECT_DICT
        str_ = super().__repr__().rsplit(">", maxsplit=1)[0]

        for key in self.__dict__:
            key_value = self.__dict__[key]
            if type(key_value) in [list, dict]:
                # 不输出 NOT_PRINT_OBJECT_DICT 中指定的列表详细
                if key in NOT_PRINT_OBJECT_DICT:
                    key_value = f"dataItem * {len(key_value)}"
                else:
                    key_value = json.dumps(key_value, indent=6)
            str_ = f"{str_}\n    .{key} = {key_value}"
        return f"{str_}\n>"


class DataObject(Api, metaclass=ABCMeta):
    """所有 DataObject 必须可以收藏/查询相似"""

    def __init__(
        self, 
        data: dict[str, Any]
    ) -> None:
        super().__init__(data)
    
    @abstractmethod
    async def subscribe(
        self, 
        in_: bool = True
    ) -> dict[str, Any]:
        """对像 收藏/取消收藏"""
        pass

    @abstractmethod
    async def similar(self) -> Any:
        """该对象的相似"""
        pass


class ListObject(metaclass=ABCMeta):
    """所有 ListObject 必须可以迭代"""

    def __init__(self) -> None:
        self.music_list: list = []

    def __iter__(self):
        self._data_len_ = len(self.music_list) if self.music_list is not None else 0
        self._index = 0
        return self

    @abstractmethod
    def __next__(self) -> Any:
        if self._index == self._data_len_:
            raise StopIteration

        data = self.music_list[self._index]
        self._index += 1
        return data


class DataListObject(DataObject, ListObject, metaclass=ABCMeta):
    """所有 DataListObject 必须可以收藏/查询相似
    并且有数据可以迭代生成对象"""

    def __init__(
        self, 
        data: dict[str, Any]
    ) -> None:
        super().__init__(data)

    @abstractmethod
    def __next__(self) -> Any:
        return super().__next__()


class CommentItemObject(Api):
    """基本单评论"""

    def __init__(
        self, 
        comment_data: dict[str, Any]
    ) -> None:
        super().__init__(comment_data)
    
    @abstractmethod
    async def floors(
        self, 
        page: int = 0,
        limit: int = 20
    ) -> Union[tuple[int, Generator["CommentItemObject", None, None]], dict[str, Any]]:
        """楼层评论"""
        pass

    @abstractmethod
    async def reply(
        self, 
        content: str
    ) -> dict[str, Any]:
        """回复评论"""
        pass

    @abstractmethod
    async def like(
        self, 
        in_: bool = True
    ) -> dict[str, Any]:
        """评论点赞"""
        pass

    @abstractmethod
    async def delete(
        self, 
    ) -> dict[str, Any]:
        """删除评论"""
        pass


class CommentObject(Api):
    """基本评论功能"""

    def __init__(
        self, 
        comment_data: dict[str, Any]
    ) -> None:
        super().__init__(comment_data)

    @abstractmethod
    async def comments(
        self, 
        hot: bool = True, 
        page: int = 0, 
        limit: int = 20,
        before_time: int = 0
    ) -> Union[tuple[int, Generator["CommentItemObject", None, None]], dict[str, Any]]:
        """该对象的评论"""
        pass

    @abstractmethod
    async def comment_send(
        self, 
        content: str
    ) -> dict[str, Any]:
        """发送评论"""
        pass