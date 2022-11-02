import json
import os
import random

import flask
from PIL import Image

import GlobalData as GD
import uploader
from websocket_functions import bcolors



url_prefix = "/doku"
blueprint = flask.Blueprint(
    "doku",
    __name__,
    url_prefix=url_prefix,
    template_folder="/extensions/documentation/src/templates" ,
    static_folder="/extensions/documentation/src/static",
)


@blueprint.route("/main")
def string_main(): 
    return "reeee"
