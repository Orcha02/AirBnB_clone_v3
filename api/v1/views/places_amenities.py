"""Place_Amenities module of view package"""

from os import getenv
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage

storage_t = getenv("HBNB_TYPE_STORAGE")


@app_views.route("places/<place_id>/amenities", methods=["GET"])
def get_amenities_of_a_place(place_id=None):
    """Get all amenities of a given id of a place"""
    obj_place = storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    list_place_amenities = []
    for amenities in obj_place.amenities:
        list_place_amenities.append(amenities.to_dict())
    return jsonify(list_place_amenities)


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE", "POST"])
def create_or_delete_place_amenity(place_id=None, amenity_id=None):
    """Create or delete a place amenity"""
    obj_place = storage.get("Place", place_id)
    obj_amenity = storage.get("Amenity", amenity_id)

    if obj_place is None or obj_amenity is None:
        abort(404)

    if request.method == "DELETE":
        for amenity in obj_place.amenities:
            dict_place_amenities = amenity.to_dict()
            if dict_place_amenities.get("id") == amenity_id:
                if storage_t == "db":
                    obj_place.amenities.remove(obj_amenity)
                else:
                    obj_place.amenity_ids.remove(amenity_id)
                storage.save()
                return jsonify({})
        abort(404)

    if request.method == "POST":
        for amenity in obj_place.amenities:
            dict_place_amenities = amenity.to_dict()
            if dict_place_amenities.get("id") == amenity_id:
                return jsonify(dict_place_amenities)
        dict_amenity = obj_amenity.to_dict()
        if storage_t == "db":
            obj_place.amenities.append(obj_amenity)
        else:
            obj_place.amenity_ids.append(dict_amenity.get("id"))
        storage.save()
        return jsonify(obj_amenity.to_dict()), 201
