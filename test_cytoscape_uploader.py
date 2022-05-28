import sys

sys.path.insert(0, "./static/test")

from network_from_cytoscape import edge_data, nodes_data

from uploader_cytoscape_network import upload_files

upload_files(
    "CytoscapeUpload_test", "CytoscapeUpload_test", nodes_data, edge_data
)  # small network
from _1000_nodes_47626_edges_from_cytoscape import edge_data, nodes_data

upload_files(
    "CytoscapeUpload_test_large", "CytoscapeUpload_test_large", nodes_data, edge_data
)  # large network
