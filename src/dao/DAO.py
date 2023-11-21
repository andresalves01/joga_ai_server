import psycopg2 as pg
from .config import config
from model.Model import Model
from model.id.Model_ID import Model_ID


class DAO:
    def __init__(self) -> None:
        self.is_connected = False
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        try:
            if self.is_connected is False:
                params = config()
                print("Connecting to PostgreSQL database ...")
                self.connection = pg.connect(**params)

                self.cursor = self.connection.cursor()
                print("PostgreSQL database version: ")
                self.cursor.execute("SELECT version()")

                db_version = self.cursor.fetchone()
                print(db_version)
                self.is_connected = True
            else:
                print("Data Access Object is already connected.")
            return True
        except (Exception, pg.DatabaseError, pg.Error) as error:
            print(error)
            return False

    def create(self, Model_object: Model) -> None | int:
        prepared_statement, data = Model_object.generate_sql_insert()
        print(prepared_statement, data)
        try:
            self.cursor.execute(prepared_statement, data)
            self.connection.commit()
            return self.cursor.fetchone()[0]
        except (Exception, pg.DatabaseError) as error:
            self.connection.rollback()
            print(error)
            return None

    def read_with_condition(
        self, model_object: Model, condition: str, data: tuple[any, ...]
    ) -> list[Model]:
        return self.__read(
            model_object,
            model_object.generate_sql_select(condition),
            data=data,
        )

    def read(self, model_id_object: Model_ID) -> list[Model_ID]:
        prepared_statement, data = model_id_object.generate_sql_select()

        return self.__read(model_id_object, prepared_statement, data)

    def __read(
        self, model_object: Model, prepared_statement: str, data: tuple[any, ...]
    ) -> list[Model_ID]:
        print(prepared_statement, data)

        self.cursor.execute(prepared_statement, data)
        rows_fetched = self.cursor.fetchall()

        models = []
        for row in rows_fetched:
            print(row)
            model_object.from_fetched_row(row)
            models.append(model_object.copy())

        return models

    def update_with_condition(
        self, model_object: Model, condition: str, values: tuple[any]
    ) -> bool:
        prepared_statement, data = model_object.generate_sql_update(condition)
        data += tuple(values)
        print(prepared_statement, data)
        try:
            self.cursor.execute(prepared_statement, data)
            self.connection.commit()
            return True
        except (Exception, pg.DatabaseError) as error:
            self.connection.rollback()
            print(error)
            return False

    def update(self, model_object: Model_ID) -> bool:
        prepared_statement, data = model_object.generate_sql_update()
        print(prepared_statement, data)
        try:
            self.cursor.execute(prepared_statement, data)
            self.connection.commit()
            return True
        except (Exception, pg.DatabaseError) as error:
            self.connection.rollback()
            print(error)
            return False

    def execute(self, command: str, values: tuple[any]) -> bool:
        try:
            print(command, values)
            self.cursor.execute(command, values)
            self.connection.commit()
            return True
        except (Exception, pg.DatabaseError) as error:
            self.connection.rollback()
            print(error)
            return False

    def delete_with_condition(
        self, model_object: Model, condition: str, data: tuple[any, ...]
    ) -> bool:
        prepared_statement = model_object.generate_sql_delete(condition)
        print(prepared_statement, data)

        try:
            self.cursor.execute(prepared_statement, data)
            self.connection.commit()
            return True
        except (Exception, pg.DatabaseError) as error:
            self.connection.rollback()
            print(error)
            return False

    def delete(self, model_object: Model_ID) -> bool:
        prepared_statement, data = model_object.generate_sql_delete()
        print(prepared_statement, data)

        try:
            self.cursor.execute(prepared_statement, data)
            self.connection.commit()
            return True
        except (Exception, pg.DatabaseError) as error:
            self.connection.rollback()
            print(error)
            return False

    def close(self) -> bool:
        if self.is_connected:
            self.cursor.close()
            self.connection.close()
            self.is_connected = False

            print("Data Access Object connection closed.")
            return True
        else:
            print("Data Access File is not connected to the PostgreSQL database")
            return False
