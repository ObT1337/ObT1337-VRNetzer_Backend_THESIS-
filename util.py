"""
Utility functions
"""
import math
from PIL import Image

class Texture:
    def __init__(self, project_nodes_dict, project_links_dict, nodes_coloring_dict):
        # define 
        self.__gray = (34, 34, 34, 255)
        self.__single = (255, 255, 255, 255)
        self.__annotation_1 = (55, 0, 179, 255)
        self.__annotation_2 = (3, 218, 198, 255)
        self.__result = (187, 134, 252, 255)
        self.name_nodes = "./temp/annotation_nodes_texture.png"
        self.name_links = "./temp/annotation_links_texture.png"

        self.__colors = {
            "gray": self.__gray,
            "single": self.__single,
            "annotation1": self.__annotation_1,
            "annotation2": self.__annotation_2,
            "result": self.__result
        }

        self.project_nodes_dict = project_nodes_dict
        self.project_links_dict = project_links_dict
        self.nodes_coloring_dict = nodes_coloring_dict

        self.width = 128
        self.height_nodes = math.ceil(len(project_nodes_dict["nodes"])/128)
        self.height_links = math.ceil(len(self.project_links_dict["links"])/128)
        self.img_data_nodes = []
        self.img_data_links = []
        self.img_nodes = Image.new("RGBA", (self.width, self.height_nodes))
        self.img_links = Image.new("RGBA", (self.width, self.height_links))


    def generate_nodes(self, name=None):
        if name is not None:
            self.name_nodes = name

        for node_object in self.project_nodes_dict["nodes"]:
            if node_object["n"] not in self.nodes_coloring_dict:
                self.img_data_nodes.append(self.__gray)
                continue
            self.img_data_nodes.append(self.__colors[self.nodes_coloring_dict[node_object["n"]]])
        
        self.img_nodes.putdata(self.img_data_nodes)
        self.img_nodes.save(self.name_nodes, "PNG")


    def generate_links(self, name=None, lazy=True):
        if name is not None:
            self.name_nodes = name

        print(self.nodes_coloring_dict)

        for link_object in self.project_links_dict["links"]:
            if lazy is True:
                self.img_data_links.append(self.__gray)
                continue
            
            # not lazy mode
            link_s = self.project_nodes_dict["nodes"][int(link_object["s"])]["n"]
            link_e = self.project_nodes_dict["nodes"][int(link_object["e"])]["n"]
            # all links with 1 or 2 gray nodes
            if link_s not in self.nodes_coloring_dict or link_e not in self.nodes_coloring_dict:
                self.img_data_links.append(self.__gray)
                continue
            
            # all links where both node colors are equal
            if self.nodes_coloring_dict[link_s] == self.nodes_coloring_dict[link_e]:
                self.img_data_links.append(self.__colors[self.nodes_coloring_dict[link_s]])
                continue
            
            # both nodes diferent and not gray -> get node annotation color
            if self.nodes_coloring_dict[link_s] in ["annotation1", "annotation2"]:
                self.img_data_links.append(self.__colors[self.nodes_coloring_dict[link_s]])
                continue
            if self.nodes_coloring_dict[link_e] in ["annotation1", "annotation2"]:
                self.img_data_links.append(self.__colors[self.nodes_coloring_dict[link_e]])
                continue

        self.img_links.putdata(self.img_data_links)
        self.img_links.save(self.name_links, "PNG")
