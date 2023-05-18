import numpy as np
import pandas as pd

from .existence_score_model import existence_score_model
from .pathway import enzyme_list, pathway_list

def start_match_enzyme(filename, output_filename, model, quiet,
                      enzyme_list=enzyme_list, pathway_list=pathway_list):
    """
    Perform pathway mapping from the predicted enzymes and output scores
    evaluated from the model
    """
    match_enzyme_existence(filename, enzyme_list)
    traverse_enzyme_reaction(pathway_list[1], enzyme_list, pathway_list)
    result = []
    result.extend(get_pathway_result(pathway_list, model, quiet))
    result.extend(get_enzyme_result(enzyme_list, model, quiet))
    with open(output_filename, "w") as f:
        f.writelines(result)
    reset_enzyme_and_pathway(enzyme_list, pathway_list)


def match_enzyme_existence(filename, enzyme_list):
    """
    Calculate scores (0 - 1) from the given model and count the number of
    enzymes that have the same function
    The results are stored in Enzyme objects

    Steps
    -----
    1. Get "identity" value from best_blast results
    2. Calculate scores from "identity"
    3. Group enzymes by "enzyme_id" and use the "probability framework" we
       established to calculate the "probability" that the enzymes with the same
       "enzyme_id" will function normally
       .
       (i.e., the edge score is determined here to stand for the probability
        that the product can be synthesized from its reactant)
    4. Update the edge scores and enzyme counts to the Enzyme objects

    """
    data = pd.read_csv(filename, usecols=["enzyme_id", "identity"])
    data = data[data["enzyme_id"] != "-"]
    data["existence_score"] = existence_score_model(data["identity"])
    data = data.groupby("enzyme_id").agg(
        count=("enzyme_id", "count"),
        prob=("existence_score", lambda x: 1 - np.nanprod(1 - x))).reset_index()
    for _, (enzyme_id, count, prob) in data.iterrows():
        try:
            enzyme_id = int(enzyme_id)
            enzyme_list[enzyme_id].set_count(count)
            enzyme_list[enzyme_id].set_prob(prob)
        except (ValueError, AttributeError):
            pass


def traverse_enzyme_reaction(material, enzyme_list, pathway_list):
    """
    Traverse the pathway and determine the scores of the compounds by the
    "react" method in the PathwayNode object.
    """
    for enzyme in material.next_enzyme:
        try:
            product = pathway_list[enzyme_list[enzyme].product]
            reactant = pathway_list[enzyme_list[enzyme].reactant]
            next_material = product.react(enzyme_list[enzyme], reactant)
        except (KeyError, AttributeError):
            next_material = None
        if next_material is not None:
            traverse_enzyme_reaction(next_material, enzyme_list, pathway_list)


def get_pathway_result(pathway_list, model, quiet):
    """
    Obtain scores (0 - 1) or existence (True / False) from Compound objects
    and print the result by default (can be muted by --quiet) 
    """
    message = []
    if not quiet:
        print("Compound list:")
    message.append("Compound list:\n")
    for pathwaynode in pathway_list.values():
        compound = pathwaynode.name
        if model == "prob":
            existence = np.round(pathwaynode.existence_prob, 6)
        elif model == "binary":
            existence = pathwaynode.visited
        else:
            raise NameError("Model name error")
        if not quiet:
            print(f"{compound}: {existence}")
        message.append(f"{compound}: {existence}\n")
    if not quiet:
        print()
    message.append("\n")
    return message


def get_enzyme_result(enzyme_list, model, quiet):
    """
    Obtain scores (0 - 1) or existence (True / False) from Enzyme objects
    and print the result by default (can be muted by --quiet) 
    """
    message = []
    if not quiet:
        print("Enzyme list:")
    message.append("Enzyme list:\n")
    for enzyme in enzyme_list.values():
        try:
            enzyme_name = enzyme.name
            if model == "prob":
                enzyme_existence = np.round(enzyme.prob, 6)
            elif model == "binary":
                enzyme_existence = enzyme.exist
            else:
                raise NameError("Model name error")
            if not quiet:
                print(f"{enzyme_name}: {enzyme_existence}")
            message.append(f"{enzyme_name}: {enzyme_existence}\n")
        except AttributeError:
            pass
    return message


def reset_enzyme_and_pathway(enzyme_list, pathway_list):
    """
    Reinitialize objects in the enzyme_list and pathway_list after pathway
    mapping
    """
    for enzyme in enzyme_list.values():
        try:
            enzyme.reset()
        except AttributeError:
            pass
    for pathway in pathway_list.values():
        pathway.reset()




