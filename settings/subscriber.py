#!/usr/bin/python3

# from models.v2.subscriber import Subscriber
# from datetime import datetime
from models import storage, Subscriber

def get_subscriber_status(user_id):
    """This returns True if a user is in the subscriber 
    table and False if otherwise"""
    if storage.search(Subscriber, user_id=user_id) != []:
        return True
    else:
        return False
    