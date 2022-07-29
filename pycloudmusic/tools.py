from typing import Any, Callable, Generator, Optional
from math import ceil
import asyncio


class Page:
    """
    Page 对象可以按内部设置的方法来遍历绑定 Api 方法的页

    from pycloudmusic import Music163Api, Page
    import asyncio


    async def main():
        musicapi = Music163Api()
        music = await musicapi.music(1902224491)
        async for comments in Page(music.comments, hot=False):
            for comment in comments:
                print(f"{comment.user_str}:  {comment.content}")

    asyncio.run(main()
    """
    
    
    def __init__(
        self, 
        api_fun: Callable, 
        limit: Optional[int] = None, 
        page: int = 0,
        **kwargs
    ) -> None:
        self.__api_fun = api_fun
        self.__page = page
        self.__max_page = 0
        self.kwargs = kwargs
        self.limit = 20 if limit is None else limit

    def __aiter__(self):
        return self

    async def _set_index(self, page_data):
        try:
            count, data = page_data
        except ValueError:
            return page_data

        self.__max_page = ceil(count / self.limit) - 1
        return data


    async def __anext__(self):
        if self.__page > self.__max_page:
            raise StopAsyncIteration

        data = await self.__api_fun(page=self.__page, limit=self.limit, **self.kwargs)
        self.__page += 1
        return await self._set_index(data)

    def set_page(self, page: int):
        if page > self.__max_page:
            raise IndexError("page > self.__max_pag")

        self.__page = page

    async def all(
        self, 
        call_fun: Optional[Callable[[dict], int]] = None
    ) -> Generator:
        """请求绑定 Api 方法的所有数据"""
        data = await self.__api_fun(page=self.__page, limit=self.limit, **self.kwargs)
        if not call_fun is None:
            self.__max_page = call_fun(data)
        else:
            await self._set_index(data)

        tasks = []
        while self.__page <= self.__max_page:
            tasks.append(asyncio.create_task(self.__api_fun(page=self.__page, limit=self.limit, **self.kwargs)))
            self.__page += 1
        
        done, _ = await asyncio.wait(tasks)
        return (task.result() for task in done)