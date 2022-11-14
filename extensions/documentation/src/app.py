import json
import os
import random

import flask
from engineio.payload import Payload
from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)
from PIL import Image

import GlobalData as GD
import uploader
from websocket_functions import bcolors



url_prefix = "/doku"
blueprint = flask.Blueprint(
    "doku",
    __name__,
    url_prefix=url_prefix,
    template_folder="/templates" ,
    static_folder="/static",
)


@blueprint.route("/main")
def string_main(): 
    return "reeee"



@blueprint.route("/ServerSideVar")
def ServerSideVarR():
    return render_template("scroll.html", data=scb1Data)


@blueprint.route("/CustomElements2")
def test3():
    return render_template("test.html")