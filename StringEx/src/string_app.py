import json
import os
import random

from flask import Blueprint, render_template, request, session
from GlobalData import pfile, sessionData
from PIL import Image
from websocket_functions import bcolors

from uploader import listProjects

from .settings import (
    _FLASK_STATIC_PATH,
    _FLASK_TEMPLATE_PATH,
    _PROJECTS_PATH,
    _STATIC_PATH,
)
from .uploader import Uploader

string_ex = Blueprint(
    "StringEx",
    __name__,
    url_prefix="/StringEx",
    template_folder=_FLASK_TEMPLATE_PATH,
    static_folder=_FLASK_STATIC_PATH,
)


@string_ex.route("/preview", methods=["GET"])
def string_preview():
    data = {}
    layoutindex = 0
    layoutRGBIndex = 0
    linkRGBIndex = 0
    html_preview = "threeJS_VIEWER_string.html"
    html_menu = "threeJS_VIEWER_Menu.html"
    if request.args.get("project") is None:
        print("project Argument not provided - redirecting to menu page")

        data["projects"] = listProjects()
        print(data["projects"])
        return render_template(html_menu, data=json.dumps(data))

    if request.args.get("layout") is None:
        layoutindex = 0
    else:
        layoutindex = int(request.args.get("layout"))

    if request.args.get("ncol") is None:
        layoutRGBIndex = 0
    else:
        layoutRGBIndex = int(request.args.get("ncol"))

    if request.args.get("lcol") is None:
        linkRGBIndex = 0
    else:
        linkRGBIndex = int(request.args.get("lcol"))

    project = request.args.get("project")
    sessionData["actPro"] = project
    y = '{"nodes": [], "links":[]}'
    testNetwork = json.loads(y)
    scale = 0.000254

    pname = os.path.join(_PROJECTS_PATH, project, "pfile")
    p = open(pname + ".json", "r")
    thispfile = json.load(p)
    thispfile["selected"] = [layoutindex, layoutRGBIndex, linkRGBIndex]
    # print(thispfile["layouts"])

    name = os.path.join(_PROJECTS_PATH, project, "nodes")
    n = open(name + ".json", "r")
    nodes = json.load(n)
    nlength = len(nodes["nodes"])
    # print(nlength)

    lname = os.path.join(_PROJECTS_PATH, project, "links")
    f = open(lname + ".json", "r")
    links = json.load(f)
    length = len(links["links"])

    nodes_im = os.path.join(
        _PROJECTS_PATH,
        project,
        "layouts",
        thispfile["layouts"][layoutindex] + ".bmp",
    )
    im = Image.open(nodes_im, "r")

    nodes_iml = os.path.join(
        _PROJECTS_PATH,
        project,
        "layoutsl",
        thispfile["layouts"][layoutindex] + "l.bmp",
    )
    iml = Image.open(nodes_iml, "r")

    nodes_col = os.path.join(
        _PROJECTS_PATH,
        project,
        "layoutsRGB",
        thispfile["layoutsRGB"][layoutRGBIndex] + ".png",
    )
    imc = Image.open(nodes_col, "r")

    links_col = os.path.join(
        _PROJECTS_PATH,
        project,
        "linksRGB",
        thispfile["linksRGB"][linkRGBIndex] + ".png",
    )
    imlc = Image.open(links_col, "r")

    width, height = im.size
    pixel_values = list(im.getdata())
    pixel_valuesl = list(iml.getdata())
    pixel_valuesc = list(imc.getdata())
    pixel_valueslc = list(imlc.getdata())

    # print(pixel_values[len(pixel_values)-1])
    i = 0
    for x in pixel_values:
        if i < nlength:
            newnode = {}
            pos = [
                float(x[0] * 255 + pixel_valuesl[i][0]) / 65536 - 0.5,
                float(x[1] * 255 + pixel_valuesl[i][1]) / 65536 - 0.5,
                float(x[2] * 255 + pixel_valuesl[i][2]) / 65536 - 0.5,
            ]

            newnode["p"] = pos
            newnode["c"] = pixel_valuesc[i]
            newnode["n"] = nodes["nodes"][i]["n"]
            testNetwork["nodes"].append(newnode)
            i = i + 1

    # print(testNetwork)

    for x in range(length - 1):
        if (
            x < 30000
        ):  # we dont negotiate with terrorists (chris V.R. huetter), who want to render millions of links
            newLink = {}
            newLink["id"] = x
            newLink["s"] = links["links"][x]["s"]
            newLink["e"] = links["links"][x]["e"]
            newLink["c"] = pixel_valueslc[x]
            testNetwork["links"].append(newLink)
        # print(links["links"][x])

    # print(testNetwork)
    # return render_template('threeJSTest1.html', data = json.dumps('{"nodes": [{"p":[1,0.5,0]},{"p":[0,0.5,1]},{"p":[0.5,0.5,0.5]}]}'))
    return render_template(
        html_preview,
        data=json.dumps(testNetwork),
        pfile=json.dumps(thispfile),
        sessionData=json.dumps(sessionData),
    )


@string_ex.route("/upload", methods=["GET"])
def uploadString():
    prolist = listProjects()
    html_page = "string_upload.html"
    return render_template(html_page, namespace=prolist)


@string_ex.route("/evidences", methods=["GET"])
def string_ev():
    html_page = "string_ev.html"
    username = request.args.get("usr")
    project = request.args.get("project")
    if username is None:
        username = str(random.randint(1001, 9998))
    else:
        username = username + str(random.randint(1001, 9998))
        print(username)

    if project is None:
        project = "none"
    else:
        print(project)

    if request.method == "GET":

        room = 1
        # Store the data in session
        session["username"] = username
        session["room"] = room
        # prolist = listProjects()
        if project != "none":
            folder = os.path.join(_VRNETZER_PATH, "static", "projects" + project + "/")
            with open(folder + "pfile.json", "r") as json_file:
                global pfile
                pfile = json.load(json_file)
                # print(pfile)
            json_file.close()

            with open(folder + "names.json", "r") as json_file:
                global names
                names = json.load(json_file)
                # print(names)
            json_file.close()
        return render_template(
            html_page,
            session=session,
            sessionData=json.dumps(sessionData),
            pfile=json.dumps(pfile),
        )
    else:
        return "error"


def prepare_session_data():
    username = request.args.get("usr")
    if username is None:
        username = str(random.randint(1001, 9998))
    else:
        username = username + str(random.randint(1001, 9998))
    session["username"] = username
