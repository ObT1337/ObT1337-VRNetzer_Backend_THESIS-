import os
import traceback
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
                print(f"\033[1;32mLoaded extension: {ext}")
            except ImportError as e:
                print(f"\u001b[33m", traceback.format_exc())
                print(f"\u001b[33mMake sure you installed a necessary python modules.")
                print(
                    f"\u001b[33mYou can use:\n\npython3 -m pip install -r {ext}/requirements.txt\n\nTo install all requirements."
                )
                print(f"Excepted an ImportError:{e}\n")
    print("\n\n\033[1;32mFinished loading extensions, server is running...\u001B[37m")
    return main_app
