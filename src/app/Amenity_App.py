from flask import Blueprint, request

from service.Service import schema, dao
import service.Service as service
from model.id.Amenity import Amenity

amenity_blueprint = Blueprint("amenity", __name__)

ROUTE = "amenity"


@amenity_blueprint.post(f"/{ROUTE}")
def amenity_post():
    return service.post(Amenity(schema), dao, request)


@amenity_blueprint.get(f"/{ROUTE}/<int:id>")
def amenity_get(id: int):
    return service.get(Amenity(schema, id), dao)


@amenity_blueprint.put(f"/{ROUTE}/<int:id>")
def amenity_put(id: int):
    return service.put(Amenity(schema, id), dao, request)


@amenity_blueprint.patch(f"/{ROUTE}/<int:id>")
def amenity_patch(id: int):
    return service.patch(Amenity(schema, id), dao, request)


@amenity_blueprint.delete(f"/{ROUTE}/<int:id>")
def amenity_delete(id: int):
    return service.delete(Amenity(schema, id), dao)
