from typing import Any
from ..Model import Model
from typing import Any


class Model_ID(Model):
    def __init__(self, schema: str, id: int = None) -> None:
        super().__init__(schema)
        self.id = id

    def from_fetched_row(self, row: tuple[Any]) -> None:
        self.id = row[-1]
        super().from_fetched_row(row)

    def from_json(self, dictonary: dict[str, Any]) -> dict[str, Any]:
        if "id" in dictonary.keys():
            self.id = dictonary["id"]
            dictonary.pop("id")
        return super().from_json(dictonary)

    def to_json_dict(self) -> dict[str, Any]:
        dictionary = super().to_json_dict()
        if self.id:
            dictionary["id"] = self.id
        return dictionary

    def generate_sql_insert(self) -> tuple[str, tuple[Any, ...]]:
        sql_query, values = super().generate_sql_insert()
        return sql_query.replace(";", " RETURNING id;"), values

    def generate_sql_select(
        self, condition: str = None
    ) -> None | str | tuple[str, tuple[int]]:
        if condition:
            return super().generate_sql_select(condition).replace(" FROM", ", id FROM")
        elif self.id:
            return super().generate_sql_select(f"id = %s").replace(
                " FROM", ", id FROM"
            ), (self.id,)

    def generate_sql_update(
        self, condition: str = None
    ) -> None | tuple[str, tuple[Any, ...]]:
        if condition:
            return super().generate_sql_update(condition)
        elif self.id:
            sql_query, values = super().generate_sql_update(f"id = %s")
            values += (self.id,)
            return sql_query, values

    def generate_sql_delete(
        self, condition: str = None
    ) -> None | str | tuple[str, tuple[int]]:
        if condition:
            return super().generate_sql_delete(condition)
        elif self.id:
            return super().generate_sql_delete(f"id = %s"), (self.id,)

    @property
    def id(self) -> int:
        return self._id_

    @id.setter
    def id(self, value: int) -> None:
        if value is None or value > 0:
            self._id_ = value
        else:
            raise Exception("Invalid ID")
