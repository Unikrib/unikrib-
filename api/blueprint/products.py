#!/usr/bin/python3

from api.blueprint import app_views, auth
from flask import jsonify, request
from models import storage, Product
# from models.v2.product import Product
from api.blueprint.upload_image import cloudinary

@app_views.route('/products', strict_slashes=False)
def all_products():
    """This returns a list of curated products in storage"""
    avail = request.args.get('available', 'yes')
    pgnum = request.args.get('pgnum', 1)
    pgsize = request.args.get('pgsize', 10)
    all_prod = []
    if avail and pgnum and pgsize:
        products = storage.paginate_query(Product, pgnum, pgsize, available=avail)
    elif pgnum and pgsize:
        products = storage.paginate_query(Product, pgnum, pgsize)
    else:
        products = storage.all(Product)

    all_prod = [prod.to_dict() for prod in products]
    # for prod in products:
    #     all_prod.append(prod.to_dict())
    return jsonify(all_prod)

@app_views.route('/products/<product_id>', strict_slashes=False)
@auth.login_required
def get_product(product_id):
    """This returns a product based on id"""
    obj = storage.get('Product', product_id)
    if obj == None:
        return jsonify("Product not found"), 404
    return jsonify(obj.to_dict())

@app_views.route('/categories/<category_id>/products', strict_slashes=False)
def categroy_prod(category_id):
    """This returns a list of all the products in a category"""
    pgnum = request.args.get('pgnum', None)
    pgsize = request.args.get('pgsize', None)
    avail = request.args.get('available', 'yes')

    cat_prod = []

    dic = {"available": avail, "category_id": category_id}
    if pgnum and pgsize:
        products = storage.paginate_query(Product, pgnum, pgsize, **dic)
    # elif not avail and limit:
    #     print("Only limit is present")
    #     dic['available'] = "no"
    #     products = storage.search_paginate(Product, limit, cursor, nav, **dic)
    else:
        products = storage.search('Product', **dic)
    if products is None:
        return []
    for product in products:
        cat_prod.append(product.to_dict())
    sorted_list = sorted(cat_prod, key=lambda d: d['name'])
    print("Length of products returned = ", len(sorted_list))
    return jsonify(sorted_list)

@app_views.route('/users/<user_id>/products', strict_slashes=False)
@auth.login_required
def user_products(user_id):
    """This returns a list of all the products under a vendor"""
    obj = storage.get('User', user_id)
    if obj == None:
        return jsonify("No user with this id found"), 404
    if obj.user_type != 'vendor':
        return jsonify("User not a vendor"), 400

    user_prod = []
    products = storage.search('Product', owner_id=user_id)
    for product in products:
        user_prod.append(product.to_dict())
    return jsonify(user_prod)

@app_views.route('/products', strict_slashes=False, methods=['POST'])
@auth.login_required(role=["vendor", "admin"])
def create_prod():
    """This creates a new product in storage"""
    if not request.json:
        return jsonify("Not a valid JSON"), 400
    request_dict = request.get_json()
    if "name" not in request_dict:
        return jsonify("Please include a product name"), 400
    if "owner_id" not in request_dict:
        return jsonify("Please include an owner_id"), 400
    if "category_id" not in request_dict:
        return jsonify("Please include a category_id"), 400
    if "price" not in request_dict:
        return jsonify("Please include the product price"), 400
    # if "delivery" in request_dict:
    #     if len(request_dict['delivery']) > 3:
    #         return jsonify("Invalid value for \"delivery\", Please send only \"yes\" or \"no\""), 400

    user = auth.current_user()
    if len(storage.search(Product, owner_id=user.id)) > 4:
        return jsonify("Maximum number of uploads reached, please buy premium package to upload more"), 403
    try:
        model = Product(**request_dict)
        model.save()
    except Exception as e:
        try:
            msg = str(e).split(')')[1][1:]
            msg = msg.split(",")[1]
        except:
            msg = str(e)
        return jsonify(f"Error encountered while uploading product: {msg}"), 400
    return jsonify(model.to_dict())

@app_views.route('/products/<product_id>', strict_slashes=False, methods=['PUT'])
@auth.login_required(role=["vendor", "admin"])
def update_product(product_id):
    """This updates a product instance"""
    if not request.json:
        return jsonify("Not a valid json"), 400
    obj = storage.get('Product', product_id)
    if obj == None:
        return jsonify("No product found"), 404
    prod_dict = request.get_json()

    for key, val in prod_dict.items():
        try:
            setattr(obj, key, val)
            obj.save()
        except Exception as e:
            try:
                msg = str(e).split(')')[1][1:]
                msg = msg.split(",")[1]
            except:
                msg = str(e)
            return jsonify(f"Error encountered while updating product: {msg}"), 400
    return jsonify(obj.to_dict())

@app_views.route('/product-search', strict_slashes=False, methods=['POST'])
def search_product():
    """This searches all the products in storage against some criteria"""
    if not request.json:
        return jsonify("Not a valid JSON"), 400

    return_list = []

    searchDict = request.get_json()
    location = searchDict['location']
    category = searchDict['category']
    query = searchDict['query']

    if category == 'all':
        possible_products = storage.all(Product).values()
    else:
        possible_products = storage.search(Product, category_id=category)

    for product in possible_products:
        owner = storage.get('User', product.owner_id)
        if owner.com_res == location or location == 'all':
            search_queries = query.lower().split()
            if len(search_queries) == 1:
                if search_queries[0].endswith('s'):
                    search_queries[0] = search_queries[0][:-1]
            for word in search_queries:
                if word in product.name.lower() or word in product.features.lower():
                    return_list.append(product.id)
    
    count_dict = {}
    for num in return_list:
        count_dict[num] = return_list.count(num)
    all_dict = dict(sorted(count_dict.items(), key=lambda x:x[1], reverse=True))
    new_list = []
    for prodId in all_dict:
        obj = storage.get('Product', prodId)
        new_list.append(obj.to_dict())
    return jsonify(new_list)

@app_views.route('/products/<product_id>', strict_slashes=False, methods=['DELETE'])
@auth.login_required(role=["vendor", "admin"])
def delete_product(product_id):
    """This removes a product instance from storage"""
    obj = storage.get('Product', product_id)
    if obj == None:
        return jsonify("No product found"), 404

    images = [obj.image1, obj.image2, obj.image3]
    for image in images:
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
    return '{}', 200
    