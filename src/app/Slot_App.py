from flask import Blueprint, request

from service.Service import schema, dao
import service.Service as service
from model.id.Slot import Slot

slot_blueprint = Blueprint("slot", __name__)

ROUTE = "slot"


@slot_blueprint.post(f"/{ROUTE}")
def slot_post():
    return service.post(Slot(schema), dao, request)


@slot_blueprint.get(f"/{ROUTE}/<int:id>")
def slot_get(id: int):
    return service.get(Slot(schema, id), dao)


@slot_blueprint.put(f"/{ROUTE}/<int:id>")
def slot_put(id: int):
    return service.put(Slot(schema, id), dao, request)


@slot_blueprint.patch(f"/{ROUTE}/<int:id>")
def slot_patch(id: int):
    return service.patch(Slot(schema, id), dao, request)


@slot_blueprint.delete(f"/{ROUTE}/<int:id>")
def slot_delete(id: int):
    return service.delete(Slot(schema, id), dao)
