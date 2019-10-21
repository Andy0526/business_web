# -*- coding: utf-8 -*-

from flask import Flask
from werkzeug.utils import import_string

# from flask_cors import CORS

blueprints = [

    # api
    'plastic.views.home:bp',
    'plastic.views.api.nav1:bp',
    'plastic.views.api.nav2:bp',
    'plastic.views.api.nav3:bp',
    'plastic.views.api.nav4:bp',
    'plastic.views.api.nav5:bp',

]


def create_app(config=None):
    app = Flask(__name__)
    # CORS(app, supports_credentials=True, resources=r'*')
    app.config.from_object('plastic.config')
    app.config.from_object(config)

    for blueprint in blueprints:
        blueprint = import_string(blueprint)
        app.register_blueprint(blueprint)

    return app
