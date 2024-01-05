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

    def copy(self) -> "Court_Rating":
        return Court_Rating(
            schema=self.schema,
            user_id=self.user_id,
            court_id=self.court_id,
            rating=self.rating,
            comment=self.comment,
        )

    def from_dict(self, dictonary: dict[str, Any]) -> "Court_Rating":
        super().from_dict(dictonary)
        self.user_id = dictonary.pop("user_id", self.user_id)
        self.court_id = dictonary.pop("court_id", self.court_id)
        self.rating = dictonary.pop("rating", self.rating)
        self.comment = dictonary.pop("comment", self.comment)

        return self.copy()

    def to_dict(self, ignore_none: bool = False) -> dict[str, Any]:
        self_dict = {
            "schema": self.schema,
            "user_id": self.user_id,
            "court_id": self.court_id,
            "rating": self.rating,
            "comment": self.comment,
        }

        result = super().to_dict(ignore_none)

        if ignore_none:
            for value, key in self_dict.items():
                if value is not None:
                    result[key] = value
        else:
            result.update(self_dict)

        return result

    @property
    def user_id(self) -> None | int:
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: None | int) -> None:
        if user_id is None:
            self._user_id = None
            return

        try:
            user_id = int(user_id)
            if user_id <= 0:
                raise ValueError("user_id should be greater than zero")

            self._user_id = user_id
        except TypeError:
            raise TypeError(f"user_id should be an Integer, not a {type(user_id)}")

    @property
    def court_id(self) -> None | int:
        return self._court_id

    @court_id.setter
    def court_id(self, court_id: None | int) -> None:
        if court_id is None:
            self._court_id = None
            return

        try:
            court_id = int(court_id)
            if court_id <= 0:
                raise ValueError("court_id should be greater than zero")

            self._court_id = court_id
        except TypeError:
            raise TypeError(f"court_id should be an Integer, not a {type(court_id)}")

    @property
    def rating(self) -> None | float:
        return self._rating

    @rating.setter
    def rating(self, rating: None | float) -> None:
        if rating is None:
            self._rating = None
            return

        try:
            rating = float(rating)
            if rating < 1.0 or rating > 5.0:
                raise ValueError("Rating should be between 1.0 and 5.0")
            self._rating = rating
        except TypeError:
            raise TypeError(f"Rating should be Float, not a {type(rating)}")

    @property
    def comment(self) -> None | str:
        return self._comment

    @comment.setter
    def comment(self, comment: None | str) -> None:
        if comment is None:
            self._comment = None
            return

        try:
            self._comment = str(comment)
        except TypeError:
            raise TypeError(f"comment should be a String, not a {type(comment)}")
