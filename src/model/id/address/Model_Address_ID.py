from typing import Any
from ..Model_ID import Model_ID


class Model_Address_ID(Model_ID):
    def __init__(self, schema: str, id: int = None, address_id: int = None) -> None:
        super().__init__(schema, id)
        self.address_id = address_id

    def from_dict(self, dictionary: dict[str, Any]) -> None:
        super().from_dict(dictionary)
        self.address_id = dictionary.pop("address_id", None)

    def to_dict(self, ignore_none: bool = False) -> dict[str, Any]:
        super_to_dict = super().to_dict(ignore_none)
        if ignore_none and self.address_id is None:
            return super_to_dict

        super_to_dict["address_id"] = self.address_id
        return super_to_dict

    @property
    def address_id(self) -> None | int:
        return self._address_id

    @address_id.setter
    def address_id(self, address_id: None | int) -> None:
        if address_id is None:
            self._address_id = None
            return

        try:
            address_id = int(address_id)
            if address_id <= 0:
                raise ValueError("Address id should be greater than zero")

            self._address_id = address_id
        except TypeError:
            raise TypeError(
                f"Address id should be an Integer, not a {type(address_id)}"
            )
