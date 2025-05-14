import os
from dotenv import load_dotenv

from flask import Flask

from .config import Config
from . import (
    helpers,
    db,
)


# Load environment variables from .env file, so we don't have to commit them to
# GitHub.
# See:
# https://flask.palletsprojects.com/en/2.0.x/config/#configuring-from-environment-variables
load_dotenv()


def create_app(test_config=None):
    """Application factory.

    Building the app here like so allows us to test it easily.

    Args:
        test_config (str): Config type for app configuration

    Returns:
        flask.Flask
    """
    # create the app instance
    app: Flask = Flask(__name__, instance_relative_config=True)

    # load flask environment variables that are set in the .env file
    # app.config.from_prefixed_env()
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # database
    db.init_app(app) # TODO: do not pass the app. Grab it from current_app

    # blueprints
    from . import auth
    app.register_blueprint(auth.bp)
    from . import blog
    app.register_blueprint(blog.bp)

    # here we are defining the root of the blog bp to be "/" (the index), so
    # that when we are in the index page, the address will jut be "/" (it is
    # just for cleanliness of the url, just makeup)
    app.add_url_rule('/', endpoint='index')

    # print(f"Current Environment: {os.getenv('ENVIRONMENT')}")
    # print(f"Using Database: {app.config.get('FLASK_DATABASE')}")
    # ic(app.config)
    # ic(sorted(os.environ))

    return app