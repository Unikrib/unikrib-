#!/usr/bin/python3

from flask import Flask, render_template, jsonify, request, abort
from api.blueprint import app_views
from models import storage
from flask_cors import CORS
from settings.caching import LFUCache
import time
import json
import logging
# import schedule
# import threading
# from dotenv import load_dotenv
# from os import environ

# load_dotenv()
app = Flask(__name__, template_folder='static')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(app_views)
cache = LFUCache()

log_file = "error.json"
log_level = logging.WARN

logger = logging.getLogger("error_logger")
logger.setLevel(log_level)

log_handler = logging.FileHandler(log_file)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)


@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"Error": "Unauthorized", "message": error}), 401

@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({"Error": "Forbidden"}), 403

@app.route('/', strict_slashes=False)
def main():
    return render_template('homepage2.html')

@app.before_request
def filter():
    """This tries to retrieve response from cache before 
    processing """

    if request.path and request.method == 'GET':
        cacheResponse = cache.get(request.path)
        if cacheResponse is None:
            return
        else:
            print(request.path + " was gotten from cache.")
            return jsonify(cacheResponse)

@app.after_request
def update_cache(response):
    """This adds the result of the request to the cache
    and also logs all server errors to the error.json file
    """
    included_paths = ['/unikrib/houses', '/unikrib/products',
                     '/unikrib/services', '/unikrib/environments/',
                     '/unikrib/streets/', '/unikrib/categories/',
                     '/unkrib/service-categories/', '/unikrib/environments/<env_id>/streets/',
                     '/unikrib/users/<user_id>/', '/unikrib/categories/<cat_id>/',
                     '/unikrib/products/<product_id>/', '/unikrib/environments/<env_id>/',
                     '/unikrib/streets/<str_id>/', '/unikrib/categories/<cat_id>/'
                     ]
    if request.method == 'GET' and cache.require_cache(request.path, included_paths):
        if response.status_code == 200 or response.status_code == 201:
            cache.put(request.path, response.get_json())

    if request.method == 'PUT' or request.method == 'POST':
        if request.method == 'PUT':
            path = str(request.path).split('/')
            path = '/' + path[0] + '/' + path[1]
        else:
            path = request.path
        if cache.get(path) is not None:
            cache.delete(request.path)
            print("Cache updated")

    if response.status_code > 401:
        error_message = {
            "status_code": response.status_code,
            "method": request.method,
            "path": request.path,
            "user_agent": request.user_agent.string,
            "remote_addr": request.remote_addr,
        }
        logger.error(error_message)
    return response

@app.teardown_appcontext
def close(exception):
    storage.close()

def run_scheduler(func, arg):
    from api.blueprint.houses import terminate_thread
    # global terminate_thread
    ttl = 60 * 60 * 24 * 3  # 3 days

    while not terminate_thread:
        time.sleep(ttl)
        func(arg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)
