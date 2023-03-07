from argparse import ArgumentParser

from .classes import AlphaFoldVersion, ColoringModes, Database

COLORMODE_CHOICES = ", ".join(list(col.value for col in ColoringModes)[:5])


def argument_parser(exec_name="main.py"):
    """Argument parser function for the main function."""
    parser = ArgumentParser(prog=exec_name)
    subparsers = parser.add_subparsers(help="mode", dest="mode")
    fetch_parser = subparsers.add_parser(
        "fetch", help="Fetch proteins from the Alphafold database."
    )
    # Argument parser for directly fetching a single structure
    fetch_parser.add_argument(
        "proteins",
        type=str,
        nargs=1,
        help="Proteins to fetch, which are separated by a comma.",
    )
    # Argument parser for processing from a directory in which either a pdb, glb, ply or xyzrgb file is contained and proceeding from this step onward.
    file_parser = subparsers.add_parser(
        "local",
        help="Process proteins from files (.pdb, .glb, .ply, .xyzrgb) in a directory.",
    )
    file_parser.add_argument(
        "source",
        type=str,
        help="Directory containing the files",
        nargs=1,
        action="store",
    )
    # Argument parser for fetching and processing a list of protein structures
    list_parser = subparsers.add_parser(
        "list",
        help="Process proteins from a file containing one UniProt ID in each line.",
    )
    list_parser.add_argument(
        "file",
        type=str,
        nargs=1,
        help="File from which the proteins are extracted from.",
    )
    # Argument parser for for unpacking tar archived from a bulk download from AlphaFold DB. Furthermore multi fraction protein structures are combined into a single glb file.
    bulk_parser = subparsers.add_parser(
        "bulk",
        help="Process proteins tar archive fetched as bulk download from AlphaFold DB",
    )
    bulk_parser.add_argument(
        "source",
        type=str,
        help="Path to the tar archive",
        nargs=1,
        action="store",
    )

    # Argument parser for clearing the processing_files directory
    clear = subparsers.add_parser(
        "clear",
        help="Removes the processing_files directory",
    )
    parser.add_argument(
        "--pdb_file",
        "-pdb",
        nargs="?",
        type=str,
        metavar="PDB_DIRECTORY",
        help="Defines, where to save the PDB Files.",
    )
    parser.add_argument(
        "--glb_file",
        "-glb",
        nargs="?",
        type=str,
        metavar="GLB_DIRECTORY",
        help="Defines, where to save the GLB Files.",
    )
    parser.add_argument(
        "--ply_file",
        "-ply",
        nargs="?",
        type=str,
        metavar="PLY_DIRECTORY",
        help="Defines, where to save the PLY Files.",
    )
    parser.add_argument(
        "--cloud",
        "-pcd",
        type=str,
        nargs="?",
        metavar="PCD_DIRECTORY",
        help="Defines, where to save the ASCII point clouds.",
    )
    parser.add_argument(
        "--map",
        "-m",
        type=str,
        nargs="?",
        metavar="MAP_DIRECTORY",
        help="Defines, where to save the color maps.",
    )
    parser.add_argument(
        "--alphafold_version",
        "-av",
        type=str,
        nargs="?",
        choices=[ver.value for ver in AlphaFoldVersion],
        help="Defines, which version of AlphaFold to use.",
        default=AlphaFoldVersion.v4.value,
    )
    parser.add_argument(
        "--batch_size",
        "-bs",
        type=int,
        nargs="?",
        metavar="BATCH_SIZE",
        help="Defines the size of the batch which will be processed",
        default=50,
    )
    parser.add_argument(
        "--keep_pdb",
        "-kpdb",
        type=bool,
        nargs="?",
        choices=[True, False],
        help="Define whether to still keep the PDB files after the GLB file is created. Default is True.",
        default=True,
    )
    parser.add_argument(
        "--keep_glb",
        "-kglb",
        type=bool,
        nargs="?",
        choices=[True, False],
        help="Define whether to still keep the GLB files after the PLY file is created. Default is False.",
        default=False,
    )
    parser.add_argument(
        "--keep_ply",
        "-kply",
        type=bool,
        nargs="?",
        choices=[True, False],
        help="Define whether to still keep the PLY files after the ASCII file is created. Default is False.",
        default=False,
    )
    parser.add_argument(
        "--keep_ascii",
        "-kasc",
        type=bool,
        nargs="?",
        choices=[True, False],
        help="Define whether to still keep the ASCII Point CLoud files after the color maps are generated. Default is False.",
        default=False,
    )
    parser.add_argument(
        "--chimerax",
        "-ch",
        type=str,
        nargs="?",
        metavar="CHIMERAX_EXEC",
        help="Defines, where to find the ChimeraX executable.",
    )
    parser.add_argument(
        "--color_mode",
        "-cm",
        type=str,
        nargs="?",
        help=f"Defines the coloring mode which will be used to color the structure. Choices: {COLORMODE_CHOICES}... . For a full list, see README.",
        default=ColoringModes.cartoons_ss_coloring.value,
    )
    parser.add_argument(
        "--img_size",
        "-imgs",
        type=int,
        nargs="?",
        help=f"Defines the size of the output images.",
        default=256,
    )
    parser.add_argument(
        "--database",
        "-db",
        type=str,
        nargs="?",
        choices=[db.value for db in Database],
        help=f"Defines the database from which the proteins will be fetched.",
    )
    parser.add_argument(
        "--thumbnails",
        "-thumb",
        action="store_true",
        help="Defines whether to create thumbnails of the structures.",
        default=False,
    )
    parser.add_argument(
        "--with_gui",
        "-gui",
        action="store_true",
        help="Turn on the gui mode of the ChimeraX processing. This has no effect on Windows systems as the GUI will always be turned on.",
        default=False,
    )
    parser.add_argument(
        "--only_images",
        "-oi",
        action="store_true",
        help="Only take images of the processed structures.",
        default=False,
    )
    if parser.parse_args().mode == None:
        parser.parse_args(["-h"])
        exit()

    return parser
