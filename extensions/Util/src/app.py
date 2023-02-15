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
def util_highlight(message):
    blueprint.emit("highlight")
    try:
        util.highlight_selected_node_links(message)
    except Exception as e:
        blueprint.emit("status", {"message": e, "status": "error"})

    set_project("tmp")
    blueprint.emit("status", {"message": "Selection highlighted!", "status": "success"})


@blueprint.on("reset")
def util_reset(message):
    project = GD.sessionData["actPro"]
    with open(os.path.join("static", "projects", project, "pfile.json")) as f:
        pfile = json.load(f)
        origin = pfile.get("origin")
        if not origin:
            return
    with open(os.path.join("static", "projects", origin, "pfile.json")) as f:
        pfile = json.load(f)
        pfile["selections"] = {
            "layout": message["layout"],
            "layoutRGB": message["layoutRGB"],
            "linkl": message["linkl"],
            "linkRGB": message["linkRGB"],
            "main_tab": message["main_tab"],
        }
    with open(os.path.join("static", "projects", origin, "pfile.json"), "w") as f:
        json.dump(pfile, f)

    set_project(origin)

    print("Resetting..")


@blueprint.on("getSelection")
def util_get_selection():
    print("Selection requested!")
    blueprint.emit("selection", GD.sessionData["selected"])


def set_project(project):
    blueprint.emit(
        "ex", {"id": "projects", "opt": project, "fn": "sel"}, namespace="/chat"
    )
