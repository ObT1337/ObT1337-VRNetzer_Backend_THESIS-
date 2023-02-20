import json
import os
import shutil
import time
from multiprocessing import Manager, Process

import pandas as pd

import GlobalData as GD
from io_blueprint import IOBlueprint
from project import Project

from . import const, util

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
    "util_main_highlight.html",
    "util_main_selection.html",
]  # List of tab templates to be loaded in the main panel
upload_tabs = []  # List of tab templates to be loaded in the upload panel
nodepanel_tabs = []  # List of tab templates to be loaded in the node panel
nodepanelppi_tabs = []
annotations = []


@blueprint.on("annotation")
def util_get_annotation(message):
    handle_annotation_request(message)


@blueprint.on("select")
def util_select(message):
    message = util.get_selection(message)
    send_result(message)


@blueprint.on("highlight")
def util_highlight(message):
    blueprint.emit("started", {"id": message["id"]})
    message = util.highlight_func(message)
    if message["status"] == "success":
        set_project("tmp")
    send_status(message)


@blueprint.on("reset")
def util_reset(message):
    if message["type"] == "project":
        origin = util.reset(message)
        if origin:
            set_project(origin)
            print("Resetting..")
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


def handle_annotation_request(message):
    project = GD.sessionData["actPro"]
    data_type = message["type"]
    if not hasattr(GD, "annotations"):
        GD.annotations = {}
    if project not in GD.annotations:
        process_annotations(message, project, data_type)
    if data_type not in GD.annotations[project]:
        process_annotations(message, project, data_type)
    if GD.annotations[project][data_type] == "processing":
        time.sleep(0.5)
        handle_annotation_request(message)
        print("Waiting for annotation..")
    message = GD.annotations[project][data_type]
    send_result(message)


def process_annotations(message, project, data_type):
    print("Processing annotation request..")
    if project not in GD.annotations:
        GD.annotations[project] = {}
    GD.annotations[project][data_type] = "processing"
    manager = Manager()
    return_dict = manager.dict()
    p = Process(target=util.get_annotation, args=(message, return_dict))
    p.start()
    p.join()
    print("Annotation request processed..")
    GD.annotations[project][data_type] = return_dict["annotations"]


def set_project(project):
    blueprint.emit(
        "ex", {"id": "projects", "opt": project, "fn": "sel"}, namespace="/chat"
    )


def send_result(message):
    blueprint.emit("result", message)


def send_status(message):
    blueprint.emit("status", message)
