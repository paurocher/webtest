"""Global variables for the flask app."""

import os


class Config:
    """Global configuration for the flask app."""
    # I still am not sure about how to deal with the secret key ...
    SECRET_KEY: str = (
        os.environ.get("SECRET_KEY") or
        "not_inspired_for_secrets"
    )

    # The DB location.
    FLASK_DATABASE: str = "ice_climbing.db"

    # Amount of seconds the session will last after closing the page.
    PERMANENT_SESSION_LIFETIME: int = 60 * 30

    # I use this one to determine the root path, so paths are resolved no
    # matter where the app is run from.
    ROOT_PATH: str = __file__.split("ICR")[0]

    # Image relate variables (pretty self-explanatory)
    IMAGE_EXTENSIONS: tuple = ('png', 'jpg', 'jpeg', 'gif')
    IMAGE_ROOT_FOLDER: str = 'ICR/static/images'
    IMAGE_UPLOAD_FOLDER: str = 'ICR/static/images/{yyyy_mm}/pictures'
    IMAGE_THUMBNAIL_UPLOAD_FOLDER: str = (
        'ICR/static/images/{yyyy_mm}/thumbnails'
    )
    IMAGE_THUMBNAIL_DIMENSIONS: tuple = (400, 400)
    IMAGE_MAX_SIZE: int = 2 * 1024 * 1024
