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