import csv
import json
import os
from io import StringIO

import networkx as nx
from flask import Flask, jsonify, redirect, render_template, request
from PIL import Image

from GlobalData import *


def makeProjectFolders(name):
    path = "static/projects/" + name
    pfile = {}
    pfile["name"] = name
    pfile["layouts"] = []
    pfile["layoutsRGB"] = []
    pfile["links"] = []
    pfile["linksRGB"] = []
    pfile["selections"] = []

    try:
        os.mkdir(path)
        os.mkdir(path + "/layouts")
        os.mkdir(path + "/layoutsl")
        os.mkdir(path + "/layoutsRGB")
        os.mkdir(path + "/links")
        os.mkdir(path + "/linksRGB")

        with open(path + "/pfile.json", "w") as outfile:
            json.dump(pfile, outfile)

    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)


def loadProjectInfo(name):
    folder = "static/projects/" + name + "/"
    layoutfolder = folder + "layouts"
    layoutRGBfolder = folder + "layoutsRGB"
    linksRGBfolder = folder + "linksRGB"
    linkfolder = folder + "links"

    if os.path.exists(folder):

        layouts = [name for name in os.listdir(layoutfolder)]
        layoutsRGB = [name for name in os.listdir(layoutRGBfolder)]
        links = [name for name in os.listdir(linkfolder)]
        linksRGB = [name for name in os.listdir(linksRGBfolder)]

        return jsonify(
            layouts=layouts, layoutsRGB=layoutsRGB, links=links, linksRGB=linksRGB
        )
    else:
        return "no such project"


def loadAnnotations(name):
    """Return all annotations corresponding to a project name."""
    namefile = "static/projects/" + name + "/names.json"
    f = open(namefile)
    data = json.load(f)
    return data


def listProjects():
    """Returns a list of all projects."""
    folder = "static/projects"
    sub_folders = [
        name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))
    ]
    print(sub_folders)
    return sub_folders


# TODO other name for variable filename. maybe Layout name
def makeNodeTex(project: str, filenname: str, nodes: dict) -> str:
    """Generates Node textures from a dictionary of nodes."""

    elem = len(nodes)
    hight = 128 * (int(elem / 16384) + 1)

    print("hight is " + str(hight))
    size = 128 * hight
    path = "static/projects/" + project

    texh = [(0, 0, 0)] * size
    texl = [(0, 0, 0)] * size
    texc = [(0, 0, 0, 0)] * size

    new_imgh = Image.new("RGB", (128, hight))
    new_imgl = Image.new("RGB", (128, hight))
    new_imgc = Image.new("RGBA", (128, hight))
    attrlist = {}
    attrlist["names"] = []
    for i, elem in enumerate(nodes):
        position = elem["pos"]
        name = ["NA"]
        if "uniprotid" in elem.keys():
            name = [elem["uniprotid"]]
        elif "display name" in elem.keys():
            gene_name = elem["display name"]
            name = [f"GENENAME={gene_name}"]
        attrlist["names"].append(name)
        coords = [0, 0, 0]  # x,y,z
        color = [255, 0, 255, 255]  # r,g,b
        for d, _ in enumerate(position):
            coords[d] = int(float(position[d]) * 65280)
            # channels[i] = int(float()) # TODO decide on color
        high = [value // 255 for value in coords]
        low = [value % 255 for value in coords]

        texh[i] = tuple(high)
        texl[i] = tuple(low)
        texc[i] = tuple(color)

    new_imgh.putdata(texh)
    new_imgl.putdata(texl)
    new_imgc.putdata(texc)

    with open(path + "/names.json", "w") as outfile:
        json.dump(attrlist, outfile)
    pathXYZ = path + "/layouts/" + filenname + "XYZ.bmp"
    pathXYZl = path + "/layoutsl/" + filenname + "XYZl.bmp"
    pathRGB = path + "/layoutsRGB/" + filenname + "RGB.png"

    # new_imgh.save(pathXYZ)
    # new_imgl.save(pathXYZl)
    # new_imgc.save(pathRGB, "PNG")
    # return '<a style="color:green;">SUCCESS </a>' + filenname + " Node Textures Created"
    if os.path.exists(pathXYZ):
        return (
            '<a style="color:red;">ERROR </a>'
            + filenname
            + " Nodelist already in project"
        )
    else:
        new_imgh.save(pathXYZ)
        new_imgl.save(pathXYZl)
        new_imgc.save(pathRGB, "PNG")
        return (
            '<a style="color:green;">SUCCESS </a>'
            + filenname
            + " Node Textures Created"
        )


# TODO other name for variable filename. maybe Layout name
def makeLinkTex(project: str, filenname: str, edges: dict, nodes: list) -> str:
    """Generate a Link texture from a dictionary of edges."""

    # elem = len(edges)
    hight = 512  # int(elem / 512)+1
    path = "static/projects/" + project

    texl = [(0, 0, 0)] * 1024 * hight
    texc = [(0, 0, 0, 0)] * 512 * hight
    new_imgl = Image.new("RGB", (1024, hight))
    new_imgc = Image.new("RGBA", (512, hight))
    node_ids = {}
    for i, node in enumerate(nodes):
        node_ids[node] = i

    for i, edge in enumerate(edges):
        source = int(node_ids[edge["source"]])
        target = int(node_ids[edge["target"]])
        sx = source % 128
        syl = source // 128 % 128
        syh = source // 16384

        ex = target % 128
        eyl = target // 128 % 128
        eyh = target // 16384
        # TODO Add Color if wished
        r = 0
        g = 100
        b = 255
        a = 90

        pixell1 = (sx, syl, syh)
        pixell2 = (ex, eyl, eyh)
        pixelc = (r, g, b, a)

        if i >= 262144:
            break

        texl[i * 2] = pixell1
        texl[i * 2 + 1] = pixell2
        texc[i] = pixelc
    new_imgl.putdata(texl)
    new_imgc.putdata(texc)
    pathl = path + "/links/" + filenname + "XYZ.bmp"
    pathRGB = path + "/linksRGB/" + filenname + "RGB.png"

    # new_imgl.save(pathl, "PNG")
    # new_imgc.save(pathRGB, "PNG")
    # return '<a style="color:green;">SUCCESS </a>' + filenname + " Link Textures Created"
    if os.path.exists(pathl):
        return (
            '<a style="color:red;">ERROR </a>'
            + filenname
            + " linklist already in project"
        )
    else:
        new_imgl.save(pathl, "PNG")
        new_imgc.save(pathRGB, "PNG")
        return (
            '<a style="color:green;">SUCCESS </a>'
            + filenname
            + " Link Textures Created"
        )


# TODO other name for variable filename. maybe Layout name
def upload_files(project: str, filename: str, node_data: dict, edge_data: dict):
    """Generates textures and upload the needed network files."""
    prolist = listProjects()
    # GET LAYOUT

    if project in prolist:
        print("project exists")
    else:
        # Make Folders
        makeProjectFolders(project)

    folder = "static/projects/" + project + "/"
    pfile = {}

    with open(folder + "pfile.json", "r") as json_file:
        pfile = json.load(json_file)
    json_file.close()

    state = ""
    # layout_files = request.files.getlist("layouts")  # If a network has multiple layouts

    state = state + " <br>" + makeNodeTex(project, filename, node_data.values())
    pfile["layouts"].append(filename + "XYZ")
    pfile["layoutsRGB"].append(filename + "RGB")

    # print(contents)
    # x = validate_layout(contents.split("\n"))
    # print("layout errors are", x)
    # if x[1] == 0:

    # Upload.upload_layouts(namespace, layout_files)

    # GET EDGES
    pfile["links"].append(filename + "XYZ")
    pfile["linksRGB"].append(filename + "RGB")
    state = (
        state
        + " <br>"
        + makeLinkTex(project, filename, edge_data.values(), node_data.keys())
    )

    # update the projects file
    with open(folder + "pfile.json", "w") as json_file:
        json.dump(pfile, json_file)

    global sessionData
    sessionData["proj"] = listProjects()

    return state


def prepare_networkx_network(G: nx.Graph, positions: dict = None) -> tuple[dict, dict]:
    """Transforms a basic networkx graph into a correct data structure to be uploaded by the Cytoscape uploader. If the positions are not given, the positions are calculated using the spring layout algorithm of networkx."""
    if positions is None:
        positions = nx.spring_layout(G, dim=3)
    nodes_data = {}
    edges_data = {}
    for node in G.nodes():
        nodes_data[node] = {
            "pos": positions[node],
            "uniprotid": node,
            "display name": "Gene Name of the Protein",
        }
    for edge in G.edges():
        edges_data[edge] = {"source": edge[0], "target": edge[1]}
    return nodes_data, edges_data


sessionData["proj"] = listProjects()
