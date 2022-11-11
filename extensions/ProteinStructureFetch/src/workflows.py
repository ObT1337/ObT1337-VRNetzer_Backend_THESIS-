import json
import os

import flask
import vrprot
from vrprot.alphafold_db_parser import AlphafoldDBParser
from vrprot.util import AlphaFoldVersion, batch

from . import settings as st
from .settings import NodeTags as NT


def get_scales(uniprot_ids=[], mode=st.DEFAULT_MODE):
    return vrprot.overview_util.get_scale(uniprot_ids, mode)


def fetch(parser: AlphafoldDBParser, request: flask.Request):
    pdb_id = request.args.get("id")
    mode = request.args.get("mode")
    alphafold_ver = request.args.get("ver")
    if pdb_id is None:
        return flask.jsonify({"error": "No PDB ID provided."})
    if mode is None:
        mode = st.DEFAULT_MODE
    if alphafold_ver is not None:
        if alphafold_ver in AlphaFoldVersion.list_of_versions():
            parser.alphafold_ver = alphafold_ver
        else:
            parser.alphafold_ver = AlphaFoldVersion.v4.value
    proteins = [pdb_id]
    batch([parser.fetch_pdb, parser.pdb_pipeline], proteins, parser.batch_size)
    result = get_scales(proteins, mode)
    return {"not_fetched": parser.not_fetched, "results": result}


def for_project(parser, request):
    project = request.args.get("project")
    mode = request.args.get("mode")
    alphafold_ver = request.args.get("ver")
    if project is None:
        return flask.jsonify({"error": "No project provided."})
    if mode is None:
        mode = st.DEFAULT_MODE
    if alphafold_ver is not None:
        if alphafold_ver in AlphaFoldVersion.list_of_versions():
            parser.alphafold_ver = alphafold_ver
        else:
            parser.alphafold_ver = AlphaFoldVersion.v4.value
    nodes_files = os.path.join(st._PROJECTS_PATH, project, "nodes.json")
    with open(nodes_files, "r") as f:
        nodes = json.load(f)["nodes"]
    proteins = [",".join(node[NT.uniprot]) for node in nodes if node.get(NT.uniprot)]
    print(proteins)
    batch([parser.fetch_pdb, parser.pdb_pipeline], proteins, parser.batch_size)
    result = get_scales(proteins, mode)
    return {"not_fetched": parser.not_fetched, "results": result}
