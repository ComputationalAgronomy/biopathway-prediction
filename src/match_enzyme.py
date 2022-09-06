import os
import sys
import pandas as pd

class PathwayNode():
    def __init__(self, name, enzyme_id, visited):
        # the name of the chemical compound
        self.name = name
        # the enzymes that can catalyze this compound to another one
        self.reaction = enzyme_id
        # has this compound been made from an enzyme?
        # (or if it's a starting material)
        self.visited = visited

class Enzyme():
    def __init__(self, name, product_id, exist=False, count=0):
        self.name = name
        self.product = product_id
        self.exist = exist
        self.count = count
    
    def react(self, pathway_list):
        # once the product has been visited, there's no need to call the next
        # reaction again
        if not pathway_list[self.product].visited:
            pathway_list[self.product].visited = True
            return self.product
        else:
            return None

pathway_list = {1: PathwayNode("trp", [1, 3], True),
                2: PathwayNode("iam_1", [2], False),
                3: PathwayNode("indole-3-acetic-acid", [0], False),
                4: PathwayNode("ipa_1", [4], False),
                5: PathwayNode("ipa_2", [5], False)
                }

enzyme_list = {0: None,
               1: Enzyme("trp_iam_1", 2),
               2: Enzyme("iam_1_indole", 3),
               3: Enzyme("trp_ipa_1", 4),
               4: Enzyme("ipa_1_2", 5),
               5: Enzyme("ipa_2_indole", 3)}


assert len(sys.argv) == 2, "Invalid arguments"
filename= sys.argv[1]

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

def match_enzyme_existence(filename, enzyme_list):
    data = pd.read_csv(filename, usecols=["enzyme_id"])
    data = data.groupby("enzyme_id").size().reset_index(name="count")
    for _, (enzyme_id, count) in data.iterrows():
        if enzyme_id != "-":
            enzyme_id = int(enzyme_id)
            if enzyme_list[enzyme_id] is not None:
                enzyme_list[enzyme_id].exist = True
                enzyme_list[enzyme_id].count = count

match_enzyme_existence(filename, enzyme_list)
enzyme_reaction(1, enzyme_list, pathway_list)
print_pathway(pathway_list)