import numpy as np

class PathwayNode():

    def __init__(self, name, pre_enzyme, next_enzyme, default_visited):

        # the name of the chemical compound
        self.name = name
        # the enzymes that can catalyze this compound to another one
        self.pre_enzyme = pre_enzyme
        self.next_enzyme = next_enzyme
        self.reacted = 0
        self.indegree = len(pre_enzyme)
        # has this compound been made from an enzyme?
        # (or if it's a starting material)
        self.default_visited = default_visited
        self.visited = self.default_visited
        self.existence_prob = float(self.default_visited)
        self.existence_prob_list = []

    def react(self, enzyme, reactant):
        # once the product has been visited, there's no need to call the next
        # reaction again
        self.reacted += 1
        if not self.visited:
            self.visited = enzyme.exist and reactant.visited
        self.existence_prob_list.append(enzyme.prob * reactant.existence_prob)
        if self.reacted == self.indegree:
            self.existence_prob = 1 - np.prod(1 - np.array(self.existence_prob_list))
            return self
        return None

    def reset(self):
        self.visited = self.default_visited
        self.existence_prob = float(self.default_visited)
        self.existence_prob_list = []
        self.reacted = 0


class Enzyme():

    def __init__(self, name, reactant_id, product_id, exist=False, count=0):
        self.name = name
        self.reactant = reactant_id
        self.product = product_id
        self.exist = exist
        self.count = count
        self.prob = 0

    def set_count(self, count):
        self.exist = True
        self.count = count
    
    def set_prob(self, prob):
        self.prob = prob

    def reset(self):
        self.exist = False
        self.count = 0
        self.prob = 0

pathway_list = {1: PathwayNode("trp", [0], [1, 3, 7, 9], True),
                2: PathwayNode("iam_1", [1, 12], [2], False),
                3: PathwayNode("iaa", [2, 5, 6, 11], [0], False),
                4: PathwayNode("ipa_1", [3], [4, 6], False),
                5: PathwayNode("ipa_2", [4, 8], [5], False),
                6: PathwayNode("tam_1", [7], [8], False),
                7: PathwayNode("iaox", [9], [10], False),
                8: PathwayNode("ian_1", [10], [11, 12], False)
                }

enzyme_list = {0: None,
               1: Enzyme("trp_iam_1", 1, 2),
               2: Enzyme("iam_1_iaa", 2, 3),
               3: Enzyme("trp_ipa_1", 1, 4),
               4: Enzyme("ipa_1_2", 4, 5),
               5: Enzyme("ipa_2_iaa", 5, 3),
               6: Enzyme("ipa_1_iaa", 4, 3),
               7: Enzyme("trp_tam_1", 1, 6),
               8: Enzyme("tam_1_ipa_2", 6, 5),
               9: Enzyme("trp_iaox", 1, 7),
               10: Enzyme("iaox_ian_1", 7, 8),
               11: Enzyme("ian_1_iaa", 8, 3),
               12: Enzyme("ian_1_iam_1", 8, 2)}
