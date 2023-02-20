import json
import os
from multiprocessing import Pool

import numpy as np
import pandas as pd
import swifter
from PIL import Image

import project as Project

SELECTED = (
    255,
    0,
    0,
    255,
)
NOT_SELECTED = (
    255,
    255,
    255,
    10,
)


def selected_color(x):
    if x[1]:
        return (SELECTED[:3] + (x[1],),)
    return x[0]
    # return SELECTED


def not_selected_color(x):
    # return x[:3] + (10,)
    return NOT_SELECTED


def extract_node_data_from_tex(project: Project, layout, node_annotation):
    # layout = os.path.join("static", "projects", project, "layouts",layout+"XYZ.bmp")
    # layout_low = os.path.join("static", "projects", project, "layoutsl",layout+"XYZl.bmp")

    # image = Image.open(layout)
    # nodes["h"] = [
    #     x if x != (0, 0, 0) else pd.NA for x in image.getdata()
    # ]

    # image = Image.open(layout_low)
    # nodes["l"] = [
    #     x if x != (0, 0, 0) else pd.NA for x in image.getdata()
    # ]
    layout_rgb = os.path.join(project.layouts_rgb_dir, layout)
    columns = ["id"]
    if node_annotation:
        columns.append(node_annotation)
    nodes = project.nodes_df.copy()

    image = Image.open(layout_rgb)
    nodes["c"] = [
        x
        if x != (0, 0, 0, 0)
        and x != "<NA>"
        and x != np.nan
        and not isinstance(x, float)
        else pd.NA
        for x in image.getdata()
    ][: len(nodes)]
    nodes = nodes[nodes["c"].notna()].copy()
    return nodes


def extract_link_data_from_tex(project: Project, layout, link_annotation):
    # layout_xyz = os.path.join(project.links_dir, layout.replace("RGB.png", "XYZ.bmp"))
    layout_rgb = os.path.join(project.links_rgb_dir, layout)
    columns = ["s", "e"]
    if link_annotation:
        columns.append(link_annotation)
    links = project.links_df[[c for c in columns]].copy()

    # Colors
    image = Image.open(layout_rgb)
    links["c"] = [x if x != (0, 0, 0, 0) or pd.isna(x) else 0 for x in image.getdata()][
        : len(links)
    ]
    links = links[links["c"].notna()].copy()
    return links, image.size


def handle_node_layout(selected_nodes, project, out, layout, node_annotation):
    nodes = extract_node_data_from_tex(project, layout, node_annotation)

    selected_nodes = nodes.index.isin(selected_nodes)
    not_selected = nodes[~selected_nodes].copy()
    selected = nodes[selected_nodes].copy()

    selected["c"] = selected["c"].swifter.progress_bar(False).apply(selected_color)
    not_selected["c"] = (
        not_selected["c"].swifter.progress_bar(False).apply(not_selected_color)
    )
    nodes = pd.concat([selected, not_selected])

    nodes["c"] = nodes["c"].fillna(0)
    nodes = nodes.sort_index()

    out = os.path.join(out.layouts_rgb_dir, layout)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img = Image.new("RGBA", (128, 128))
    img.putdata(nodes["c"])

    img.save(out)
    return


def highlight_nodes(selected, layouts, project, out, node_annotation):
    n = len(layouts)
    p = n
    project.read_nodes()
    project.nodes_df = pd.DataFrame(project.nodes["nodes"])
    if n > os.cpu_count():
        p = os.cpu_count()
    pool = Pool(p)
    args = [(selected, project, out, layout, node_annotation) for layout in layouts]
    pool.starmap(handle_node_layout, args)
    pool.close()
    return


def handle_link_layout(
    selected_nodes, selected_links, project, out, mode, layout, link_annotation
):
    # log.debug("Handling layout", layout)
    links, img_size = extract_link_data_from_tex(project, layout, link_annotation)
    if mode == "highlight":
        selected_links = links["s"].isin(selected_nodes) | links["e"].isin(
            selected_nodes
        )
    elif mode == "isolate":
        selected_links = links["s"].isin(selected_nodes) & links["e"].isin(
            selected_nodes
        )
    elif mode == "bipartite":
        selected_links = links["s"].isin(selected_nodes) ^ links["e"].isin(
            selected_nodes
        )
    not_selected = links[~selected_links.values].copy()
    selected = links[selected_links.values].copy()

    not_selected["c"].values[:] = 0

    links = pd.concat([selected, not_selected])

    links = links.sort_index()
    links["c"] = links["c"].fillna(0)
    out = os.path.join(out.links_rgb_dir, layout)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img = Image.new("RGBA", img_size)
    img.putdata(links["c"])
    img.save(out)
    return


def highlight_links(
    selected_nodes,
    selected_links,
    layouts,
    project: Project,
    out,
    mode,
    link_annotation,
):
    n = len(layouts)
    p = n
    project.read_links()
    project.links_df = pd.DataFrame(project.links["links"])
    project.links_df: pd.DateOffset
    if len(selected_nodes) == 0:
        project.links_df = project.links_df[project.links_df.index.isin(selected_links)]
        selected_nodes = pd.concat(project.links_df[["s", "e"]]).unique()

    if n > os.cpu_count():
        p = os.cpu_count()
    pool = Pool(p)
    args = [
        (selected_nodes, selected_links, project, out, mode, layout, link_annotation)
        for layout in layouts
    ]
    pool.starmap(handle_link_layout, args)
    return selected_nodes


if __name__ == "__main__":
    # nodes = extract_node_data_from_tex("alz_100_ppi","cy")
    selected = [20, 50, 30]
    highlight_nodes(selected, "alz_100_ppi", "cy")
    # print("Nodes extracted")
    # extract_link_data_from_tex("alz_100_ppi", "any")
    # print("Links extracted")
