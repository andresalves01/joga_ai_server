from typing import Any
from ..Model import Model
from typing import Any


class Model_ID(Model):
    def __init__(self, schema: str, id: int = None) -> None:
        super().__init__(schema)
        self.id = id

    def from_dict(self, dictonary: dict[str, Any]) -> dict[str, Any]:
        if "id" in dictonary.keys():
            self.id = dictonary["id"]
            dictonary.pop("id")

        return dictonary

    def to_dict(
        self, shoud_ignore_none: bool = False, include_id: bool = False
    ) -> dict[str, Any]:
        if not include_id or (self.id is None and shoud_ignore_none):
            return {}
        return {"id": self.id}

    def generate_sql_insert(self) -> tuple[str, tuple[Any, ...]]:
        query, values = super().generate_sql_insert()
        return query.replace(";", " RETURNING id;"), values

    def generate_sql_select(
        self, condition: str = None
    ) -> str | tuple[str, tuple[int]]:
        if condition is None and self.id is None:
            raise ValueError("Condition and id can't both be None")

        if condition is None:
            return super().generate_sql_select("id = %s"), (self.id,)
        else:
            return super().generate_sql_select(condition)

    def generate_sql_update(self, condition: str = None) -> tuple[str, tuple[Any, ...]]:
        if condition is None and self.id is None:
            raise ValueError("Condition and id can't both be None")

        if condition is None:
            query, values = super().generate_sql_update("id = %s")
            return query, values + (self.id,)
        else:
            return super().generate_sql_update(condition)

    def generate_sql_delete(
        self, condition: str = None
    ) -> str | tuple[str, tuple[int]]:
        if condition is None and self.id is None:
            raise ValueError("Condition and id can't both be None")

        if condition is None:
            return super().generate_sql_delete("id = %s"), (self.id,)
        else:
            return super().generate_sql_delete(condition)

    @property
    def id(self) -> None | int:
        return self._id

    @id.setter
    def id(self, id: int) -> None:
        if id is None:
            self._id = None
            return

        try:
            self._id = int(id)
        except TypeError:
            raise TypeError(f"Schema should be an Integer, not a {type(id)}")

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Model_ID):
            return self.id == __value.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)
