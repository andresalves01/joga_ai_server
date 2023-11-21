from typing import Any, Dict
from .Model_ID import Model_ID
from ..Model import Model


class Photo(Model_ID):
    def __init__(
        self, schema: str, id: int = None, url: str = None, court_id: int = None
    ) -> None:
        super().__init__(schema, id)
        self.url = url
        self.court_id = court_id

    def copy(self) -> Model:
        return Photo(self.schema, self.id, self.url, self.court_id)

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, value: str) -> None:
        if value is None or len(value) <= 2080:
            self.__url = value
        else:
            raise Exception("Invalid Icon Url")

    @property
    def court_id(self) -> int:
        return self.__court_id

    @court_id.setter
    def court_id(self, value: int) -> None:
        if value is None or value > 0:
            self.__court_id = value
        else:
            raise Exception("Invalid Court ID")
