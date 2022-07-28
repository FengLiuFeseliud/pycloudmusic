from typing import Callable, Optional
from math import ceil


class Page:
    
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

    async def __anext__(self):
        if self.__page > self.__max_page:
            raise StopAsyncIteration

        data = await self.__api_fun(page=self.__page, limit=self.limit, **self.kwargs)
        try:
            count, page_data = data
        except ValueError:
            self.__page += 1
            return data
            
        self.__max_page = ceil(count / self.limit) - 1
        self.__page += 1
        return page_data

    def set_page(self, page: int):
        if page > self.__max_page:
            raise IndexError("page > self.__max_pag")

        self.__page = page