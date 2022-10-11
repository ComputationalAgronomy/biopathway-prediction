class PathwayNode():

    def __init__(self, name, enzyme_id, default_visited):
        # the name of the chemical compound
        self.name = name
        # the enzymes that can catalyze this compound to another one
        self.reaction = enzyme_id
        # has this compound been made from an enzyme?
        # (or if it's a starting material)
        self.default_visited = default_visited
        self.visited = self.default_visited
    
    def reset(self):
        self.visited = self.default_visited


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
        return None

    def set_count(self, count):
        self.exist = True
        self.count = count

    def reset(self):
        self.exist = False
        self.count = 0

pathway_list = {1: PathwayNode("trp", [1, 3, 7, 9], True),
                2: PathwayNode("iam_1", [2], False),
                3: PathwayNode("iaa", [0], False),
                4: PathwayNode("ipa_1", [4, 6], False),
                5: PathwayNode("ipa_2", [5], False),
                6: PathwayNode("tam_1", [8], False),
                7: PathwayNode("iaox", [10], False),
                8: PathwayNode("ian_1", [11, 12], False)
                }

enzyme_list = {0: None,
               1: Enzyme("trp_iam_1", 2),
               2: Enzyme("iam_1_iaa", 3),
               3: Enzyme("trp_ipa_1", 4),
               4: Enzyme("ipa_1_2", 5),
               5: Enzyme("ipa_2_iaa", 3),
               6: Enzyme("ipa_1_iaa", 3),
               7: Enzyme("trp_tam_1", 6),
               8: Enzyme("tam_1_ipa_2", 5),
               9: Enzyme("trp_iaox", 7),
               10: Enzyme("iaox_ian_1", 8),
               11: Enzyme("ian_1_iaa", 3),
               12: Enzyme("ian_1_iam_1", 2)}
