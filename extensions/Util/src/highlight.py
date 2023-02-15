import json
import os
from multiprocessing import Pool

import numpy as np
import pandas as pd
import swifter
from PIL import Image

SELECTED = (
    255,
    0,
    0,
    255,
)
NOT_SELECTED = (
    0,
    0,
    200,
    10,
)


def selected_color(x):
    # return x
    return SELECTED


def not_selected_color(x):
    # return x[:3] + (10,)
    return NOT_SELECTED


def extract_node_data_from_tex(project, layout):
    # layout = os.path.join("static", "projects", project, "layouts",layout+"XYZ.bmp")
    # layout_low = os.path.join("static", "projects", project, "layoutsl",layout+"XYZl.bmp")
    layout_rgb = os.path.join("static", "projects", project, "layoutsRGB", layout)
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
        x
        if x != (0, 0, 0, 0)
        and x != "<NA>"
        and x != np.nan
        and not isinstance(x, float)
        else pd.NA
        for x in image.getdata()
    ]
    nodes = nodes[nodes["c"].notna()].copy()
    nodes = nodes.reindex(range(0, nodes.index.max() + 1))

    # names_file = os.path.join("static", "projects", project, "names.json")

    # names = pd.read_json(names_file)
    # nodes["name"] = names["names"].apply(lambda x: x[0])
    # nodes["attr"] = names["names"].apply(lambda x: x[1:])

    return nodes


def extract_link_data_from_tex(project, layout):
    layout_xyz = os.path.join(
        "static", "projects", project, "links", layout.replace("RGB.png", "XYZ.bmp")
    )
    layout_rgb = os.path.join("static", "projects", project, "linksRGB", layout)
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
    img_data = pd.DataFrame()
    img_data["data"] = [
        x
        if x != (0, 0, 0, 0)
        and x != "<NA>"
        and x != np.nan
        and not isinstance(x, float)
        else pd.NA
        for x in image.getdata()
    ]
    img_data = img_data[img_data["data"].notna()].copy()
    img_data = img_data.reindex(range(0, img_data.index.max() + 1))
    img_data = img_data.applymap(get_index)
    links["start"] = img_data[::2].reset_index().drop(columns="index")
    links["end"] = img_data[1::2].reset_index().drop(columns="index")

    # Colors
    image = Image.open(layout_rgb)
    colors = pd.DataFrame()
    colors["data"] = None
    colors["data"] = [
        x if x != (0, 0, 0, 0) or pd.isna(x) else 0 for x in image.getdata()
    ]
    links["c"] = colors
    return links, image.size


def handle_node_layout(selected_nodes, project, out, layout):
    # log.debug("Handling layout", layout)
    nodes = extract_node_data_from_tex(project, layout)
    selected_nodes = nodes.index.isin(selected_nodes)
    not_selected = nodes[~selected_nodes].copy()
    selected = nodes[selected_nodes].copy()

    selected["c"] = selected["c"].swifter.apply(selected_color)
    not_selected["c"] = not_selected["c"].swifter.apply(not_selected_color)
    nodes = pd.concat([selected, not_selected])
    color_float = nodes["c"].apply(lambda x: True if x == np.nan else False)
    color_float = nodes[color_float]

    nodes["c"] = nodes["c"].fillna(0)
    nodes = nodes.sort_index()

    out = os.path.join("static", "projects", out, "layoutsRGB", layout)
    img = Image.new("RGBA", (128, 128))
    img.putdata(nodes["c"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out)
    return


def highlight_nodes(selected, layouts, project, out):
    n = len(layouts)
    p = n
    if n > os.cpu_count():
        p = os.cpu_count()
    pool = Pool(p)
    pool.starmap(
        handle_node_layout, zip([selected] * n, [project] * n, [out] * n, layouts)
    )
    # for layout in layouts:
    #     handle_node_layout(selected, project, out, layout)

    return


def handle_link_layout(selected_nodes, project, out, layout):
    # log.debug("Handling layout", layout)
    links, img_size = extract_link_data_from_tex(project, layout)
    selected_links = links["start"].isin(selected_nodes) | links["end"].isin(
        selected_nodes
    )
    not_selected = links[~selected_links.values].copy()
    selected = links[selected_links.values].copy()

    not_selected["c"].values[:] = 0

    links = pd.concat([selected, not_selected])

    links = links.sort_index()
    links["c"] = links["c"].fillna(0)

    out = os.path.join("static", "projects", out, "linksRGB", layout)
    img = Image.new("RGBA", img_size)
    img.putdata(links["c"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out)


def highlight_links(selected_nodes, layouts, project, out):
    n = len(layouts)
    p = n
    if n > os.cpu_count():
        p = os.cpu_count()
    pool = Pool(p)

    pool.starmap(
        handle_link_layout, zip([selected_nodes] * n, [project] * n, [out] * n, layouts)
    )


if __name__ == "__main__":
    # nodes = extract_node_data_from_tex("alz_100_ppi","cy")
    selected = [20, 50, 30]
    highlight_nodes(selected, "alz_100_ppi", "cy")
    # print("Nodes extracted")
    # extract_link_data_from_tex("alz_100_ppi", "any")
    # print("Links extracted")
