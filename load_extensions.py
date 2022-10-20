import os
from importlib import import_module

import flask


def load(main_app: flask.Flask):
    _WORKING_DIR = os.path.abspath(os.path.dirname(__file__))
    extensions = os.path.join(_WORKING_DIR, "extensions")
    if os.path.exists(extensions):
        for ext in os.listdir(extensions):
            module = f"extensions.{ext}.src.app"
            print(module)
            module = import_module(module)
            main_app.register_blueprint(module.blueprint, url_prefix=module.url_prefix)
            print(f"Loaded extension: {ext}")
    return main_app
