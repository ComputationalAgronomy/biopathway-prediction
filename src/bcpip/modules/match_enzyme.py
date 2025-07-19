from pathlib import Path
from typing import Dict, List, Literal, Union

import numpy as np
import pandas as pd

from bcpip.modules.existence_score_model import existence_score_model
from bcpip.modules.pathway import (Enzyme, PathwayNode, enzyme_dict,
                                         pathway_dict)


def start_match_enzyme(filepath: Union[str, Path],
                       output_filepath: Union[str, Path],
                       model: Literal["logistic", "binary"],
                       verbose: bool,
                       enzyme_dict: Dict[int, Union[None, Enzyme]] = enzyme_dict,
                       pathway_dict: Dict[int, PathwayNode] = pathway_dict):
    """
    Perform pathway mapping from the predicted enzymes and output scores
    evaluated from the model.

    Args:
        filepath: The path to a .csv file containing best alignment results.
        output_filepath: The path for saving output.
        model: The `logistic` or `binary` model in calculating pathway node score.
        verbose: Whether to print the result to screen.
        enzyme_dict: The dictionary that contains the enzyme info of the pathway.
        pathway_dict: The dictionary that contains the compound info of the pathway.
    """
    match_enzyme_existence(filepath, enzyme_dict)
    # The starting compound is given the key: 1
    traverse_enzyme_reaction(pathway_dict[1], enzyme_dict, pathway_dict)
    result = []
    result.extend(get_pathway_result(pathway_dict, model, verbose))
    result.extend(get_enzyme_result(enzyme_dict, model, verbose))
    with open(output_filepath, "w") as f:
        f.writelines(result)
    reset_enzyme_and_pathway(enzyme_dict, pathway_dict)


def match_enzyme_existence(filepath: Union[str, Path],
                           enzyme_dict: Dict[int, Union[None, Enzyme]]):
    """
    Calculate scores (0 - 1) from the given model and count the number of
    enzymes that have the same function. The results are stored in Enzyme objects.

    Args:
        filepath: See parameter `filepath` in `start_match_enzyme`.
        enzyme_dict: See parameter `enzyme_dict` in `start_match_enzyme`.

    Steps
    -----
    1. Get "identity" value from best_blast results.
    2. Calculate scores from "identity".
    3. Group enzymes by "enzyme_id" and use the "probability framework" we
       established to calculate the "probability" that the enzymes with the same
       "enzyme_id" will function normally.
       .
       (i.e., the edge score is determined here to stand for the probability
        that the product can be synthesized from its reactant)
    4. Update the edge scores and enzyme counts to the Enzyme objects.
    """
    data = pd.read_csv(filepath, usecols=["enzyme_id", "identity"])
    data = data[data["enzyme_id"] != "-"]
    data["existence_score"] = existence_score_model(data["identity"])
    data = data.groupby("enzyme_id").agg(
        count=("enzyme_id", "count"),
        prob=("existence_score", lambda x: 1 - np.nanprod(1 - x))).reset_index()
    for _, (enzyme_id, count, prob) in data.iterrows():
        try:
            enzyme_id = int(enzyme_id)
            enzyme_dict[enzyme_id].set_count(count)
            enzyme_dict[enzyme_id].set_prob(prob)
        except (ValueError, AttributeError):
            pass


def traverse_enzyme_reaction(compound: PathwayNode,
                             enzyme_dict: Dict[int, Union[None, Enzyme]],
                             pathway_dict: Dict[int, PathwayNode]):
    """
    Traverse the pathway and determine the scores of the compounds by the
    "react" method in the PathwayNode object.

    Args:
        compound: A PathwayNode object containing compound info.
        enzyme_dict: See parameter `enzyme_dict` in `start_match_enzyme`.
        pathway_dict: See parameter `pathway_dict` in `start_match_enzyme`.
    """
    for enzyme in compound.next_enzyme:
        try:
            product = pathway_dict[enzyme_dict[enzyme].product]
            reactant = pathway_dict[enzyme_dict[enzyme].reactant]
            next_material = product.react(enzyme_dict[enzyme], reactant)
        except (KeyError, AttributeError):
            next_material = None
        if next_material is not None:
            traverse_enzyme_reaction(next_material, enzyme_dict, pathway_dict)


def get_pathway_result(pathway_dict: Dict[int, PathwayNode],
                       model: Literal["logistic", "binary"],
                       verbose: bool) -> List[str]:
    """
    Obtain scores (0 - 1) or existence (True / False) from Compound objects.

    The result can be printed to screen by setting `verbose` to true.

    Args:
        pathway_dict: See parameter `pathway_dict` in `start_match_enzyme`.
        model: See parameter `model` in `start_match_enzyme`.
        verbose: See parameter `verbose` in `start_match_enzyme`.

    Returns:
        A list of strings containing the pathway mapping result (compound part).
    """
    result_message = []
    if verbose:
        print("Compound list:")
    result_message.append("Compound list:\n")
    for pathwaynode in pathway_dict.values():
        compound = pathwaynode.name
        if model == "logistic":
            existence = np.round(pathwaynode.existence_prob, 6)
        elif model == "binary":
            existence = pathwaynode.visited
        else:
            raise NameError("Model name error")
        if verbose:
            print(f"{compound}: {existence}")
        result_message.append(f"{compound}: {existence}\n")
    if verbose:
        print()
    result_message.append("\n")

    return result_message


def get_enzyme_result(enzyme_dict: Dict[int, Union[None, Enzyme]],
                      model: Literal["logistic", "binary"],
                      verbose: bool) -> List[str]:
    """
    Obtain scores (0 - 1) or existence (True / False) from Enzyme objects.

    The result can be printed to screen by setting `verbose` to true.

    Args:
        enzyme_dict: See parameter `enzyme_dict` in `start_match_enzyme`.
        model: See parameter `model` in `start_match_enzyme`.
        verbose: See parameter `verbose` in `start_match_enzyme`.

    Returns:
        A list of strings containing the pathway mapping result (enzyme part).
    """
    result_message = []
    if verbose:
        print("Enzyme list:")
    result_message.append("Enzyme list:\n")
    for enzyme in enzyme_dict.values():
        try:
            enzyme_name = enzyme.name
            if model == "logistic":
                enzyme_existence = np.round(enzyme.prob, 6)
            elif model == "binary":
                enzyme_existence = enzyme.exist
            else:
                raise NameError("Model name error")
            if verbose:
                print(f"{enzyme_name}: {enzyme_existence}")
            result_message.append(f"{enzyme_name}: {enzyme_existence}\n")
        except AttributeError:
            pass

    return result_message


def reset_enzyme_and_pathway(enzyme_dict: Dict[int, Union[None, Enzyme]],
                             pathway_dict: Dict[int, PathwayNode]):
    """
    Reinitialize objects in the enzyme_list and pathway_list after pathway
    mapping.
    """
    for enzyme in enzyme_dict.values():
        try:
            enzyme.reset()
        except AttributeError:
            pass
    for pathway in pathway_dict.values():
        pathway.reset()
