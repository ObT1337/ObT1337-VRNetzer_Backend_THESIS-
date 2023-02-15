import json
import os
import random
import shutil
import time
from multiprocessing import Process

import GlobalData as GD

from . import highlight


def highlight_selected_node_links(message):
    selected = GD.sessionData["selected"]
    # selected = random.choices(range(16421), k=100)
    selected = [int(i) for i in selected]
    project = GD.sessionData["actPro"]
    layout = message["layout"]
    layout_rgb = message["layoutRGB"]
    linkl = message["linkl"]
    link_rgb = message["linkRGB"]
    tab = message["main_tab"]
    with open(os.path.join("static", "projects", project, "pfile.json")) as f:
        pfile = json.load(f)
        origin = pfile.get("origin")
        if origin:
            project = origin
        pfile["selections"] = {
            "layout": layout,
            "layoutRGB": layout_rgb,
            "linkl": linkl,
            "linkRGB": link_rgb,
            "main_tab": tab,
        }
        pfile["origin"] = project
        pfile["name"] = "tmp"

    project_dir = os.path.join("static", "projects", project)
    tmp_dir = os.path.join("static", "projects", "tmp")
    process_dir = os.path.join("static", "projects", "process")
    if os.path.exists(process_dir):
        shutil.rmtree(process_dir)

    shutil.copytree(project_dir, process_dir, dirs_exist_ok=True)

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    shutil.copytree(process_dir, tmp_dir, dirs_exist_ok=True)

    shutil.rmtree(os.path.join(tmp_dir, "layoutsRGB"))
    shutil.rmtree(os.path.join(tmp_dir, "linksRGB"))
    with open(os.path.join("static", "projects", "tmp", "pfile.json"), "w") as f:
        json.dump(pfile, f)

    layouts = os.listdir(os.path.join(process_dir, "layoutsRGB"))
    layout = os.path.join(tmp_dir, "layouts", layout + ".bmp")
    layout_rgb = os.path.join(tmp_dir, "layoutsRGB", layout_rgb + ".png")
    linkl = os.path.join(tmp_dir, "links", linkl + ".bmp")
    link_rgb = os.path.join(tmp_dir, "linksRGB", link_rgb + ".png")

    nodes = Process(
        target=highlight.highlight_nodes,
        args=(
            selected,
            layouts,
            "process",
            "tmp",
        ),
    )

    layouts = os.listdir(os.path.join(process_dir, "linksRGB"))
    links = Process(
        target=highlight.highlight_links,
        args=(
            selected,
            layouts,
            "process",
            "tmp",
        ),
    )

    for proc in [nodes, links]:
        proc.start()
    for proc in [nodes, links]:
        proc.join()

    shutil.rmtree(process_dir)
