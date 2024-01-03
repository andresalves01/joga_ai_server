from typing import Any, overload
from ..Model import Model
from typing import Any


class Model_ID(Model):
    def __init__(self, schema: str, id: int = None) -> None:
        super().__init__(schema)
        self.id = id

    def from_dict(self, dictionary: dict[str, Any]) -> "Model_ID":
        self.id = dictionary.pop("id", None)

    def to_dict(
        self, ignore_none: bool = False, include_id: bool = False
    ) -> dict[str, Any]:
        if not include_id or (self.id is None and ignore_none):
            return {}
        return {"id": self.id}

    def generate_sql_insert(self) -> tuple[str, tuple[Any, ...]]:
        query, values = super().generate_sql_insert()
        return query.replace(";", " RETURNING id;"), values

    @overload
    def generate_sql_select(self, condition: str) -> str:
        ...

    @overload
    def generate_sql_select(self) -> tuple[str, tuple[int]]:
        ...

    def generate_sql_select(
        self, condition: str = None
    ) -> str | tuple[str, tuple[int]]:
        if condition is None and self.id is None:
            raise ValueError("Condition and id can't both be None")

        if condition is not None:
            return super().generate_sql_select(condition)
        else:
            return super().generate_sql_select("id = %s"), (self.id,)

    @overload
    def generate_sql_update(self, condition: str) -> tuple[str, tuple[Any, ...]]:
        ...

    @overload
    def generate_sql_update(self) -> tuple[str, tuple[Any, ...]]:
        ...

    def generate_sql_update(self, condition: str = None) -> tuple[str, tuple[Any, ...]]:
        if condition is None and self.id is None:
            raise ValueError("Condition and id can't both be None")

        if condition is None:
            query, values = super().generate_sql_update("id = %s")
            return query, values + (self.id,)
        else:
            return super().generate_sql_update(condition)

    @overload
    def generate_sql_delete(self, condition: str) -> str:
        ...

    @overload
    def generate_sql_delete(self) -> tuple[str, tuple[int]]:
        ...

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
    def id(self, id: None | int) -> None:
        if id is None:
            self._id = None
            return

        try:
            id = int(id)
            if id <= 0:
                raise ValueError("Id should be greater than zero")

            self._id = id
        except TypeError:
            raise TypeError(f"Id should be an Integer, not a {type(id)}")

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Model_ID):
            return self.id == __value.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)
