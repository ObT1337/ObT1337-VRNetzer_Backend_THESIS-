import json
import os
import random
import shutil
import time
from multiprocessing import Process

import pandas as pd

import GlobalData as GD
from project import Project

from . import const, highlight

MAX_ANNOT = 30


def highlight_selected_node_links(message):

    mode = message.get("mode", "highlight")
    layout = message.get("layout")
    layout_rgb = message.get("nodecolors")
    linkl = message.get("links")
    link_rgb = message.get("linkcolors")
    tab = message.get("main_tab")

    selected = GD.sessionData.get("selected")
    node_annotation = GD.sessionData.get("node_annotation")
    selected_links = GD.sessionData.get("selected_links")
    link_annotation = GD.sessionData.get("link_annotation")
    # selected = random.choices(range(16421), k=100)
    selected = [int(i) for i in selected]
    project = GD.sessionData["actPro"]
    project = Project(project)
    if layout is None:
        layout = project.get_all_layouts()[0]
    if layout_rgb is None:
        layout_rgb = project.get_all_node_colors()[0]
    if linkl is None:
        linkl = project.get_all_links()[0]
    if link_rgb is None:
        link_rgb = project.get_all_link_colors()[0]

    origin = project.get_pfile_value("origin")
    if origin:
        project = Project(origin)

    process = Project("process")
    process.pfile = project.pfile
    process.set_pfile_value(
        "stateData",
        {
            "layout": layout,
            "nodecolors": layout_rgb,
            "links": linkl,
            "linkcolors": link_rgb,
            "main_tab": tab,
        },
    )
    process.set_pfile_value("origin", project.name)

    if process.exists():
        process.remove()

    project.copy(process.location)
    process.remove_subdir("layoutsRGB")
    process.remove_subdir("linksRGB")
    process.set_pfile_value("name", "tmp")
    process.write_pfile()
    nodes_args = (
        selected,
        project.get_files_in_dir("layoutsRGB"),
        project,
        process,
        node_annotation,
    )
    links_args = (
        selected,
        selected_links,
        project.get_files_in_dir("linksRGB"),
        project,
        process,
        mode,
        link_annotation,
    )
    if len(selected) == 0:
        selected = highlight.highlight_links(*links_args)
        nodes_args[0] = selected
        nodes = highlight.highlight_nodes(*nodes_args)
    else:
        nodes = Process(
            target=highlight.highlight_nodes,
            args=nodes_args,
        )
        links = Process(
            target=highlight.highlight_links,
            args=links_args,
        )

        for proc in [nodes, links]:
            proc.start()
        for proc in [nodes, links]:
            proc.join()

    tmp = Project("tmp")
    if tmp.exists():
        tmp.remove()
    process.copy(tmp.location)
    process.remove()


def select_nodes(message):
    proj = GD.sessionData["actPro"]
    proj = Project(proj)
    nodes = pd.DataFrame(proj.nodes["nodes"])
    dtype = message["dtype"]
    annotation = message["annotation"]
    value = message["value"]
    if dtype in ["float", "int"]:
        nodes = nodes[nodes[annotation] >= value]
    elif dtype in ["object", "bool"]:
        nodes = nodes[nodes[annotation] == value]
    elif dtype in ["str"]:
        if value.endswith("..."):
            value = value[:-3]
        check = nodes[annotation].copy()
        check = check.fillna("")
        nodes = nodes[check.str.startswith(value)]
        nodes = nodes[nodes[annotation].str.startswith(value)]
    GD.sessionData["selected"] = nodes.index.tolist()
    return GD.sessionData["selected"]


def select_links(message):
    proj = GD.sessionData["actPro"]
    proj = Project(proj)
    links = pd.DataFrame(proj.links["links"])
    dtype = message["dtype"]
    annotation = message["annotation"]
    value = message["value"]
    if dtype in ["float", "int"]:
        links = links[links[annotation] >= value]
    elif dtype in ["object", "bool"]:
        links = links[links[annotation] == value]
    GD.sessionData["selected_links"] = links["id"].tolist()
    return GD.sessionData["selected_links"]


def get_annotation(message, return_dict):
    project = message["project"]
    project = Project(project)
    annotation_type = message["type"]
    if annotation_type == "node":
        df = pd.DataFrame(project.nodes["nodes"])
    if annotation_type == "link":
        df = pd.DataFrame(project.links["links"])
        nodes = pd.DataFrame(project.nodes["nodes"])
    dtypes = df.dtypes.astype(str).to_dict()
    drops = [c for c in const.IGNORE_COLS if c in df.columns]
    df = df.drop(columns=drops)
    annotations = {}
    option_annots = {}
    lengths = {}
    for col in df.columns:
        dtype = dtypes[col]
        annot = {"dtype": dtype}
        if col in [const.START_COL, const.END_COL]:
            annot["dtype"] = "int"
            annot["min"] = 0
            annot["max"] = len(nodes) - 1
            annot["values"] = nodes[const.NAME_COL].tolist()
        elif col in const.NAME_COL and annotation_type == "node":
            annot["dtype"] = "int"
            annot["min"] = 0
            annot["max"] = len(df) - 1
            annot["values"] = df[const.NAME_COL].tolist()
            df = df.drop(columns=const.NAME_COL)
        elif pd.api.types.is_integer_dtype(dtype):
            annot["min"] = int(df[col].min())
            annot["max"] = int(df[col].max())
            annot["dtype"] = "int"
        elif pd.api.types.is_float_dtype(dtype):
            annot["min"] = float(df[col].min())
            annot["max"] = float(df[col].max())
            if annot["min"] == annot["max"]:
                continue
            annot["dtype"] = "float"
        elif pd.api.types.is_string_dtype(dtype):

            class set_counter:
                def __init__(self):
                    self.set = set()
                    self.counter = {}

                def add(self, value):
                    self.set.add(value)

                def add_value(self, value):
                    if isinstance(value, str) and len(value) > 20:
                        value = value[:20] + "..."
                    value = str(value)
                    self.add(value)
                    if value not in self.counter:
                        self.counter[value] = 0
                    self.counter[value] += 1

            options = set_counter()

            def collect_values(x):
                if len(options.set) > 100:
                    return
                if isinstance(x, str):
                    options.add_value(x)
                if pd.api.types.is_list_like(x):
                    for val in x:
                        if pd.isna(val):
                            continue
                        options.add_value(val)

            df[col].swifter.progress_bar(False).apply(lambda x: collect_values(x))
            for value in options.counter:
                if options.counter[value] <= 1:
                    options.set.remove(value)
            if len(options.set) < 2:
                continue
            options.set = sorted(
                options.set, key=lambda x: options.counter[x], reverse=True
            )
            annot["dtype"] = "str"
            annot["options"] = list(options.set)
            if len(annot["options"]) > 100:
                continue
            option_annots[col] = annot
            lengths[col] = len(annot["options"])
            continue
        elif dtype == "object":
            continue
        annotations[col] = annot
    # limit the number of annotations to 20 to reduce traffic
    if not len(annotations) + len(option_annots) > MAX_ANNOT:
        space = MAX_ANNOT - len(annotations)
        lengths = sorted(lengths.items(), key=lambda x: x[1], reverse=True)
        option_annots = {key: option_annots[key] for key, _ in lengths[:space]}
        annotations.update(option_annots)
    message = (
        {
            "data": "annotations",
            "type": annotation_type,
            "annotations": annotations,
        },
    )
    return_dict["annotations"] = message


def get_selection(message):
    if message["type"] == "node":
        if message["annotation"] in [const.NAME_COL, const.ID_COL, const.SUID_COL]:
            message["dtype"] = "object"
        selection = select_nodes(message)
        GD.pfile["stateData"]["node_annotation"] = message["annotation"]
        GD.pfile["stateData"]["selected"] = selection
    elif message["type"] == "link":
        if message["annotation"] in [const.START_COL, const.END_COL, const.ID_COL]:
            message["dtype"] = "object"
        selection = select_links(message)
        GD.pfile["stateData"]["link_annotation"] = message["annotation"]
        GD.pfile["stateData"]["selectedLinks"] = selection
    message = {
        "data": "selection",
        "selection": selection,
        "type": message["type"],
    }
    return message


def highlight_func(message):
    mode = message.get("mode", "highlight")
    if mode == "store":
        response = store_highlight(message)
    else:
        selected = GD.pfile.get("stateData", {}).get("selected")
        selectedLinks = GD.pfile.get("stateData", {}).get("selectedLinks")
        if selected is None and selectedLinks is None:
            response = {"status": "error", "message": "No nodes or links selected!"}
            message.update(response)
            return message
        try:
            highlight_selected_node_links(message)
            response = {"message": "Selection highlighted!", "status": "success"}
        except Exception as e:
            response = {"message": str(e), "status": "error"}
    message.update(response)
    return message


def store_highlight(message):
    project = GD.sessionData["actPro"]
    project = Project(project)
    origin = project.get_pfile_value("origin")
    if not origin:
        message = {"message": "Nothing highlighted!", "status": "error"}
        return message
    project = Project(origin)
    new_name = project.name + "_highlight"
    i = 1
    while True:
        if new_name not in GD.sessionData["proj"]:
            break
        new_name += str(i)
        i += 1
    project.copy(new_name)
    GD.sessionData["proj"].append(new_name)
    highlight = Project(new_name)
    highlight.set_pfile_value("origin", origin)
    stateData = {
        "layouts": message["layout"],
        "nodecolors": message["nodecolors"],
        "links": message["links"],
        "linkcolors": message["linkcolors"],
        "main_tab": message["main_tab"],
    }
    highlight.set_pfile_value("stateData", stateData)
    highlight.write_pfile()
    message = {"message": f"Highlighting store as {new_name}", "status": "error"}
    print("Highlighting stored..")
    return message


def reset(message):
    project = GD.sessionData["actPro"]
    project = Project(project)
    origin = project.pfile.get("origin")
    if not origin:
        return None
    project.set_pfile_value(
        "stateData",
        {
            "layouts": message["layout"],
            "nodecolors": message["nodecolors"],
            "links": message["links"],
            "linkcolors": message["linkcolors"],
            "main_tab": message["main_tab"],
        },
    )
    project.write_pfile()
    return origin
