from flask import Request, Response, jsonify
from model.Model import Model
from dao.DAO import DAO


def model_post(model_object: Model, dao: DAO, request_json: dict[str, any]) -> Response:
    if dao.connect():
        try:
            model_object.from_json(request_json)

            # Prepare the response data with default values
            response_data = {
                "id": dao.create(model_object),
                "message": f"{model_object.get_class_name()} row successfully created.",
            }

            response = jsonify(response_data)
            response.status = 201
            return response
        except Exception as error:
            print(error)  # Log the error for debugging purposes

            response_data = {
                "message": f"Empty or invalid parameters, unable to create {model_object.get_class_name()} object row."
            }
            response = jsonify(response_data)
            response.status = 400  # Set status to "Bad Request" (400)

            return response
    else:
        # If the DAO connection fails, return a service unavailable response (status 503)
        dao.is_connected = False
        response = jsonify({"message": "Service unavailable."})
        response.status = 503
        return response


def model_get(
    model_object: Model,
    dao: DAO,
    conditions: str,
    values: list[any],
) -> Response:
    if dao.connect():
        try:
            response_data = {
                "objects": [{}],
                "message": f"No conditions were received, unable to select {model_object.get_class_name()} objects.",
            }

            # Imediatly returns the function if there is no valid condition and values
            if not conditions and not values:
                response = jsonify(response_data)
                response.status = 400
                return response

            objects_found = dao.read_with_condition(model_object, conditions, values)

            if len(objects_found) > 0:
                # If addresses are found, populate the addresses list and message
                response_data["objects"] = [
                    object_found.to_json_dict() for object_found in objects_found
                ]
                response_data[
                    "message"
                ] = f"{model_object.get_class_name()} data successfully found."
                status = 200  # Set status to success (200)
            else:
                # If no addresses are found, set a message and status accordingly
                response_data[
                    "message"
                ] = f"No {model_object.get_class_name()} data found with the specified condition."
                status = 404  # Set status to "Not Found" (404)

            # Create a JSON response with the response data and appropriate status
            response = jsonify(response_data)
            response.status = status

            return response
        except Exception as error:
            print(error)  # Log the error for debugging purposes
            response = jsonify(
                {"message": "There was an internal error in the server."}
            )
            response.status = 500
            return response
    else:
        # If the DAO connection fails, return a service unavailable response (status 503)
        dao.is_connected = False
        response = jsonify({"message": "Service unavailable."})
        response.status = 503
        return response


def model_put(
    model_object: Model,
    dao: DAO,
    request: Request,
    condition: str,
    values: list[any],
) -> Response:
    if dao.connect():
        try:
            response_data = {
                "message": f"No condition or values were received, unable to update {model_object.get_class_name()} objects.",
            }
            status = 400

            # Imediatly returns the function if there is no valid condition and values
            if not condition and not values:
                response = jsonify(response_data)
                response.status = status
                return response

            model_object.from_json(request.get_json())
            if dao.update_with_condition(model_object, condition, values):
                response_data[
                    "message"
                ] = f"{model_object.get_class_name()} successfully updated."
                status = 200  # Set status to success (200)
            else:
                # If no addresses are found, set a message and status accordingly
                response_data[
                    "message"
                ] = f"No {model_object.get_class_name()} data found with the specified condition."
                status = 404  # Set status to "Not Found" (404)

            # Create a JSON response with the response data and appropriate status
            response = jsonify(response_data)
            response.status = status

            return response
        except Exception as error:
            print(error)  # Log the error for debugging purposes
    else:
        # If the DAO connection fails, return a service unavailable response (status 503)
        dao.is_connected = False
        response = jsonify({"message": "Service unavailable."})
        response.status = 503
        return response


def model_delete(
    model_object: Model,
    dao: DAO,
    condition: str,
    values: list[any],
) -> Response:
    if dao.connect():
        try:
            response_data = {
                "message": f"No condition or values were received, unable to delete {model_object.get_class_name()} objects.",
            }
            status = 400

            # Imediatly returns the function if there is no valid condition and values
            if not condition and not values:
                response = jsonify(response_data)
                response.status = status
                return response

            if dao.delete_with_condition(model_object, condition, values):
                response_data[
                    "message"
                ] = f"{model_object.get_class_name()} successfully deleted."
                status = 200  # Set status to success (200)
            else:
                # If no addresses are found, set a message and status accordingly
                response_data[
                    "message"
                ] = f"No {model_object.get_class_name()} data found with the specified condition."
                status = 404  # Set status to "Not Found" (404)

            # Create a JSON response with the response data and appropriate status
            response = jsonify(response_data)
            response.status = status

            return response
        except Exception as error:
            print(error)  # Log the error for debugging purposes
    else:
        # If the DAO connection fails, return a service unavailable response (status 503)
        dao.is_connected = False
        response = jsonify({"message": "Service unavailable."})
        response.status = 503
        return response
