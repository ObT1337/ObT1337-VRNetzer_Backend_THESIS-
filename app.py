import csv
import json
import logging
import os
from cgi import print_arguments
from io import StringIO

import flask
# from flask_session import Session
from engineio.payload import Payload
from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)
from flask_socketio import SocketIO, emit, join_room, leave_room
from PIL import Image

import GlobalData as GD
import load_extensions
import search
import uploader
import util
import websocket_functions as webfunc

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

# Payload.max_decode_packets = 50


app = Flask(__name__)
app.debug = False
app.config["SECRET_KEY"] = "secret"
app.config["SESSION_TYPE"] = "filesystem"

app, extensions = load_extensions.load(app)


socketio = SocketIO(app, manage_session=False)

### HTML ROUTES ###
@app.route("/websocket_tutorial")
def websockets_tutorial():
    data = json.dumps(
        {
            "fruits": ["apples", "bananas", "oranges"],
            "pets": ["lizard", "bug", "cat", "mouse", "pokemon"],
        }
    )
    return render_template("websockets_tutorial.html", data=data)


@app.route("/tabstest")
def tabstest():
    data = json.dumps(
        {
            "fruits": ["apples", "bananas", "oranges"],
            "pets": ["lizard", "bug", "cat", "mouse", "pokemon"],
        }
    )
    return render_template("dyntabtest.html", data=data)


# note to self:
# - only include 100% working code in releases
# - have homies commit stuff and star the git
# - make a webscraper for git and display contributors for a spec software in vr


@app.route("/main", methods=["GET"])
def main():
    username = util.generate_username()
    project = flask.request.args.get("project")
    if project is None:
        project = "none"
    else:
        print(project)

    if flask.request.method == "GET":

        room = 1
        # Store the data in session
        flask.session["username"] = username
        flask.session["room"] = room
        # prolist = uploader.listProjects()
        if project != "none":
            folder = "static/projects/" + project + "/"
            with open(folder + "pfile.json", "r") as json_file:
                GD.pfile = json.load(json_file)
                print(GD.pfile)
            json_file.close()

            with open(folder + "names.json", "r") as json_file:
                GD.names = json.load(json_file)
                # print(names)
            json_file.close()
        return render_template(
            "main.html",
            session=flask.session,
            sessionData=json.dumps(GD.sessionData),
            pfile=json.dumps(GD.pfile),
            extensions=extensions,
        )
    else:
        return "error"


@app.route("/nodepanel", methods=["GET"])
def nodepanel():
    # try:
    #    id = int(request.args.get("id"))
    # except:
    #    print('C_DEBUG: in except at start')
    #    if id is None:
    #        id=0
    nodes = {"nodes": []}
    project = flask.request.args.get("project")
    if project is None:
        project = GD.sessionData.get("actPro", "new_ppi")

    folder = os.path.join("static", "projects", project)

    if os.path.exists(os.path.join(folder, "pfile.json")):
        with open(os.path.join(folder, "pfile.json"), "r") as json_file:
            GD.pfile = json.load(json_file)

        with open(os.path.join(folder, "nodes.json"), "r") as json_file:
            nodes = json.load(json_file)
    else:
        GD.pfile = None

    add_key = "NA"  # Additional key to show under Structural Information
    # nodes = {node["id"]: node for node in nodes}

    if GD.pfile:
        ppi = False
        if "ppi" in GD.pfile["name"].lower():
            ppi = True
        if GD.pfile.get("network_type"):
            if GD.pfile["network_type"] == "ppi":
                ppi = True
        if ppi:
            try:
                id = int(flask.request.args.get("id"))
            except Exception as e:
                print(e)
                id = 0
            node = nodes["nodes"][id]
            uniprots = node.get("uniprot")
            if uniprots:
                room = flask.session.get("room")
                # GD.sessionData["actStruc"] = uniprots[0]
                x = '{"id": "prot", "val":[], "fn": "prot"}'
                data = json.loads(x)
                data["val"] = uniprots
                print(data)
                socketio.emit("ex", data, namespace="/chat", room=room)
            # data = names["names"][id]
            return render_template(
                "new_nodepanelppi.html",
                sessionData=json.dumps(GD.sessionData),
                session=flask.session,
                pfile=GD.pfile,
                id=id,
                add_key=add_key,
                node=json.dumps({"node": node}),
                extensions=extensions,
            )

        else:
            try:
                id = int(flask.request.args.get("id"))
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
                sessionData=json.dumps(GD.sessionData),
                extensions=extensions,
            )
    else:
        try:
            id = int(flask.request.args.get("id"))
        except Exception as e:
            id = 0
            print(e)
        print("C_DEBUG: in except else (no pfile)")
        data = {"names": [id]}
        return render_template(
            "nodepanel.html",
            data=data,
            sessionData=json.dumps(GD.sessionData),
            extensions=extensions,
        )


@app.route("/upload", methods=["GET"])
def upload():
    prolist = uploader.listProjects()
    return render_template(
        "upload.html",
        namespaces=prolist,
        extensions=extensions,
        sessionData=json.dumps(GD.sessionData),
    )


@app.route("/uploadfiles", methods=["GET", "POST"])
def upload_files():
    return uploader.upload_files(flask.request)


@app.route("/delpro", methods=["GET", "POST"])
def delete_project():

    return util.delete_project(flask.request)


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


@app.route("/ForceLayout")
def force():
    nname = "static/csv/force/nodes/" + flask.request.args.get("nname")
    nodestxt = open(nname + ".json", "r")
    nodes = json.load(nodestxt)

    lname = "static/csv/force/links/" + flask.request.args.get("lname")
    linkstxt = open(lname + ".json", "r")
    links = json.load(linkstxt)
    return render_template(
        "threeJSForceLayout.html",
        nodes=json.dumps(nodes),
        links=json.dumps(links),
        sessionData=json.dumps(GD.sessionData),
    )


@app.route("/preview", methods=["GET"])
def preview():
    data = {}
    layoutindex = 0
    layoutRGBIndex = 0
    linkRGBIndex = 0

    if flask.request.args.get("project") is None:
        print("project Argument not provided - redirecting to menu page")

        data["projects"] = uploader.listProjects()
        return render_template(
            "threeJS_VIEWER_Menu.html",
            data=json.dumps(data),
            sessionData=json.dumps(GD.sessionData),
        )

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

    print(flask.request.args.get("layout"))
    y = '{"nodes": [], "links":[]}'
    testNetwork = json.loads(y)
    scale = 0.000254

    pname = "static/projects/" + flask.request.args.get("project") + "/pfile"
    p = open(pname + ".json", "r")
    thispfile = json.load(p)
    thispfile["selected"] = [layoutindex, layoutRGBIndex, linkRGBIndex]
    # print(thispfile["layouts"])

    name = "static/projects/" + flask.request.args.get("project") + "/nodes"
    n = open(name + ".json", "r")
    nodes = json.load(n)
    nlength = len(nodes["nodes"])
    # print(nlength)

    lname = "static/projects/" + flask.request.args.get("project") + "/links"
    f = open(lname + ".json", "r")
    links = json.load(f)
    length = len(links["links"])

    im = Image.open(
        "static/projects/"
        + flask.request.args.get("project")
        + "/layouts/"
        + thispfile["layouts"][layoutindex]
        + ".bmp",
        "r",
    )
    iml = Image.open(
        "static/projects/"
        + flask.request.args.get("project")
        + "/layoutsl/"
        + thispfile["layouts"][layoutindex]
        + "l.bmp",
        "r",
    )
    imc = Image.open(
        "static/projects/"
        + flask.request.args.get("project")
        + "/layoutsRGB/"
        + thispfile["layoutsRGB"][layoutRGBIndex]
        + ".png",
        "r",
    )
    imlc = Image.open(
        "static/projects/"
        + flask.request.args.get("project")
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
        "threeJS_VIEWER.html",
        data=json.dumps(testNetwork),
        pfile=json.dumps(thispfile),
        sessionData=json.dumps(GD.sessionData),
    )


# gets information about a specific node (project must be provided as argument)
@app.route("/node", methods=["GET", "POST"])
def nodeinfo():
    id = flask.request.args.get("id")
    key = flask.request.args.get("key")
    name = "static/projects/" + str(flask.request.args.get("project")) + "/nodes"
    nodestxt = open(name + ".json", "r")
    nodes = json.load(nodestxt)
    if key:
        return str(nodes["nodes"][int(id)].get(key))
    else:
        return nodes["nodes"][int(id)]


@app.route("/scale", methods=["GET"])
def get_structure_scale() -> float or str:
    """Return the scale of the structure as a float. If the structure is not found (or not provided), the size file is not available or the mode is not given, the function will return an error message as string. To provide the UniProtID add the 'uniprot=<UniProtID>', for the mode add 'mode=<mode>' to the URL. Currently available modes are 'cartoon' and 'electrostatic'. The default mode is 'cartoon'."""

    uniprot = flask.request.args.get("uniprot")
    mode = flask.request.args.get("mode")
    if mode is None:
        print("Error: No mode provided. Will use default mode 'cartoon'.")
        mode = "cartoon"

    if uniprot is None:
        return f"Error: No UniProtID provided. Example:\n<a href='{flask.request.base_url}?uniprot=A1IGU5'>{flask.request.base_url}?uniprot=A1IGU5</a>"

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


@app.route("/home")
def home():
    if not flask.session.get("username"):
        flask.session["username"] = util.generate_username()
        flask.session["room"] = 1
    return render_template("home.html", sessionData=json.dumps(GD.sessionData))


### DATA ROUTES###


@app.route("/load_all_projects", methods=["GET", "POST"])
def loadAllProjectsR():
    return jsonify(projects=uploader.listProjects())


@app.route("/load_project/<name>", methods=["GET", "POST"])
def loadProjectInfoR(name):
    return uploader.loadProjectInfo(name)


@app.route("/projectAnnotations/<name>", methods=["GET"])
def loadProjectAnnotations(name):
    return uploader.loadAnnotations(name)


### Execute code before first request ###
@app.before_first_request
def execute_before_first_request():
    util.create_dynamic_links(app)
    # util.add_tabs(extensions)
    ...


###SocketIO ROUTES###


@socketio.on("join", namespace="/chat")
def join(message):
    room = flask.session.get("room")
    join_room(room)
    print(
        webfunc.bcolors.WARNING
        + flask.session.get("username")
        + " has entered the room."
        + webfunc.bcolors.ENDC
    )
    emit(
        "status",
        {"msg": flask.session.get("username") + " has entered the room."},
        room=room,
    )


@socketio.on("ex", namespace="/chat")
def ex(message):
    room = flask.session.get("room")
    print(
        webfunc.bcolors.WARNING
        + flask.session.get("username")
        + "ex: "
        + json.dumps(message)
        + webfunc.bcolors.ENDC
    )
    message["usr"] = flask.session.get("username")

    if message["id"] == "projects":
        GD.sessionData["actPro"] = message["opt"]
        folder = os.path.join("static", "projects", GD.sessionData["actPro"])
        with open(os.path.join(folder, "names.json"), "r") as json_file:
            GD.names = json.load(json_file)
        print("changed project to " + GD.sessionData["actPro"])
        print("names_files to " + str(GD.names))
        print("changed activ project " + message["opt"])

    if message["id"] == "search":
        if len(message["val"]) > 1:
            x = '{"id": "sres", "val":[], "fn": "sres"}'
            results = json.loads(x)
            results["val"] = search.search(message["val"])

            emit("ex", results, room=room)

    if message["id"] == "nl":
        message["names"] = []
        message["fn"] = "cnl"
        message["prot"] = []
        message["protsize"] = []
        for id in message["data"]:
            message["names"].append(GD.names["names"][id][0])

            if len(GD.names["names"][id]) == 5:
                message["prot"].append(GD.names["names"][id][3])
                message["protsize"].append(GD.names["names"][id][4])
            else:
                message["prot"].append("x")
                message["protsize"].append(-1)

        
        emit("ex", message, room=room)

    if message["id"] == "structure":
        """Fetch the structure if it is not already available."""
        if "ProteinStructureFetch" in extensions["loaded"]:
            import extensions.ProteinStructureFetch.src.workflows as psf_workflows

            uniprot = message.get("opt")
            if uniprot:
                psf_workflows.fetch([uniprot])
    else:
        emit("ex", message, room=room)
    # webfunc.sendUE4('http://127.0.0.1:3000/in',  {'msg': flask.session.get('username') + ' : ' + message['msg']})


@socketio.on("left", namespace="/chat")
def left(message):
    room = flask.session.get("room")
    username = flask.session.get("username")
    leave_room(room)
    flask.session.clear()
    emit("status", {"msg": username + " has left the room."}, room=room)
    print(
        webfunc.bcolors.WARNING
        + flask.session.get("username")
        + " has left the room."
        + webfunc.bcolors.ENDC
    )
    util.construct_nav_bar(app)


if __name__ == "__main__":
    socketio.run(app, debug=True)
