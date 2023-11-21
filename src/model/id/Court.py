from typing import Any, Dict
from .Model_ID import Model_ID
from ..Model import Model
import re


class Court(Model_ID):
    def __init__(
        self,
        schema: str,
        name: str = None,
        id: int = None,
        player_qty: int = None,
        description: str = None,
        modality: str = None,
        rating: float = None,
        address_id: int = None,
    ) -> None:
        super().__init__(schema, id)
        self.name = name
        self.player_qty = player_qty
        self.description = description
        self.modality = modality
        self.rating = rating
        self.address_id = address_id

    def copy(self) -> Model:
        return Court(
            self.schema,
            self.name,
            self.address_id,
            self.player_qty,
            self.description,
            self.modality,
            self.rating,
            self.address_id,
        )

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if value is None or re.match(r"^[a-zA-Z0-9]{2,}([ ][a-zA-Z0-9]+)*$", value):
            self.__name = value
        else:
            raise Exception("Invalid name")

    @property
    def player_qty(self) -> int:
        return self.__player_qty

    @player_qty.setter
    def player_qty(self, value: int) -> None:
        if value is None or (value > 1 and value < 23):
            self.__player_qty = value
        else:
            raise Exception("Invalid Player Quantity")

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str) -> None:
        if value is None or len(value) < 1000:
            self.__description = value
        else:
            raise Exception("Invalid description")

    @property
    def modality(self) -> str:
        return self.__modality

    @modality.setter
    def modality(self, value: str) -> None:
        if value is None or len(value) <= 50:
            self.__modality = value
        else:
            raise Exception("Invalid modality")

    @property
    def rating(self) -> float:
        return self.__rating

    @rating.setter
    def rating(self, value: float) -> None:
        if value is None or value >= 0.0:
            self.__rating = value
        else:
            raise Exception("Invalid rating")

    @property
    def address_id(self) -> int:
        return self.__address_id

    @address_id.setter
    def address_id(self, value: int):
        if value is None or value > 0:
            self.__address_id = value
        else:
            raise Exception("Invalid Address ID")
