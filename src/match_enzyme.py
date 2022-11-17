import numpy as np
import pandas as pd
from .pathway import PathwayNode, Enzyme, pathway_list, enzyme_list



def traverse_enzyme_reaction(material, enzyme_list, pathway_list):
    for enzyme in material.next_enzyme:
        try:
            product = pathway_list[enzyme_list[enzyme].product]
            reactant = pathway_list[enzyme_list[enzyme].reactant]
            next_material = product.react(enzyme_list[enzyme], reactant)
        except AttributeError:
            next_material = None
        if next_material is not None:
            traverse_enzyme_reaction(next_material, enzyme_list, pathway_list)
    

def get_pathway_result(pathway_list, model, quiet):
    message = []
    if not quiet:
        print("Compound list:")
    message.append("Compound list:\n")
    for pathwaynode in pathway_list.values():
        compound = pathwaynode.name
        if model == "prob":
            existence = np.round(pathwaynode.existence_prob, 3)
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
    message = []
    if not quiet:
        print("Enzyme list:")
    message.append("Enzyme list:\n")
    for enzyme in enzyme_list.values():
        try:
            enzyme_name = enzyme.name
            if model == "prob":
                enzyme_existence = np.round(enzyme.prob, 3)
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

def existence_score_model(x):
    x = x[x > 40]
    y = 0.18 * np.log(0.15 * (x - 40) + 1) + 0.6
    y = np.minimum(y, 1)
    return y

def match_enzyme_existence(filename, enzyme_list):
    data = pd.read_csv(filename, usecols=["enzyme_id", "identity_percentage"])
    data = data[data["enzyme_id"] != "-"]
    data["existence_score"] = existence_score_model(data["identity_percentage"])
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

def reset_enzyme_and_pathway(enzyme_list, pathway_list):
    for enzyme in enzyme_list.values():
        try:
            enzyme.reset()
        except AttributeError:
            pass
    for pathway in pathway_list.values():
        pathway.reset()

def _run_match_enzyme(filename, output_filename, model, quiet,
                      enzyme_list=enzyme_list, pathway_list=pathway_list):
    match_enzyme_existence(filename, enzyme_list)
    traverse_enzyme_reaction(pathway_list[1], enzyme_list, pathway_list)
    result = []
    result.extend(get_pathway_result(pathway_list, model, quiet))
    result.extend(get_enzyme_result(enzyme_list, model, quiet))
    with open(output_filename, "w") as f:
        f.writelines(result)
    reset_enzyme_and_pathway(enzyme_list, pathway_list)

    
