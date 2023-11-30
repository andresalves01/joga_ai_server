from typing import Any, Dict
from .Model_ID import Model_ID
from ..Model import Model
import re


class Amenity(Model_ID):
    def __init__(
        self, schema: str, name: str = None, id: int = None, icon_url: str = None
    ) -> None:
        super().__init__(schema, id)
        self.name = name
        self.icon_url = icon_url

    def copy(self) -> Model:
        return Amenity(self.schema, self.name, self.id, self.icon_url)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def icon_url(self) -> str:
        return self.__icon_url

    @icon_url.setter
    def icon_url(self, value: str) -> None:
        if value is None or (len(value) <= 2080):
            self.__icon_url = value
        else:
            raise Exception("Invalid Icon Url")
