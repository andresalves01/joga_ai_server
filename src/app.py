from dao.DAO import DAO
from model.Model import Model
from model.id.Model_ID import Model_ID
from model.id.Address import Address
from model.id.Amenity import Amenity
from model.Court_Bookmark import Court_Bookmark
from model.Court_has_Amenity import Court_has_Amenity
from model.Court_Rating import Court_Rating
from model.id.Court import Court
from model.id.Photo import Photo
from model.id.Slot import Slot
from model.id.User import User

from service.Model_Service import model_post, model_get, model_put, model_delete
from service.Model_ID_Service import (
    model_id_get,
    model_id_put,
    model_id_delete,
    post_and_update_id,
    post_referenced_and_dependent_models,
    get_related_models,
)

from flask import Flask, request, Response, jsonify

import atexit
from datetime import datetime

app = Flask(__name__)

dao = DAO()
schema = "joga_ai"


@app.route("/user/login", methods=["post"])
def user_login() -> Response:
    if dao.connect():
        query = f'SELECT id FROM joga_ai."user" WHERE email = %s AND password = %s'
        request_json = request.get_json()

        dao.cursor.execute(query, (request_json["email"], request_json["password"]))
        try:
            id = dao.cursor.fetchone()[0]
            response_data = {"id": int(id)}
            response = jsonify(response_data)
            response.status = 200

            return response
        except Exception as e:
            return Response(status=404)
    else:
        response = jsonify({"message": "Service unavailable."})
        response.status = 503
        return response


class Searchable_object:
    def __init__(self, model_object: Model_ID) -> None:
        self.model_object = model_object

    def get_query_parameters(self) -> str:
        select_query = ""

        object_name = self.model_object.get_class_name().lower()
        for attribute in self.model_object.attributes_to_dict().keys():
            select_query += f'"{object_name}".{attribute},\n'

        return select_query.removesuffix(",\n")


class Searchable_multiple_object:
    def __init__(
        self,
        multiple_object: Model,
        join_type: str,
        table_to_join: str,
        where_clause: str = "",
    ) -> None:
        self.multiple_object = multiple_object
        self.join_type = join_type
        self.table_to_join = table_to_join
        self.where_clause = where_clause

    def get_query_parameters(self) -> tuple[str, str]:
        multiple_object_name = self.multiple_object.get_class_name().lower()
        select_columns = ""

        join_arguments = ""
        join_select_columns = ""
        column_to_join = ""

        for attribute in self.multiple_object.attributes_to_dict().keys():
            if attribute.endswith(f"{self.table_to_join.lower()}_id"):
                join_select_columns += f'"{multiple_object_name}".{attribute},\n'
                column_to_join = attribute
            else:
                join_select_columns += f"string_agg(\"{multiple_object_name}\".{attribute}::text, ';') AS {attribute},\n"

            select_columns += f"{multiple_object_name}s.{attribute},\n"

        join_select_columns = join_select_columns.removesuffix(",\n")

        join_arguments += f"""{self.join_type} JOIN (
            SELECT
                {join_select_columns}
            FROM
                {self.multiple_object.schema}."{multiple_object_name}"
            {self.where_clause}
            {f"GROUP BY {column_to_join}" if column_to_join else ""}
            ) AS {multiple_object_name}s ON 
              "{self.table_to_join.lower()}".id = {multiple_object_name}s.{column_to_join}"""

        return select_columns.removesuffix(",\n"), join_arguments


@app.route("/search/slot", methods=["get"])
def search_slot() -> Response:
    if not dao.connect():
        return Response(status=503)

    single_objects: tuple[Searchable_object, ...] = (
        Searchable_object(Court(schema)),
        Searchable_object(Address(schema)),
    )

    multiple_objects: tuple[Searchable_multiple_object, ...] = (
        Searchable_multiple_object(
            multiple_object=Slot(schema),
            join_type="INNER",
            table_to_join="court",
            where_clause="WHERE slot.user_id IS NULL AND slot.cancellation_datetime IS NULL",
        ),
        Searchable_multiple_object(Photo(schema), "LEFT", "court"),
    )

    query = get_search_query(
        single_objects,
        multiple_objects,
        other_select_columns="amenities.name, amenities.icon_url, amenities.id",
        other_joins='INNER JOIN joga_ai."address" ON "court".address_id = "address".id\n'
        + """LEFT JOIN (
            SELECT 
                "court_has_amenity".court_id,
                string_agg("amenity".id::text, ';') as id,
                string_agg("amenity".name::text, ';') as name,
                string_agg("amenity".icon_url::text, ';') as icon_url
            FROM
                joga_ai."court_has_amenity"
            INNER JOIN
                joga_ai."amenity" ON "court_has_amenity".amenity_id = "amenity".id
            GROUP BY
                "court_has_amenity".court_id
            ) AS amenities ON "court".id = amenities.court_id""",
        where_clauses='"address".id IS NOT NULL\n ORDER BY "court".rating DESC',
    )

    # Perform SQL execute and fetch
    dao.cursor.execute(query)
    multiple_objects += (Searchable_multiple_object(Amenity(schema), "", ""),)
    results = fetch_results(single_objects, multiple_objects)
    response = jsonify(results)
    response.status_code = 200

    return response


def get_search_query(
    single_objects: tuple[Searchable_object, ...],
    multiple_objects: tuple[Searchable_multiple_object, ...],
    other_select_columns: str = "",
    other_joins: str = "",
    where_clauses: str = "",
) -> str:
    select_columns = ",\n".join(
        [
            searchable_object.get_query_parameters()
            for searchable_object in single_objects
        ]
    )
    join_arguments = ""

    for searchable_object in multiple_objects:
        columns, join_argument = searchable_object.get_query_parameters()
        select_columns += f",\n{columns}"
        join_arguments += f"{join_argument}\n"

    select_columns += ",\n" + other_select_columns

    main_object = single_objects[0].model_object
    query = f"""
        SELECT
            {select_columns}
        FROM
            {main_object.schema}."{main_object.get_class_name().lower()}"
            {join_arguments}
            {other_joins}
        {f"WHERE {where_clauses}" if where_clauses else ""}
        """.strip()
    print(query)

    return query


def fetch_results(
    single_objects: tuple[Searchable_object, ...],
    multiple_objects: tuple[Searchable_multiple_object, ...],
):
    results = []
    for row in dao.cursor.fetchall():
        result: dict[str, dict[str, any]] = {}
        starting_position = 0
        ending_position = 0

        for single_object in single_objects:
            model_object = single_object.model_object
            ending_position += len(model_object.attributes_to_dict().keys())

            model_object.from_fetched_row(row[starting_position:ending_position])
            result[
                model_object.get_class_name().lower()
            ] = model_object.attributes_to_dict()

            starting_position = ending_position

        for multiple_object in multiple_objects:
            model_object = multiple_object.multiple_object
            ending_position += len(model_object.attributes_to_dict().keys())

            # Separates aggrouped columns into a matrix[column][row]
            disagroupped_columns: list[list[str | float | int]] = []
            for aggrouped_column in row[starting_position:ending_position]:
                if isinstance(aggrouped_column, str):
                    tuples = aggrouped_column.split(";")
                    for i in range(len(tuples)):
                        try:
                            new_value = float(tuples[i])
                            if new_value.is_integer():
                                new_value = int(new_value)
                            tuples[i] = new_value
                        except (TypeError, ValueError):
                            try:
                                new_value = datetime(tuples[i])
                                tuples[i] = new_value
                            except (TypeError, ValueError):
                                pass
                    disagroupped_columns.append(tuples)
                else:
                    disagroupped_columns.append(aggrouped_column)

            if not disagroupped_columns[0]:
                continue

            disagroupped_rows = [
                [
                    disagroupped_row[i]
                    if isinstance(disagroupped_row, (list, tuple))
                    else disagroupped_row
                    for disagroupped_row in disagroupped_columns
                ]
                for i in range(len(disagroupped_columns[0]))
            ]

            objects = []
            for disagroupped_row in disagroupped_rows:
                model_object.from_fetched_row(disagroupped_row)
                objects.append(model_object.attributes_to_dict())

            result[model_object.get_class_name().lower() + "s"] = objects

            starting_position = ending_position

        results.append(result)

    return results


@app.route("/user/<int:id>/address", methods=["post"])
def user_address_post(id: int) -> Response:
    return post_and_update_id(
        Address(schema), User(schema, id=id), dao, request.get_json()
    )


@app.route("/user/address", methods=["post"])
def user_and_address_post() -> Response:
    return post_referenced_and_dependent_models(
        Address(schema), User(schema), dao, request.get_json()
    )


@app.route("/user/<int:id>/address", methods=["get"])
def user_address_get(id: int) -> Response:
    return get_related_models(Address(schema), User(schema, id=id), dao)


@app.route("/court/<int:id>/address", methods=["post"])
def court_address_post(id: int) -> Response:
    return post_and_update_id(
        Address(schema), Court(schema, id=id), dao, request.get_json()
    )


@app.route("/court/address", methods=["post"])
def court_and_address_post() -> Response:
    return post_referenced_and_dependent_models(
        Address(schema), Court(schema), dao, request.get_json()
    )


@app.route("/court/<int:id>/address", methods=["get"])
def court_address_get(id: int) -> Response:
    return get_related_models(Address(schema), Court(schema, id), dao, id)


@app.route("/address", methods=["post"])
def address_post() -> Response:
    return model_post(Address(schema), dao, request.get_json())


@app.route("/address", methods=["get"])
def address_get() -> Response:
    return model_id_get(Address(schema), dao, request)


@app.put("/address")
def address_put() -> Response:
    return model_id_put(Address(schema), dao, request)


@app.route("/address", methods=["delete"])
def address_delete() -> Response:
    return model_id_delete(Address(schema), dao, request)


@app.route("/amenity", methods=["post"])
def amenity_post() -> Response:
    return model_post(Amenity(schema), dao, request.get_json())


@app.route("/amenity", methods=["get"])
def amenity_get() -> Response:
    return model_id_get(Amenity(schema), dao, request)


@app.put("/amenity")
def amenity_put() -> Response:
    return model_id_put(Amenity(schema), dao, request)


@app.route("/amenity", methods=["delete"])
def amenity_delete() -> Response:
    return model_id_delete(Amenity(schema), dao, request)


@app.route("/court_bookmark", methods=["post"])
def court_bookmark_post() -> Response:
    return model_post(Court_Bookmark(schema), dao, request.get_json())


@app.route("/court_bookmark", methods=["get"])
def court_bookmark_get() -> Response:
    condition = ""
    values = []

    if court_id := request.args.get("court_id"):
        condition += f"court_id = %s AND "
        values.append(court_id)

    if user_id := request.args.get("user_id"):
        condition += f"user_id = %s AND "
        values.append(user_id)

    condition = condition.removesuffix(" AND ")
    return model_get(Court_Bookmark(schema), dao, condition, values)


@app.route("/court_bookmark", methods=["delete"])
def court_bookmark_delete() -> Response:
    if (court_id := request.args.get("court_id")) and (
        user_id := request.args.get("user_id")
    ):
        return model_delete(
            Court_Bookmark(schema),
            dao,
            f"court_id = %s AND user_id = %s",
            (court_id, user_id),
        )


@app.route("/court_has_amenity", methods=["post"])
def court_has_amenity_post() -> Response:
    return model_post(Court_has_Amenity(schema), dao, request.get_json())


@app.route("/court_has_amenity", methods=["get"])
def court_has_amenity_get() -> Response:
    condition = ""
    values = []

    if court_id := request.args.get("court_id"):
        condition += f"court_id = %s AND "
        values.append(court_id)

    if amenity_id := request.args.get("amenity_id"):
        condition += f"amenity_id = %s AND "
        values.append(amenity_id)

    condition = condition.removesuffix(" AND ")
    return model_get(Court_has_Amenity(schema), dao, condition, values)


@app.route("/court_has_amenity", methods=["delete"])
def court_has_amenity_delete() -> Response:
    if (court_id := request.args.get("court_id")) and (
        amenity_id := request.args.get("amenity_id")
    ):
        return model_delete(
            Court_Bookmark(schema),
            dao,
            f"court_id = %s AND amenity_id = %s",
            (court_id, amenity_id),
        )


@app.route("/court_rating", methods=["post"])
def court_rating_post() -> Response:
    return model_post(Court_Rating(schema), dao, request.get_json())


@app.route("/court_rating", methods=["get"])
def court_rating_get() -> Response:
    condition = ""
    values = []

    if court_id := request.args.get("court_id"):
        condition += f"court_id = %s AND "
        values.append(court_id)

    if user_id := request.args.get("user_id"):
        condition += f"user_id = %s AND "
        values.append(user_id)

    condition = condition.removesuffix(" AND ")
    return model_get(Court_Rating(schema), dao, condition, values)


@app.put("/court_rating")
def court_rating_put() -> Response:
    condition = ""
    values = []

    if court_id := request.args.get("court_id"):
        condition += f"court_id = %s AND "
        values.append(court_id)

    if user_id := request.args.get("user_id"):
        condition += f"user_id = %s AND "
        values.append(user_id)

    condition = condition.removesuffix(" AND ")
    return model_put(Court_Rating(schema), dao, request, condition, values)


@app.route("/court_rating", methods=["delete"])
def court_rating_delete() -> Response:
    condition = ""
    values = []

    if court_id := request.args.get("court_id"):
        condition += f"court_id = %s AND "
        values.append(court_id)

    if user_id := request.args.get("user_id"):
        condition += f"user_id = %s AND "
        values.append(user_id)

    condition = condition.removesuffix(" AND ")
    return model_delete(Court_Rating(schema), dao, condition, values)


@app.route("/court", methods=["post"])
def court_post() -> Response:
    return model_post(Court(schema), dao, request.get_json())


@app.route("/court", methods=["get"])
def court_get() -> Response:
    return model_id_get(Court(schema), dao, request)


@app.put("/court")
def court_put() -> Response:
    return model_id_put(Court(schema), dao, request)


@app.route("/court", methods=["delete"])
def court_delete() -> Response:
    return model_id_delete(Court(schema), dao, request)


@app.route("/photo", methods=["post"])
def photo_post() -> Response:
    return model_post(Photo(schema), dao, request.get_json())


@app.route("/photo", methods=["get"])
def photo_get() -> Response:
    return model_id_get(Photo(schema), dao, request)


@app.put("/photo")
def photo_put() -> Response:
    return model_id_put(Photo(schema), dao, request)


@app.route("/photo", methods=["delete"])
def photo_delete() -> Response:
    return model_id_delete(Photo(schema), dao, request)


@app.route("/slot", methods=["post"])
def slot_post() -> Response:
    return model_post(Slot(schema), dao, request.get_json())


@app.route("/slot", methods=["get"])
def slot_get() -> Response:
    return model_id_get(Slot(schema), dao, request)


@app.put("/slot")
def slot_put() -> Response:
    return model_id_put(Slot(schema), dao, request)


@app.route("/slot", methods=["delete"])
def slot_delete() -> Response:
    return model_id_delete(Slot(schema), dao, request)


@app.route("/user", methods=["post"])
def user_post() -> Response:
    return model_post(User(schema), dao, request.get_json())


@app.route("/user", methods=["get"])
def user_get() -> Response:
    return model_id_get(User(schema), dao, request)


@app.put("/user")
def user_put() -> Response:
    return model_id_put(User(schema), dao, request)


@app.route("/user", methods=["delete"])
def user_delete() -> Response:
    return model_id_delete(User(schema), dao, request)


application = app


def cleanup():
    print("Performing cleanup tasks before exiting...")
    dao.close()


# Register the cleanup function with atexit
atexit.register(cleanup)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
