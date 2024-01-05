import atexit
from typing import Any, overload
from model.Model import Model
from model.id.Model_ID import Model_ID
from dao.DAO import DAO

from flask import Request, Response, jsonify

import psycopg2 as pg
from configparser import NoSectionError

URL = "https://example.com"

schema = "joga_ai"
dao = DAO()


def cleanup():
    print("Performing cleanup tasks before exiting...")
    dao.close()


# Register the cleanup function with atexit
atexit.register(cleanup)


def post(model: Model, dao: DAO, request: Request) -> Response:
    id: None | int = None
    try:
        request_dict = request.get_json()
        model.from_dict(request_dict)
        id = dao.create(model)
    except (ValueError, TypeError, pg.DatabaseError) as bad_request:
        print(bad_request)
        return get_bad_request_error_response(bad_request)
    except (NoSectionError, pg.InterfaceError) as configuration_error:
        print(configuration_error.message)
        return get_configuration_error_response()

    response_dict = {
        "data": {
            "type": f"{model.get_class_name()}",
            "id": f"{id}",
            "attributes": model.to_dict(),
            "links": {
                "self": f"{URL}/{model.get_class_name()}/{id if id is not None else ''}"
            },
        }
    }

    response = jsonify(response_dict)
    response.status_code = 201
    return response


@overload
def get(
    model: Model, dao: DAO, condition: str, condition_values: tuple[Any, ...] = None
) -> Response:
    ...


@overload
def get(model: Model_ID, dao: DAO) -> Response:
    ...


def get(
    model: Model,
    dao: DAO,
    condition: str = None,
    condition_values: tuple[Any, ...] = None,
) -> Response:
    results: list[Model]

    try:
        if isinstance(model, Model_ID) and condition is None:
            results = dao.read(model)
        else:
            results = dao.read(model, condition, condition_values)
    except (ValueError, TypeError, pg.DatabaseError) as bad_request:
        print(bad_request)
        return get_bad_request_error_response(bad_request)
    except (NoSectionError, pg.InterfaceError) as configuration_error:
        print(configuration_error.message)
        return get_configuration_error_response()

    response_dict = {
        "links": {"self": f"{URL}/"},
        "data": [
            {
                "type": f"{result.get_class_name()}",
                "id": (result_dict := result.to_dict()).pop("id", None),
                "attributes": result_dict,
            }
            for result in results
        ],
    }

    response = jsonify(response_dict)
    response.status_code = 200
    return response


@overload
def put(
    model: Model,
    dao: DAO,
    request: Request,
    condition: str,
    condition_values: tuple[Any, ...] = None,
) -> Response:
    ...


@overload
def put(model: Model_ID, dao: DAO, request: Request) -> Response:
    ...


def put(
    model: Model,
    dao: DAO,
    request: Request,
    condition: str = None,
    condition_values: tuple[Any, ...] = None,
) -> Response:
    return update_service(
        model=model,
        dao=dao,
        request=request,
        ignore_none=False,
        condition=condition,
        condition_values=condition_values,
    )


@overload
def patch(
    model: Model,
    dao: DAO,
    request: Request,
    condition: str,
    condition_values: tuple[Any, ...] = None,
) -> Response:
    ...


@overload
def patch(model: Model_ID, dao: DAO, request: Request) -> Response:
    ...


def patch(
    model: Model,
    dao: DAO,
    request: Request,
    condition: str = None,
    condition_values: tuple[Any, ...] = None,
) -> Response:
    return update_service(
        model=model,
        dao=dao,
        request=request,
        ignore_none=True,
        condition=condition,
        condition_values=condition_values,
    )


def update_service(
    model: Model,
    dao: DAO,
    request: Request,
    ignore_none: bool,
    condition: str = None,
    condition_values: tuple[Any, ...] = None,
) -> Response:
    try:
        request_dict = request.get_json()
        model.from_dict(request_dict)
        if isinstance(model, Model_ID) and condition is None:
            dao.update(model, ignore_none=ignore_none)
        else:
            dao.update(model, condition, ignore_none, condition_values)
    except (ValueError, TypeError, pg.DatabaseError) as bad_request:
        print(bad_request)
        return get_bad_request_error_response(bad_request)
    except (NoSectionError, pg.InterfaceError) as configuration_error:
        print(configuration_error.message)
        return get_configuration_error_response()

    response_dict = {
        "data": {
            "type": f"{model.get_class_name()}",
            "id": (result_dict := model.to_dict(ignore_none)).pop("id", None),
            "attributes": result_dict,
        },
    }

    response = jsonify(response_dict)
    response.status_code = 202

    return response


@overload
def delete(
    model: Model,
    dao: DAO,
    condition: str,
    condition_values: tuple[Any, ...],
) -> Response:
    ...


@overload
def delete(model: Model_ID, dao: DAO) -> Response:
    ...


def delete(
    model: Model,
    dao: DAO,
    condition: str = None,
    condition_values: tuple[Any, ...] = None,
) -> Response:
    try:
        if isinstance(model, Model_ID) and condition is None:
            dao.delete(model)
        else:
            dao.delete(model, condition, condition_values)
    except (ValueError, TypeError, pg.DatabaseError) as bad_request:
        print(bad_request)
        return get_bad_request_error_response(bad_request)
    except (NoSectionError, pg.InterfaceError) as configuration_error:
        print(configuration_error.message)
        return get_configuration_error_response()

    response_dict = {
        "data": {
            "type": f"{model.get_class_name()}",
            "id": model.id if isinstance(model, Model_ID) else None,
        },
    }

    response = jsonify(response_dict)
    response.status_code = 200

    return response


def get_configuration_error_response() -> Response:
    response_dict = {
        "status": "500",
        "title": "Internal Server Configuration Error",
        "detail": "The server found a configuration error, try again later or contact the provider for more information.",
    }

    response = jsonify(response_dict)
    response.status_code = 500
    return response


def get_bad_request_error_response(exception: Exception) -> Response:
    response_dict = {
        "status": "400",
        "title": "Bad Request - Invalid Parameter Error",
        "detail": f"{exception}",
    }

    response = jsonify(response_dict)
    response.status_code = 400
    return response
