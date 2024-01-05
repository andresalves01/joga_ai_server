from flask import Blueprint, request

from service.Service import schema, dao
import service.Service as service
from model.id.Photo import Photo

photo_blueprint = Blueprint("photo", __name__)

ROUTE = "photo"


@photo_blueprint.post(f"/{ROUTE}")
def photo_post():
    return service.post(Photo(schema), dao, request)


@photo_blueprint.get(f"/{ROUTE}/<int:id>")
def photo_get(id: int):
    return service.get(Photo(schema, id), dao)


@photo_blueprint.put(f"/{ROUTE}/<int:id>")
def photo_put(id: int):
    return service.put(Photo(schema, id), dao, request)


@photo_blueprint.patch(f"/{ROUTE}/<int:id>")
def photo_patch(id: int):
    return service.patch(Photo(schema, id), dao, request)


@photo_blueprint.delete(f"/{ROUTE}/<int:id>")
def photo_delete(id: int):
    return service.delete(Photo(schema, id), dao)
