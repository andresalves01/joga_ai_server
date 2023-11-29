from abc import ABC, abstractmethod
from typing import Any


class Model(ABC):
    def __init__(self, schema: str) -> None:
        super().__init__()
        self.schema = schema

    @abstractmethod
    def copy(self) -> Any:
        pass

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def from_json(self, json_dictonary: dict[str, Any]) -> dict[str, Any]:
        used_items = {}
        for key, value in json_dictonary.items():
            attribute_name = f"_{self.get_class_name()}__{key}"

            if hasattr(self, attribute_name):
                self.__setattr__(attribute_name, value)
                used_items[key] = value

        json_dictonary = {
            key: value for key, value in json_dictonary.items() if key not in used_items
        }
        return json_dictonary

    def from_fetched_row(self, row: tuple[Any]) -> tuple[Any]:
        attributes = iter(self.__dict__.keys())

        used_elements = []
        for name, value in zip(attributes, row):
            while name.endswith("_"):
                name = next(attributes)

            self.__dict__[name] = value
            used_elements.append(value)

        unused_elements = [x for x in row if x not in used_elements]
        return tuple(unused_elements)

    def attributes_to_dict(self, ignore_None: bool = False) -> dict[str, Any]:
        attribute_dict: dict[str, Any] = vars(self.copy())
        mangling_name = f"_{self.get_class_name()}__"

        return_dict = {}
        for name, value in attribute_dict.items():
            if name.endswith("_") or (ignore_None and not value):
                continue

            name = name.removeprefix(mangling_name)
            return_dict[name] = value

        return return_dict

    def generate_sql_insert(self) -> tuple[str, tuple[Any, ...]]:
        sql_query = f'INSERT INTO {self.schema}."{self.get_class_name().lower()}"('
        sql_values = "VALUES ("
        values = []

        for name, value in self.attributes_to_dict(ignore_None=True).items():
            sql_query += f"{name}, "
            sql_values += f"%s, "
            values.append(value)

        sql_query = sql_query.removesuffix(", ") + ") "
        sql_values = sql_values.removesuffix(", ") + ");"

        sql_query += sql_values
        return sql_query, tuple(values)

    def generate_sql_select(self, condition: str) -> str:
        sql_query = "SELECT "

        for name in self.attributes_to_dict().keys():
            sql_query += f"{name}, "

        sql_query = f'{sql_query.removesuffix(", ")} FROM {self.schema}."{self.get_class_name().lower()}" WHERE {condition};'
        return sql_query

    def generate_sql_update(self, condition: str) -> tuple[str, tuple[Any]]:
        sql_query = f'UPDATE {self.schema}."{self.get_class_name().lower()}" SET '
        values = []

        for name, value in self.attributes_to_dict().items():
            sql_query += f"{name} = %s, "
            values.append(value)

        sql_query = f'{sql_query.rstrip(", ")} WHERE {condition};'
        return sql_query, tuple(values)

    def generate_sql_delete(self, condition: str) -> str:
        sql_query = f'DELETE FROM {self.schema}."{self.get_class_name().lower()}" WHERE {condition};'
        return sql_query

    def __str__(self) -> str:
        return_string = f"{self.get_class_name()} {{"

        for name, value in self.attributes_to_dict().items():
            return_string += f"\n  {name} = {value}"
        return return_string + "\n}"

    @property
    def schema(self) -> str:
        return self.__schema_

    @schema.setter
    def schema(self, value) -> None:
        self.__schema_ = value
