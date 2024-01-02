from typing import Any
from .Model_Address_ID import Model_Address_ID


class Court(Model_Address_ID):
    def __init__(
        self,
        schema: str,
        id: int = None,
        name: str = None,
        description: str = None,
        rating: float = None,
        address_id: int = None,
    ) -> None:
        super().__init__(schema, id, address_id)
        self.name = name
        self.description = description
        self.rating = rating

    def copy(self) -> "Court":
        return Court(
            schema=self.schema,
            id=self.id,
            name=self.name,
            description=self.description,
            rating=self.rating,
            address_id=self.address_id,
        )

    def from_dict(self, dictionary: dict[str, Any]) -> None:
        super().from_dict(dictionary)
        self.name = dictionary.pop("name", None)
        self.description = dictionary.pop("description", None)
        self.rating = dictionary.pop("rating", None)

    def to_dict(
        self, ignore_none: bool = False, include_id: bool = False
    ) -> dict[str, Any]:
        self_dict = {
            "name": self.name,
            "description": self.description,
            "rating": self.rating,
        }

        result = super().to_dict(ignore_none, include_id)
        if ignore_none:
            for key, value in self_dict.items():
                if value is not None:
                    result[key] = value

        return result

    @property
    def name(self) -> None | str:
        return self._name

    @name.setter
    def name(self, name: None | str) -> None:
        if name is None:
            self._name = None
            return

        try:
            name = str(name)
            if len(name) > 100:
                raise ValueError(
                    "Name length should not be greater than 100 characters."
                )

            self._name = name
        except TypeError:
            raise TypeError(f"Name should be a String, not a {type(name)}")

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        if description is None:
            self._description = None
            return

        try:
            self._description = str(description)
        except TypeError:
            raise TypeError(
                f"Description should be a String, not a {type(description)}"
            )

    @property
    def rating(self) -> float:
        return self._rating

    @rating.setter
    def rating(self, rating: float) -> None:
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
