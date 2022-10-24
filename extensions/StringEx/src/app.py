import json
import os
import random

import flask
from PIL import Image
from websocket_functions import bcolors

import GlobalData as GD
import uploader

from .settings import (_FLASK_STATIC_PATH, _FLASK_TEMPLATE_PATH,
                       _PROJECTS_PATH, _STATIC_PATH, _VRNETZER_PATH,
                       LayoutAlgroithms)
from .workflows import VRNetzer_upload_workflow

GD.sessionData["layoutAlgos"] = LayoutAlgroithms.all_algos
GD.sessionData["actAlgo"] = LayoutAlgroithms.spring
url_prefix = "/StringEx"
blueprint = flask.Blueprint(
    "StringEx",
    __name__,
    url_prefix=url_prefix,
    template_folder=_FLASK_TEMPLATE_PATH,
    static_folder=_FLASK_STATIC_PATH,
)


@blueprint.route("/preview", methods=["GET"])
def string_preview():
    data = {}
    layoutindex = 0
    layoutRGBIndex = 0
    linkRGBIndex = 0
    html_preview = "threeJS_VIEWER_string.html"
    html_menu = "threeJS_VIEWER_Menu.html"
    if flask.request.args.get("project") is None:
        print("project Argument not provided - redirecting to menu page")

        data["projects"] = uploader.listProjects()
        print(data["projects"])
        return flask.render_template(html_menu, data=json.dumps(data))

    if flask.request.args.get("layout") is None:
        layoutindex = 0
    else:
        layoutindex = int(flask.request.args.get("layout"))

    if flask.request.args.get("ncol") is None:
        layoutRGBIndex = 0
    else:
        layoutRGBIndex = int(flask.request.args.get("ncol"))

    if flask.request.args.get("lcol") is None:
        linkRGBIndex = 0
    else:
        linkRGBIndex = int(flask.request.args.get("lcol"))

    project = flask.request.args.get("project")
    GD.sessionData["actPro"] = project
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
    # return flask.render_template('threeJSTest1.html', data = json.dumps('{"nodes": [{"p":[1,0.5,0]},{"p":[0,0.5,1]},{"p":[0.5,0.5,0.5]}]}'))
    return flask.render_template(
        html_preview,
        data=json.dumps(testNetwork),
        pfile=json.dumps(thispfile),
        sessionData=json.dumps(GD.sessionData),
    )


@blueprint.route("/upload", methods=["GET"])
def upload_string():
    prolist = listProjects()
    html_page = "string_upload.html"
    return flask.render_template(
        html_page,
        namespaces=prolist,
        algorithms=LayoutAlgroithms.all_algos,
    )


@blueprint.route("/uploadfiles", methods=["GET", "POST"])
def execute_upload():
    return VRNetzer_upload_workflow(flask.request)


@blueprint.route("/evidences", methods=["GET"])
def string_ev():
    html_page = "string_ev.html"
    username = flask.request.args.get("usr")
    project = flask.request.args.get("project")
    if username is None:
        username = str(random.randint(1001, 9998))
    else:
        username = username + str(random.randint(1001, 9998))
        print(username)

    if project is None:
        project = "none"
    else:
        print(project)

    if flask.request.method == "GET":

        room = 1
        # Store the data in flask.session
        flask.session["username"] = username
        flask.session["room"] = room
        # prolist = listProjects()
        if project != "none":
            folder = os.path.join(_VRNETZER_PATH, "static", "projects" + project + "/")
            with open(folder + "pfile.json", "r") as json_file:
                # global pfile
                GD.pfile = json.load(json_file)
                # print(pfile)
            json_file.close()

            with open(folder + "names.json", "r") as json_file:
                global names
                names = json.load(json_file)
                # print(names)
            json_file.close()
        return flask.render_template(
            html_page,
            session=flask.session,
            sessionData=json.dumps(GD.sessionData),
            pfile=json.dumps(GD.pfile),
        )
    else:
        return "error"

@blueprint.route("/ev_tab", methods=["GET","POST"])
def ev_tab():
    return flask.render_template("string_ev.html")
    
@blueprint.route("/up_tab", methods=["GET","POST"])
def up_tab():
    return flask.render_template("string_upload_panel.html")
def prepare_session_data():
    username = flask.request.args.get("usr")
    if username is None:
        username = str(random.randint(1001, 9998))
    else:
        username = username + str(random.randint(1001, 9998))
    flask.session["username"] = username

@blueprint.route("/nodepanel",  methods=["GET"])
def string_nodepanel():
    username = flask.request.args.get("usr")
    project = flask.request.args.get("project")
    if username is None:
            username = str(random.randint(1001, 9998))
    else:
        username = username + str(random.randint(1001, 9998))
        print(username)
    if flask.request.method == "GET":
        room = 1
        # Store the data in flask.session
        flask.session["username"] = username
        flask.session["room"] = room
        # prolist = listProjects()
        data = {"names": [0]}
        return flask.render_template("string_nodepanel.html",data=data)

