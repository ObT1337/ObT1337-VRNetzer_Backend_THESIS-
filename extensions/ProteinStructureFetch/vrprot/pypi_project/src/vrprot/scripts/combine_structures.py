# Author: Till Pascal Oblau
# To Run this script, use the following command:
# chimerax --script '"combine_structures.py" "<directory where the pdbs files are located>" "<directory where the combined structures should be saved>"'

import ast
import glob
import os
import shutil
import sys
import argparse
import re

SCRIPTS = os.path.dirname(os.path.realpath(__file__))
sys.path.append(SCRIPTS)
import chimerax_bundle

from chimerax.core.commands import run


def main(
    directory: str,
    target: str,
    subprocess: bool,
    processing: str,
    color: list,
    image=False,
):
    """Script used to combine multiple structure fractions into one single structure. Processing is not applied as this will lead to a memory overflow.

    Args:
        directory (str): Directory that contains all PDB files from the bulk download.
        target (str): Directory where the combined structures should be saved.
        subprocess (bool): If the script is called inside the chimerax command line, this will be set to False. This will prevent the script from exiting the ChimeraX session.
    """
    os.makedirs(target, exist_ok=True)
    all_files = glob.glob(f"{directory}/*.pdb")
    bundle = chimerax_bundle.Bundle(session, directory, target)
    bundle.apply_processing(processing, color)
    while len(all_files) > 1:
        # Get first structure ID and version
        first_structure = os.path.basename(all_files[0])
        ver = re.findall(r"_v(\d+)\.pdb", first_structure)[0]
        first_structure = re.findall(r"AF-(\w+)-", first_structure)[0]

        # Find all files with same structure ID
        structures = []
        for file in all_files:
            tmp = os.path.basename(file)
            tmp = re.findall(r"AF-(\w+)-", tmp)[0]
            if tmp == first_structure:
                structures.append(file)

        if len(structures) == 1:
            all_files.remove(structures[0])
            continue
        if os.path.exists(f"{target}/AF-{first_structure}-F1-model_{ver}.glb"):
            for file in structures:
                all_files.remove(file)
            continue

        # Run bundle command on all files
        files = [os.path.basename(file) for file in structures]
        tmp_names = ["tmp_" + file for file in files]
        bundle.run(files, tmp_names)

        # Open and save file for first structure
        for file in tmp_names:
            run(session, f'open {target}/{file.replace("pdb","glb")}')
        run(session, f"save {target}/AF-{first_structure}-F1-model_{ver}.glb")

        # Remove all other files for this structure
        for file in tmp_names:
            os.remove(f"{target}/{file.replace('pdb','glb')}")

        # Close session and remove processed files from all_files
        run(session, "close")
        for file in structures:
            all_files.remove(file)
            # os.makedirs(f"{directory}/{first_structure}", exist_ok=True)
            # shutil.move(file, f"{directory}/{first_structure}/{filename}")
    if subprocess:
        run(session, "exit")


if __name__ == "ChimeraX_sandbox_1":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        help="Directory that contains all PDB files from the bulk download.",
    )
    parser.add_argument(
        "target", help="Directory where the combined structures should be saved."
    )
    parser.add_argument(
        "--subprocess",
        "-sp",
        help="If this is set ChimeraX will close after all structures are done.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--processing_mode",
        "-mode",
        help="The processing mode that should be applied to the structures.",
        default="cartoons_ss_coloring",
    )
    # parser.add_argument("--colors","-c", help="The coloring that should be applied to the structures.", default=['red','green','blue'],nargs=3,type=str)
    args = parser.parse_args()
    directory = args.directory
    target = args.target
    subprocess = args.subprocess
    processing = args.processing_mode
    print(processing)
    # color = ast.literal_eval(args.colors)
    color = ["red", "green", "blue"]
    run(session, f"echo {subprocess}")
    main(directory, target, subprocess, processing, color)
