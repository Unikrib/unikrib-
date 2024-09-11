import json
import uuid
from models import storage, School, Environment, Notification, Code, House
import requests
import time
from os import getenv
# from models.v1.school import School
# from models.v1.environment import Environment
# import webbrowser
from datetime import datetime, timedelta
# from models.notification import Notification
# from models.code import Code
# from models.house import House
from flask import jsonify
# from twilio.rest import Client

# api = "https://unikribmailer.onrender.com"
api = "https://unikribbackend.onrender.com/unikrib"
email = "akinwonjowodennisco+2@gmail.com"
firstName = "Dennis"

def send_mail():
    # check status
    url = api + '/mail-status'
    res = requests.get(url)
    print(res.text)

    print("______________")
    print("checking mail endpoint...")
    url = api + '/sendWelcome'
    user_id = 'fc643005-8614-4e95-ad06-c546c3c3fa89'

    data = {"email": email, "firstName": firstName, "user_id": user_id}
    # data = json.loads(data)

    res = requests.post(url, data=data)
    if res.status_code != 200:
        print("Error occured:", res.text)
        return None
    print("status code --> ", res.status_code)
    print("Content:", res.text)

    # code = res.json().get("code", None)
    # print("Code --> {}".format(code))
    # obj.save()
    return code

def verify_link(code):
    user_id = 'fc643005-8614-4e95-ad06-c546c3c3fa89'
    stored_code = storage.search("Code", user_id=user_id)
    if stored_code == []:
        print("No code found")
        return None
    
    if stored_code[0].code == code:
        print("Codes Match!!!")

    user = storage.search("User", id=user_id)
    if user == []:
        print("No user found")
        return None
    dic = {"isVerified": True}
    user[0].update(**dic)
    print("User verified: {}".format(user[0].isVerified))
    codes = Code()
    codes.delete_code(user_id)
    print("All done!")

def sendotp():
    print("Sending otp...")
    url = api + '/sendotp'
    res = requests.post(url, data={"email": email, "firstName":firstName})
    print(res.status_code)
    if res.status_code == 200:
        print("OTP sent succesfully")
        code = res.json().get("code")
        print(code)
        if code:
            dic = {"reset_code": code}
        return jsonify("OTP sent, please check your email"), 200
    else:
        return jsonify("Service unavailable now, please try again later"), 404

def test_search_paginate():
    dic = {"owner_id": "44891a67-9185-4731-83bc-4819d121c8d6"}
    init_houses = storage.search("House", **dic)
    print(len(init_houses), "have this owner")
    for house in init_houses:
        print(f"{house.name} --> {house.id}")
    print("___________________________________")
    print()

    all_apart = []
    dic = {"owner_id": "44891a67-9185-4731-83bc-4819d121c8d6"}
    houses = storage.search_paginate(House, 2, '52916830-3b08-4a0f-85f9-625ef4b03f53', 'prev', **dic)
    if houses is None:
        print("None found")
    # print(houses)
    for house in houses:
        all_apart.append(house.name)
        print(house.name)
    print(len(all_apart))

def test_search_paginate_2():
    url = 'http://localhost:8000/unikrib/products?limit=2&available=yes'
    print(url)
    res = requests.get(url)
    res = res.text
    print(res)

def test_prods_returns():
    res = requests.get('http://localhost:8000/unikrib/products?available=yes&limit=15')
    res = res.json()
    i = 1
    for prod in res:
        print("{}) {} -> {}".format(i, prod['name'], prod['price']))
        i += 1

def test_paginate_query():
    houses = []
    res = requests.get('http://localhost:8000/unikrib/products?available=yes&limit=4,b81d5b12-1b02-4e9e-88c5-fe7315c1cd47&nav=prev')
    res = res.json()
    for prod in res:
        print(prod['id'])

def clear_notification():
    for key, obj in storage.all(Notification).items():
        # setattr(obj, "read", False)
        ttl = 24 * 60 * 60 * 1000   # 24 hours
        valid_period = obj.updated_at + timedelta(seconds = ttl)
        if valid_period < datetime.now():
            obj.delete()
            print(f"Notification of id {obj.id} deleted")

def test_payment():
    url = "https://api.paystack.co/transaction/initialize"
    amount = 200000
    reference = str(uuid.uuid4())
    res = requests.post(url, data={"amount": amount, "email": email, "reference": reference,
                                    "callback_url": "http://localhost:8001/static/Apartment-info-page.html?id=0bdea1d5-a61c-476c-910d-1e55b18edefa"},
                headers={"Authorization": "Bearer sk_test_75a906701bd31d8ec23f55a38da4dd8f29bd0c76",
                "content_type": "application/json"})
    print(res.status_code)
    print(res.text)
    res = res.json()
    webbrowser.open(res['data']['authorization_url'])

def test_verify_payment():
    url = "https://api.paystack.co/transaction/verify/487a7708-b070-456c-a118-4cccc174ed26"
    res = requests.get(url, headers={"Authorization": "Bearer sk_test_75a906701bd31d8ec23f55a38da4dd8f29bd0c76",
                "content_type": "application/json"})
    print(res.status_code)
    print(res.text)
    
def test_payment_notification():
    from api.blueprint.houses import callback
    callback("9ab4680e-6abc-4f54-84fc-4eeaad65e837", "Dennis Akinwonjowo", "191ba48c-de1b-4924-9c8a-e59b4c187dfe", "a6e5f241-60af-4a93-bdc5-da98c5ab9f46")

def send_agent_bulk_sms():
    agents_no = []
    users_with_uploaded_apartments = []
    houses = storage.all("House")
    for key, house in houses.items():
        users_with_uploaded_apartments.append(house.owner_id)
    agents = storage.search("User", user_type='agent')
    for agent in agents:
        if agent.phone_no in users_with_uploaded_apartments:
            continue
        phone = str(agent.phone_no)
        if phone[0] == '0':
            phone = '+234' + phone[1:]
        elif phone.startswith('+234') or phone.startswith('234'):
            phone = phone
        elif int(phone[0]) > 0:
            phone = '+234' + phone

        agents_no.append(phone)

    # print(agents_no)
    message = "Good day Kribite,\nWe noticed that you signed up sometime ago but have not uploaded any apartment yet. "
    message += "Upload a vacant apartment today to experience seamless and effective advertisement for your brand. "
    message += "If you encounter any issue while uploading on the platform please ensure to reach out to us.\n"
    message += "Do not forget to recommend us to your friends and colleagues😉 \nHave a nice day."
    headers = {'Content-Type': 'application/json'}
    url = 'https://api.ng.termii.com/api/sms/send/bulk'
    api_key = getenv("TERMII_API_KEY")
    data = {"to": agents_no, "api_key": api_key,
            "from": "Unikrib", "sms": message, "type": "plain", "channel": "generic"}
    res = requests.post(url, json=data, headers=headers)
    if res == 200:
        print("Sms sent successfully")
    else:
        print("Error sending sms:", res.text)
    # for number in agents_no:
    #     data["to"] = number
    #     res = requests.post(url, json=data, headers=headers)
    #     time.sleep(1)
    #     if res.status_code == 200:
    #         print(res.text)
    #         print(f"sms sent successfully to {number}")
    #     else:
    #         print(f"{number} --> {res.status_code}, {res.text}")
            # print(f"An error was encountered while sending sms to {number}")
    # print(message)

def backup_houses():
    filepath = 'backup.json'
    all_objs = []
    houses = storage.all("House")
    for key, house in houses.items():
        all_objs.append(house.to_dict())
    print(all_objs[0])
    with open(filepath, 'w') as f:
        json.dump(all_objs, f)

def backup_users():
    filepath = 'backup.json'
    all_objs = []
    users = storage.all("User")
    for key, user in users.items():
        all_objs.append(user.to_dict())
    print(all_objs[0])
    with open(filepath, 'w') as f:
        json.dump(all_objs, f)

def backup_usersession():
    filepath = 'backup.json'
    all_objs = []
    objs = storage.all("UserSession")
    for key, obj in objs.items():
        # obj = obj.to_dict()
        # obj.pop('__class__', None)
        all_objs.append(obj.to_dict())
    print(all_objs[0])
    with open(filepath, 'w') as f:
        json.dump(all_objs, f)

def update_phone():
    for user in storage.all('User').values():
        try:
            url = 'https://unikribbackend.onrender.com/' + user.id
            dic = {"phone_no": user.phone_no}
            headers = {"content_type": "application/json", "Authorization": "unikrib dfe57c69-bef2-40b1-ba7f-e42fcc2752ca"}
            requests.put(url, data=dic, headers=headers)
            print(f"{user.first_name} has been updated succesfully")
        except Exception as e:
            print("Error:", e)

def add_schools():
    schools = [("FUTO", "Federal University of Technology Owerri", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872081/Schools/FUTO_urv8ak.jpg"),
               ("LASU", "Lagos state University", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872081/Schools/LASU_a5dfu5.jpg"),
               ("AAU", "Ambrose Alli University", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872082/Schools/AAU_iwzcen.jpg"),
               ("FUPRE", "Federal University Of Petroleum Resources Effurun", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872082/Schools/FUPRE_ojmx3s.jpg"),
               ("ABSU", "Abia State University", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872082/Schools/ABSU_llmd5v.jpg"),
               ("OOU", "Olabisi Onabanjo University", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872082/Schools/OOU_fbec2p.jpg"),
               ("CRUTECH", "University of Cross River State", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872081/Schools/CRUTECH_pgclxg.jpg"),
               ("FUOYE", "Federal University of Oye Ekiti", "https://res.cloudinary.com/deg1j9wbh/image/upload/v1710872081/Schools/FUOYE_wsjjli.jpg")]
    for sch in schools:
        sc = School(name=sch[0], full_name=sch[1], image_url=sch[2])
        try:
            sc.save()
            print(f"{sch[0]} added!")
        except Exception as e:
            print(e)

def add_env():
    environs = {"FUTO": ("Nekede", "Ihiagwa", "Eziobodo", "Obinze", "Umuchima", "Ezeogwu", "Okolochi"),
            "LASU": ("First Gate", "Post service", "Ojo", "Akesan", "Iba"),
            "AAU": ("School gate", "Ihumudum", "Ujemen", "Idumebo"),
            "FUPRE": ("Ugbomoro", "Iteregbi", "Ugolo", "Okorikpehre"),
            "ABSU": ("Isuikwato", "Uloma", "Okigwe", "Obiagu"),
            "OOU": ("Ago Iwoye", "Oru", "Ilaporu", "Aha", "Awa"),
            "CRUTECH": ("Ene-Obong", "Eko basi", "Mount zion", "Idim ita", "Edibe Edibe", "Efut Abua", "Atamunu", "Anantigha"),
            "FUOYE": ("Odo-oro", "Ootunja", "Isaba", "Usin", "Ikoyi", "Ikoyi tuntun", "School gate", "Asin", "Shell", "Market", "Garage")}
    for sch, envs in environs.items():
        print(f"\n Adding environments for {sch}")
        school = storage.search("School", name=sch)
        if len(school) == 0:
            print(f"{sch} was not found")
            continue
        school = school[0]
        for env in envs:
            try:
                ev = Environment(name=env, school_id=school.id)
                ev.save()
                print(f"{env} added!")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    print("Starting test...")
    update_phone()