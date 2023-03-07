# VRPROT

## ABOUT VRPROT

A pipeline that processes protein structures in ProteinDataBank (PDB) file format
using ChimeraX and enables them to be analyzed on the [VRNetzer](https://github.com/menchelab/VRNetzer) platform.

---

## PROTEIN STRUCTURE ANALYSIS

---

## USAGE OF THIS PROJECT

The main purpose of this project is to serve as an easy-to-use pipeline to facilitate the processing of protein structures for presentation on the [VRNetzer](https://github.com/menchelab/VRNetzer). It is mainly used in the [ProteinStructureFetch Extension](TODO) of the [VRNetzer](https://github.com/menchelab/VRNetzer). For everyone who wants to analyze their own protein structures, with your desired highlighting and coloring, this project is the right place to start.
The program consists of five parts:
| Part | Description |
| ----------| --- |
|**Fetcher** | Fetches PDB files from [AlphaFold Database](https://alphafold.ebi.ac.uk/)|
|**ChimeraX Processor**| Processes the PDB files with [ChimeraX](https://www.cgl.ucsf.edu/chimerax/download.html)|
|**GLB Converter**|Converts GLB files to PLY files|
|**Point Cloud Sampler**|samples point clouds from the PLY files|
|**Color Map Generator**| generates the final color maps which are needed to present protein structures on the [VRNetzer](https://github.com/menchelab/VRNetzer) platform.|

For easy usage of this project, we provide a one-file executable that allows using the program without further installation of Python and any dependencies. Nevertheless, a [ChimeraX](https://www.cgl.ucsf.edu/chimerax/download.html) installation is mandatory to use the full potential of this project.
Without [ChimeraX](https://www.cgl.ucsf.edu/chimerax/download.html) the **ChimeraX Processor** cannot work.

---
