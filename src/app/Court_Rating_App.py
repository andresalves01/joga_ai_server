from flask import Blueprint, request

from service.Service import schema, dao
import service.Service as service
from model.Court_Rating import Court_Rating

court_rating_blueprint = Blueprint("court_rating", __name__)

ROUTE = "rating"


@court_rating_blueprint.post(f"/court/<int:id>/{ROUTE}")
def court_rating_post(id: int):
    return service.post(Court_Rating(schema, id), dao, request)


@court_rating_blueprint.get(f"/user/<int:id>/{ROUTE}s")
def user_ratings_get(id: int):
    return service.get(
        Court_Rating(schema), dao, condition="user_id = %s", condition_values=(id,)
    )


@court_rating_blueprint.get(f"/court/<int:id>/{ROUTE}s")
def court_ratings_get(id: int):
    return service.get(
        Court_Rating(schema), dao, condition="court_id = %s", condition_values=(id,)
    )


@court_rating_blueprint.put(f"/court/<int:id>/{ROUTE}")
def court_rating_put(id: int):
    request_json = dict(request.get_json())
    user_id = request_json.pop("user_id")
    return service.put(
        Court_Rating(schema, user_id, id),
        dao,
        request,
        condition="court_id = %s AND user_id = %s",
        condition_values=(id, user_id),
    )


@court_rating_blueprint.delete(f"/court/<int:id>/{ROUTE}")
def court_rating_delete(id: int):
    request_json = request.get_json()
    user_id = request_json["user_id"]
    return service.delete(
        Court_Rating(schema),
        dao,
        condition="court_id = %s AND user_id = %s",
        condition_values=(id, user_id),
    )
