from sys import argv

from src.vrprot.classes import ColoringModes
from src.vrprot.pointcloud2map_8bit import pcd_to_png
from src.vrprot.sample_pointcloud import sample_pcd
from src.vrprot.util import (
    convert_glb_to_ply,
    fetch_pdb_from_alphafold,
    run_chimerax_coloring_script,
    search_for_chimerax,
)


def test_alphafold_fetch(structure):
    output = "/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/pdbs/"
    fetch_pdb_from_alphafold(structure, output, "v2")


def test_chimerax_process(structure, cm: str = None):
    if cm is None:
        cm = ColoringModes.cartoons_ss_coloring.value
    src = "/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/pdbs"
    output = "/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/glbs"
    chimerax = search_for_chimerax()
    run_chimerax_coloring_script(
        chimerax,
        src,
        [f"AF-{structure}-F1-model_v2.pdb"],
        output,
        cm,
        ["red,green,blue"],
    )


def test_glb_ply_convert(structure, debug=False):
    src = f"/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/glbs/AF-{structure}-F1-model_v2.glb"
    output = f"/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/plys/AF-{structure}-F1-model_v2.ply"
    print("testing convert")
    convert_glb_to_ply(src, output, debug)


def text_sample_pcd(structure, debug=False):
    source = f"/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/plys/AF-{structure}-F1-model_v2.ply"
    output = f"/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/ASCII_clouds/AF-{structure}-F1-model_v2.xyzrgb"
    sample_pcd(source, output=output, SAMPLE_POINTS=256 * 256, debug=debug)


def test_ascii_to_png(structure):
    src = f"/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/ASCII_clouds/AF-{structure}-F1-model_v2.xyzrgb"
    png = f"AF-{structure}-F1-model_v2.png"
    bmp = png.replace("png", "bmp")
    rgb = "/Users/till/Documents/Playground/VRNetzer_Backend/static/NewMaps/rgb/" + png
    xyz_high = (
        "/Users/till/Documents/Playground/VRNetzer_Backend/static/NewMaps/xyz/high/"
        + bmp
    )
    xyz_low = (
        "/Users/till/Documents/Playground/VRNetzer_Backend/static/NewMaps/xyz/low/"
        + bmp
    )

    pcd_to_png(src, rgb, xyz_low, xyz_high, img_size=256)


def run_tests_for_structure(structure):
    if structure is None:
        structure = "A0A0A0MRZ8"
    test_alphafold_fetch(structure)
    # for cm in ColoringModes:
    for cm in [ColoringModes.cartoons_ss_coloring]:
        # if cm.value is ColoringModes.cartoons_ss_coloring.value:
        #     continue
        print("Testing coloring mode: " + cm.value)
        test_chimerax_process(structure, cm.value)
        test_glb_ply_convert(structure, True)
        text_sample_pcd(structure, True)
        test_ascii_to_png(structure)


run_tests_for_structure("O06917")
