#!/usr/bin/python3

from api.blueprint import app_views
from models.category import Category
from models import storage
from flask import jsonify, request, abort

@app_views.route('/categories', strict_slashes=False)
def all_cats():
    """This returns a list of all categories"""
    all_cat = []
    for key, obj in storage.all(Category).items():
        all_cat.append(obj.to_dict())
    sorted_list = sorted(all_cat, key=lambda d: d['name'])
    return jsonify(sorted_list)

@app_views.route('/categories/<cat_id>', strict_slashes=False)
def get_cat(cat_id):
    """This returns a category based on id"""
    obj = storage.get('Category', cat_id)
    if obj == None:
        return jsonify("No category found"), 404
    return jsonify(obj.to_dict())