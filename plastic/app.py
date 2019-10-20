# -*- coding: utf-8 -*-

from flask import Flask
from werkzeug.utils import import_string

# from flask_cors import CORS

blueprints = [

    # api
    'ctdcxy.views.api.layouts:bp',

]


def create_app(config=None):
    app = Flask(__name__)
    # CORS(app, supports_credentials=True, resources=r'*')
    app.config.from_object('ctdcxy.config')
    app.config.from_object(config)

    for blueprint in blueprints:
        blueprint = import_string(blueprint)
        app.register_blueprint(blueprint)

    return app
