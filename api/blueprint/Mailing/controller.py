#!/usr/bin/python3

from rq import Queue
import random
import uuid
import json
from redis import from_url
from redis import Redis
from api.blueprint.Mailing.worker import perform_task
from os import getenv
from models import storage

redis_url = getenv('REDIS_URL')
redis_conn = from_url(redis_url)


class Controller:
    def __init__(self):
        self.queue = Queue(connection=redis_conn, name='unikrib')
        # self.queue = Queue('default', connection=Redis(host=redis_url))

    def sendVerifyLink(self, email, first_name, user_id):
        code = str(uuid.uuid4())
        data = {"email": email, "first_name": first_name, "code": code, "user_id": user_id, "type": "verifyLink"}
        data = json.dumps(data)
        self.queue.enqueue(perform_task(data), data)
        return {"message": "Verification code sent succesfully",
                                "code": code, "status_code": 200}

    def sendWelcome(self, email, first_name):
        data = {"email": email, "first_name": first_name, "type": "welcome"}
        data = json.dumps(data)
        self.queue.enqueue(perform_task(data))
        return {'message': "Welcome mail sent successfully", 'status_code': 200}
    
    def sendOTP(self, email, first_name):
        otp = random.randint(1000, 9999)
        data = {"email": email, "first_name": first_name, "otp": otp, "type": "sendOTP"}
        data = json.dumps(data)
        self.queue.enqueue(perform_task(data))
        return {'message': "OTP sent successfully", 'code': otp, 'status_code': 200}

    def resetPassword(self, email, first_name):
        otp = random.randint(1000, 9999)
        data = json.dumps({"email": email, "first_name": first_name, "otp": otp, "type": "resetCode"})
        self.queue.enqueue(perform_task(data))
        return {'message': "Mail sent successfully", 'otp': otp, 'status_code': 200}

    def newReport(self, reporter, reported, topic, description):
        data = {"email": "unikrib@gmail.com", "reporter": reporter, "reported": reported,
                "topic": topic, "description": description, "type": "newReport"}
        data = json.dumps(data)
        self.queue.enqueue(perform_task(data))
        return {'message': "Report added successfully", "status_code": 200}

    def sendNotification(self, email, first_name, typ, itemId=None):
        if typ not in ['inspection_request', 'inspection_accepted', 'inspection_denied', 'new_review']:
            return {'error': "type can only be 'inspection_request' || 'inspection_accepted' || 'inspection_denied'"}
        data = {"email": email, "first_name": first_name, "type": typ}
        if typ == 'inspection_accepted':
            data['itemId'] = itemId
        data = json.dumps(data)
        self.queue.enqueue(perform_task(data))
        return {'message': "Mail successfully sent to agent", "status_code": 200}
    
    def userVerification(self, *args, **kwargs):
        data = {"first_name": kwargs.get('first_name'), 'last_name': kwargs.get('last_name'),
                'face_image': kwargs.get('face_image'),
                'id_image': kwargs.get('id_image'), 'email': 'unikrib@gmail.com', 'type': 'userVerification',
                'user_id': kwargs.get('user_id')}
        data = json.dumps(data)
        self.queue.enqueue(perform_task(data))
        return {'message': 'User verification submitted successfully', 'status_code': 200}
        

runner = Controller()
