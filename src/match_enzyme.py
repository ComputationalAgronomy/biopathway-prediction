if __name__ == "__main__":
    import sys
    import pandas as pd
    from pathway import PathwayNode, Enzyme, PATHWAY_LIST, ENZYME_LIST
else:
    import pandas as pd
    from pathway import PathwayNode, Enzyme, PATHWAY_LIST, ENZYME_LIST


# traverse from the starting material
def enzyme_reaction(material, enzyme_list, pathway_list):
    for enzyme in pathway_list[material].reaction:
        if enzyme_list[enzyme] is not None and enzyme_list[enzyme].exist:
            next_reaction = enzyme_list[enzyme].react(pathway_list)
            if next_reaction is not None:
                enzyme_reaction(next_reaction, enzyme_list, pathway_list)

def print_pathway(pathway_list):
    for pathwaynode in pathway_list.values():
        print(f"{pathwaynode.name}: {pathwaynode.visited}")

def print_enzyme(enzyme_list):
    for enzyme in enzyme_list.values():
        print(f"{enzyme.name}: {enzyme.count}")

def match_enzyme_existence(filename, enzyme_list):
    data = pd.read_csv(filename, usecols=["enzyme_id"])
    data = data.groupby("enzyme_id").size().reset_index(name="count")
    for _, (enzyme_id, count) in data.iterrows():
        if enzyme_id != "-":
            enzyme_id = int(enzyme_id)
            if enzyme_list[enzyme_id] is not None:
                enzyme_list[enzyme_id].exist = True
                enzyme_list[enzyme_id].count = count

def run_match_enzyme(filename, enzyme_list=ENZYME_LIST, pathway_list=pathway_list):
    match_enzyme_existence(filename, enzyme_list)
    enzyme_reaction(1, enzyme_list, pathway_list)
    print_pathway(pathway_list)
    print_enzyme(enzyme_list)

if __name__ == "__main__":
    assert len(sys.argv) == 2, "Invalid arguments"
    filename= sys.argv[1]
    run_match_enzyme(filename)