import os

import flask
import vrprot
from PIL import Image
from vrprot.util import AlphaFoldVersion

import GlobalData as GD

from . import settings as st
from . import workflows
from .settings import parser

url_prefix = "/vrprot"

blueprint = flask.Blueprint(
    "vrprot",
    __name__,
    url_prefix=url_prefix,
    template_folder=st._FLASK_TEMPLATE_PATH,
    static_folder=st._FLASK_STATIC_PATH,
)


@blueprint.route("/fetch", methods=["GET"])
def fetch():
    """Fetches the image from the server and returns it as a response."""
    res = workflows.fetch(parser, flask.request)
    return flask.jsonify(res)


@blueprint.route("/project", methods=["GET"])
def fetch_structures_for_project():
    res = workflows.for_project(parser, flask.request)
    return flask.jsonify(res)
