from flask import Request, Response, jsonify
from model.id.Model_ID import Model_ID
from dao.DAO import DAO
from .Model_Service import model_post, model_get, model_put, model_delete


def model_id_get(
    model_object: Model_ID,
    dao: DAO,
    request: Request = None,
    condition: str = None,
    values: list[any] = None,
) -> Response:
    if condition and values:
        return model_get(model_object, dao, condition, values)

    if dao.connect():
        response_data = {
            "objects": [{}],
            "message": f"No {model_object.get_class_name()} data were found",
        }

        status = 404

        if id := request.args.get("id"):
            model_object.id = int(id)
            objects_found = dao.read(model_object)

            if len(objects_found) > 0:
                # If addresses are found, populate the addresses list and message
                response_data["objects"] = [
                    object_found.attributes_to_dict() for object_found in objects_found
                ]
                response_data[
                    "message"
                ] = f"{model_object.get_class_name()} data successfully found"
                status = 200  # Set status to success (200)

        response = jsonify(response_data)
        response.status_code = status
        return response

    else:
        # If the DAO connection fails, return a service unavailable response (status 503)
        dao.is_connected = False
        response = jsonify({"message": "Service unavailable."})
        response.status = 503
        return response


def model_id_put(
    model_object: Model_ID,
    dao: DAO,
    request: Request,
    condition: str = None,
    values: list[any] = None,
) -> Response:
    if condition and values:
        return model_put(model_object, dao, request, condition, values)

    if dao.connect() and "id" in (request_data := request.get_json()):
        model_object.from_json(request_data)
        response_data = {
            "message": f"No {model_object.get_class_name()} data found with the specified condition",
        }
        status = 404

        if dao.update(model_object):
            response_data[
                "message"
            ] = f"{model_object.get_class_name()} successfully updated"
            status = 200  # Set status to success (200)

        response = jsonify(response_data)
        response.status_code = status

        return response
    else:
        # If the DAO connection fails, return a service unavailable response (status 503)
        dao.is_connected = False
        response = jsonify({"message": "Service unavailable."})
        response.status = 503
        return response


def model_id_delete(
    model_object: Model_ID,
    dao: DAO,
    request: Request = None,
    condition: str = None,
    values: list[any] = None,
) -> Response:
    if condition and values:
        return model_delete(model_object, dao, condition, values)

    if dao.connect():
        response_data = {
            "message": f"No {model_object.get_class_name()} data found with the specified condition",
        }
        status = 404

        if id := request.args.get("id"):
            model_object.id = int(id)
            if dao.delete(model_object):
                response_data[
                    "message"
                ] = f"{model_object.get_class_name()} successfully deleted"
                status = 200  # Set status to success (200)

        response = jsonify(response_data)
        response.status_code = status

        return response
    else:
        # If the DAO connection fails, return a service unavailable response (status 503)
        dao.is_connected = False
        response = jsonify({"message": "Service unavailable."})
        response.status = 503
        return response


def post_and_update_id(
    object_to_post: Model_ID,
    object_to_update: Model_ID,
    dao: DAO,
    request_json: dict[str, any],
) -> Response:
    response = model_post(object_to_post, dao, request_json)

    if response.status_code == 201:
        command = f"""UPDATE {object_to_update.schema}."{object_to_update.get_class_name().lower()}"
        SET {object_to_post.get_class_name().lower()}_id = %s
        WHERE id = %s"""

        object_to_post.id = response.get_json()["id"]
        if dao.execute(command, (object_to_post.id, object_to_update.id)) is False:
            dao.delete(object_to_post)
            response = Response(status=404)

    return response


def post_referenced_and_dependent_models(
    referenced: Model_ID, dependent: Model_ID, dao: DAO, request_json: dict[str, any]
) -> Response:
    referenced_name = referenced.get_class_name().lower()
    referenced_response = model_post(referenced, dao, request_json[referenced_name])

    if referenced_response.status_code == 201:
        referenced_id = referenced_response.get_json()["id"]

        # Add the referenced model's ID to the dependent model's request JSON
        dependent_name = dependent.get_class_name().lower()
        dependent_request = request_json[dependent_name]
        dependent_request[f"{referenced_name}_id"] = referenced_id

        # Create the dependent model
        dependent_response = model_post(dependent, dao, dependent_request)

        if dependent_response.status_code != 201:
            # Handle the error, e.g., log it or perform rollback operations
            dao.delete(referenced, referenced_id)

        return dependent_response

    return referenced_response


def get_related_models(referenced: Model_ID, dependent: Model_ID, dao: DAO):
    if dao.connect():
        query = get_dependent_select_query(referenced, dependent)
        print(query, values := (dependent.id,))

        dao.cursor.execute(query, values)
        rows_fetched = dao.cursor.fetchall()

        # Execute the query and handle errors as needed
        if len(rows_fetched) > 0:
            results = []

            for row in rows_fetched:
                attribute_length = len(dependent.attributes_to_dict().keys())
                dependent.from_fetched_row(row[:attribute_length])
                referenced.from_fetched_row(row[attribute_length:])

                dependent_json = dependent.attributes_to_dict()
                dependent_json[
                    referenced.get_class_name().lower()
                ] = referenced.attributes_to_dict()

                print(dependent_json)
                results.append(dependent_json)

            response = jsonify(results)
            response.status = 200

            return response
        else:
            return Response(status=404)
    else:
        dao.is_connected = False
        response = jsonify({"message": "Service unavailable."})
        response.status = 503
        return response


def get_dependent_select_query(referenced: Model_ID, dependent: Model_ID) -> str:
    dependent_attributes = dependent.attributes_to_dict().keys()
    referenced_attributes = referenced.attributes_to_dict().keys()

    dependent_name = dependent.get_class_name().lower()
    referenced_name = referenced.get_class_name().lower()

    query = f"""SELECT {get_select_str(dependent_attributes)}, {get_select_str(referenced_attributes)}
            FROM {dependent.schema}."{dependent_name}"
            INNER JOIN {referenced.schema}."{referenced_name}" ON "{dependent_name}".{referenced_name}_id = "{referenced_name}".id
            WHERE "{dependent_name}".id = %s"""

    return query


def get_select_str(attribute_names: list[str]) -> str:
    return ", ".join(attribute_names)
