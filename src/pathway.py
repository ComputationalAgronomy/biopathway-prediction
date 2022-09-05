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
    def __init__(self, name, product_id, exist):
        self.name = name
        self.product = product_id
        self.exist = exist
    
    def react(self, pathway_list):
        # once the product has been visited, there's no need to call the next
        # reaction again
        if not pathway_list[self.product].visited:
            pathway_list[self.product].visited = True
            return self.product
        else:
            return None



pathway_list = {1: PathwayNode("trp", [1, 2, 3], True),
                2: PathwayNode("trp_1", [4], False),
                3: PathwayNode("trp_2", [0], False),
                4: PathwayNode("trp_3", [0], False),
                5: PathwayNode("trp_1_1", [0], False)
                }

enzyme_list = {0: None,
               1: Enzyme("trp_to_1", 2, False),
               2: Enzyme("trp_to_2", 3, True),
               3: Enzyme("trp_to_3", 4, True),
               4: Enzyme("trp_1_to_1", 5, True)}

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

enzyme_reaction(1, enzyme_list, pathway_list)
print_pathway(pathway_list)
