import csv
import json
import logging
import os
import random
import re
import string
from cgi import print_arguments
from io import StringIO

import flask
# from flask_session import Session
import requests
from engineio.payload import Payload
from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)
from flask_socketio import SocketIO, emit, join_room, leave_room
from PIL import Image

import GlobalData as GD
import load_extensions
import uploader
from search import *
from uploader import *
from websocket_functions import *
from websocket_functions import bcolors

url_prefix = "/doku"
blueprint = flask.Blueprint(
    "doku",
    __name__,
    url_prefix=url_prefix,
    template_folder="/templates" ,
    static_folder="/static",
)

@blueprint.route("/index")
def string_main(): 
    return "reeee"

@blueprint.route('/CustomElements1')
def CustomElements1R():
    return render_template('geneElement.html')

#@blueprint.route('/ServerSideVar')
#def ServerSideVarR():
#    return render_template('scroll.html', data = GD.scb1Data)

@blueprint.route('/CustomElements2')
def test3():
    return render_template('test.html')

