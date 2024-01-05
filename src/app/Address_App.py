from flask import Blueprint, request

from service.Service import schema, dao
import service.Service as service
from model.id.Address import Address

address_blueprint = Blueprint("address", __name__)

ROUTE = "address"


@address_blueprint.post(f"/{ROUTE}")
def address_post():
    return service.post(Address(schema), dao, request)


@address_blueprint.get(f"/{ROUTE}/<int:id>")
def address_get(id: int):
    return service.get(Address(schema, id), dao)


@address_blueprint.put(f"/{ROUTE}/<int:id>")
def address_put(id: int):
    return service.put(Address(schema, id), dao, request)


@address_blueprint.patch(f"/{ROUTE}/<int:id>")
def address_patch(id: int):
    return service.patch(Address(schema, id), dao, request)


@address_blueprint.delete(f"/{ROUTE}/<int:id>")
def address_delete(id: int):
    return service.delete(Address(schema, id), dao)
