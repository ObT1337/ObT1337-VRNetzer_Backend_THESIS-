import os
from importlib import import_module

import flask


def load(main_app: flask.Flask):
    _WORKING_DIR = os.path.abspath(os.path.dirname(__file__))
    extensions = os.path.join(_WORKING_DIR, "extensions")
    if os.path.exists(extensions):
        for ext in os.listdir(extensions):
            module = f"extensions.{ext}.src.app"
            try:
                module = import_module(module)
                main_app.register_blueprint(
                    module.blueprint, url_prefix=module.url_prefix
                )
                print(f"Loaded extension: {ext}")
            except ImportError:
                print(f"Failed to load extension: {ext}")
                print(f"Make sure you installed a necessary python modules.")
                print(
                    f"You can use:\n\npython3 -m pip install -r {ext}/requirements.txt\n\nTo install all requirements"
                )
    return main_app
