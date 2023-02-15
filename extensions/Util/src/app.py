import json
import os
import shutil
import time
from multiprocessing import Process, Queue

import GlobalData as GD
from io_blueprint import IOBlueprint

from . import util

# Prefix for the extension, as well as the names space of the extension
url_prefix = "/Util"  # MANDATORY
extensions_name = "Util"

# Define where all templates and static files of your extension are located
templates = os.path.abspath("./extensions/Util/templates")
static = os.path.abspath("./extensions/Util/static")

# Create a blueprint for the extension this will be loaded by the main app
blueprint = IOBlueprint(
    extensions_name,
    __name__,
    url_prefix=url_prefix,
    template_folder=templates,  # defaults to static of main app.py
    static_folder=static,  # defaults to static of main app.py
)  # MANDATORY

main_tabs = [
    "util_main_tab.html"
]  # List of tab templates to be loaded in the main panel
upload_tabs = []  # List of tab templates to be loaded in the upload panel
nodepanel_tabs = []  # List of tab templates to be loaded in the node panel
nodepanelppi_tabs = []


@blueprint.on("highlight")
def example_highlight(message):
    blueprint.emit("highlight")
    util.highlight_workflow(message, blueprint)


@blueprint.on("getSelection")
def analytics_get_selection():
    print("Selection requested!")
    blueprint.emit("selection", GD.sessionData["selected"])


# # Define your first route
# @blueprint.route("/hello", methods=["GET"])
# def hello():
#     return "Hello World!"


# # Adds a tab to the main panel route to this is /example/main
# @blueprint.route("/main", methods=["GET"])
# def example_main():
#     return flask.render_template("example_main.html")


# @blueprint.route("/nodepanel", methods=["GET"])
# def example_node_info():
#     return "Node Info"


# @blueprint.route("/upload", methods=["GET"])
# def example_upload():
#     return "Upload"


# @blueprint.route("/preview", methods=["GET"])
# def example_preview():
#     return "Example Preview"


# @blueprint.route("/uploadfiles", methods=["POST"])
# def example_upload_files():
#     success = False
#     if success:
#         return "<a style='color:green;'>Success</a>", 200
#     else:
#         return "<a style='color:red;'>Error</a>", 500


# @blueprint.before_app_first_request
# def example_extension_setup():
#     # prepare some important variables
#     # do more important stuff
#     pass


# @blueprint.route("/emit", methods=["GET"])
# def example_emit_socketio_to_main():
#     """This will send a socketio message to the main panel. Check the console of the main panel to see the message."""
#     namespace = "/chat"
#     room = 1
#     blueprint.emit(
#         "ex",
#         {"id": "someId", "opt": "someOption", "fn": "SomeFunction"},
#         namespace=namespace,
#         room=room,
#     )
#     return "sent"


# @blueprint.route("/send", methods=["GET"])
# def example_send_socketio():
#     """Webpage with a button, when pressed a socketio message to this extension is send."""
#     return flask.render_template("example_send_socketio.html")


# @blueprint.on("example")
# def example_receive_socketio(message):
#     print("Received example form client:")
#     print(message)


# @blueprint.on("example", namespace="/chat")
# def example_receive_socketio_in_main(message):
#     print("Received example form client:")
#     print(message)
