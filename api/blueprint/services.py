#!/usr/bin/python3

from api.blueprint import app_views, auth
from flask import jsonify,  request
from models import storage
from models.service import Service
from api.blueprint.upload_image import cloudinary

@app_views.route('/services', strict_slashes=False)
def all_services():
    """This returns a list of all services in storage"""
    all_serv = []
    pgnum = request.args.get('pgnum', 1)
    pgsize = request.args.get('pgsize', 10)

    services = storage.paginate_query(Service, pgnum, pgsize)
    for service in services:
        all_serv.append(service.to_dict())
    print(f"Pgnum: {pgnum}, pgsize: {pgsize}")
    # else:
    #     for key, obj in storage.all(Service).items():
    #         all_serv.append(obj.to_dict())
    # all_serv = sorted(all_serv, key=lambda x: x['id'])
    return jsonify(all_serv)

@app_views.route('/services/<service_id>', strict_slashes=False)
@auth.login_required
def get_service(service_id):
    """This returns a service based on id"""
    obj = storage.get('Service', service_id)
    if obj == None:
        return jsonify("service not found"), 404
    return jsonify(obj.to_dict())

@app_views.route('/users/<user_id>/services', strict_slashes=False)
@auth.login_required
def user_service(user_id):
    """This return the service associated with a user"""
    obj = storage.get('User', user_id)
    if obj == None:
        return jsonify("No user found"), 404

    service = storage.search(Service, owner_id=user_id)
    if service == [] or service is None:
        return jsonify([])
    return jsonify(service[0].to_dict())

@app_views.route('/service-categories/<cat_id>/services', strict_slashes=False)
def cat_services(cat_id):
    """This returns a list of all services in a category"""
    cat_serv = []
    pgnum = request.args.get('pgnum', 1)
    pgsize = request.args.get('pgsize', 10)

    dic = {"category_id": cat_id}
    # if limit:
    services = storage.paginate_query(Service, pgnum, pgsize, **dic)
    for service in services:
        cat_serv.append(service.to_dict())
    # else:
    #     for key, obj in storage.search(Service, category_id=cat_id).items():
    #         cat_serv.append(obj.to_dict())
    # cat_serv = sorted(cat_serv, key=lambda x: x['id'])

    return jsonify(cat_serv)

@app_views.route('/service-search', strict_slashes=False, methods=['POST'])
def search_services():
    """This searces for services that meet some criteria"""
    if not request.json:
        return jsonify("Not a valid json"), 400

    searchList = []

    search_dict = request.get_json()
    location = search_dict['location']
    category = search_dict['category_id']

    objs = storage.search(Service, category_id=category)
    if objs is None:
        return []
    for obj in objs:
        owner = storage.get('User', obj.owner_id)
        if owner.com_res == location or location == 'all':
            searchList.append(obj.to_dict())
    return jsonify(searchList)

@app_views.route('/services', strict_slashes=False, methods=['POST'])
@auth.login_required(role=["sp", "admin"])
def create_service():
    """This creates a new service in storage"""
    if not request.json:
        return jsonify("Not a valid JSON"), 400
    request_dict = request.get_json()
    if "category_id" not in request_dict:
        return jsonify("Please include a category_id"), 400
    if "owner_id" not in request_dict:
        return jsonify("Please include an owner_id"), 400
    model = Service(**request_dict)
    model.save()
    return jsonify(model.to_dict())

@app_views.route('/services/<service_id>', strict_slashes=False, methods=['PUT'])
@auth.login_required(role=["sp", "admin"])
def update_service(service_id):
    """This updates an instance of a service in storage"""
    obj = storage.get('Service', service_id)
    if obj == None:
        return jsonify("No service instance found"), 404
    request_dict = request.get_json()
    for key, val in request_dict.items():
        setattr(obj, key, val)
        obj.save()
    return jsonify(obj.to_dict())

@app_views.route('/services/<service_id>', strict_slashes=False, methods=['DELETE'])
@auth.login_required(role=["sp", "admin"])
def delete_service(service_id):
    """This removes a service instance from storage"""
    obj = storage.get('Service', service_id)
    if obj == None:
        return jsonify("No service found"), 404
    for image in [obj.image1, obj.image2, obj.image3, obj.image4, obj.image5]:
        if image and len(image) > 50:
            try:
                fields = image.split('/')
                public_id = fields[7] + '/' + fields[8][:-4]
                print(public_id)
                cloudinary.uploader.destroy(public_id)
            except Exception as e:
                print("Error: ", e)
                continue
    obj.delete()
    return '{}'
    