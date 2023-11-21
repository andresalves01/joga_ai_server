from dao.DAO import DAO
from model.Model import Model
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
    get_attributes,
    get_select_str,
)

from flask import Flask, request, Response, jsonify

import atexit

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


@app.route("/search/slot", methods=["get"])
def search_slot() -> Response:
    if not dao.connect():
        return Response(status=503)

    placeholders: tuple[Model] = (Court(schema), Address(schema), Slot(schema))

    attributes_list = tuple(get_attributes(placeholder) for placeholder in placeholders)
    attributes_str = tuple(get_select_str(attributes) for attributes in attributes_list)

    query = f"""SELECT {", ".join(attributes_str)}
        FROM joga_ai.slot
        INNER JOIN joga_ai.court ON slot.court_id = court.id
        INNER JOIN joga_ai.address ON court.address_id = address.id
        LEFT JOIN (
            SELECT court_has_amenity.court_id, string_agg(amenity.id::text, ', ') as amenities
            FROM joga_ai.court_has_amenity
            INNER JOIN joga_ai.amenity ON court_has_amenity.amenity_id = amenity.id
            GROUP BY court_has_amenity.court_id
        ) amenity ON court.id = amenity.court_id
        WHERE slot.user_id IS NULL
        AND slot.cancellation_datetime IS NULL
        AND court.address_id IS NOT NULL;"""
    print(query)

    # Perform SQL execute and fetch
    dao.cursor.execute(query)
    rows_fetched = dao.cursor.fetchall()

    if len(rows_fetched) == 0:
        return Response(status=404)

    courts: dict[int, dict[str, dict[str, any] | list[dict[str, any]]]] = {}

    for row in rows_fetched:
        ending_position = 0
        referenced_court_id = 0

        for placeholder, attributes in zip(placeholders, attributes_list):
            starting_position = ending_position
            ending_position += len(attributes)

            placeholder.from_fetched_row(row[starting_position:ending_position])

            if isinstance(placeholder, Court):
                referenced_court_id = placeholder.id
                if not referenced_court_id in courts.keys():
                    courts[referenced_court_id] = placeholder.to_json_dict()
            elif isinstance(placeholder, Address):
                courts[referenced_court_id]["address"] = placeholder.to_json_dict()
            elif isinstance(placeholder, Slot):
                if "slots" in courts[referenced_court_id].keys():
                    courts[referenced_court_id]["slots"].append(
                        placeholder.to_json_dict()
                    )
                else:
                    courts[referenced_court_id]["slots"] = [placeholder.to_json_dict()]
            else:
                raise ValueError(
                    "Invalid placeholder type: should be Court, Address or Slot."
                )

    results = {"results": list(courts.values())}
    response = jsonify(results)
    response.status = 200

    return response


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
