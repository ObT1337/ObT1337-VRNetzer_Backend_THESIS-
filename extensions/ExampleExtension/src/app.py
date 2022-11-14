import json
import os
import random

import flask
import util

import GlobalData as GD
import uploader

# Prefix for the extension, as well as the names space of the extension
url_prefix = "/example"  # MANDATORY
extensions_name = "ExampleExtension"

# Define where all templates and static files of your extension are located
templates = os.path.abspath("./extensions/ExampleExtension/templates")
static = os.path.abspath("./extensions/ExampleExtension/static")

# Create a blueprint for the extension this will be loaded by the main app
blueprint = flask.Blueprint(
    extensions_name,
    __name__,
    url_prefix=url_prefix,
    template_folder=templates, # defaults to static of main app.py
    static_folder=static, # defaults to static of main app.py
)  # MANDATORY

# Define your first route
@blueprint.route("/hello", methods=["GET"])
def hello():
    return "Hello World!"


# Adds a tab to the main panel route to this is /example/main
@blueprint.route("/main", methods=["GET"])
def example_main():
    """Route to extended Main panel"""
    username = util.generate_username()
    project = flask.request.args.get("project")

    if project is None or project == "none":
        project = uploader.listProjects()[0]
    print(project)
    if flask.request.method == "GET":

        room = 1
        # Store the data in session
        flask.session["username"] = username
        flask.session["room"] = room
        folder = "static/projects/" + project + "/"

        # Update global pfile and global names variables
        with open(folder + "pfile.json", "r") as json_file:
            GD.pfile = json.load(json_file)

        with open(folder + "names.json", "r") as json_file:
            GD.names = json.load(json_file)

        return flask.render_template(
            "example_main_tab.html",
            session=flask.session,
            sessionData=json.dumps(GD.sessionData),
            pfile=json.dumps(GD.pfile),
        )
    else:
        return "error"
