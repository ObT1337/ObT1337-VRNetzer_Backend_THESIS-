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

import load_extensions
from GlobalData import *
from search import *
from uploader import *
from websocket_functions import *

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

# Payload.max_decode_packets = 50


app = Flask(__name__)
app.debug = False
app.config["SECRET_KEY"] = "secret"
app.config["SESSION_TYPE"] = "filesystem"

app = load_extensions.load(app)

socketio = SocketIO(app, manage_session=False)

### HTML ROUTES ###


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


# note to self:
# - only include 100% working code in releases
# - have homies commit stuff and star the git
# - make a webscraper for git and display contributors for a spec software in vr


@app.route("/search", methods=["GET"])
def searchR():
    term = request.args.get("term")
    return jsonify(search(term))


@app.route("/upload", methods=["GET"])
def upload():
    prolist = listProjects()
    return render_template("upload.html", namespaces=prolist)


@app.route("/Examples/CustomElements1")
def CustomElements1R():
    return render_template("geneElement.html")


@app.route("/Examples/ServerSideVar")
def ServerSideVarR():
    return render_template("scroll.html", data=scb1Data)


@app.route("/Examples/CustomElements2")
def test3():
    return render_template("test.html")


@app.route("/ForceLayout")
def force():
    nname = "static/csv/force/nodes/" + request.args.get("nname")
    nodestxt = open(nname + ".json", "r")
    nodes = json.load(nodestxt)

    lname = "static/csv/force/links/" + request.args.get("lname")
    linkstxt = open(lname + ".json", "r")
    links = json.load(linkstxt)
    return render_template(
        "threeJSForceLayout.html", nodes=json.dumps(nodes), links=json.dumps(links)
    )


@app.route("/Graph")
def test4():
    # y = '{"nodes": [{"p":[10,0.5,0]},{"p":[0,-10,1]},{"p":[0.5,0.5,0.5]}], "links":[{"s":0,"e":1},{"s":1,"e":2},{"s":2,"e":0}]}'
    y = '{"nodes": [], "links":[]}'
    testNetwork = json.loads(y)
    scale = 10.0

    name = "static/csv/teapot_nodes"
    f = open(name + ".csv", "r")
    lines = f.readlines()

    for i in lines:
        verts = list(i.split(","))
        newnode = {}
        newnode["p"] = [
            float(verts[0]) * scale,
            float(verts[1]) * scale,
            float(verts[2]) * scale,
        ]
        testNetwork["nodes"].append(newnode)

    f.close()

    name = "static/csv/teapot_links"
    f = open(name + ".csv", "r")
    lines = f.readlines()

    for i in lines:
        verts = list(i.split(","))
        newlink = {}
        newlink["s"] = int(verts[0])
        newlink["e"] = int(verts[1])
        testNetwork["links"].append(newlink)

    f.close()

    # print(testNetwork)
    # return render_template('threeJSTest1.html', data = json.dumps('{"nodes": [{"p":[1,0.5,0]},{"p":[0,0.5,1]},{"p":[0.5,0.5,0.5]}]}'))
    return render_template("threeJS_VIEWER.html", data=json.dumps(testNetwork))


@app.route("/preview", methods=["GET"])
def test44():
    data = {}
    layoutindex = 0
    layoutRGBIndex = 0
    linkRGBIndex = 0

    if request.args.get("project") is None:
        print("project Argument not provided - redirecting to menu page")

        data["projects"] = listProjects()
        return render_template("threeJS_VIEWER_Menu.html", data=json.dumps(data))

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

    print(request.args.get("layout"))
    y = '{"nodes": [], "links":[]}'
    testNetwork = json.loads(y)
    scale = 0.000254

    pname = "static/projects/" + request.args.get("project") + "/pfile"
    p = open(pname + ".json", "r")
    thispfile = json.load(p)
    thispfile["selected"] = [layoutindex, layoutRGBIndex, linkRGBIndex]
    # print(thispfile["layouts"])

    name = "static/projects/" + request.args.get("project") + "/nodes"
    n = open(name + ".json", "r")
    nodes = json.load(n)
    nlength = len(nodes["nodes"])
    # print(nlength)

    lname = "static/projects/" + request.args.get("project") + "/links"
    f = open(lname + ".json", "r")
    links = json.load(f)
    length = len(links["links"])

    im = Image.open(
        "static/projects/"
        + request.args.get("project")
        + "/layouts/"
        + thispfile["layouts"][layoutindex]
        + ".bmp",
        "r",
    )
    iml = Image.open(
        "static/projects/"
        + request.args.get("project")
        + "/layoutsl/"
        + thispfile["layouts"][layoutindex]
        + "l.bmp",
        "r",
    )
    imc = Image.open(
        "static/projects/"
        + request.args.get("project")
        + "/layoutsRGB/"
        + thispfile["layoutsRGB"][layoutRGBIndex]
        + ".png",
        "r",
    )
    imlc = Image.open(
        "static/projects/"
        + request.args.get("project")
        + "/linksRGB/"
        + thispfile["linksRGB"][linkRGBIndex]
        + ".png",
        "r",
    )

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
        "threeJS_VIEWER.html", data=json.dumps(testNetwork), pfile=json.dumps(thispfile)
    )


@app.route("/node", methods=["GET", "POST"])
def nodeinfo():
    id = request.args.get("id")
    key = request.args.get("key")
    name = "static/projects/" + str(request.args.get("project")) + "/nodes"
    nodestxt = open(name + ".json", "r")
    nodes = json.load(nodestxt)
    if key:
        return str(nodes["nodes"][int(id)].get(key))
    else:
        return nodes["nodes"][int(id)]


@app.route("/scale", methods=["GET"])
def get_structure_scale() -> float or str:
    """Return the scale of the structure as a float. If the structure is not found (or not provided), the size file is not available or the mode is not given, the function will return an error message as string. To provide the UniProtID add the 'uniprot=<UniProtID>', for the mode add 'mode=<mode>' to the URL. Currently available modes are 'cartoon' and 'electrostatic'. The default mode is 'cartoon'."""

    uniprot = request.args.get("uniprot")
    mode = request.args.get("mode")

    if mode is None:
        print("Error: No mode provided. Will use default mode 'cartoon'.")
        mode = "cartoon"

    if uniprot is None:
        return "Error: No UniProtID provided."

    possible_files = {
        "cartoon": os.path.join(".", "static", "csv", "scales_Cartoon.csv"),
        "electrostatic": os.path.join(
            ".", "static", "csv", "scales_electrostatic_surface.csv"
        ),
    }
    scale_file = possible_files.get(mode)

    # Prevent FileNotFound errors.
    if scale_file is None:
        return "Error: Mode not available."
    if not os.path.exists(scale_file):
        return "Error: File not found."

    # Search for size of structure.
    with open(scale_file, "r") as f:
        csv_file = csv.reader(f)
        for row in csv_file:
            if row[0] == uniprot:
                scale = row[1]
                return scale

    # Structure not found in the scale file -> no available.
    return "Error: No structure available for this UniProtID."


### DATA ROUTES###

###RECEIVE INCOMING WEBSOCKET MSG FROM NODE.JS
@app.route("/flask", methods=["GET", "POST"])
def ws_receiver():
    wsreceiver(socketio)
    return


@app.route("/uploadfiles", methods=["GET", "POST"])
def uploadR():
    return upload_files(request)


@app.route("/load_all_projects", methods=["GET", "POST"])
def loadAllProjectsR():
    return jsonify(projects=listProjects())


@app.route("/load_project/<name>", methods=["GET", "POST"])
def loadProjectInfoR(name):
    return loadProjectInfo(name)


@app.route("/projectAnnotations/<name>", methods=["GET"])
def loadProjectAnnotations(name):
    return loadAnnotations(name)


@app.route("/main", methods=["GET"])
def main():
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
            folder = "static/projects/" + project + "/"
            with open(folder + "pfile.json", "r") as json_file:
                global pfile
                pfile = json.load(json_file)
                print(pfile)
            json_file.close()

            with open(folder + "names.json", "r") as json_file:
                global names
                names = json.load(json_file)
                # print(names)
            json_file.close()
        return render_template(
            "main.html",
            session=session,
            sessionData=json.dumps(sessionData),
            pfile=json.dumps(pfile),
        )
    else:
        return "error"


@app.route("/login/<usr>", methods=["GET"])
def loginR(usr):
    if request.method == "GET":
        username = usr
        room = 1
        # Store the data in session
        session["username"] = username
        session["room"] = room
        return render_template("geneElement.html", session=session)
    else:
        return "error"


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        username = request.form["username"]
        room = request.form["room"]
        # Store the data in session
        session["username"] = username
        session["room"] = room
        return render_template("chat.html", session=session)
    else:
        if session.get("username") is not None:
            session["username"] = "reee"
            session["room"] = "2"
            return render_template("chat.html", session=session)
        else:
            return redirect(url_for("index"))


@app.route("/Test")
def test():
    return render_template("test.html")


@app.route("/nodepanel", methods=["GET"])
def nodepanel():
    # try:
    #    id = int(request.args.get("id"))
    # except:
    #    print('C_DEBUG: in except at start')
    #    if id is None:
    #        id=0
    nodes = {"nodes": []}
    project = request.args.get("project")
    if project is None:
        project = "new_ppi"

    folder = os.path.join("static", "projects", project)
    with open(os.path.join(folder, "pfile.json"), "r") as json_file:
        global pfile
        pfile = json.load(json_file)

    with open(os.path.join(folder, "nodes.json"), "r") as json_file:
        nodes = json.load(json_file)

    add_key = "NA"  # Additional key to show under Structural Information
    # nodes = {node["id"]: node for node in nodes}
    global sessionData

    if pfile:
        if "ppi" in pfile["name"].lower():
            try:
                id = int(request.args.get("id"))
            except Exception as e:
                print(e)
                id = 0
            uniprots = nodes["nodes"][id].get("uniprot")
            if uniprots:
                room = session.get("room")
                # sessionData["actStruc"] = uniprots[0]
                x = '{"id": "prot", "val":[], "fn": "prot"}'
                data = json.loads(x)
                data["val"] = uniprots
                print(data)
                socketio.emit("ex", data, namespace="/chat", room=room)
            # data = names["names"][id]
            return render_template(
                "new_nodepanelppi.html",
                sessionData=json.dumps(sessionData),
                session=session,
                pfile=pfile,
                id=id,
                add_key=add_key,
                nodes=nodes,
            )

        else:
            try:
                id = int(request.args.get("id"))
            except Exception as e:
                print("C_DEBUG: in except else with pfile")
                print(e)
                id = 0

            # data = names["names"][id]
            data = [id]
            print("C_DEBUG: general nodepanel")
            return render_template(
                "nodepanel.html",
                data=data,
            )
    else:
        try:
            id = int(request.args.get("id"))
        except Exception as e:
            id = 0
            print(e)
        print("C_DEBUG: in except else (no pfile)")
        data = {"names": [id]}
        return render_template(
            "nodepanel.html",
            data=data,
        )


###SocketIO ROUTES###


@socketio.on("join", namespace="/chat")
def join(message):
    room = session.get("room")
    join_room(room)
    print(
        bcolors.WARNING
        + session.get("username")
        + " has entered the room."
        + bcolors.ENDC
    )
    emit(
        "status", {"msg": session.get("username") + " has entered the room."}, room=room
    )


@socketio.on("ex", namespace="/chat")
def ex(message):
    room = session.get("room")
    print(
        bcolors.WARNING
        + session.get("username")
        + "ex: "
        + json.dumps(message)
        + bcolors.ENDC
    )
    message["usr"] = session.get("username")

    if message["id"] == "projects":
        global sessionData
        sessionData["actPro"] = message["opt"]

        print("changed activ project " + message["opt"])

    if message["id"] == "search":
        if len(message["val"]) > 1:
            x = '{"id": "sres", "val":[], "fn": "sres"}'
            results = json.loads(x)
            results["val"] = search(message["val"])

            emit("ex", results, room=room)

    if message["id"] == "nl":
        message["names"] = []
        message["fn"] = "cnl"
        message["prot"] = []
        message["protsize"] = []
        for id in message["data"]:
            message["names"].append(names["names"][id][0])

            if len(names["names"][id]) == 5:
                message["prot"].append(names["names"][id][3])
                message["protsize"].append(names["names"][id][4])
            else:
                message["prot"].append("x")
                message["protsize"].append(-1)

        print(message)
        emit("ex", message, room=room)

    else:
        emit("ex", message, room=room)
    # sendUE4('http://127.0.0.1:3000/in',  {'msg': session.get('username') + ' : ' + message['msg']})


@socketio.on("left", namespace="/chat")
def left(message):
    room = session.get("room")
    username = session.get("username")
    leave_room(room)
    session.clear()
    emit("status", {"msg": username + " has left the room."}, room=room)
    print(
        bcolors.WARNING + session.get("username") + " has left the room." + bcolors.ENDC
    )


if __name__ == "__main__":
    socketio.run(app, port=3000, debug=True)
