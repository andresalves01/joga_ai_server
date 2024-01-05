from flask import Blueprint, request

from service.Service import schema, dao
import service.Service as service
from model.Court_has_Amenity import Court_has_Amenity

court_amenity_blueprint = Blueprint("court_amenity", __name__)

ROUTE = "amenity"


@court_amenity_blueprint.post(f"/court/<int:id>/{ROUTE}")
def court_amenity_post(id: int):
    return service.post(Court_has_Amenity(schema, id), dao, request)


@court_amenity_blueprint.get(f"/court/<int:id>/amenities")
def court_amenitys_get(id: int):
    return service.get(
        Court_has_Amenity(schema),
        dao,
        condition="court_id = %s",
        condition_values=(id,),
    )


@court_amenity_blueprint.delete(f"/court/<int:id>/{ROUTE}")
def court_amenity_delete(id: int):
    request_json = request.get_json()
    user_id = request_json["user_id"]
    return service.delete(
        Court_has_Amenity(schema),
        dao,
        condition="court_id = %s AND user_id = %s",
        condition_values=(id, user_id),
    )
