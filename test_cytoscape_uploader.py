import sys
from ast import literal_eval

from uploader_cytoscape_network import upload_files

# with open("./static/test/_100_nodes_from_Cytoscape.json", "r") as f:
#     content = f.readlines()
#     nodes_data = literal_eval(content[0].strip("\n"))
#     edge_data = literal_eval(content[1].strip("\n"))
# upload_files(
#     "CytoscapeUpload_test", "CytoscapeUpload_test", nodes_data, edge_data
# )  # small network
with open("./static/test/_1000_nodes_47626_edges_from_cytoscape.json", "r") as f:
    content = f.readlines()
    nodes_data = literal_eval(content[0].strip("\n"))
    edge_data = literal_eval(content[1].strip("\n"))
upload_files(
    "CytoscapeUpload_test_large", "CytoscapeUpload_test_large", nodes_data, edge_data
)  # large network
