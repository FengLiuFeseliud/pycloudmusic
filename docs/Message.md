# `class` Message

私信 (Message) 支持调用私信相关的 Api

## 类实例方法

### Message.comments

**`async def comments(self, before_time: int = -1, limit: int = 30) -> dict[str, Any]:`**

获取评论

> `before_time`: 取上一页最后一个歌单的 updateTime，获取下一页数据
>
> `limit`: 一页的数据量

### Message.forwards

**` async def forwards(self, page: int = 0, limit: int = 30) -> dict[str, Any]:`**

获取@我

> `page`: 页
>
> `limit`: 一页的数据量

### Message.notices

**`async def notices(self, last_time: int = -1, limit: int = 30) -> dict[str, Any]:`**

获取通知

> `last_time`: 传入上一次返回结果的 time， 将会返回下一页的数据
>
> `limit`: 一页的数据量

### Message.private_new

**`async def private_new(self) -> dict[str, Any]:`**

获取最接近联系人

### Message.private_history

**`async def private_history(self, id_: Union[str, int], page: int = 0, limit: int = 30) -> dict[str, Any]:`**

获取指定用户历史私信

> `id_`: 用户 id
>
> `page`: 页
>
> `limit`: 一页的数据量

### Message.private

**`async def private(self, page: int = 0, limit: int = 30) -> dict[str, Any]:`**

获取私信列表

> `page`: 页
>
> `limit`: 一页的数据量

### Message.send

**`async def send(self, msg: str, to_user_id: Union[int, str, list[Union[int, str]]]) -> dict[str, Any]:`**

发送私信

> `msg`: 私信内容
>
> `to_user_id`: 发送至指定用户 id，支持多 id 群发 (使用列表)

### Message.send_music

**`async def send_music(self, msg: str, to_user_id: Union[int, str, list[Union[int, str]]], id_: Union[int, str]) -> dict[str, Any]:`**

发送私信 带歌曲 

> `msg`: 私信内容
>
> `to_user_id`: 发送至指定用户 id，支持多 id 群发 (使用列表)
>
> `id_`: 歌曲 id

### Message.send_album

**`async def send_album(self, msg: str, to_user_id: Union[int, str, list[Union[int, str]]], id_: Union[int, str]) -> dict[str, Any]:`**

发送私信 带专辑 

> `msg`: 私信内容
>
> `to_user_id`: 发送至指定用户 id，支持多 id 群发 (使用列表)
>
> `id_`: 专辑 id

### Message.send_playlist

**`async def send_playlist(self, msg: str, to_user_id: Union[int, str, list[Union[int, str]]], id_: Union[int, str]) -> dict[str, Any]:`**

发送私信 带歌单 不能发送重复的歌单 

> `msg`: 私信内容
>
> `to_user_id`: 发送至指定用户 id，支持多 id 群发 (使用列表)
>
> `id_`: 歌单 id