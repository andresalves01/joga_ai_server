from abc import ABC, abstractmethod
from typing import Any, Dict


class Model(ABC):
    def __init__(self, schema: str) -> None:
        super().__init__()
        self.schema = schema

    @abstractmethod
    def copy(self) -> Any:
        pass

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def get_attributes(self) -> Dict[str, Any]:
        return vars(self)

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

    def to_json_dict(self) -> dict[str, Any]:
        dictionary = {}

        private_prefix = "_" + self.get_class_name() + "__"
        for name, attribute_value in self.__dict__.items():
            if not name.endswith("_"):
                dictionary[name.removeprefix(private_prefix)] = attribute_value
        return dictionary

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

    def generate_sql_insert(self) -> tuple[str, tuple[Any, ...]]:
        sql_query = f'INSERT INTO {self.schema}."{self.get_class_name().lower()}"('
        sql_values = "VALUES ("
        values = []

        attributes = self.get_attributes()
        private_prefix = "_" + self.get_class_name() + "__"
        for name, attribute_value in attributes.items():
            if name.endswith("_") or attribute_value is None:
                continue

            sql_query += f"{name.removeprefix(private_prefix)}, "
            sql_values += f"%s, "
            values.append(attribute_value)

        sql_query = sql_query.removesuffix(", ") + ") "
        sql_values = sql_values.removesuffix(", ") + ");"

        sql_query += sql_values
        return sql_query, tuple(values)

    def generate_sql_select(self, condition: str) -> str:
        sql_query = "SELECT "

        atrributes = self.get_attributes()
        private_prefix = "_" + self.get_class_name() + "__"
        for name in atrributes.keys():
            if name.endswith("_"):
                continue
            sql_query += f"{name.removeprefix(private_prefix)}, "

        sql_query = f'{sql_query.removesuffix(", ")} FROM {self.schema}."{self.get_class_name().lower()}" WHERE {condition};'
        return sql_query

    def generate_sql_update(self, condition: str) -> tuple[str, tuple[Any]]:
        sql_query = f'UPDATE {self.schema}."{self.get_class_name().lower()}" SET '
        values = []

        attributes = self.get_attributes()
        private_prefix = "_" + self.get_class_name() + "__"

        for name, attribute_value in attributes.items():
            if name.endswith("_"):
                continue

            sql_query += f"{name.removeprefix(private_prefix)} = %s, "
            values.append(attribute_value)

        sql_query = f'{sql_query.rstrip(", ")} WHERE {condition};'
        return sql_query, tuple(values)

    def generate_sql_delete(self, condition: str) -> str:
        sql_query = f'DELETE FROM {self.schema}."{self.get_class_name().lower()}" WHERE {condition};'
        return sql_query

    def __str__(self) -> str:
        return_string = f"{self.get_class_name()} {{"
        attributes = self.get_attributes()

        for name, value in attributes.items():
            return_string += f"\n  {name} = {value}"
        return return_string + "\n}"

    @property
    def schema(self) -> str:
        return self.__schema_

    @schema.setter
    def schema(self, value) -> None:
        self.__schema_ = value
