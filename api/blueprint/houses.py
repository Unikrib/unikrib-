#!/usr/bin/python3

import uuid
import redis
import requests
import threading
from os import getenv
from models import storage
from models.house import House
from flask import jsonify, request
from api.blueprint import app_views, auth
from models.transaction import Transaction
from models.notification import Notification
from api.blueprint.upload_image import cloudinary

base_url = 'https://api.ng.termii.com/api'
api_key = getenv("TERMII_API_KEY")
headers = {'Content-Type': 'application/json'}

redis_url = getenv('REDIS_URL')
redis_client = redis.Redis(redis_url, db=0)
terminate_thread = False


def prompt_apartment_deletion(houseId):
    """This prompts the agent to delete the apartment if it is no
    longer available"""
    print("Scheduled job started: " + houseId)
    house = storage.get(House, houseId)
    if house is None or house == []:
        return
    
    agent = storage.get("User", house.owner_id)

    # send sms
    url = base_url + '/sms/send'
    if getenv('HOST') == 'localhost':
        href = 'http://localhost:8001/static/apartment-info-page2.html?id=' + house.id
    else:
        href = 'https://unikrib.com/static/apartment-info-page2.html?id=' + house.id
    message = f'Good day {agent.first_name},\nThis is a reminder to delete the apartment {house.name} '
    message += f'if it is no longer available. \nClick the link below to delete the apartment. {href}'
    data = {"api_key": api_key, "to": agent.phone_no, "from": "Unikrib", "sms": message, "type": "plain",
                "channel": "generic"}
    res = requests.post(url, headers=headers, json=data)
    if res.status_code != 200:
        print("Error sending apartment deletion prompt to agent " + house.id)
        print(res.status_code, res.text)
    else:
        global terminate_thread
        terminate_thread = True
        print(f"sms sent successfully to agent: {agent.id} on apartment: {house.id}")

def callback(sender_id, sender_name, houseId, reference=None):
    """This verifies the status of transaction and sends 
        a notification to apartment owner if transaction is successful"""

    if reference is None:
        return jsonify({"message": False}), 200
    house = storage.get("House", houseId)
    owner = storage.get("User", house.owner_id)

    # send the house owner a notification
    message = f"{sender_name} has booked an inspection on your {house.apartment} apartment at {house.name} and will contact you soon for inspection."
    if reference == 'physical':
        message += "\nInpection fee to be paid physically"
    else:
        message += "\nInspection fee has been paid online and will be sent to you soon"
    model = Notification(user_id=house.owner_id, text=message, category="inspection_booked", sender=sender_id, item_id=houseId)
    model.save()
    # Also send an sms to the house owner
    base_url = 'https://api.ng.termii.com/api'
    api_key = getenv("TERMII_API_KEY")
    url = base_url + '/sms/send'
    data = {"api_key": api_key, "to": owner.phone_no, "from": "Unikrib", "sms": message, "type": "plain",
            "channel": "generic"}
    res = requests.post(url, headers={ 'Content-Type': 'application/json' }, json=data)
    if res.status_code == 200:
        print("House owner has been notified of recent booking")
    else:
        print("Error encountered while notifying owner of recent booking: ", res.text, res.status_code)

    # schedule an sms notification for the agent in 3 days time
    from api.app import run_scheduler
    threading.Thread(target=lambda: run_scheduler(prompt_apartment_deletion, house.id)).start()
    print("Job has been scheduled...")

def confirm_inspection_occured(house_id, user_id):
    """This confirms from the agent if inspection has occured"""
    house = storage.get(House, house_id)
    if house is None:
        return
    
    agent = storage.get("User", house.owner_id)
    user = storage.get("User", user_id)
    agent_not = Notification(user_id=agent.id, text=f"Did inspection with {user.first_name} at {house.name} occur?",
                        item_id=house.id, category="confirm_inspection")
    user_not = Notification(user_id=user.id, text=f"Did inspection with {user.first_name} at {house.name} occur?",
                            item_id=house.id, category="confirm_inspection")
    agent_not.save()
    user_not.save()
    
    # send sms to both user and agent
    url = base_url + '/sms/send'
    message = f"This is to confirm if the inspection with {user.first_name} occured at {house.apartment}, {house.name}"
    data = {"api_key": api_key, "to": agent.phone_no, "from": "Unikrib", "sms": message, "type": "plain",
                "channel": "generic"}
    res = requests.post(url, data=data, headers=headers)
    if res.status_code != 200:
        print(res.status_code, res.text)

@app_views.route('/houses', strict_slashes=False)
def get_all_houses():
    """This returns a list of all the houses in storage"""
    houses_list = []
    # limit = request.args.get('limit', None)
    # nav = request.args.get('nav', None)
    # cursor = request.args.get('cursor', None)
    pgnum = request.args.get('pgnum', None)
    pgsize = request.args.get('pgsize', None)

    if pgsize or pgnum:
        pgnum = request.args.get('pgnum', None)
        pgsize = request.args.get('pgsize', None)
        houses = storage.paginate_query(House, pgnum, pgsize)
        for house in houses:
            houseDict = house.to_dict()
            owner = storage.get("User", house.owner_id)
            if owner.user_type != "agent":
                houseDict['owner_id'] = "2626708b-5f46-4bc3-8ae9-9371c1de57d4"
            houses_list.append(houseDict)
    else:
        for key, house in storage.all(House).items():
            houseDict = house.to_dict()
            owner = storage.get("User", house.owner_id)
            if owner.user_type != "agent":
                houseDict['owner_id'] = "2626708b-5f46-4bc3-8ae9-9371c1de57d4"
            houses_list.append(house.to_dict())
    houses_list = sorted(houses_list, key=lambda x: x['id'])
    return jsonify(houses_list)

@app_views.route('/houses/<house_id>', strict_slashes=False)
@auth.login_required
def get_house(house_id):
    """This return a house based on an id"""
    house = storage.get('House', house_id)
    if house is None:
        return jsonify("House not found"), 404
    houseDict = house.to_dict()
    owner = storage.get("User", house.owner_id)
    if owner.user_type != "agent":
        houseDict['owner_id'] = "2626708b-5f46-4bc3-8ae9-9371c1de57d4"
    house.no_clicks = house.no_clicks + 1
    house.save()
    return jsonify(houseDict), 200

@app_views.route('/users/<user_id>/houses', strict_slashes=False)
@auth.login_required
def get_agent_houses(user_id):
    """This returns a list of all the houses registered under an agent"""
    houses = []
    user = auth.current_user()
    if user_id == 'me':
        house_list = storage.search('House', owner_id=user.id)
    else:
        house_list = storage.search('House', owner_id=user_id)
        
    if house_list is None:
        return []
    for house in house_list:
        houses.append(house.to_dict())

    return jsonify(houses)

@app_views.route('/houses/stats', strict_slashes=False)
def get_stat():
    """This returns the number of all the houses in storage"""
    return jsonify(storage.count(House))

@app_views.route('/houses', strict_slashes=False, methods=['POST'])
@auth.login_required
def create_house():
    """This creates a new house in storage"""
    try:
        if not request.json:
            return jsonify("Not a valid json"), 400
        house_dict = request.get_json()
        try:
            int(house_dict['price'])
        except TypeError:
            return jsonify("Price must be a number"), 400
        # if "street_id" not in house_dict or house_dict["street_id"] == "":
        #     return jsonify("House must contain a street_id"), 400

        user = auth.current_user()
        apartment_types = ('Single-room', 'Self-contain', 'One-bedroom', 'Two-bedroom', 'Three-bedroom')
        if "apartment" in house_dict and house_dict.get("apartment") not in apartment_types:
            return jsonify("Invalid apartment type"), 400
        
        # if len(storage.search(House, owner_id=user.id)) > 4:
        #     return jsonify("Maximum number of uploads reached, please buy premium package to upload more"), 403
        # house_dict = request.get_json()
        if "owner_id" not in house_dict or house_dict['owner_id'] == "":
            house_dict['owner_id'] = user.id
        if house_dict["daily_power"] == "":
            house_dict["daily_power"] = 12
        if house_dict.get('newly_built', None):
            val = house_dict['newly_built'].lower() == "true"
            house_dict["newly_built"] = val
        if house_dict.get("security_available", None):
            val = house_dict['security_available'].lower() == "true"
            house_dict['security_available'] = val
        if house_dict.get("tiled", None):
            val = house_dict['tiled'].lower() == "true"
            house_dict['tiled'] = val
        if not house_dict.get("agent_fee") or house_dict["agent_fee"] == '':
            house_dict["agent_fee"] = None
        if 'school_id' not in house_dict:
            return jsonify('Please include school_id'), 400
        # if "school_id" not in house_dict:
        #     res = user.com_res
        #     school = storage.get("School", res.school_id)
        #     house_dict['school_id'] = school.id
        try:
            model = House(**house_dict)
            model.save()
        except Exception as e:
            try:
                msg = str(e).split(')')[1][1:]
                msg = msg.split(",")[1]
            except:
                msg = str(e)
            return jsonify(f"Error encountered while creating apartment: {msg}"), 400
        return jsonify(model.to_dict()), 201
    except Exception as e:
        return jsonify(str(e)), 404

@app_views.route('/houses/<house_id>', strict_slashes=False, methods=['PUT'])
@auth.login_required(role=["agent", "admin"])
def update_house(house_id):
    """This updates the attributes of a house based on id"""
    if not request.json:
        return jsonify("Not a valid json"), 400
    house_dict = request.get_json()
    obj = storage.get('House', house_id)
    if obj is None:
        return jsonify("House not found"), 404

    if house_dict.get('newly_built', None):
        val = house_dict['newly_built'].lower() == "true"
        house_dict["newly_built"] = val
    if house_dict.get("security_available", None):
        val = house_dict['security_available'].lower() == "true"
        house_dict['security_available'] = val
    if house_dict.get("tiled", None):
        val = house_dict['tiled'].lower() == "true"
        house_dict['tiled'] = val
    if not house_dict.get("agent_fee") or house_dict["agent_fee"] == '':
        house_dict["agent_fee"] = None

    for key, val in house_dict.items():
        try:
            setattr(obj, key, val)
            obj.save()
        except Exception as e:
            try:
                msg = str(e).split(')')[1][1:]
                msg = msg.split(",")[1]
            except:
                msg = str(e)
            return jsonify(f"Error encountered while updating apartment: {msg}"), 400
    return jsonify(obj.to_dict()), 200

@app_views.route('/houses/<house_id>', strict_slashes=False, methods=['DELETE'])
@auth.login_required(role=["agent", "admin"])
def delete_house(house_id):
    """This remove the house instance from storage"""
    obj = storage.get('House', house_id)
    if obj == None:
        return jsonify("Apartment was not found"), 404
    images = [obj.image1, obj.image2, obj.image3]
    for image in images:
        if image and len(image) > 50:
            try:
                fields = image.split('/')
                public_id = fields[7] + '/' + fields[8][:-4]
                cloudinary.uploader.destroy(public_id)
            except Exception as e:
                continue

    global terminate_thread
    terminate_thread = True

    # obj.delete()
    storage.delete(obj)
    storage.save()
    return {}, 201

@app_views.route('/houses/search', strict_slashes=False, methods=['POST'])
def search_house():
    """This receives a dict and returns houses that match the criteria"""
    if not request.json:
        return jsonify("Not a valid json"), 400
    search_dict = request.get_json()
    
    apartment = search_dict.get('apartment', None)
    min_price = int(search_dict.get('min_price', None))
    max_price = int(search_dict.get('max_price', None))
    env_id = search_dict.get('env_id', None)

    print(f"apartment: {apartment}, min: {min_price}, max: {max_price}, envid: {env_id}")

    if not env_id:
        return jsonify("Please include \"env_id\""), 400
    else:
        result = []
        objs = storage.listFilter(House, **search_dict)
        # objs = storage.search(House, env_id=env_id, apartment=apartment)
        print(objs)
        if not objs:
            return jsonify([])
        for obj in objs:
            if (obj.price >= min_price) and (obj.price <= max_price):
                result.append(obj.to_dict())
        return jsonify(result), 200

    streets = storage.search("Street", env_id=env)
    streetsId = []
    for street in streets:
        streetsId.append(street.id)
    result = []

    dic = {"apartment": apartment, "street_id": streetsId, "max_price": max_price, "min_price": min_price}
    for obj in storage.listFilter(House, **dic):
        result.append(obj.to_dict())
    return jsonify(result)

@app_views.route('/book_inspection', strict_slashes=False, methods=['POST'])
@auth.login_required
def book_inspection():
    if not request.json:
        return jsonify("Not a valid json"), 400
    data = request.get_json()
    if "itemId" not in data:
        return jsonify("Please include the apartment id"), 400
    itemId = data.get('itemId')
    user = auth.current_user()

    if "type" in data and data['type'] == "physical":
        house = storage.get("House", itemId)
        owner = storage.get("User", house.owner_id)
        callback(owner.id, owner.first_name, house.id, "physical")
        return jsonify({"message": True, "owner_phone": owner.phone_no}), 200

    url = "https://api.paystack.co/transaction/initialize"
    amount = 1000 * 100
    
    reference = str(uuid.uuid4())
    key = getenv('PAYSTACK_SECRET_KEY')
    autho = "Bearer " + key
    callback_url = data.get('callback_url', 'https://www.unikrib.com')

    res = requests.post(url, data={"amount": amount, "email": user.email, "reference": reference,
                        "callback_url": callback_url, "callback": verify_transaction(itemId)},
                        headers={"Authorization": autho, "content_type": "application/json"})
    if res.status_code == 200:
        res = res.json()
        model = Transaction(userId=user.id, itemId=itemId, reference=reference, status='started')
        model.save()
        # user_name = user.first_name + " " + user.last_name
        (res['data']['authorization_url'])
        # callback(user.id, user_name, itemId, reference)
        return jsonify(res['data']['authorization_url']), 200
    else:
        print(res.status_code, res.text)
        return jsonify("An error was encountered")

@app_views.route('/verify_payment/<item_id>', strict_slashes=False, methods=['GET'])
@auth.login_required
def verify_transaction(item_id):
    # print("Verify transaction called")
    user = auth.current_user()
    transaction = storage.search("Transaction", userId=user.id, itemId=item_id)
    if transaction is None or transaction == []:
        print("No transaction record found")
        return jsonify({"message": False}), 200
    
    house = storage.get("House", item_id)
    owner = storage.get("User", house.owner_id)
    transaction = transaction[0]
    
    if transaction.status == "success":
        return jsonify({"message": True, "owner_phone": owner.phone_no}), 200
    
    url = "https://api.paystack.co/transaction/verify/" + transaction.reference
    key = getenv('PAYSTACK_SECRET_KEY')
    autho = "Bearer " + key
    res = requests.get(url, headers={"Authorization": autho, "content_type": "application/json"})
    if res.status_code == 200:
        res = res.json()
        if res['data']['status'] == "success":
            transaction.status = "success"
            transaction.save()
            callback(user.id, user.first_name, house.id, transaction.reference)
            return jsonify({"message": True, "owner_phone": owner.phone_no}), 200
        else:
            return jsonify({"message": False}), 200
    else:
        return jsonify("Error encountered while verifying payment"), 404

@app_views.route('/get-trending-apartments', strict_slashes=False)
def get_trending():
    trend_dict = storage.sort_limit(House, 4)
    trending_aparts = []
    for house in trend_dict:
        trending_aparts.append(house.to_dict())
    return jsonify(trending_aparts)
