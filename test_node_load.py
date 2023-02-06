import pandas as pd
from PIL import Image
import os
import numpy as np


import pandas as pd
from PIL import Image
import os
import numpy as np
import json

def extract_node_data_from_tex(project,layout):
    # layout = os.path.join("static", "projects", project, "layouts",layout+"XYZ.bmp")
    # layout_low = os.path.join("static", "projects", project, "layoutsl",layout+"XYZl.bmp")
    layout_rgb = os.path.join("static", "projects", project, "layoutsRGB",layout+".png")
    nodes = pd.DataFrame()
    # image = Image.open(layout)
    # nodes["h"] = [
    #     x if x != (0, 0, 0) else pd.NA for x in image.getdata()
    # ]

    # image = Image.open(layout_low)
    # nodes["l"] = [
    #     x if x != (0, 0, 0) else pd.NA for x in image.getdata()
    # ]

    image = Image.open(layout_rgb)
    nodes["c"] = [
        x if x != (0, 0, 0, 0) else pd.NA for x in image.getdata()
    ]
    nodes = nodes.dropna(how="all")
    nodes = nodes.reindex(range(0, nodes.index.max() + 1))

    # names_file = os.path.join("static", "projects", project, "names.json")


    # names = pd.read_json(names_file)
    # nodes["name"] = names["names"].apply(lambda x: x[0])
    # nodes["attr"] = names["names"].apply(lambda x: x[1:])

    return nodes

def extract_link_data_from_tex(project, layout):
    layout_xyz = os.path.join("static", "projects", project, "links",layout+".bmp")
    layout_rgb = os.path.join("static", "projects", project, "linksRGB",layout+".png")
    links = pd.DataFrame(columns=["start", "end"])

    def get_index(x):
        if isinstance(x, int):
            return x
        if pd.isna(x):
            return 0
        s, l, h = x
        x = s + l * 128 + h * 128**2
        return x
    
    # Link starts and ends
    image = Image.open(layout_xyz).convert("RGB")
    img_data = pd.DataFrame(
        [(x,) if x != (0, 0, 0) and x != "<NA>" else pd.NA for x in image.getdata()]
    )
    img_data = img_data.dropna(how="all")
    img_data = img_data.reindex(range(0, img_data.index.max() + 1))
    img_data = img_data.applymap(get_index)
    links["start"] = img_data[::2].reset_index().drop(columns="index")
    links["end"] = img_data[1::2].reset_index().drop(columns="index")

    # Colors
    image = Image.open(layout_rgb)
    colors = [(x,) if x != (0, 0, 0, 0) else pd.NA for x in image.getdata()]
    colors = pd.DataFrame(colors)
    colors = colors.dropna(how="all")
    links["c"] = colors
    return links

def highlight_nodes(selected,project,layout,):
    nodes = extract_node_data_from_tex(project,layout)
    selected = nodes.index.isin(selected)
    not_selected = nodes[~selected].copy()
    selected = nodes[selected].copy()
    selected["c"] = selected["c"].apply(lambda x: x[:3]+(255,))
    not_selected["c"] = not_selected["c"].apply(lambda x: x[:3]+(255//8,))
    nodes = pd.concat([selected,not_selected])
    nodes = nodes.sort_index()
    tmp_file = os.path.join("static", "projects", project, "layoutsRGB","tmpRGB.png")
    img = Image.new("RGBA", (128, 128))
    img.putdata(nodes["c"])
    img.save(tmp_file)
    return

def highlight_links(selected,project,layout):
    pass



if __name__ == "__main__":
    # nodes = extract_node_data_from_tex("alz_100_ppi","cy")
    selected = [20,50,30]
    highlight_nodes(selected,"alz_100_ppi","cy")
    # print("Nodes extracted")
    # extract_link_data_from_tex("alz_100_ppi", "any")
    # print("Links extracted")



# @blueprint.on("highlight", namespace="/chat")
# def example_highlight(message):
#     print(message)
#     selected = GD.sessionData["selected"]
#     project = GD.sessionData["actPro"]
#     if message["id"] == "Nodes":
#         print("Highlight Nodes")
#         highlight.highlight_nodes(selected,project,message["layout"])

#         with open(os.path.join("static", "projects", project, "pfile.json"), "r") as f:
#             pfile = json.load(f)
#         if "tmpRGB" not in pfile["layoutsRGB"]:
#             pfile["layoutsRGB"].append("tmpRGB")

#         blueprint.emit("ex", {"pdata":json.dumps(pfile),"fn":"pdata"},namespace="/chat")
#         blueprint.emit("ex",{"id":"project","opt":project,"fn":"sel"},namespace="/chat")
#         blueprint.emit("ex",{"id":"nodecolors","opt":"tmpRGB","fn":"sel"},namespace="/chat")

#     elif message["id"] == "Links":
#         print("Highlight Links")