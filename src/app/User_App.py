from flask import Blueprint, request

from service.Service import schema, dao
import service.Service as service
from model.id.address.User import User

user_blueprint = Blueprint("user", __name__)

ROUTE = "user"


@user_blueprint.post(f"/{ROUTE}")
def user_post():
    return service.post(User(schema), dao, request)


@user_blueprint.get(f"/{ROUTE}/<int:id>")
def user_get(id: int):
    return service.get(User(schema, id), dao)


@user_blueprint.put(f"/{ROUTE}/<int:id>")
def user_put(id: int):
    return service.put(User(schema, id), dao, request)


@user_blueprint.patch(f"/{ROUTE}/<int:id>")
def user_patch(id: int):
    return service.patch(User(schema, id), dao, request)


@user_blueprint.delete(f"/{ROUTE}/<int:id>")
def user_delete(id: int):
    return service.delete(User(schema, id), dao)
