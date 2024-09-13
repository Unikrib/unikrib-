#!/usr/bin/python3

from api.blueprint import app_views, auth
# from models.v2.review import Review
from models import storage, Review
from flask import jsonify, request

@app_views.route('/reviews', strict_slashes=False)
@auth.login_required(role="admin")
def get_all_reviews():
    """This returns a list of all the reviews in storage"""
    all_reviews = []
    for key, obj in storage.all(Review).items():
        all_reviews.append(obj.to_dict())

    return jsonify(all_reviews)

@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """This returns a review based on id"""
    obj = storage.get('Review', review_id)
    if obj == None:
        return jsonify("No review found"), 404
    return jsonify(obj.to_dict())

@app_views.route('/users/<user_id>/reviews', strict_slashes=False)
# @auth.login_required
def get_user_review(user_id):
    """This returns a list of all the reviews about a user"""
    all_reviews = []
    if user_id == 'me':
        user = auth.current_user()
        user_id = user.id
    reviews = storage.search(Review, reviewee=user_id)
    if reviews is None:
        return jsonify([])
    for review in reviews:
        all_reviews.append(review.to_dict())

    sorted_list = sorted(all_reviews, key=lambda d: d['created_at'], reverse=True)
    return jsonify(sorted_list)

@app_views.route('/reviews', strict_slashes=False, methods=['POST'])
@auth.login_required
def create_review():
    """This creates a new review instance"""
    if not request.json:
        return jsonify("Not a valid json"), 400
    review_dict = request.get_json()
    if "text" not in review_dict:
        return jsonify("Please include review text"), 400
    if "reviewer" not in review_dict:
        review_dict['reviewer'] = auth.current_user().id
    if "reviewee" not in review_dict:
        return jsonify("Please include a reviewee"), 400
    if "star" not in review_dict:
        return jsonify("Please include a star rating"), 400

    if review_dict['reviewer'] == review_dict['reviewee']:
        return jsonify("You cannot leave a review for yourself"), 400

    if len(review_dict['text']) < 2:
        return jsonify("Please include a text"), 400

    model = Review(**review_dict)
    model.save()
    return jsonify(model.to_dict()), 201

@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
@auth.login_required
def update_review(review_id):
    """This updates the attributes of a review"""
    if not request.json:
        return jsonify("Not a valid json"), 400
    review_dict = request.get_json()
    if 'text' in review_dict:
        try:
            text = review_dict['text']
            text.encode('ascii')
        except Exception:
            return jsonify(f"Invalid character found in review"), 400
    obj = storage.get('Review', review_id)
    if obj is None:
        return jsonify("No review found"), 404
    for key, val in review_dict.items():
        setattr(obj, key, val)
        obj.save()
    return jsonify(obj.to_dict())

@app_views.route('/reviews/<reviews_id>', strict_slashes=False, methods=['DELETE'])
@auth.login_required
def delete_review(review_id):
    """This destroy a review frm storage based on id"""
    obj = storage.get('Review', review_id)
    if obj is None:
        return jsonify("No review found"), 404
    obj.delete()
    return "{}"

@app_views.route('/review_eligibility', strict_slashes=False, methods=['POST'])
def check_create_review_eligibility():
    """This checks if a user is eligible to post a review"""
    if not request.json:
        return jsonify("Not a valid json"), 400
    requestDict = request.get_json()
    if "reviewer" not in requestDict:
        return jsonify("Please include a reviewer"), 400
    if requestDict['reviewer'] == None:
        return jsonify({"message": "false"}), 200
    if "reviewee" not in requestDict:
        return jsonify("Please include the reviewee id")

    if requestDict['reviewer'] == requestDict['reviewee']:
        return jsonify({"message": "false"})
    
    nots = storage.search("Notification", sender=requestDict['reviewer'], user_id=requestDict['reviewee'])
    if not nots or len(nots) == 0:
        return jsonify({"message": "false"}), 200
    else:
        return jsonify({"message": "true"}), 200