from typing import Any, Dict
from .Model import Model


class Court_Rating(Model):
    def __init__(
        self,
        schema: str,
        user_id: int = None,
        court_id: int = None,
        rating: int = None,
        comment: str = None,
    ) -> None:
        super().__init__(schema)
        self.user_id = user_id
        self.court_id = court_id
        self.rating = rating
        self.comment = comment

    def copy(self) -> Model:
        return Court_Rating(
            self.schema, self.user_id, self.court_id, self.rating, self.comment
        )

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

    @property
    def rating(self) -> int:
        return self.__rating

    @rating.setter
    def rating(self, value: int) -> None:
        if value is None or (value > 0 and value <= 5):
            self.__rating = value
        else:
            raise Exception("invalid rating")

    @property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, value: str) -> None:
        if value is None or len(value) <= 480:
            self.__comment = value
        else:
            raise Exception("Invalid Comment")
