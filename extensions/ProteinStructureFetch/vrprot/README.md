# VRPROT

## ABOUT VRPROT

A pipeline that processes protein structures in ProteinDataBank (PDB) file format
using ChimeraX and enables them to be analyzed on the [VRNetzer](https://github.com/menchelab/VRNetzer) platform.

---

## PROTEIN STRUCTURE ANALYSIS

---

## USAGE OF THIS PROJECT

The main purpose of this project is to serve as an easy to use pipeline to facilitate the processing of protein structures for presentation on the [VRNetzer](https://github.com/menchelab/VRNetzer). It is mainly used in a the [ProteinStructureFetch Extension](TODO) of the [VRNetzer](https://github.com/menchelab/VRNetzer). For everyone who wants to analyze their own protein structures, with your desired highlighting and coloring, this project is the right place to start. For easy usage of this project, we provide a one file executable which allows to use the program without further installation of python and any dependencies. Nevertheless, a [ChimeraX](https://www.cgl.ucsf.edu/chimerax/download.html) installation is mandatory to use the full potential of this project.
Without ChimeraX this software only provides a fetcher with which you can easily fetch pdb files from the [AlphaFold Database](https://alphafold.ebi.ac.uk/) as well as some converter functions.

---

# Quickstart

#### Software/OS requirements

- An installation of ChimeraX

### Installation

Tested with Python 3.9+ .

Install the package e.g. in a virtual environment:

- create a virtual environment<br>
  `python3 -m venv name_of_env`
- activate it<br>
  `source name_of_env/bin/activate`
- install requirements packages<br>
  `python3 -m pip install -r requirements.txt`

- under mac you might have to install the following packages<br>
  `brew install libomp`
- install alphafold_to_vrnetzer<br>
  `TODO`

### Process a single structure

`./main.py fetch <UniProtID`<br>
example:<br>
`./main.py fetch O95352`<br>
This will fetch the structure of O95352 from the AlphaFold database and
processes it using the pipeline. As coloring the secondary structures are
colored in red, green and blue.

### Process multiple structures

`./main.py fetch <list_separated_by_comma>`<br>
example:<br>
`./main.py fetch O95352,Q9Y5M8,Q9UKX5`<br>
This will fetch the structure of O95352, Q9Y5M8 and Q9UKX5 from the AlphaFold
database and processes them using the pipeline. As coloring the secondary structures are
colored in red, green and blue.

### Process from a list of proteins

`./main.py list <path_to_file>`
<br>
example:<br>
`./main.py list proteins.txt`
<br>
Works like the previous command, but the python list is read from a file.

### Process from local PDB files

`./main.py local <path_to_directory>`<br>
example:<br>
`./main.py local /User/Documents/pdb_files`<br>
This will process all structures in this directory. If there are only PDB files
in this directory, for all of them the complete pipeline will be executed. It is also possible to
have a directory containing intermediate states like PLY files.
For these structures the process will start at the corresponding step.

### Get help

To get an overview of the available commands, use the `--help` command.<br>
`./main.py --help`

### Usage and flags

`./main.py [optional arguments] <command> (positional arguments)`<br>

```
usage: main.py [-h] [-pdb_file [PDB_DIRECTORY]] [-glb_file [GLB_DIRECTORY]] [-ply_file [PLY_DIRECTORY]] [-cloud [PCD_DIRECTORY]]
               [-map [MAP_DIRECTORY]] [-alphafold_version [{v1,v2}]] [-batch_size [BATCH_SIZE]] [-keep_pdb [{True,False}]]
               [-keep_glb [{True,False}]] [-keep_ply [{True,False}]] [-keep_ascii [{True,False}]] [-chimerax [CHIMERAX_EXEC]]
               [-color_mode [CM]]
               {fetch,local,list,clear} ...

positional arguments:
  {fetch,local,list,clear}
                        mode
    fetch               Fetch proteins from the Alphafold database.
    local               Process proteins from files (.pdb, .glb, .ply, .xyzrgb) in a directory.
    list                Process proteins from a python list of paths to PDB files.
    clear               Removes the processing_files directory

optional arguments:
  -h, --help            show this help message and exit
  -pdb_file [PDB_DIRECTORY], --pdb [PDB_DIRECTORY]
                        Defines, where to save the PDB Files.
  -glb_file [GLB_DIRECTORY], --glb [GLB_DIRECTORY]
                        Defines, where to save the GLB Files.
  -ply_file [PLY_DIRECTORY], --ply [PLY_DIRECTORY]
                        Defines, where to save the PLY Files.
  -cloud [PCD_DIRECTORY], --pcd [PCD_DIRECTORY]
                        Defines, where to save the ASCII point clouds.
  -map [MAP_DIRECTORY], --m [MAP_DIRECTORY]
                        Defines, where to save the color maps.
  -alphafold_version [{v1,v2}], --av [{v1,v2}]
                        Defines, which version of Alphafold to use.
  -batch_size [BATCH_SIZE], --bs [BATCH_SIZE]
                        Defines the size of the batch which will be processed
  -keep_pdb [{True,False}], -kpdb [{True,False}]
                        Define whether to still keep the PDB files after the GLB file is created. Default is True.
  -keep_glb [{True,False}], -kglb [{True,False}]
                        Define whether to still keep the GLB files after the PLY file is created. Default is False.
  -keep_ply [{True,False}], -kply [{True,False}]
                        Define whether to still keep the PLY files after the ASCII file is created. Default is False.
  -keep_ascii [{True,False}], -kasc [{True,False}]
                        Define whether to still keep the ASCII Point CLoud files after the color maps are generated. Default is False.
  -chimerax [CHIMERAX_EXEC], --ch [CHIMERAX_EXEC]
                        Defines, where to find the ChimeraX executable.
  -color_mode [CM], --cm [CM]
                        Defines the coloring mode which will be used to color the structure. Choices: cartoons_ss_coloring,
                        cartoons_rainbow_coloring, cartoons_heteroatom_coloring, cartoons_polymer_coloring, cartoons_chain_coloring... . For
                        a full list, see README.
```

## Larger structures from the AlphaFold DB

All structures fetched directly from the AlphaFold DB have a maximum length of 2700 amino acids.
Larger structures are contained in the [bulk downloads](https://alphafold.ebi.ac.uk/download) offered by AlphaFold DB.
To unpack the pdb files from these archives, one can use the extract_alphafold.sh bash script located in "pypi_project/src/vrprot/scripts/".
This script will extract all pdb files from the archive and save them in the desired directory.
Use the script as follows:

```
  pypi_project/src/vrprot/scripts/extract_alphafold.sh <path_to_archive> <path_to_output_directory>
```

Structures larger than 2700 amino acids are seperated in multiple fractions (F1 - Fn).
A python script is provided to combine these fractions into one structure. Use the script with ChimeraX's python interpreter.
The script can be run either directly from the command line interface:

Linux:

```
  chimerax --offscreen --script '"combine_structures.py" "<path_to_directory>" "<path_to_output_directory>" -sp (optional) -mode <color_mode>'
```

Mac:

```
  /Applications/ChimeraX-<version>.app/Contents/MacOS/chimerax --script '"combine_structures.py" "<path_to_directory>" "<path_to_output_directory>" -sp (optional) -mode <color_mode>'
```

Windows:

```
  #TODO:Try this
  "C:\Program Files\ChimeraX-X\bin\chimerax.exe" --script '"combine_structures.py" "<path_to_directory>" "<path_to_output_directory>" -sp (optional) -mode <color_mode>'
```

Be sure to position the quotation marks correctly!
Or inside of ChimeraX executing the following command:

```
  runscript combine_structures.py <path_to_directory> <path_to_output_directory>
```

## Possible Color Modes

```
cartoons_ss_coloring
cartoons_rainbow_coloring
cartoons_heteroatom_coloring
cartoons_polymer_coloring
cartoons_chain_coloring
cartoons_bFactor_coloring
cartoons_nucleotide_coloring
surface_ss_cooloring
surface_rainbow_cooloring
surface_heteroatom_cooloring
surface_polymer_cooloring
surface_chain_cooloring
surface_electrostatic_coloring
surface_hydrophic_coloring
surface_bFactor_coloring
surface_nucleotide_coloring
stick_ss_coloring
stick_rainbow_coloring
stick_heteroatom_coloring
stick_polymer_coloring
stick_chain_coloring
stick_bFactor_coloring
stick_nucleotide_coloring
ball_ss_coloring
ball_rainbow_coloring
ball_heteroatom_coloring
ball_polymer_coloring
ball_chain_coloring
ball_bFactor_coloring
ball_nucleotide_coloring
sphere_ss_coloring
sphere_rainbow_coloring
sphere_heteroatom_coloring
sphere_polymer_coloring
sphere_chain_coloring
sphere_bFactor_coloring
sphere_nucleotide_coloring
```

---

---

# **_DEPRECATED_**

---

---

# PDB Parser

#### Author: Till Pascal Oblau

You can import the class ChimeraXProcessing from pdb_parser.py
to parse a PDB file.

## Create a Protein object with:

```
from pdb_parser import ChimeraXProcessing

pdb_parser = ChimeraXProcessing(protein={"P38606":"P38606"}, keepFiles = <True/False>)

```

The protein dictionary contains all the protein structures you want to process.
You can add a new structure by using:

```
pdb_parser.add_protein(<UniProtID>)
```

The keepFiles argument can be used, to tell the program, to not delete PDB and
GLB file after the processing is accomplished.

## Fetch the PDB

```
pdb_parser.fetch_pdb(protein)
```

This will download the PDB file from the AlphaFold DB if available. This will be saved in a subfolder called "./pdbs/".

If the structure is not available on the AlphaFold DB it will try to download it from the RCSB database. If the structure is also not available here, it will report it to you.

## Color the secondary structures

You can define the installation Path to your ChimeraX installation by using:

```
# For Linux (default))
pdb_parser.ChimeraX = "chimerax"
# For Mac
pdb_parser.ChimeraX = "/Applications/<ChimeraX_Version>.app/Contents/MacOS/ChimeraX"
```

Then you should be able to use:

```
pdb_parser.color_ss_chimerax(portein,colors=["red", "green", "blue"]) # color argument is optional (Coil = "red", Helix = "green", Strand = "blue")
```

This will open Chimerax, select the secondary structures and color them as asked.

It will save the results as a .glb file.

## Convert .glb with colors to .ply file

To convert a GLB file to PLY you can use the convertGLBToPLY function of the
ChimeraXProcessing class. You can simply call the function together with the
UniProtID of the respective protein. You can then use:

```
pdb_parser.convertGLPToPly(<UniProtID>)
```

This will convert the GLB file, which has been processed beforehand,
to a PLY file.

# Create the PointCloud

# sample_pointcloud.py

#### Author: Felix Fischer

## Requires python library open3d

## Requires "Cube_no_lines.ply" in base folder of script.

This script will import the protein mesh (requires uniport ID of protein as input) and the mesh "Cube_no_lines.ply". The cube mesh (based on "Cube.fbx") is used for normalization of coordinate space of protein-mesh. The protein-mesh will be translated to the center coordinates of the cube-mesh and scaled to approximately the size of the cube-mesh. The two meshes will then be merged and a point cloud is sampled (1048576 points sampled) and stored as ASCII file in /ASCII_clouds (will create folder if it does not exist).

# Create .png files

# pointcloud2map

#### Author: Felix Fischer

## Requires python library PyPNG, numpy

This script opens the ASCII cloud of protein (requires uniport ID of protein as input) from ASCII_clouds foler, reads and stores the xyz coordinates and rgb value for each point in the point cloud in a seperate matrix, which is then converted in to two PNG files of size 1024x1024. The resulting PNG maps are stored in /MAPS/xyz and /MAPS/rgb (will create folder if it does not exist).
