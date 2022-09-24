import pandas as pd
from .pathway import PathwayNode, Enzyme, PATHWAY_LIST, ENZYME_LIST


# traverse from the starting material
def enzyme_reaction(material, enzyme_list, pathway_list):
    for enzyme in pathway_list[material].reaction:
        if enzyme_list[enzyme] is not None and enzyme_list[enzyme].exist:
            next_reaction = enzyme_list[enzyme].react(pathway_list)
            if next_reaction is not None:
                enzyme_reaction(next_reaction, enzyme_list, pathway_list)

def print_pathway(pathway_list):
    message = []
    print("Compound list:")
    message.append("Compound list:\n")
    for pathwaynode in pathway_list.values():
        print(f"{pathwaynode.name}: {pathwaynode.visited}")
        message.append(f"{pathwaynode.name}: {pathwaynode.visited}\n")
    print()
    message.append("\n")
    return message

def print_enzyme(enzyme_list):
    message = []
    print("Enzyme list:")
    message.append("Enzyme list:\n")
    for enzyme in enzyme_list.values():
        if enzyme is not None:
            print(f"{enzyme.name}: {enzyme.count}")
            message.append(f"{enzyme.name}: {enzyme.count}\n")
    return message

def match_enzyme_existence(filename, enzyme_list):
    data = pd.read_csv(filename, usecols=["enzyme_id"])
    data = data.groupby("enzyme_id").size().reset_index(name="count")
    for _, (enzyme_id, count) in data.iterrows():
        if enzyme_id != "-":
            enzyme_id = int(enzyme_id)
            if enzyme_list[enzyme_id] is not None:
                enzyme_list[enzyme_id].exist = True
                enzyme_list[enzyme_id].count = count

def run_match_enzyme(filename, output, enzyme_list=ENZYME_LIST,
                     pathway_list=PATHWAY_LIST):
    match_enzyme_existence(filename, enzyme_list)
    enzyme_reaction(1, enzyme_list, pathway_list)
    result = []
    result.extend(print_pathway(pathway_list))
    result.extend(print_enzyme(enzyme_list))
    with open(output, "w") as f:
        f.writelines(result)
