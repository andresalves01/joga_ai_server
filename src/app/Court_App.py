from flask import Blueprint, request

from service.Service import schema, dao
import service.Service as service
from model.id.address.Court import Court

court_blueprint = Blueprint("court", __name__)

ROUTE = "court"


@court_blueprint.post(f"/{ROUTE}")
def court_post():
    return service.post(Court(schema), dao, request)


@court_blueprint.get(f"/{ROUTE}/<int:id>")
def court_get(id: int):
    return service.get(Court(schema, id), dao)


@court_blueprint.put(f"/{ROUTE}/<int:id>")
def court_put(id: int):
    return service.put(Court(schema, id), dao, request)


@court_blueprint.patch(f"/{ROUTE}/<int:id>")
def court_patch(id: int):
    return service.patch(Court(schema, id), dao, request)


@court_blueprint.delete(f"/{ROUTE}/<int:id>")
def court_delete(id: int):
    return service.delete(Court(schema, id), dao)
