#!/usr/bin/python3

from api.blueprint import app_views
from models import storage
from models.environment import Environment
from flask import request, jsonify, abort

@app_views.route('/environments', strict_slashes=False)
def all_env():
    """This returns a list of all environments"""
    # print("Environment fetched from database.")
    all_env = []
    school = storage.search("School", name='UniBen')
    for obj in storage.search("Environment", school_id=school.id):
        all_env.append(obj.to_dict())
    sorted_list = sorted(all_env, key=lambda d: d['name'])

    return jsonify(sorted_list)

@app_views.route('/environments/<env_id>', strict_slashes=False)
def get_env(env_id):
    """This returns an environment based on id"""
    obj = storage.get('Environment', env_id)
    if obj is None:
        return jsonify("Environment does not exists"), 404
    return jsonify(obj.to_dict())

@app_views.route('/school/<school_id>/environments', strict_slashes=False)
def get_school_environments(school_id):
    """This returns all the environments in a school"""
    envs = storage.search("Environment", school_id=school_id)
    if not envs or len(envs) == 0:
        return jsonify("School not found"), 404
    envs = [env.to_dict() for env in envs]
    return jsonify(envs), 200
