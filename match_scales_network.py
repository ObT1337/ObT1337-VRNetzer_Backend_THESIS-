import pandas as pd


def write_csv_noHeader(
    network_file="./1_spring.csv",
    scales_file="./scales.csv",
    mapping_file="./uniprot_mapping.csv",
):
    """
    Will add UniProt IDs to each Gene Name and, if available, the scale of the corresponding protein structure.
    Needs 3 files:
    - network file which contains the network information.
    - scale file which contains the scaling information for each protein structure
    - mapping_file to map UniProt IDs to Gene Names
    """
    scales = {}
    ## Extract information from UniProt Mapping file
    with open(mapping_file) as f:
        lines = f.readlines()
        uniProt_Mapping = {}
        for line in lines:
            UniProt = line.split(",")[1]
            network_identifier = line.split(",")[2].strip("\n")
            uniProt_Mapping[network_identifier] = UniProt

    ## Extract scale information
    with open(scales_file) as f:
        scale_Mapping = f.readlines()
        for line in scale_Mapping[1:]:
            protein, scale = line.split(",")
            scales[protein] = scale.strip("\n")

    ## extract network information
    with open(network_file) as f:
        lines = f.read().strip().split("\n")
        network_Mapping = {}
        for line in lines:
            identifier = line.split(";")[1]
            network_Mapping[identifier] = line

    ## write new network information
    with open(f"{network_file[:-4]}_mapping.csv", "w+") as w:
        for k, node in network_Mapping.items():
            network_identifier = node.split(";")[1]
            if network_identifier in uniProt_Mapping.keys():
                uniProt = uniProt_Mapping[network_identifier]
                network_Mapping[network_identifier] = node + f";{uniProt}"
                if uniProt in scales.keys():
                    scale = scales[uniProt]
                    print(scale)
                    network_Mapping[network_identifier] += f";{scale}"
                else:
                    network_Mapping[network_identifier] += f";-1"
            else:
                network_Mapping[network_identifier] = node + f";-1;-1"

        for line in list(network_Mapping.values())[:-1]:
            w.write(f"{line}\n")
        w.write(f"{list(network_Mapping.values())[-1]}")


def write_csv_WithHeader(
    network_file="./static/csv/ID_entrez_sym.csv",
    scales_file="./static/csv/scales_Cartoon.csv",
    mapping_file="./static/csv/uniprot_mapping.csv",
):
    """
    Will add UniProt IDs to each Gene Name and, if available, the scale of the corresponding protein structure.
    Needs 3 files:
    - network file which contains the network information.
    - scale file which contains the scaling information for each protein structure
    - mapping_file to map UniProt IDs to Gene Names
    Applied on ID_entrez_sym.csv format
    """
    # TODO use pandas to use header for column targeting
    scales = {}
    ## Extract information from UniProt Mapping file
    with open(mapping_file) as f:
        lines = f.readlines()
        uniProt_Mapping = {}
        for line in lines:
            UniProt = line.split(",")[1]
            genesym = line.split(",")[0].strip("\n")
            uniProt_Mapping[genesym] = UniProt

    ## Extract scale information
    with open(scales_file) as f:
        scale_Mapping = f.readlines()
        for line in scale_Mapping[1:]:
            protein, scale = line.split(",")
            scales[protein] = scale.strip("\n")

    ## extract network information
    with open(network_file) as f:
        lines = f.read().strip().split("\n")
        network_Mapping = {}
        for line in lines:
            identifier = line.split(",")[2]
            network_Mapping[identifier] = line

    ## write new network information
    with open(f"{network_file[:-4]}_mapping.csv", "w+") as w:
        for k, node in list(network_Mapping.items())[1:]:
            node_num, entry, genesym = node.strip("\n").split(",")
            if genesym in uniProt_Mapping.keys():
                uniProt = uniProt_Mapping[genesym]
                network_Mapping[
                    genesym
                ] = f"{node_num},{entry},,,,,,{genesym};;;{uniProt}"
                if uniProt in scales.keys():
                    scale = scales[uniProt]
                    network_Mapping[genesym] += f";{scale}"
                else:
                    network_Mapping[genesym] += f";-1"
            else:
                network_Mapping[genesym] = node + f";-1;-1"

        for line in list(network_Mapping.values())[1:-1]:
            w.write(f"{line}\n")
        w.write(f"{list(network_Mapping.values())[-1]}")


def pandas_writing(
    network_file="./static/csv/ID_entrez_sym.csv",
    network_col_idx="Genesym",
    scales_file="./static/csv/scales_Cartoon.csv",
    scales_col_idx="UniProtID",
    mapping_file="./static/csv/uniprot_mapping.csv",
    mapping_col_idx="Approved symbol",
):
    """
    Will add UniProt IDs to each Gene Name and, if available, the scale of the corresponding protein structure.
    Needs 3 files:
    - network file which contains the network information.
    - scale file which contains the scaling information for each protein structure
    - mapping_file to map UniProt IDs to Gene Names
    Applied on ID_entrez_sym.csv format
    """
    # TODO use pandas to use header for column targeting
    scales = {}
    ## Extract information from UniProt Mapping file
    uniProt_Mapping = pd.read_csv(mapping_file, index_col=mapping_col_idx, header=0)
    # ## Extract scale information
    scales = pd.read_csv(scales_file, index_col=scales_col_idx, header=0)
    # ## extract network information
    network_Mapping = pd.read_csv(network_file, index_col=network_col_idx)
    output_dataframe = pd.DataFrame(
        columns=["x", "y", "z", "r", "g", "b", "a", "annotations"]
    )
    annotation_dataframe = pd.DataFrame(
        columns=[
            "Approved symbol",
            "NCBI Gene ID",
            "description",
            "UniProt ID",
            "scale of structure map",
        ]
    )
    ## write new network information
    with open(f"{network_file[:-4]}_mapping.csv", "w+") as w:
        for protein in network_Mapping.index:
            ncbi = network_Mapping.loc[protein]["entrez"]
            scale = -1
            uniProt = -1
            if protein in uniProt_Mapping.index:
                print(protein, uniProt_Mapping.loc[protein])
                uniProt = uniProt_Mapping.loc[protein][
                    "UniProt ID(supplied by UniProt)"
                ]
                ncbi = uniProt_Mapping.loc[protein]["NCBI Gene ID(supplied by NCBI)"]
                if uniProt in scales.index:
                    scale = scales.loc[uniProt]["scale"]
            newAnnotations = {
                "Approved symbol": protein,
                "NCBI Gene ID": ncbi,
                "description": "TEST",
                "UniProt ID": uniProt,
                "scale of structure map": scale,
            }
            newRow = {
                "x": "",
                "y": "",
                "z": "",
                "r": "",
                "g": "",
                "b": "",
                "annotations": newAnnotations,
            }
            output_dataframe.append(newRow, ignore_index=True)
            print(output_dataframe.iloc[-1:]["annotations"])
            exit()


write_csv_WithHeader()
