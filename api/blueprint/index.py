#!/usr/bin/python3

from api.blueprint import app_views
from flask import abort, jsonify, request
from models import storage, Product, House, Service, User
# from models.v2.product import Product
# from models.v2.house import House
# from models.v2.service import Service
# from models.v2.user import User

@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({"status": "ok"}), 200

@app_views.route('/unauthorized', strict_slashes=False)
def unauthorized():
    abort(401)

@app_views.route('/forbidden', strict_slashes=False)
def forbidden():
    abort(403)

@app_views.route('/count/<objects>', strict_slashes=False)
def count_objs(objects):
    """This returns the total number of items in storage"""
    page = request.args.get("page", None)
    if objects == 'products':
        dic = {'available': 'yes'}
        cat = request.args.get("cat", None)
        if cat:
            dic['category_id'] = cat
        objs = storage.search(Product, **dic)
        count = len(objs)
    elif objects == 'houses':
        if page == "hp":
            count = int(storage.count(House, "rooms_available"))
        else:
            count = int(storage.count(House))
    elif objects == 'services':
        cat = request.args.get("cat", None)
        if cat:
            count = len(storage.search(Service, category_id=cat))
        else:
            count = storage.count(Service)
    elif objects == 'users':
        agents = len(storage.search(User, user_type='agent'))
        vendors = len(storage.search(User, user_type='vendor'))
        sp = len(storage.search(User, user_type='sp'))
        return jsonify({'agent': agents, 'vendor': vendors, 'sp': sp})
    else:
        return jsonify("Invalid class!")
    return jsonify(count)