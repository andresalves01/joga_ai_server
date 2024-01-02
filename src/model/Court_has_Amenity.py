from typing import Any
from .Model import Model


class Court_has_Amenity(Model):
    def __init__(
        self,
        schema: str,
        amenity_id: int = None,
        court_id: int = None,
    ) -> None:
        super().__init__(schema)
        self.amenity_id = amenity_id
        self.court_id = court_id

    def copy(self) -> Model:
        return Court_has_Amenity(
            schema=self.schema, amenity_id=self.amenity_id, court_id=self.court_id
        )

    def from_dict(self, dictonary: dict[str, Any]) -> None:
        super().from_dict(dictonary)
        self.amenity_id = dictonary.pop("amenity_id", None)
        self.court_id = dictonary.pop("court_id", None)

    @property
    def amenity_id(self) -> None | int:
        return self._amenity_id

    @amenity_id.setter
    def amenity_id(self, amenity_id: None | int) -> None:
        if amenity_id is None:
            self._amenity_id = None
            return

        try:
            amenity_id = int(amenity_id)
            if amenity_id <= 0:
                raise ValueError("amenity_id should be greater than zero")

            self._amenity_id = amenity_id
        except TypeError:
            raise TypeError(
                f"amenity_id should be an Integer, not a {type(amenity_id)}"
            )

    @property
    def court_id(self) -> None | int:
        return self._court_id

    @court_id.setter
    def court_id(self, value: None | int) -> None:
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
