from typing import Any
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
        return Court_Bookmark(
            schema=self.schema, user_id=self.user_id, court_id=self.court_id
        )

    def from_dict(self, dictonary: dict[str, Any]) -> "Court_Bookmark":
        super().from_dict(dictonary)
        self.user_id = dictonary.pop("user_id", None)
        self.court_id = dictonary.pop("court_id", None)

        return self.copy()

    def to_dict(self, ignore_none: bool = False) -> dict[str, Any]:
        self_dict = {"user_id": self.user_id, "court_id": self.court_id}

        result = super().to_dict(ignore_none)

        if ignore_none:
            for key, value in self_dict.items():
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
