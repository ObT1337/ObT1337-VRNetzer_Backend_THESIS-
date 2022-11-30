import os
import traceback
from importlib import import_module

import flask

import util


def import_blueprint(app: flask.Flask,ext:str,extensions_path:str):
    try:
        if not os.path.isfile(os.path.join(extensions_path, ext,"src","app.py")):
            raise ImportError(f"No app.py found in '/extension/{ext}/src'.")

        module = f"extensions.{ext}.src.app"
        module = import_module(module)

        if not hasattr(module, "blueprint") or not hasattr(module, "url_prefix"):
            raise AttributeError(f"Attributes 'blueprint' or 'url_prefix' not found in module {ext}.")

        app.register_blueprint(
            module.blueprint, url_prefix=module.url_prefix
        )
        print(f"\033[1;32mLoaded extension: {ext}")
        return module
    except ImportError:
        print(f"\u001b[33m", traceback.format_exc())
        print(f"\u001b[33mMake sure you installed a necessary python modules.")
        print(
            f"\u001b[33mYou can use:\n\npython3 -m pip install -r {ext}/requirements.txt\n\nTo install all requirements."
        )
    except AttributeError:
        print(f"\u001b[33m", traceback.format_exc())
        print(
            f"\u001b[33mMake sure you have an app.py file in the '/src/' folder of your extension."
        )
        print(
            f"\u001b[33mMake sure that you have defined a 'url_prefix' for your in the app.py file."
        )
        print(
            f"\u001b[33mMake sure your flask blueprint is called 'blueprint'."
        )
        return False

def load(main_app: flask.Flask):
    _WORKING_DIR = os.path.abspath(os.path.dirname(__file__))
    extensions = os.path.join(_WORKING_DIR, "extensions")
    loaded_extensions = []
    add_tab_to_main, add_tab_to_upload=[],[]
    if os.path.exists(extensions):
        for ext in os.listdir(extensions):
            module = import_blueprint(main_app,ext,extensions)
            if module:
                loaded_extensions.append(ext)
            if hasattr(module,"main_tabs"):
                for tab in module.main_tabs:
                    tab = os.path.join("extensions",ext,"templates",tab)
                    add_tab_to_main.append(tab)
            if hasattr(module,"upload_tabs"):
                for tab in module.upload_tabs:
                    tab = os.path.join("extensions",ext,"templates",tab)
                    add_tab_to_upload.append(tab)
            if hasattr(module,"before_first_request"):
                main_app.before_first_request_funcs += module.before_first_request
                    

    print("\n\n\033[1;32mFinished loading extensions, server is running... \u001b[37m")
    res ={"loaded":loaded_extensions,"main_tabs":add_tab_to_main,"upload_tabs":add_tab_to_upload}
    return main_app, res
