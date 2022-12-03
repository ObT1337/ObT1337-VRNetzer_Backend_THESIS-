import networkx as nx
import random 

layout = []
edgelist = []

def normalise_list(in_list):
    out_list = [(i - min(in_list))/max(in_list) for i in in_list]
    return(out_list)


def rand_color():
    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    return [r, g, b, 255]

def create_spring_layout(edgelist):
    G = nx.from_edgelist(edgelist)
    positions = nx.spring_layout(G, iterations=50, dim=3)
    nodes, x, y, z = [], [], [], []
    # edges = list(G.edges)
    for node in positions.keys():
        nodes.append(node)
        x.append(positions[node][0])
        y.append(positions[node][1])
        z.append(positions[node][2])

    x_max, x_min = max(x), min(x)
    y_max, y_min = max(y), min(y)
    z_max, z_min = max(z), min(z)
    x = [(val-x_min)/(x_max-x_min) for val in x]
    y = [(val-y_min)/(y_max-y_min) for val in y]
    z = [(val-z_min)/(z_max-z_min) for val in z]

    return nodes, x, y, z

def create_files(nodes, x, y, z):
    color = rand_color()
    for i in range(len(nodes)):
        row = [x[i], y[i], z[i], color[0], color[1], color[2], color[3], "annotation" + nodes[i]]
        layout.append(row)
    return(layout)

def spring_main(content_list):
    for i in content_list:
        x,y = i.split(",")
        edge = [x,y]
        edgelist.append(edge)
    nodes, x, y, z = create_spring_layout(edgelist)
    layout = create_files(nodes, x, y, z)
    return(layout)
