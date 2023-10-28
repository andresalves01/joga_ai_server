from typing import Any, Dict
from .Model import Model


class Court_Bookmark(Model):
    def __init__(
        self,
        schema: str,
        user_id: int = None,
        court_id: int = None,
    ) -> None:
        super().__init__(schema)
        self.user_id = user_id
        self.court_id = court_id

    def copy(self) -> Model:
        return Court_Bookmark(self.schema, self.user_id, self.court_id)

    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        if value is None or value > 0:
            self.__user_id = value
        else:
            raise Exception("Invalid User ID")

    @property
    def court_id(self) -> int:
        return self.__court_id

    @court_id.setter
    def court_id(self, value: int) -> None:
        if value is None or value > 0:
            self.__court_id = value
        else:
            raise Exception("Invalid Court ID")
