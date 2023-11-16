#!/usr/bin/python3

from api.blueprint import app_views
from models import storage
from models.service_category import ServiceCategory
from flask import jsonify, abort, request

@app_views.route('/service-categories', strict_slashes=False)
def all_serv_cats():
    """This returns a list of all service categories"""
    all_cats = []
    for key, obj in storage.all(ServiceCategory).items():
        all_cats.append(obj.to_dict())
    sorted_list = sorted(all_cats, key=lambda d: d['name'])
    return jsonify(sorted_list)

@app_views.route('/service-categories/<cat_id>', strict_slashes=False)
def get_serv_cat(cat_id):
    """This returns a category by id"""
    obj = storage.get('ServiceCategory', cat_id)
    if obj == None:
        return jsonify("No category found"), 404
    return jsonify(obj.to_dict())