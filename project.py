import json
import os
import shutil

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
PROJECTS_DIR = os.path.join(STATIC_DIR, "projects")
DEFAULT_PFILE = {
    "name": "",
    "layouts": [],
    "layoutsRGB": [],
    "links": [],
    "linksRGB": [],
    "selections": [],
    "stateData": {},
}
DEFAUT_NAMES = {"names": []}
DEFAULT_NODES = {"nodes": []}
DEFAULT_LINKS = {"links": []}


class Project:
    def __init__(self, name: str, read=True, check_exists=True):
        """Project class for handling project directories and their data.
        Initializes a project object. All variables are initialized and the pfile is read, if it does not exist, it is created.
        Args:
            name (str): Name of the project
            read (bool, optional): If the pfile should be read. Defaults to True.
        """
        if not isinstance(name, str):
            raise TypeError(f"Name must be a string, not {type(name)}")
        self.name = name
        self.location = os.path.join(PROJECTS_DIR, name)
        self.pfile_file = os.path.join(self.location, f"pfile.json")
        self.names_file = os.path.join(self.location, f"names.json")
        self.nodes_file = os.path.join(self.location, f"nodes.json")
        self.links_file = os.path.join(self.location, f"links.json")
        self.layouts_dir = os.path.join(self.location, f"layouts")
        self.layoutsl_dir = os.path.join(self.location, f"layoutsl")
        self.layouts_rgb_dir = os.path.join(self.location, f"layoutsRGB")
        self.links_dir = os.path.join(self.location, f"links")
        self.links_rgb_dir = os.path.join(self.location, f"linksRGB")

        self.pfile = DEFAULT_PFILE
        self.pfile["name"] = name
        self.origin = None
        self.names = DEFAUT_NAMES
        self.nodes = DEFAULT_NODES
        self.links = DEFAULT_LINKS
        self.write_functions = [
            self.write_pfile,
            self.write_names,
            self.write_nodes,
            self.write_links,
        ]
        self.read_functions = [
            self.read_pfile,
            self.read_names,
            self.read_nodes,
            self.read_links,
        ]
        self.print_functions = [
            self.print_pfile,
            self.print_names,
            self.print_nodes,
            self.print_links,
        ]
        self.create_directory_functions = [
            self.create_layouts_dir,
            self.create_layoutsl_dir,
            self.create_layouts_rgb_dir,
            self.create_links_dir,
            self.create_links_rgb_dir,
        ]
        if read:
            if check_exists and not self.exists():
                pass
            else:
                self.read_pfile()

    @staticmethod
    def write_json(file: str, data: object):
        """Generic write function for json files."""
        with open(file, "w+", encoding="UTF-8") as f:
            json.dump(data, f)

    def read_json(self, file: str, default: object = {}):
        """Generic read function for json files.

        Args:
            file (str): Path to the file to be read.
            default (json, optional): Default value to return if file does not exist. Defaults to None.
        Returns:
            json: Data from file or default value.
        """
        origin = self.get_pfile_value("origin")
        if not origin and not os.path.exists(file):
            Project.create_directory(os.path.dirname(file))
            Project.write_json(file, default)
            return default
        if "pfile.json" not in file:
            if origin and not os.path.exists(file):
                origin = Project(origin)
                file = os.path.join(origin.location, os.path.basename(file))
        with open(file, "r", encoding="UTF-8") as f:
            return json.load(f)

    @staticmethod
    def run_functions(
        functions: list, args: list[tuple] = None, kwargs: list[dict] = None
    ):
        """Runs all functions in list functions. For each function, the args and kwargs are passed.

        Args:
            functions (list): _description_
            args (list[tuple], optional): List of tuples with arguments, one tuple for every function. Defaults to None.
            kwargs (list[dict], optional): List of dicts with key word arguments, one for every function. Defaults to None.
        """
        if args is None:
            args = [[]] * len(functions)
        if kwargs is None:
            kwargs = [{}] * len(functions)
        for idx, func in enumerate(functions):
            if args[idx] is None:
                args[idx] = []
            if kwargs[idx] is None:
                kwargs[idx] = {}
            func(*args[idx], **kwargs[idx])

    @staticmethod
    def print_data(data: object):
        """Generic print function for json data.

        Args:
            data (json): Data to print, should be in a json format.
        """
        print(json.dumps(data))

    @staticmethod
    def create_directory(dir: str):
        """Generic function for creating directories.

        Args:
            dir (str): Path to the directory to be made.
        """
        os.makedirs(dir, exist_ok=True)

    def write_pfile(
        self,
    ):
        self.write_json(self.pfile_file, self.pfile)

    def write_names(self):
        self.write_json(self.names_file, self.names)

    def write_nodes(self):
        self.write_json(self.nodes_file, self.nodes)

    def write_links(self):
        self.write_json(self.links_file, self.links)

    def write_all_jsons(self):
        self.run_functions(self.write_functions)

    def read_pfile(
        self,
    ):
        self.pfile = self.read_json(self.pfile_file, DEFAULT_PFILE)
        self.origin = self.get_pfile_value("origin", None)

    def read_names(self):
        self.names = self.read_json(self.names_file, DEFAUT_NAMES)

    def read_nodes(self):
        self.nodes = self.read_json(self.nodes_file, DEFAULT_NODES)

    def read_links(self):
        self.links = self.read_json(self.links_file, DEFAULT_LINKS)

    def read_all_jsons(self):
        self.run_functions(self.read_functions)

    def print_pfile(self):
        self.print_data(self.pfile)

    def print_names(self):
        self.print_data(self.names)

    def print_nodes(self):
        self.print_data(self.nodes)

    def print_links(self):
        self.print_data(self.links)

    def print_all_jsons(self):
        self.run_functions(self.print_functions)

    def get_pfile_value(self, key: str, default: object = None):
        if key not in self.pfile:
            self.pfile[key] = default
        return self.pfile[key]

    def set_pfile_value(self, key: str, value: object):
        self.pfile[key] = value

    def append_pfile_value(self, key: str, value: object):
        if key not in self.pfile:
            self.pfile[key] = []
        if type(self.pfile[key]) != list:
            raise TypeError(f"pfile[{key}] is not a list.\n{self.pfile[key]}")
        self.pfile[key]: list
        self.pfile[key].append(value)

    def define_pfile_value(self, key, dict_key, value):
        self.pfile[key][dict_key] = value

    def get_all_layouts(self):
        return self.get_pfile_value("layouts", [])

    def get_all_node_colors(self):
        return self.get_pfile_value("layoutsRGB", [])

    def get_all_links(self):
        return self.get_pfile_value("links", [])

    def get_all_link_colors(self):
        return self.get_pfile_value("linksRGB", [])

    def get_selections(self):
        return self.get_pfile_value("selections", [])

    def get_state_data(self):
        return self.get_pfile_value("stateData", [])

    def set_all_layouts(self, layouts):
        self.set_pfile_value("layouts", layouts)

    def set_all_node_colors(self, colors):
        self.set_pfile_value("nodesRGB", colors)

    def set_all_links(self, links):
        self.set_pfile_value("links", links)

    def set_all_link_colors(self, colors):
        self.set_pfile_value("linksRGB", colors)

    def set_selections(self, selections):
        self.set_pfile_value("selections", selections)

    def set_state_data(self, state_data):
        self.set_pfile_value("stateData", state_data)

    def append_layout(self, layout):
        self.append_pfile_value("layouts", layout)

    def append_node_color(self, color):
        self.append_pfile_value("nodesRGB", color)

    def append_link(self, link):
        self.append_pfile_value("links", link)

    def append_link_color(self, color):
        self.append_pfile_value("linksRGB", color)

    def append_selection(self, selection):
        self.append_pfile_value("selections", selection)

    def set_state_data_value(self, key, value):
        self.define_pfile_value("stateData", key, value)

    def get_all_data(self):
        return self.pfile, self.names, self.nodes, self.links

    def create_layouts_dir(self):
        self.create_directory(self.layouts_dir)

    def create_layoutsl_dir(self):
        self.create_directory(self.layoutsl_dir)

    def create_layouts_rgb_dir(self):
        self.create_directory(self.layouts_rgb_dir)

    def create_links_dir(self):
        self.create_directory(self.links_dir)

    def create_links_rgb_dir(self):
        self.create_directory(self.links_rgb_dir)

    def create_all_directories(self):
        self.run_functions(self.create_directory_functions)

    def exists(self):
        return os.path.exists(self.location)

    def get_files_in_dir(self, dir: str):
        return os.listdir(os.path.join(self.location, dir))

    def has_own_nodes(self):
        return os.path.exists(self.nodes_file)

    def has_own_links(self):
        return os.path.exists(self.links_file)

    def remove(self):
        shutil.rmtree(self.location, ignore_errors=True)

    def remove_subdir(self, subdir: str):
        shutil.rmtree(os.path.join(self.location, subdir))

    def copy(self, target: str, *args, ignore=None, **kwargs):
        """Copies the whole directory of the project to the target location."""
        if ignore:
            ignore = shutil.ignore_patterns("names.json", "nodes.json", "links.json")
        shutil.copytree(
            self.location,
            target,
            *args,
            **kwargs,
            ignore=ignore,
            dirs_exist_ok=True,
        )
