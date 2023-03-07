import glob
import ntpath
import os
import platform
import shutil
import subprocess as sp
import time

import requests
import trimesh
from trimesh.exchange import ply
from trimesh.exchange.export import export_mesh

from .classes import AlphaFoldVersion, FileTypes, Logger
from .exceptions import ChimeraXException, StructureNotFoundError

wd = os.path.dirname(".")  # for final executable
# wd = os.path.dirname(__file__)  # for development
WD = os.path.abspath(wd)  # for development
FILE_DIR = os.path.dirname(__file__)
SCRIPTS = os.path.join(FILE_DIR, "scripts")
log = Logger("util")


def fetch_pdb_from_rcsb(uniprot_id: str, save_location: str) -> None:
    file_name = uniprot_id + ".pdb"
    url = "https://files.rcsb.org/download/" + file_name
    return fetch_pdb(uniprot_id, url, save_location, file_name)


def fetch_pdb_from_alphafold(
    uniprot_id: str,
    save_location: str,
    db_version: AlphaFoldVersion = AlphaFoldVersion.v1.value,
) -> bool:
    """
    Fetches .pdb File from the AlphaFold Server. This function uses the request module from python standard library to directly download pdb files from the AlphaFold server.

    Requested .pdb files can be found at https://alphafold.ebi.ac.uk/files/AF-<UniProtID>-F1-model_<db_version>.pdb.

    The loaded .pdb file is saved in a subfolder called "pdbs" in the current directory.

    Args:
        uniprot_id (string): UniProtID of the requested protein.
        save_location (string): Path to the directory where the .pdb file should be saved.
        db_version (string): Version of the database.

    Returns:
        success (bool) : tells whether the fetching was successful or not.
    """
    log.debug(f"AlphaFoldDB version: {db_version}.")
    file_name = f"AF-{uniprot_id}-F1-model_{db_version}.pdb"  # Resulting file name which will be downloaded from the alphafold DB
    url = "https://alphafold.ebi.ac.uk/files/" + file_name  # Url to request
    return fetch_pdb(uniprot_id, url, save_location, file_name)


def fetch_pdb(uniprot_id: str, url: str, save_location: str, file_name: str) -> bool:

    success = True
    try:
        # try to fetch the structure from the given url
        r = requests.get(url, allow_redirects=True)  # opens url
        if r.status_code == 404:
            # If the file it not available, an exception will be raised
            raise StructureNotFoundError(
                "StructureNotFoundError: There is no structure on the server with this UniProtID."
            )
        # downloads the pdb file and saves it in the pdbs directory
        os.makedirs(save_location, exist_ok=True)
        open(f"{save_location}/{file_name}", "wb").write(r.content)
        log.debug(
            f"Successfully fetched {uniprot_id} from URL {url}. Saved in {save_location}."
        )
    except StructureNotFoundError as e:
        log.error(f"StructureNotFoundError:{e}")
        log.warning(f"Failed to fetch {uniprot_id} from URL: {url}")
        success = False
    return success


def search_for_chimerax() -> str:
    """Will search for the chimerax executeable on the system. Does not work with windows so far."""
    if platform.system() == "Darwin":
        locations = glob.glob(
            "/Applications/ChimeraX*.app/Contents/MacOS/chimerax", recursive=True
        )
        if len(locations) == 0:
            raise ChimeraXException("ChimeraX not found. Is it installed?")
        chimerax = locations[0]
    elif platform.system() == "Linux":
        chimerax = "chimerax"
    elif platform.system() == "Windows":
        import win32api

        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split("\000")[:-1]
        for drive in drives:
            drive = drive.replace("\\", "/")
            p = f"{drive}*/ChimeraX*/bin/ChimeraX*-console.exe"
            chimerax = glob.glob(p, recursive=True)
            log.debug(chimerax)
            if len(chimerax) > 0:
                chimerax = f'"{chimerax[0]}"'.replace("/", "\\")
                break
        if len(chimerax) == 0:
            raise ChimeraXException("ChimeraX not found. Is it installed?")
    return chimerax


def run_chimerax_coloring_script(
    chimearx: str,
    pdb_dir: str,
    proteins: list[str],
    save_location: str,
    processing: str,
    colors: list or None,
    images_dir: str = "",
    images: bool = False,
    gui: bool = False,
    only_images: bool = False,
) -> None:
    """
    This will use the give ChimeraX installation to process the .pdb files.It will color the secondary structures in the given colors.
    The offscreen render does only work under linux.

    Args:
        protein (string): UniProtID of the protein which will be processed
        colors (list, optional): List containing three colors. The first is the color of coil. The second will be the color of the helix. And the last color is the color of the strands. Defaults to ["red", "green", "blue"] i.e. coils will be red, helix will be green and stands will be blue.
    """
    # Define script to call.
    bundle = os.path.join(SCRIPTS, "chimerax_bundle.py")
    # Setup the arguments to call with the script.
    file_string = ""
    for file in proteins:
        _, file = ntpath.split(file)
        file_string += f"{file},"
    file_string = file_string[:-1]
    images_dir = os.path.abspath(images_dir)
    os.makedirs(save_location, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    if platform.system() == "Windows":
        bundle = bundle
        pdb_dir = pdb_dir.split("\\")
        pdb_dir = "/".join(pdb_dir)
        save_location = save_location.split("\\")
        save_location = "/".join(save_location)
        images_dir = images_dir.split("\\")
        images_dir = "/".join(images_dir)
    arg = [
        bundle,  # Path to chimeraX bundle.
        "-s",
        pdb_dir,  # Path to the directory where the .pdb files are stored.
        "-d",
        save_location,  # Path to the directory where the .glb files should be saved.
        "-fn",
        file_string,  # Filename
        "-m",
        processing,  # Define mode as secondary structure coloring.,  # Path to the directory where the colored .pdb files should be saved.
    ]
    if colors:
        arg.append("-c")
        arg.append(" ".join(colors))

    if only_images:
        arg.append("-oi")
        images = True

    if images:
        arg.append("-i")
        arg.append(images_dir)
        gui = True
    try:
        # Call chimeraX to process the desired object.
        call_ChimeraX_bundle(chimearx, arg, gui)
        # Clean tmp files
    except FileNotFoundError:
        # raise an expection if chimeraX could not be found
        log.error(
            "Installation of chimeraX could not be found. Please define the Path to the Application."
        )
        exit()


def call_ChimeraX_bundle(chimerax: str, args: list, gui: bool = True) -> None:
    """
    Function to call chimeraX and run chimeraX Python script with the mode applied.

    Args:
        script (string): chimeraX python script/bundle which should be called
        working_Directory (string): Define the working directory to which chimeraX should direct to (run(session,"cd "+arg[1]))
        file_name (string): target file which will be processed
        mode (string): Tells which pipline is used during chimeraX processing
        (ss = secondary structures, aa = aminoacids, ch = chain). Only ss is implemented at that moment.
        script_arg (list, strings): all arguments needed by the function used in the chimeraX Python script/bundle (size is dynamic). All Arguments are strings.
    """
    # prepare Arguments for script execution
    if platform.system() == "Linux":
        # for Linux we can use off screen render. This does not work on Windows or macOS
        command = [
            chimerax,
            "--script",
            ("%s " * len(args)) % (tuple(args)),
        ]
        if not gui:
            command.append("--offscreen")
        # command = (
        #     '%s --offscreen --script "' % chimerax
        #     + ("%s " * len(arg)) % (tuple(arg))
        #     + '"'
        # )
    elif platform.system() == "Windows":
        # if not gui:
        #     args.append("--nogui")
        command = '%s --script "' % chimerax + ("%s " * len(args)) % (tuple(args)) + '"'
    else:
        # call chimeraX with commandline in a subprocess
        command = [chimerax, "--script", ("%s " * len(args)) % (tuple(args))]
        if not gui:
            command.append("--nogui")
    try:
        process = sp.Popen(command, stdout=sp.DEVNULL, stdin=sp.PIPE)
        # wait until chimeraX is finished with processing
        process.wait()
    except Exception as e:
        # raise an expecting if chimeraX could not be found
        log.error(
            "Could not run ChimeraX. Is the installation path setup correctly?\n"
            + chimerax
            + "\nIf not please correct it."
        )
        raise Exception


def convert_glb_to_ply(glb_file: str, ply_file: str, debug: bool = False) -> None:
    """
    This function converts a glb file to a ply file.

    Args:
        glb_file (string): Path to the glb file.
    """
    save_location, _ = ntpath.split(glb_file)
    os.makedirs(save_location, exist_ok=True)
    mesh = trimesh.load(glb_file, force="mesh")
    if debug:
        mesh.show()
    export_mesh(mesh, ply_file, "ply")
    ## Deprecated
    # file = ply.export_ply(mesh)
    # with open(ply_file, "wb+") as f:
    #     f.write(file)
    if debug:
        mesh = trimesh.load(ply_file, force="mesh")
        mesh.show()
    return True


def batch(
    funcs: list[object], proteins: list[str], batch_size: int = 50, **kwargs
) -> None:
    """Will run the functions listed in funcs in a batched process."""
    start = 0
    end = batch_size
    que = proteins.copy()
    while len(que) > 0:
        log.debug(f"Starting Batch form: {start} to {end}")
        batch_proteins = que[:batch_size]
        for func in funcs:
            func(batch_proteins, **kwargs)
        start = end
        end += batch_size
        del que[:batch_size]


def remove_dirs(directory):
    """Removes a directory an all underlying subdirectories. WARNING this can lead to loss of data!"""
    if os.path.isdir(directory):
        shutil.rmtree(directory)


def combine_fractions(
    directory: str,
    target: str,
    coloring_mode: str,
    chimerax: str = None,
    gui: bool = True,
):
    """Combines multi fraction protein structure to a single structure and exports it as glb file."""
    if chimerax is None:
        chimerax = search_for_chimerax()
    script = os.path.join(SCRIPTS, "combine_structures.py")
    if platform.system() == "Windows":
        directory = directory.split("\\")
        directory = "/".join(directory)
        target = target.split("\\")
        target = "/".join(target)
        args = [script, directory, target, "-sp", "-mode", coloring_mode]
        # if not gui:
        #     args.append("--nogui")
        command = '%s --script "' % chimerax + ("%s " * len(args)) % (tuple(args)) + '"'
    else:
        command = [
            chimerax,
            "--script",
            f"{script} {directory} {target} -sp -mode {coloring_mode}",
        ]
        if not gui:
            command.append("--nogui")
    process = sp.Popen(command, stdout=sp.DEVNULL, stdin=sp.PIPE)
    process.wait()
    print("All multi fraction structures handled.")


def free_space(
    DIRS: dict[FileTypes, str],
    new: int,
    space: int = None,
    proteins: list = None,
    version: str = None,
):
    """Removes as many old files until there is enough space for the new files.

    Args:
        DIRS (dict): Maps File Types to directories
        space (int): How mach space is maximal available.
        new (int): How much space is needed for the new files.
    """
    if space is None:
        return None
    if space <= 0:
        return None
    tmp = {}
    for ft, _dir in DIRS.items():
        if ft == "output":
            continue
        if os.path.isdir(_dir):
            files = [os.path.join(_dir, f) for f in os.listdir(_dir)]
            if space - len(files) < new:
                files = {f: time.ctime(os.path.getmtime(f)) for f in files}
                files = sorted(files.items(), key=lambda x: x[1], reverse=True)
                while space - len(files) < new:
                    file = files.pop()
                    if ft not in tmp:
                        tmp[ft] = []
                    remove = True
                    for protein in proteins:
                        if protein in file[0] and version in file[0]:
                            remove = False
                            break
                    if remove:
                        tmp[ft].append(file[0])
    return tmp


def remove_cached_files(tmp: dict[FileTypes, str], space: int, new: int):
    """Removes all cached files."""
    if space is None or tmp is None:
        return
    for ft, files in tmp.items():
        for file in files:
            os.remove(file)
