#!/usr/bin/python3
""" Routes for State responses """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
def all_reviews(place_id=None):
    """retrieves a list of all reviews in a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    reviews_list = [review.to_dict() for review in reviews]
    return (jsonify(reviews_list), 200)


@app_views.route('/reviews/<review_id>', methods=["GET"], strict_slashes=False)
def specific_review(review_id=None):
    """Get review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return (jsonify(review.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a place by ID """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('places/<place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates new review from a place"""
    req = request.get_json()
    if req is False:
        abort(400, "Not a JSON")
    if "text" not in req:
        abort(400, "Missing text")
    if storage.get(Place, place_id) is None:
        abort(404)
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user = storage.get(User, req.get('user_id'))
    if not user:
        abort(404)

    new_review = Review()
    new_review.place_id = place_id
    for key, value in req.items():
        setattr(new_review, key, value)
    new_review.save()
    return (jsonify(new_review.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """ Update a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(review, key, value)
    review.save()
    return (jsonify(review.to_dict()), 200)
