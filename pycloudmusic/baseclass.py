from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Union
from pycloudmusic.ahttp import Http


class Api(Http, metaclass=ABCMeta):

    def __init__(self, 
        headers: Optional[dict[str, str]] = None
    ) -> None:
        super().__init__(headers)


class DataObject(Api, metaclass=ABCMeta):

    def __init__(self, 
        headers: Optional[dict[str, str]], 
        data: dict[str, Any]
    ) -> None:
        super().__init__(headers)
    
    @abstractmethod
    async def subscribe(self, 
        in_: bool = True
    ) -> dict[str, Any]:
        """
        对像 收藏/取消收藏
        """
        pass

    @abstractmethod
    async def similar(self) -> Any:
        """
        该对象的相似
        """
        pass


class ListObject(metaclass=ABCMeta):

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

    def __init__(self, 
        headers: Optional[dict[str, str]], 
        data: dict[str, Any]
    ) -> None:
        super().__init__(headers, data)

    @abstractmethod
    def __next__(self) -> Any:
        return super().__next__()


class CommentObject(Api):

    def __init__(self, 
        headers: Optional[dict[str, str]] = None
    ) -> None:
        super().__init__(headers)

    @abstractmethod
    async def comment(self, 
        hot: bool = True, 
        page: int = 0, 
        limit: int = 20,
        before_time: int = 0
    ) -> dict[str, Any]:
        """
        该对象的评论
        """
        pass

    @abstractmethod
    async def comment_floor(self, 
        comment_id: Union[str, int], 
        page: int = 0,
        limit: int = 20
    ) -> dict[str, Any]:
        """
        楼层评论
        """
        pass

    @abstractmethod
    async def comment_like(self, 
        comment_id: Union[str, int], 
        in_: bool
    ) -> dict[str, Any]:
        """
        评论点赞
        """
        pass

    @abstractmethod
    async def comment_add(self, 
        content: str
    ) -> dict[str, Any]:
        """
        发送评论
        """
        pass

    @abstractmethod
    async def comment_delete(self, 
        comment_id: Union[str, int]
    ) -> dict[str, Any]:
        """
        删除评论
        """
        pass

    @abstractmethod
    async def comment_reply(self, 
        comment_id: Union[str, int], 
        content: str
    ) -> dict[str, Any]:
        """
        回复评论
        """
        pass