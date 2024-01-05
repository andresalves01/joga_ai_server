from flask import Blueprint, request

from service.Service import schema, dao
import service.Service as service
from model.Court_Bookmark import Court_Bookmark

court_bookmark_blueprint = Blueprint("court_bookmark", __name__)

ROUTE = "bookmark"


@court_bookmark_blueprint.post(f"/user/<int:id>/{ROUTE}")
def court_bookmark_post(id: int):
    return service.post(Court_Bookmark(schema, id), dao, request)


@court_bookmark_blueprint.get(f"/user/<int:id>/{ROUTE}s")
def user_bookmarks_get(id: int):
    return service.get(
        Court_Bookmark(schema), dao, condition="user_id = %s", condition_values=(id,)
    )


@court_bookmark_blueprint.get(f"/court/<int:id>/{ROUTE}s")
def court_bookmarks_get(id: int):
    return service.get(
        Court_Bookmark(schema), dao, condition="court_id = %s", condition_values=(id,)
    )


@court_bookmark_blueprint.delete(f"/user/<int:id>/{ROUTE}")
def court_bookmark_delete(id: int):
    request_json = request.get_json()
    court_id = request_json["court_id"]
    return service.delete(
        Court_Bookmark(schema),
        dao,
        condition="user_id = %s AND court_id = %s",
        condition_values=(id, court_id),
    )
