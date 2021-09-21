#!/usr/bin/python3
"""Place_Amenities module of view package"""
from api.v1.views import app_views
from flask import jsonify, abort
from models.place import Place
from models.amenity import Amenity
import models
from models import storage


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def get_amenities_from_place(place_id):
    """Get all amenities of a given id of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if models.storage_t == "db":
        list_res = place.amenities
    else:
        list_res = place.amenity_ids
    return jsonify([amenity.to_dict() for amenity in list_res])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def create_link_place_amenity(place_id, amenity_id):
    """Stores a link between a an amenity and a place"""
    place = models.storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = models.storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if models.storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    models.storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_link_place_amenity(place_id, amenity_id):
    """Deletes a link between a place and an amenity and
    returns an empty JSON"""
    place = models.storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = models.storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if models.storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    models.storage.save()
    return jsonify({}), 200
