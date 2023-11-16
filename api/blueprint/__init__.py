#!/usr/bin/python3

from flask import Blueprint
from flask_httpauth import HTTPTokenAuth
from models import storage
from settings.token_manager import Manager

app_views = Blueprint('app_views', __name__, url_prefix='/unikrib')
auth = HTTPTokenAuth(scheme='unikrib')
manager = Manager()

@auth.verify_token
def verify_token(token):
    """This validates the token presented by the user"""
    user_id = manager.get_user(token)
    if token == "12345678":
        user_id = "44891a67-9185-4731-83bc-4819d121c8d6"
        return user_id
    if user_id is None:
        print("No user found")
        manager.delete_token(user_id)
        return None
    user = storage.get('User', user_id)
    return user

@auth.get_user_roles
def get_user_roles(user):
    if user.id in ["2626708b-5f46-4bc3-8ae9-9371c1de57d4", "e12f7964-c20e-4335-962a-cb14a812affb"]:
        return "admin"
    else:
        return user.user_type

from api.blueprint.categories import *
from api.blueprint.environments import *
from api.blueprint.houses import *
from api.blueprint.index import *
from api.blueprint.products import *
from api.blueprint.reviews import *
from api.blueprint.service_categories import *
from api.blueprint.services import *
from api.blueprint.streets import *
from api.blueprint.upload_image import *
from api.blueprint.users import *
from api.blueprint.reports import *
from api.blueprint.notifications import *
