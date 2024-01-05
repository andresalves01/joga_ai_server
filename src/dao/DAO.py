import psycopg2 as pg
import psycopg2.extras as pge
from typing import Any, overload
from .config import config
from model.Model import Model
from model.id.Model_ID import Model_ID


class DAO:
    def __init__(self) -> None:
        self.is_connected = False
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        if self.is_connected:
            return

        config_params = " ".join(f"{key}={value}" for key, value in config().items())
        print("Connecting to PostgreSQL database ...")

        self.connection = pg.connect(config_params)

        self.cursor = self.connection.cursor(cursor_factory=pge.RealDictCursor)
        print("PostgreSQL database version: ")
        self.cursor.execute("SELECT version()")

        db_version = self.cursor.fetchone()
        print(*db_version.values())

        self.is_connected = True

    def create(self, model: Model, commit_changes: bool = True) -> None | int:
        self.connect()

        query, data = model.generate_sql_insert()
        try:
            self.cursor.execute(query, data)

            if commit_changes:
                self.connection.commit()
        except (Exception, pg.DatabaseError) as error:
            self.connection.rollback()
            raise error

        if isinstance(model, Model_ID):
            return self.cursor.fetchone()["id"]

    @overload
    def read(
        self, model: Model, condition: str, condition_values: tuple[Any, ...] = None
    ) -> list[Model]:
        ...

    @overload
    def read(self, model: Model_ID) -> list[Model_ID]:
        ...

    def read(
        self,
        model: Model,
        condition: str = None,
        condition_values: tuple[Any, ...] = None,
    ) -> list[Model]:
        self.connect()

        if isinstance(model, Model_ID) and condition is None:
            query, data = model.generate_sql_select()
            self.cursor.execute(query, data)
        elif condition_values is not None:
            query = model.generate_sql_select(condition)
            self.cursor.execute(query, condition_values)
        else:
            query = model.generate_sql_select(condition)
            self.cursor.execute(query)

        return [model.from_dict(row) for row in self.cursor.fetchall()]

    @overload
    def update(
        self,
        model: Model,
        condition: str,
        ignore_none: bool,
        condition_values: tuple[Any, ...] = None,
        commit_changes: bool = True,
    ) -> None:
        ...

    @overload
    def update(
        self, model: Model_ID, *, ignore_none: bool, commit_changes: bool = True
    ) -> None:
        ...

    def update(
        self,
        model: Model,
        condition: str = None,
        ignore_none: bool = True,
        condition_values: tuple[Any, ...] = None,
        commit_changes: bool = True,
    ) -> None:
        self.connect()

        if isinstance(model, Model_ID) and condition is None:
            query, data = model.generate_sql_update(ignore_none=ignore_none)
        elif condition_values is not None:
            query, data = model.generate_sql_update(condition, ignore_none)
            data += condition_values
        else:
            query, data = model.generate_sql_update(condition, ignore_none)

        try:
            self.cursor.execute(query, data)
            if commit_changes:
                self.connection.commit()
        except (Exception, pg.DatabaseError) as error:
            self.connection.rollback()
            raise error

    @overload
    def delete(
        self,
        model: Model,
        condition: str,
        condition_values: tuple[Any, ...] = None,
        commit_changes: bool = True,
    ) -> None:
        ...

    @overload
    def delete(self, model: Model_ID, *, commit_changes: bool = True) -> None:
        ...

    def delete(
        self,
        model: Model,
        condition: str = None,
        condition_values: tuple[Any, ...] = None,
        commit_changes: bool = True,
    ) -> None:
        self.connect()

        try:
            if isinstance(model, Model_ID) and condition is None:
                query, data = model.generate_sql_delete()
                self.cursor.execute(query, data)
            elif condition_values is not None:
                query = model.generate_sql_delete(condition)
                self.cursor.execute(query, condition_values)
            else:
                query = model.generate_sql_delete()
                self.cursor.execute(query)

            if commit_changes:
                self.connection.commit()
        except (Exception, pg.DatabaseError) as error:
            self.connection.rollback()
            raise error

    # def execute(self, command: str, values: tuple[Any, ...]):
    #     return_data = None
    #     try:
    #         print(command, values)
    #         self.cursor.execute(command, values)
    #         self.connection.commit()
    #         return_data = self.cursor.fetchall()
    #     except (Exception, pg.DatabaseError) as error:
    #         self.connection.rollback()
    #         raise error

    #     return return_data

    def close(self) -> bool:
        if not self.is_connected:
            print("Data Access File is not connected to the PostgreSQL database")
            return False

        self.cursor.close()
        self.connection.close()
        self.is_connected = False

        print("Data Access Object connection closed.")
        return True
