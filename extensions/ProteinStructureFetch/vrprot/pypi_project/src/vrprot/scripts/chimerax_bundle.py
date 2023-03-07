# Author: Till Pascal Oblau
import argparse
import os
import sys

from chimerax.core.commands import run


class Bundle:
    """
    Object to be run as python script during chimeraX runtime.
    """

    def __init__(self, session, path, target, images=None, only_images=False):
        """
        Initialization of the Bundle Class. Will define the chimeraX session
        which is needed by the ChimeraX api and will define the colors for the
        color coding.

        Args:
            session (chimerax.session): Defines ChimeraX process
            colors (list, string): List of strings. Contains which colors each selection will be colored.
        """
        self.session = session
        self.wd = os.path.abspath(".")
        self.target = target
        self.images = images
        self.pipeline = ["N/A"]
        self.path = path
        self.only_images = only_images

    def debug(self, string):
        run(self.session, f"echo {string}")

    def run_command(self, command):
        run(self.session, command)

    ## Utility
    def open_file(self, structure):
        "Open structure"
        self.pipeline[0] = f"open {structure}"

    def run_pipeline(self, structure, tmp_name):
        """
        Function to executed the pipeline and save the file as glb
        """
        out_name = structure.replace("pdb", "glb")
        tmp_name = tmp_name.replace("pdb", "glb")
        save_loc = f"{self.target}/{tmp_name}"
        pipeline = self.pipeline.copy()
        if self.images:
            pipeline = pipeline[:-2] + self.take_screenshot(out_name) + pipeline[-2:]
        if not self.only_images:
            pipeline[-2] = f"save {save_loc}"
        for command in pipeline:
            run(self.session, f"echo {command}")
            run(self.session, command)

    ## display modes
    def change_display_to(self, mode: str):
        """
        Changes display mode to only show the desired display.
        Possible display modes: "atoms", "cartoons", or "surface".
        """
        modes = ["atoms", "cartoons", "surface"]
        # TODO: cartoons translates to show sel\xa0cartoons dunno why tho.
        for m in modes:
            if m == mode:
                self.pipeline.extend(["sel", f"show sel {m}"])
            else:
                self.pipeline.extend(["sel", f"hide sel {m}"])

    def change_style_to(self, style):
        """
        Changes style mode to only show the desired style.
        Possible style modes: "stick", "sphere", or "ball".
        """
        styles = ["stick", "sphere", "ball"]
        self.change_display_to("atoms")
        for s in styles:
            if s == style:
                self.pipeline.extend([f"style sel {s}"])

    ## Coloring modes
    def ss_coloring(self, colors):
        """
        Add color coding of secondary structures.
        """
        if colors is None:
            colors = ["red", "green", "blue"]
        self.pipeline.extend(
            [
                "select coil",
                "color sel " + colors[0],
                "select helix",
                "color sel " + colors[1],
                "select strand",
                "color sel " + colors[2],
            ]
        )

    def rainbow_coloring(self):
        """
        Add rainbow coloring.
        """
        self.pipeline.extend(["sel", "rainbow sel"])

    def heteroatom_coloring(self):
        """
        Add heteroatom coloring.
        """
        self.pipeline.extend(["sel", "color sel byhetero"])

    def chain_coloring(self):
        """
        Add chain coloring.
        """
        self.pipeline.extend(["sel", "color sel bychain"])

    def polymer_coloring(self):
        """
        Add polymer coloring.
        """
        self.pipeline.extend(["sel", "color sel bypolymer"])

    def electrostatic_coloring(self):
        """
        Add electrostatic coloring.
        """
        self.pipeline.extend(["sel", "coulombic sel"])
        self.change_display_to("surface")

    def hydrophobic_coloring(self):
        """
        Add hydrophobic coloring.
        """
        self.pipeline.extend(["sel", "mlp sel"])
        self.change_display_to("surface")

    def bFactor_coloring(self):
        """
        Add hydrophobic coloring.
        """
        self.pipeline.extend(["sel", "color bfactor sel"])

    def nucleotide_coloring(self):
        """
        Add hydrophobic coloring.
        """
        self.pipeline.extend(["sel", "color sel bynucleotide"])

    def mfpl_coloring(self):
        """
        Add Max F Perutz Lab coloring.
        """
        self.pipeline.extend(["sel", "color sel #00cac0"])

    ## Complete processes
    def mode_ss_coloring(self, colors, mode):
        """
        Will color the secondary structures of the protein according to the specified colors, if colors are None, colors will be red, green, blue for coil, helix, and strand respectivley. Desired display mode is set.
        """
        self.change_display_to(mode)
        self.ss_coloring(colors)

    def mode_rainbow_coloring(self, mode):
        """
        Will color the protein structure using the rainbow coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.rainbow_coloring()

    def mode_heteroatom_coloring(self, mode):
        """
        Will color the protein structure using the heteroatom coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.heteroatom_coloring()

    def mode_chain_coloring(self, mode):
        """
        Will color the protein structure using the chain coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.chain_coloring()

    def mode_polymer_coloring(self, mode):
        """
        Will color the protein structure using the polymer coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.polymer_coloring()

    def mode_electrostatic_coloring(self, mode):
        """
        Will color the protein structure using the electrostatic coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.electrostatic_coloring()

    def mode_bFactor_coloring(self, mode):
        """
        Will color the protein structure using the b-factor coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.bFactor_coloring()

    def mode_nucleotide_coloring(self, mode):
        """
        Will color the protein structure using the nucleotide coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.nucleotide_coloring()

    def mode_mfpl_coloring(self, mode):
        """Will color the protein structures in the Max Ferdinand Perutz Labs turquoise.
        Args:
            mode (str): Display mode to use.
        """
        self.change_display_to(mode)
        self.mfpl_coloring()

    def take_screenshot(self, structure):
        """
        Takes a screenshot of the current scene and saves it to the specified path.
        """
        out_name = structure.replace(".glb", ".png")
        if os.path.isfile(f"{self.images}/{out_name}"):
            return []
        unselect = "~select"
        view = "view"

        save = f"save {self.images}/{out_name} width 512 height 512 supersample 3 transparentBackground true"
        select = f"select"
        return [unselect, view, save, select]

    def apply_processing(self, mode, colors):
        cases = {
            "ss": self.mode_ss_coloring,
            "rainbow": self.mode_rainbow_coloring,
            "heteroatom": self.mode_heteroatom_coloring,
            "polymer": self.mode_polymer_coloring,
            "chain": self.mode_chain_coloring,
            "electrostatic": self.electrostatic_coloring,
            "hydrophobic": self.hydrophobic_coloring,
            "bFactor": self.mode_bFactor_coloring,
            "nucleotide": self.mode_nucleotide_coloring,
            "mfpl": self.mode_mfpl_coloring,
        }
        mode, coloring, _ = mode.split("_")
        style = None
        if mode in ["stick", "sphere", "ball"]:
            style = mode
            mode = "atoms"

        if coloring == "ss":
            """
            This part will be executed, if the argument is ss_coloring, i.e. coloring the secondary structures.
            """
            cases[coloring](colors, mode)
            if style is not None:
                self.change_style_to(style)
        elif coloring in ["electrostatic", "hydrophobic"]:
            cases[coloring]()

        else:
            # General coloring cases
            cases[coloring](mode)
            if style is not None:
                # if mode was ["stick", "sphere", "ball"] atoms is the new mode and style is one out of ["stick", "sphere", "ball"]
                self.change_style_to(style)

        if self.images is not None:
            run(self.session, "lighting soft")
            run(self.session, "lighting shadows false")

        if self.only_images:
            self.pipeline += ["echo NA", "close"]
            return
        else:
            self.pipeline += ["save", "close"]

    def run(self, file_names, tmp_names=None):
        if tmp_names is None:
            tmp_names = file_names
        for structure, tmp_name in zip(file_names, tmp_names):
            run(self.session, f"echo {structure}")
            self.open_file(os.path.join(self.path, structure))
            self.run_pipeline(structure, tmp_name)
        # Close ChimeraX


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--source",
        help="Path to the directory containing the protein files.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-d",
        "--dest",
        help="Path to the directory where the glbs will be saved.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-i",
        "--images",
        help="Path to the directory where the images will be saved.",
        required=False,
        default=None,
        type=str,
    )
    parser.add_argument(
        "-m",
        "--mode",
        help="Mode to use for coloring the protein.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-fn",
        "--filenames",
        help="Names of the files to be processed.",
        required=False,
        type=str,
    )
    parser.add_argument(
        "-cl",
        "--colors",
        help="Colors to use for coloring the protein.",
        required=False,
        nargs="*",
        type=str,
    )
    parser.add_argument(
        "--only_images",
        "-oi",
        help="Only take images of the protein.",
        required=False,
        default=False,
        action="store_true",
    )
    args = parser.parse_args()
    file_names = args.filenames.split(",")
    bundle = Bundle(session, args.source, args.dest, args.images, args.only_images)
    bundle.apply_processing(args.mode, args.colors)
    bundle.run(file_names)
    run(session, "exit")


# "ChimeraX_sandbox_1" seems to be the default name for a script but did not work

if __name__ == "ChimeraX_sandbox_1":
    main()
