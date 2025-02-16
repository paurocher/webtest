import os
from dotenv import load_dotenv

from flask import Flask

from . import (
    helpers,
    db,
)


# Load environment variables from .env file, so we don't have to commit them to
# GitHub.
# See https://flask.palletsprojects.com/en/2.0.x/config/#configuring-from-environment-variables
load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # load flask environment variables that are set in the .env file
    app.config.from_prefixed_env()
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # database
    db.init_app(app)

    # blueprints
    from . import auth
    app.register_blueprint(auth.bp)
    from . import blog
    app.register_blueprint(blog.bp)

    # here we are defining the root of the blog bp to be "/" (the index), so
    # that all blog pages will start with "/".

    # This app_url_rule makes the
    # index url be "index.html" and not "blog/index.html".
    app.add_url_rule('/', endpoint='index')

    print(f"Current Environment: {os.getenv('ENVIRONMENT')}")
    print(f"Using Database: {app.config.get('DATABASE')}")

    return app