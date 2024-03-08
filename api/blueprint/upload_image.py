#!/usr/bin/python3
"""This uploads images to the cloudinary storage
"""

from api.blueprint import app_views, auth
from flask import jsonify, request
from cloudinary import uploader, CloudinaryImage
import cloudinary
from os import getenv


cloudinary.config(
    cloud_name = getenv("CLOUD_NAME"),
    api_key = getenv("API_KEY"),
    api_secret = getenv("API_SECRET")
)

@app_views.route('/upload_image', strict_slashes=False, methods=['POST'])
@auth.login_required
def upload_image():
    """This defines the upload image route"""
    file_to_upload = request.files['file']
    if not file_to_upload:
        return jsonify("File not found"), 404

    if 'folder' in request.form:
        folder = request.form['folder']
    else:
        folder = 'general'
    if 'fileName' not in request.form:
        return jsonify("Include a fileName in request form"), 400
    else:
        public_id = request.form['fileName']
    initial_image = uploader.upload(file_to_upload, folder=folder, public_id=public_id, quality="auto:best")
    if folder != 'user_avatar':
        # Add watermarks to all images except user avatars
        initial_width = initial_image['width']
        initial_url = initial_image['secure_url']
        overlay_width = int(0.25 * initial_width)
        result = uploader.upload(initial_url, folder=folder, public_id=public_id,
                    transformation=[
                        {'overlay': {'url': "https://res.cloudinary.com/deg1j9wbh/image/upload/v1687794852/Black_logo_on_white_jqkejx.png"}},
                        {'width': overlay_width, 'crop': "scale"},
                        {'opacity': 50},
                        {'flags': ["layer_apply", "no_overflow"], 'gravity': "south_east", 'x': "0.05", 'y': "0.05"},
                    ]
                )
        return jsonify(result['secure_url']), 200
    else:
        return jsonify(initial_image['secure_url'])