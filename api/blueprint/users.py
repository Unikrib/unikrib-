#!/usr/bin/python3

import bcrypt
from models import storage, User, Code, Notification
from api.blueprint import app_views, auth, manager
from flask import request, jsonify, redirect
from settings.redactor import Redacter
from api.blueprint.upload_image import cloudinary
from api.blueprint.Mailing.controller import runner


fields = ["password", "email", "phone_no"]
format = Redacter(fields)
frontAPI = "https://unikrib.com"


@app_views.route('/users', strict_slashes=False)
@auth.login_required(role="admin")
def get_all_users():
    """This returns a list of all the user objects in storage"""
    user_list = []
    for key, obj in storage.all(User).items():
        user = format.filter_datum(",", obj.to_dict())
        user_list.append(user)

    return jsonify(user_list)

@app_views.route('/user/profile', strict_slashes=False)
@auth.login_required
def get_profile():
    """This returns the profile of the current user"""
    user = auth.current_user()
    format = Redacter(['password'])
    user = format.filter_datum(",", user.to_dict())
    return jsonify(user)

@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """This returns a user based on id"""
    user = storage.get('User', user_id)
    if user is None:
        return jsonify("No user found"), 404
    if user.user_type == 'agent':
        fields = ["password", "email"]
        format = Redacter(fields)
        user = format.filter_datum(",", user.to_dict())
    else:
        format = Redacter(["password", "email"])
        user = format.filter_datum(",", user.to_dict())
    
    return jsonify(user)

@app_views.route('/stats/users', strict_slashes=False)
def type_count():
    """This returns the count of all user-types in storage"""
    agent = len(storage.search(User, user_type='agent'))
    vendor = len(storage.search(User, user_type='vendor'))
    sp = len(storage.search(User, user_type='sp'))
    stats = {"agent": agent, "vendor": vendor, "sp": sp}
    return jsonify(stats)

@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """This creates a new user and stores it"""
    if not request.json:
        return jsonify("Not a valid Json"), 400
    if "email" not in request.json:
        return jsonify("Request must include email"), 400
    if "password" not in request.json:
        return jsonify("Request must include password"), 400
    user_dict = request.get_json()
    if user_dict['email'] == "":
        return jsonify("Please include an email"), 400
    if "@" not in user_dict['email']:
        return jsonify("Please enter a valid email"), 400
    if user_dict['password'] == "":
        return jsonify("Please include a password"), 400
    
    email = user_dict['email']
    user = storage.search('User', email=email.lower())
    if user != []:
        return jsonify("This email is already registered"), 400

    for key, val in user_dict.items():
        if key == 'password':
            val = val.encode()
            val = bcrypt.hashpw(val, bcrypt.gensalt())
            user_dict[key] = val
        if key == 'phone_no':
            phone = val
            if phone[0] == '0':
                phone = '+234' + phone[1:]
            elif phone.startswith('+234') or phone.startswith('234'):
                phone = phone
            elif int(phone[0]) > 0:
                phone = '+234' + phone
            user_dict[key] = phone
        else:
            user_dict[key] = val.strip()
    if 'whatsapp_no' not in user_dict:
        user_dict['whatsapp_no'] = user_dict.get('phone_no', None)

    try:
        user = User(**user_dict)
        user.save()
    except Exception as e:
        try:
            msg = str(e).split(')')[1][1:]
            msg = msg.split(",")[1]
        except:
            msg = str(e)
        return jsonify(str(msg)), 400
    token = manager.create_session(user.id)

    # send verify mail
    res = runner.sendVerifyLink(user.email, user.first_name, user.id)

    # store the code
    code = res["code"]
    code_dict = {"code": code, "user_id": user.id}
    obj = Code(**code_dict)
    obj.save()

    return jsonify({"message": f"Welcome ${user.first_name}, Please visit your email to complete your verification",
                    "token": token,
                    "id": user.id,
                    "user_type": user.user_type,
                    "first_name": user.first_name}), 201

@app_views.route('/auth/login', strict_slashes=False, methods=['POST'])
def user_login():
    """This creates a session for a user and returns the authorization token
    """
    if not request.json:
        return jsonify("Not a valid json"), 400
    if "email" not in request.json:
        return jsonify("Include an email in request"), 400
    if "password" not in request.json:
        return jsonify("Include a password in request"), 400

    user_dict = request.get_json()
    email = user_dict.get('email')
    password = user_dict.get('password')
    
    if not email:
        return jsonify("Please include an email"), 400
    if not password:
        return jsonify("Please include a password"), 400

    user = storage.search('User', email=email)
    if not user:
        return jsonify("No user with this email found"), 404

    user = user[0]
    password = password.strip()

    password = password.encode()
    try:
        user_pass = user.password.encode()
    except:
        user_pass = user.password

    if bcrypt.checkpw(password, user_pass):
        token = manager.create_session(user.id)
        if not user.com_res:
            message = f"Welcome back {user.first_name}, please complete your sign up"
            signup_complete = False
        else:
            message = f"Welcome back {user.first_name}"
            signup_complete = True
        return jsonify({"message": message,
                        "token": token,
                        "signup_complete": signup_complete,
                        "id": user.id,
                        "user_type": user.user_type,
                        "first_name": user.first_name})
    else:
        return jsonify("Incorrect password"), 400

@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
@auth.login_required
def update_user(user_id):
    """This updates the attributes of a user"""
    if not request.json:
        return jsonify("Not a valid Json"), 400
    new_dict = request.get_json()
    obj = storage.get('User', user_id)
    if obj is None:
        return jsonify("No user found"), 404
    if "password" in new_dict:
        passwd = new_dict['password']
        passwd = passwd.encode()
        passwd = bcrypt.hashpw(passwd, bcrypt.gensalt())
        new_dict['password'] = passwd
    if 'phone_no' in new_dict:
        phone = str(new_dict['phone_no'])
        if phone[0] == '0':
            phone = '+234' + phone[1:]
        elif phone.startswith('+234') or phone.startswith('234'):
            phone = phone
        elif int(phone[0]) > 0:
            phone = '+234' + phone
        new_dict['phone_no'] = phone
    if 'whatsapp_no' in new_dict:
        phone = new_dict['whatsapp_no']
        if phone[0] == '0':
            phone = '+234' + phone[1:]
        elif phone.startswith('+234') or phone.startswith('234'):
            phone = phone
        elif int(phone[0]) > 0:
            phone = '+234' + phone
        new_dict['whatsapp_no'] = phone


    obj.update(**new_dict)
    obj.save()
    user = format.filter_datum(",", obj.to_dict())
    # print(f"${user['first_name']} has been updated")
    return jsonify(user)

@app_views.route('/users/email', strict_slashes=False, methods=['PUT'])
def change_pass():
    """This updates the user password after the neccessary authentications"""
    if not request.json:
        return jsonify("Not a valid json"), 400
    if "email" not in request.json or "password" not in request.json:
        return jsonify("Missing email/password"), 400

    new_dict = request.get_json()
    user = storage.search(User, email=new_dict.get('email'))
    if user is None or len(user) == 0:
        return jsonify("Email not found"), 404
    obj = user[0]
    
    password = new_dict.get("password")
    password = password.encode()
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    dic = {"password": password,
            "reset_code": None}
    obj.update(**dic)
    token = manager.create_session(obj.id)
    return jsonify({
        "message": "Password changed successfully",
        "id": obj.id,
        "user_type": obj.user_type,
        "token": token})

@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
# @auth.login_required
def delete_user(user_id):
    """This deletes a user from storage"""
    if user_id == 'current':
        request_dict = request.get_json()
        obj = storage.search(User, **request_dict)
        if obj is None or obj == []:
            return jsonify("Pleae try again")
        else:
            obj[0].delete()
            return jsonify("Incomplete user removed"), 200
    obj = storage.get('User', user_id)
    if obj is None:
        return jsonify("User not found"), 404
    if obj.avatar and len(obj.avatar) > 50:
        try:
            fields = obj.avatar.split('/')
            public_id = fields[7] + '/' + fields[8][:-4]
            cloudinary.uploader.destroy(public_id)
        except Exception as e:
            print("Error: ", e)
            pass
    obj.delete()
    return {}

@app_views.route('/logout', strict_slashes=False, methods=['DELETE'])
@auth.login_required
def user_logout():
    """This destroys a user session_token"""
    user = auth.current_user()
    manager.delete_token(user.id)
    return jsonify({"message": "You have been succesfully logged out"})

@app_views.route('/user/<user_id>/verify-email', strict_slashes=False, methods=['GET'])
def verify_email(user_id):
    """This verifies the link sent to the email of a user"""
    code = request.args.get('code', None)
    if code is None:
        return False

    stored_code = storage.search(Code, user_id=user_id)
    if stored_code == []:
        return jsonify({"error": "The link has expired"})

    if code == stored_code[0].code:
        
        # Send Welcome mail to the verified user
        user = storage.get('User', user_id)
        if user is None or user == []:
            return jsonify({'error': 'User not found'})

        res = runner.sendWelcome(user.email, user.first_name)

        # change user status to verified
        # update_dict = {"isVerified": True}
        # user.update(**update_dict)

        # delete the stored code from storage
        codes = Code()
        codes.delete_code(user.id)

        # Redirect the user to the corresponding page
        if user.user_type == 'vendor':
            return redirect(f'{frontAPI}/static/product-page.html', 302)
        elif user.user_type == 'sp':
            return redirect(f'{frontAPI}/static/service-page.html', 302)
        else:
            return redirect(f'{frontAPI}/static/Apartment-page.html', 302)
        
    else:
        # print("code: {}, stored_code: {}".format(code, stored_code))
        return jsonify({"error": "The link is invalid"})

@app_views.route('/users/reset-password', strict_slashes=False, methods=['POST'])
def send_reset_code():
    """This sends a reset otp to the user to confirm their identity"""
    if not request.json:
        return jsonify({"Error": "Invalid request"}), 400
    if "email" not in request.json:
        return jsonify({"error": "Missing email"}), 400

    reqDict = request.get_json()
    email = reqDict.get("email")
    user = storage.search(User, email=email)
    if user is None or len(user) == 0:
        return jsonify("Email not found"), 404

    # send OTP mail
    res = runner.resetPassword(email, user[0].first_name)
    if res['status_code'] != 200:
        print("Error", res.message)
    if res['status_code'] == 200:
        code = res.get("otp")
        if code:
            dic = {"reset_code": code}
            user[0].update(**dic)
        return jsonify("OTP sent, please check your email"), 200
    else:
        print("Error", res.message)
        return jsonify("Service unavailable now, please try again later"), 404

@app_views.route('/users/confirm-reset-code', strict_slashes=False, methods=['POST'])
def confirm_code():
    """This confirms the user inputted the correct code"""
    if not request.json:
        return jsonify("Not a valid json"), 400
    if "code" not in request.json:
        return jsonify("Missing code")
    if "email" not in request.json:
        return jsonify("Missing email"), 400
    
    reqDict = request.get_json()
    code = reqDict.get("code")
    email = reqDict.get("email")
    if code == "" or email == "":
        return jsonify("Missing code/email"), 400
    user = storage.search(User, email=email)
    stored_code = user[0].reset_code

    if code == stored_code:
        dic = {'reset_code': "Valid"}
        user[0].update(**dic)
        return jsonify("code valid"), 200
    else:
        return jsonify("Invalid code"), 400

@app_views.route('users/verify', strict_slashes=False, methods=['POST'])
# @auth.login_required
def user_verification():
    if not request.json:
        return jsonify("Not a valid json"), 400
    
    user_data = request.get_json()

    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    face_image = user_data.get('face_image')
    id_image = user_data.get('id_image')
    email = user_data.get('email')

    params = {'first_name': first_name, 'last_name': last_name,
              'face_image': face_image, 'id_image': id_image, 'email': email}
    for key, val in params.items():
        if not val:
            return jsonify(f'Please include the required {key} field'), 400

    user = storage.search('User', email=email)
    if user:
        user = user[0]
    else:
        return jsonify("No user with this email found"), 400  

    res = runner.userVerification(first_name=first_name, last_name=last_name,
                                  face_image=face_image,
                                  id_image=id_image, user_id=user.id)
    if res.get('status_code') == 200:
        setattr(user, 'isVerified', 'pending')
        user.save()

        return jsonify("User verification submitted successfully, please wait 24 hours for confirmation"), 200
    else:
        return jsonify("An error occured while submitting request, please try again later"), 404
    
@app_views.route('/verify_user/<user_id>/<text>', strict_slashes=False, methods=['GET'])
# This endpoint should be reserved for admins only
def accept_or_deny_user_verification(user_id, text):
    if not user_id or not text:
        return jsonify('Incorrect url'), 400
    
    user = storage.get('User', user_id)
    text = text.lower()
    if not user:
        return jsonify('User not found'), 404
    
    if text == 'accept':
        setattr(user, 'isVerified', True)
        user.save()
        text = f"Congratulations {user.first_name}, Your profile has been verified."
        notif = Notification(user_id=user_id, text=text, category='Verification successful')
        notif.save()
        return jsonify('User profile has been verified successfully')
    elif text == 'deny':
        setattr(user, 'isVerified', False)
        user.save()
        text = f"Dear {user.first_name}, Your profile verification request has been denied due to inconsistency in your data"
        notif = Notification(user_id=user_id, text=text, category='Verification denied')
        notif.save()
        return jsonify('User verification has been denied')
    else:
        return jsonify('Invalid command, please use \'accept\' or \'deny\''), 400
    