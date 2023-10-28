from typing import Any, Dict
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
        return Court_has_Amenity(self.schema, self.amenity_id, self.court_id)

    @property
    def amenity_id(self) -> int:
        return self.__amenity_id

    @amenity_id.setter
    def amenity_id(self, value: int) -> None:
        if value is None or value > 0:
            self.__amenity_id = value
        else:
            raise Exception("Invalid Amenity ID")

    @property
    def court_id(self) -> int:
        return self.__court_id

    @court_id.setter
    def court_id(self, value: int) -> None:
        if value is None or value > 0:
            self.__court_id = value
        else:
            raise Exception("Invalid Court ID")
