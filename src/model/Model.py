from abc import ABC, abstractmethod
from typing import Any


class Model(ABC):
    def __init__(self, schema: str) -> None:
        super().__init__()
        self.schema = schema

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def get_table_name(self) -> str:
        return f'{self.schema}."{self.get_class_name().lower()}"'

    @abstractmethod
    def copy(self) -> "Model":
        pass

    @abstractmethod
    def from_dict(self, dictonary: dict[str, Any]) -> "Model":
        pass

    @abstractmethod
    def to_dict(self, ignore_none: bool = False) -> dict[str, Any]:
        pass

    def generate_sql_insert(self) -> tuple[str, tuple[Any, ...]]:
        self_dict = self.to_dict(shoud_ignore_none=True)
        attributes = self_dict.keys()

        query = f"""INSERT INTO {self.get_table_name()} ({", ".join(attributes)})
                    VALUES ({", ".join(["%s" for i in attributes])});"""

        return query, tuple(self_dict.values())

    def generate_sql_select(self, condition: str) -> str:
        return f"""SELECT {', '.join(self.to_dict().keys())} FROM {self.get_table_name()}
                    WHERE {condition};"""

    def generate_sql_update(self, condition: str) -> tuple[str, tuple[Any, ...]]:
        self_dict = self.to_dict()
        query = f"UPDATE {self.get_table_name()} SET {' = %s, '.join(self_dict.keys()) + ' = %s'} WHERE {condition};"

        return query, tuple(self_dict.values())

    def generate_sql_delete(self, condition: str) -> str:
        return f"DELETE FROM {self.get_table_name()} WHERE {condition};"

    @property
    def schema(self) -> None | str:
        return self._schema

    @schema.setter
    def schema(self, schema: None | str) -> None:
        if schema is None:
            self._schema = None
            return

        try:
            self._schema = str(schema)
        except TypeError:
            raise TypeError(f"Schema should be a String, not a {type(schema)}")
