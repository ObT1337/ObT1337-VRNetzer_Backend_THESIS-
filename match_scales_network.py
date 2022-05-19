def write_csv(
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
    with open("./uniprot_mapping.csv") as f:
        lines = f.readlines()
        uniProt_Mapping = {}
        for line in lines:
            UniProt = line.split(",")[1]
            network_identifier = line.split(",")[2].strip("\n")
            uniProt_Mapping[network_identifier] = UniProt

    ## Extract scale information
    with open("./scales.csv") as f:
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
