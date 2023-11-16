#!/usr/bin/python3

import requests
from os import getenv
from api.blueprint import app_views, auth
from models import storage
from flask import jsonify, request
from models.notification import Notification
from api.blueprint.Mailing.controller import runner
from datetime import datetime, timedelta

base_url = 'https://api.ng.termii.com/api'
api_key = getenv("TERMII_API_KEY")
headers = {'Content-Type': 'application/json'}

@app_views.route('/get_all_notifications', strict_slashes=False)
@auth.login_required(role=['admin'])
def get_all_nots():
    """This returns a list of all notifications"""
    nots_list = []
    for key, obj in storage.all(Notification).items():
        nots_list.append(obj.to_dict())

    return jsonify(nots_list), 200

@app_views.route('/get_user_notifications', strict_slashes=False)
@auth.login_required
def get_user_nots():
    """This returns the notification of a user"""
    user = auth.current_user()

    user_not = []
    user_nots = storage.search(Notification, user_id=user.id)
    # ttl = 24 * 60 * 60 * 1000   # 24 hours
    for obj in user_nots:
        # valid_period = obj.updated_at + timedelta(seconds = ttl)
        # if valid_period < datetime.now():
        #     continue
        # else:
        user_not.append(obj.to_dict())
    sorted_list = sorted(user_not, key=lambda d: d['created_at'], reverse=True)
    return jsonify(sorted_list), 200

@app_views.route('/send_notification', strict_slashes=False, methods=['POST'])
@auth.login_required
def create_not():
    """This creates and sends a notification message to the specified user"""
    if not request.json:
        return jsonify("Not a valid json"), 400

    sender = auth.current_user()

    requestDict = request.get_json()
    if "to" not in requestDict:
        return jsonify("Please include Recipient id with key 'to'"), 400
    if "type" not in requestDict:
        return jsonify("Please include the sms type with key 'type'"), 400

    user = storage.get("User", requestDict['to'])
    if user == None:
        return jsonify("No user found with id {}".format(requestDict['to'])), 400

    if requestDict['type'] in ['inspection_request', 'inspection_accepted', 'inspection_denied',
                            'inspection_booked']:
        if "item_id" not in requestDict:
            return jsonify("Please include an item_id"), 400

        itemId = requestDict['item_id']
        house = storage.get("House", itemId)

        if requestDict['type'] == "inspection_request":
            message = f"An inquiry has been made on your {house.apartment} at {house.name}, please come confirm if the apartment is still available "
            text_url = "https://unikrib.com/static/notification-page.html"
        
        elif requestDict['type'] == "inspection_accepted":
            if "not_id" not in requestDict:
                return jsonify("Please include a not_id"), 400
            nots = storage.get(Notification, requestDict['not_id'])
            dic = {"response": 'accepted'}
            nots.update(**dic)
            message = f"Hello {user.first_name}, \nYour inspection request has been accepted, please come contact the agent "
            text_url = 'https://unikrib.com/static/Apartment-info-page.html?id=' + nots.item_id

        elif requestDict['type'] == "inspection_booked":
            message = f"{sender.first_name} has booked an inspection on your {house.apartment} apartment at {house.name} and contact you soon for inspection"
            text_url = ''
        
        elif requestDict['type'] == "inspection_denied":
            if "not_id" not in requestDict:
                return jsonify("Please include a not_id"), 400
            nots = storage.get(Notification, requestDict['not_id'])
            dic = {"response": 'denied'}
            nots.update(**dic)
            message = f"Hello {user.first_name}, your inspection request at {house.apartment} in {house.name} has been denied, come check out more apartments "
            text_url = "https://unikrib.com/static/Apartment-page.html"
    
    elif requestDict['type'] == "new_review":
        itemId = None
        message = f"A new review has been added for you. visit your profile page for more"
    else:
        return jsonify("Invalid type, type not recognized"), 400

    # create Notification
    model = Notification(user_id=user.id, text=message, category=requestDict['type'], sender=sender.id, item_id=itemId)
    model.save()

    # parse phone no to include country code
    phone = str(user.phone_no)
    if phone[0] == '0':
        phone = '+234' + phone[1:]
    elif phone.startswith('+234') or phone.startswith('234'):
        phone = phone
    elif int(phone[0]) > 0:
        phone = '+234' + phone

    if requestDict['type'] in ['inspection_request', 'inspection_accepted', 'inspection_booked']:
        # send sms
        url = base_url + '/sms/send'
        message += text_url
        data = {"api_key": api_key, "to": phone, "from": "Unikrib", "sms": message, "type": "plain",
                "channel": "dnd"}
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            print("sms sent to {}".format(user.phone_no))
        else:
            print("Error message", res.text, res.status_code)

    if requestDict['type'] in ['inspection_request', 'inspection_accepted', 'inspection_denied']:
        # send email
        try:
            res2 = runner.sendNotification(user.email, user.first_name, requestDict['type'], itemId)
            if res2["status_code"] == 200:
                print("email sent to {}".format(user.phone_no))
            else:
                return jsonify("An error occured"), 404
        except Exception as e:
            print("Error sending mail")
            pass

    return jsonify("Notification created successfully"), 200

@app_views.route('/notifications/<not_id>', strict_slashes=False, methods=['PUT'])
@auth.login_required
def update_not(not_id):
    """This updates the attributes of a notification"""
    if not request.json:
        return jsonify("Not a valid json"), 400
    nots = storage.get(Notification, not_id)
    if nots is None:
        return jsonify("Notification not found"), 404
    not_dict = request.get_json()
    for key, val in not_dict.items():
        setattr(nots, key, val)
        nots.save()
    return jsonify(nots.to_dict()), 200

@app_views.route('/delete_notification/<not_id>', strict_slashes=False, methods=['DELETE'])
@auth.login_required
def delete_nots(nots_id):
    """This destroys a Notification instance"""
    nots = storage.get(Notification, nots_id)
    if nots is None:
        return jsonify("Notification not found"), 400
    
    nots.delete()
    return jsonify({}), 200
