import os
import random
import re
import shutil

import bs4
import flask
from bs4 import BeautifulSoup as bs

import GlobalData as GD
import uploader


def delete_project(request: flask.request):
    """
    Delete a project folder and all its contents.
    """
    project_name = request.args.get("project")
    projects = uploader.listProjects()
    if project_name is None:
        return f"Error: No project name provided. Example:\n<a href='{flask.request.base_url}?project={projects[0]}'>{flask.request.base_url}?project={projects[0]}</a>"

    project_path = os.path.join("static", "projects", project_name)
    if not os.path.exists(project_path):
        return f"<h4>Project {project_name} does not exist!</h4>"
    shutil.rmtree(project_path)
    return f"<h4>Project {project_name} deleted!</h4>"


def generate_username():
    """
    If no username is provided, generate a random one and return it
    """
    username = flask.request.args.get("usr")
    if username is None:
        username = str(random.randint(1001, 9998))
    else:
        username = username + str(random.randint(1001, 9998))
    return username


def has_no_empty_params(rule):
    """
    Filters the route to ignore route with empty params.
    """
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def get_all_links(app) -> list[list[str, str]]:
    """Extracts all routes from flask app and return a list of tuples of which the first value is the route and the seconds is the name of the corresponding python function."""
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = flask.url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return links


def create_dynamic_links(app: flask.app.Flask):
    # Get all links from flask
    links = get_all_links(app)
    # links = [link for link in links if len(link[0].split("/"))>2]
    GD.sessionData["url_map"] = links


def get_valid_filename(filename: str):
    s = filename.strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)
