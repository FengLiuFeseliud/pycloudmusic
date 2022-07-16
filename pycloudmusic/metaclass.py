from abc import ABCMeta, abstractmethod
from typing import Optional
from pycloudmusic.ahttp import Http


class Api(Http, metaclass=ABCMeta):

    def __init__(self, headers: Optional[dict[str, str]] = None) -> None:
        super().__init__(headers)