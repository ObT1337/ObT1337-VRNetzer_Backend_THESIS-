import os
import traceback
from importlib import import_module

import flask

import util


def import_blueprint(app: flask.Flask, ext: str, extensions_path: str) -> bool:
    try:
        if not os.path.isfile(os.path.join(extensions_path, ext, "src", "app.py")):
            raise ImportError(f"No app.py found in '/extension/{ext}/src'.")

        module = f"extensions.{ext}.src.app"
        module = import_module(module)

        if not hasattr(module, "blueprint") or not hasattr(module, "url_prefix"):
            raise AttributeError(
                f"Attributes 'blueprint' or 'url_prefix' not found in module {ext}."
            )

        app.register_blueprint(module.blueprint, url_prefix=module.url_prefix)
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
        print(f"\u001b[33mMake sure your flask blueprint is called 'blueprint'.")
        return False


def load(main_app: flask.Flask) -> tuple[flask.Flask, dict]:
    """Loads all extensions contained in the directory extensions."""
    _WORKING_DIR = os.path.abspath(os.path.dirname(__file__))
    extensions = os.path.join(_WORKING_DIR, "extensions")
    loaded_extensions = []
    add_tab_to_main, add_tab_to_upload, add_tab_to_nodepanel_ppi = [], [], []
    # add_tab_to_nodepanel = []
    if os.path.exists(extensions):
        for ext in os.listdir(extensions):
            module = import_blueprint(main_app, ext, extensions)
            if module:
                loaded_extensions.append(ext)
            if hasattr(module, "main_tabs"):
                add_tab_to_main += add_tabs(module.main_tabs, ext)
            if hasattr(module, "upload_tabs"):
                add_tab_to_upload += add_tabs(module.upload_tabs, ext)
            if hasattr(module, "nodepanel_ppi_tabs"):
                add_tab_to_nodepanel_ppi += add_tabs(module.nodepanel_ppi_tabs, ext)

            # TODO: Add other websites with tabs

            # if hasattr(module, "nodepanel_tabs"):
            #     add_tab_to_nodepanel_ppi += add_tabs(module.nodepanel_ppi_tabs, ext)
            # ...

            if hasattr(module, "before_first_request"):
                main_app.before_first_request_funcs += module.before_first_request

    print("\n\n\033[1;32mFinished loading extensions, server is running... \u001b[37m")
    res = {
        "loaded": loaded_extensions,
        "main_tabs": add_tab_to_main,
        "upload_tabs": add_tab_to_upload,
        "nodepanel_ppi_tabs": add_tab_to_nodepanel_ppi,
        # "nodepanel_tabs": add_tab_to_nodepanel_ppi,
        # ...
    }
    return main_app, res


def add_tabs(tabs: list[str], ext: str) -> list[str]:
    """Add tabs to the list of tabs."""
    to_add = []
    for tab in tabs:
        tab = os.path.join("extensions", ext, "templates", tab)
        to_add.append(tab)
    return to_add
