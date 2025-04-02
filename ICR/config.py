import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "not_inspired_for_secrets"
    FLASK_DATABASE = "ice_climbing.db"

    ROOT_PATH = __file__.split("ICR")[0]
    print(f"{ROOT_PATH=}")

    IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')
    IMAGE_ROOT_FOLDER = 'ICR/static/images'
    IMAGE_UPLOAD_FOLDER = 'ICR/static/images/{yyyy_mm}/pictures'
    IMAGE_THUMBNAIL_UPLOAD_FOLDER = 'ICR/static/images/{yyyy_mm}/thumbnails'
    IMAGE_THUMBNAIL_DIMENSIONS = (400, 400)
    IMAGE_MAX_SIZE = 2 * 1024 * 1024
