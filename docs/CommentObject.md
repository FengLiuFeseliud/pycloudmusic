# **`class`** CommentObject

CommentObject 规定了数据类 (DataObject/DataListObject)评论操作的几种 Api，所有支持评论操作的对象都可以使用这些 Api

## 类实例方法

### CommentObject.comments

**`sync def comments(self, hot: bool = True, page: int = 0, limit: int = 20,before_time: int = 0) -> tuple[int, Generator[CommentItemObject, None, None]]:`**

该对象的评论，返回一个元组 (tuple) 包含所有的评论数，一个 [CommentItemObject 对像](/pycloudmusic/CommentObject?id=class-commentitemobject)生成器(Generator)

> `hot`: 热评 / 最新评论
>
> `page`: 页
>
> `limit`: 一页的数据量
>
> `before_time`: 分页参数, 取上一页最后一项的 time 获取下一页数据(获取超过5000条评论的时候需要用到)

### CommentObject.comment_send

**`async def comment_send(self, content: str) -> dict[str, Any]:`**

发送评论

> `content`: 评论内容

# `class` CommentItemObject

CommentItemObject 规定了评论操作的几种 Api

## 类实例变量

在外部使用 `.` 即可读取数据

```python
class Music163CommentItem(CommentItemObject):

    def __init__(
        self, 
        headers: Optional[dict[str, str]], 
        comment_data: dict[str, Any]
    ) -> None:
        super().__init__(headers, comment_data)
        # 评论 id
        self.id = comment_data["commentId"]
        # 资源 id 
        self.thread_id =  comment_data["threadId"]
        # 用户 id
        self.user = comment_data["user"]
        # 用户名
        self.user_str = comment_data["user"]["nickname"]
        # 评论内容
        self.content = comment_data["content"]
        # 评论时间
        self.time = comment_data["time"]
        self.time_str = comment_data["timeStr"]
        # 评论点赞数
        self.liked_count = comment_data["likedCount"]
        # 是否点赞了该评论
        self.liked = comment_data["liked"]
```

## 类实例方法

### CommentItemObject.floors

**`async def floors(self, page: int = 0,limit: int = 20) -> tuple[int, Generator[CommentItemObject, None, None]]:`**

楼层评论，返回一个元组 (tuple) 包含所有的评论数，一个 [CommentItemObject 对像](/pycloudmusic/CommentObject?id=class-commentitemobject)生成器(Generator)

> `page`: 页
>
> `limit`: 一页的数据量

### CommentItemObject.like

**`async def like(self, in_: bool) -> dict[str, Any]:`**

评论点赞

> `in_`: 点赞 / 取消点赞

### CommentItemObject.reply

**`async def reply(self, content: str) -> dict[str, Any]:`**

回复评论

> `content`: 评论内容

### CommentItemObject.delete

**`async def delete(self) -> dict[str, Any]:`**

删除评论