if __name__ == "__main__":
    import sys
    import pandas as pd
    from pathway import PathwayNode, Enzyme, PATHWAY_LIST, ENZYME_LIST
else:
    import pandas as pd
    from .pathway import PathwayNode, Enzyme, PATHWAY_LIST, ENZYME_LIST



def traverse_enzyme_reaction(material, enzyme_list, pathway_list):
    for enzyme in pathway_list[material].reaction:
        if enzyme_list[enzyme] is not None and enzyme_list[enzyme].exist:
            next_reaction = enzyme_list[enzyme].react(pathway_list)
            if next_reaction is not None:
                traverse_enzyme_reaction(next_reaction, enzyme_list, pathway_list)


def print_pathway(pathway_list):
    print("Compound list:")
    for pathwaynode in pathway_list.values():
        print(f"{pathwaynode.name}: {pathwaynode.visited}")


def print_enzyme(enzyme_list):
    print("Enzyme list:")
    for enzyme in enzyme_list.values():
        try:
            print(f"{enzyme.name}: {enzyme.count}")
        except AttributeError:
            pass


def match_enzyme_existence(filename, enzyme_list):
    data = pd.read_csv(filename, usecols=["enzyme_id"])
    data = data.groupby("enzyme_id").size().reset_index(name="count")
    for _, (enzyme_id, count) in data.iterrows():
        try:
            enzyme_id = int(enzyme_id)
            enzyme_list[enzyme_id].set_count(count)
        except ValueError:
            pass  # Note This is for int(): Remove this comment later
        except AttributeError:
            pass  # Note: This is for None.set_count: Remove this comment later


def run_match_enzyme(filename, enzyme_list=ENZYME_LIST, pathway_list=PATHWAY_LIST):
    match_enzyme_existence(filename, enzyme_list)
    traverse_enzyme_reaction(1, enzyme_list, pathway_list)
    print_pathway(pathway_list)
    print_enzyme(enzyme_list)


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Invalid arguments"
    filename = sys.argv[1]
    run_match_enzyme(filename)
