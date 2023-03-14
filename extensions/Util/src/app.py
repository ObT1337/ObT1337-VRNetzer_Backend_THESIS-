import multiprocessing as mp
import os
import threading
import time

import GlobalData as GD
import socket_handlers
from io_blueprint import IOBlueprint
from . import anntoation_scraper, util

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
    "util_flask_styles.html",
    "util_scripts.html",
    "util_main_highlight.html",
    "util_main_selection.html",
]  # List of tab templates to be loaded in the main panel
upload_tabs = []  # List of tab templates to be loaded in the upload panel
nodepanel_tabs = []  # List of tab templates to be loaded in the node panel
nodepanelppi_tabs = []
annotations = []


@blueprint.before_app_first_request
def util_setup():
    GD.annotationScraper = anntoation_scraper.AnnotationScraper(send_result=send_result)
    threading.Thread(target=GD.annotationScraper.start, args=(2,)).start()
    ...


@blueprint.on("annotation")
def util_get_annotation(message):
    threading.Thread(target=waiter, args=(message,)).start()
    ...


def waiter(message):
    response = GD.annotationScraper.wait_for_annotation(message)
    if response is not None:
        message.update(response)
    send_result(message)
    pass


@blueprint.on("select")
def util_select(message):
    message = util.get_selection(message)
    send_result(message)


@blueprint.on("highlight")
def util_highlight(message):
    blueprint.emit("started", {"id": message["id"]})
    message = util.highlight_func(message)
    print(message)
    if message.get("set_project"):
        print("Setting project..")
        set_project("tmp")
        time.sleep(2)

    send_status(message)


@blueprint.on("reset")
def util_reset(message):
    print(message)
    if message["type"] == "project":
        project = GD.pfile.get("origin")
        if project:
            set_project(project)
            message["message"] = f"Project reset to {project}."
            message["status"] = "success"
            print("Resetting..")
            time.sleep(0.5)
        else:
            message["message"] = "Current project is not highlighted."
            message["status"] = "error"
        send_status(message)
        return

    state_data = GD.pfile.get("stateData")
    if state_data is None:
        state_data = {}
        GD.pfile["stateData"] = state_data
    if message["type"] == "node":
        state_data["selected"] = None
    if message["type"] == "link":
        state_data["selectedLinks"] = None
    GD.pfile["stateData"] = state_data


def set_project(project):
    print("Setting project..", project)
    message = {"id": "projects", "opt": project, "fn": "sel"}
    socket_handlers.projects(message)
    blueprint.emit("ex", message, namespace="/chat")
    print("Project set..")


def set_layout(id, value):
    message = {"id": id, "opt": value, "fn": "sel"}
    socket_handlers.select_menu(message)
    blueprint.emit("ex", message, namespace="/chat")


def send_result(message):
    blueprint.emit("result", message)


def send_status(message):
    blueprint.emit("status", message)
