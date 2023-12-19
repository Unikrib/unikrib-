#!/usr/bin/python3

from api.blueprint import app_views
from models.school import School
from models import storage
from flask import jsonify

@app_views.route('/schools', methods=['GET'], strict_slashes=False)
def get_all_schools():
    """This returns a list of all schools"""
    schools = storage.all("School")
    schools = [school.to_dict() for key, school in schools.items()]
    return jsonify(schools), 200

@app_views.route('/schools/<school_id>', methods=['GET'], strict_slashes=False)
def get_school(school_id):
    """This returns a school by id"""
    school = storage.get("School", school_id)
    if not school:
        return jsonify("School not found"), 404
    return jsonify(school.to_dict()), 200
