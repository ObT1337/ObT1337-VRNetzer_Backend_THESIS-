import json
import os
import random

import flask
from PIL import Image

import GlobalData as GD
import uploader
from websocket_functions import bcolors



import csv
import json
import logging
import os
import random
import re
import string
from cgi import print_arguments
from io import StringIO

# from flask_session import Session
import requests
from engineio.payload import Payload
from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)
from flask_socketio import SocketIO, emit, join_room, leave_room
from PIL import Image

import GlobalData as GD
import load_extensions
from search import *
from uploader import *
from websocket_functions import *


url_prefix = "/doku"
blueprint = flask.Blueprint(
    "doku",
    __name__,
    url_prefix=url_prefix,
    template_folder="/extensions/documentation/src/templates" ,
    static_folder="/extensions/documentation/src/static",
)


@blueprint.route('/CustomElements1')
def CustomElements1R():
    return render_template('geneElement.html')

@blueprint.route('/ServerSideVar')
def ServerSideVarR():
    return render_template('scroll.html', data = GD.scb1Data)

@blueprint.route('/CustomElements2')
def test3():
    return render_template('test.html')

