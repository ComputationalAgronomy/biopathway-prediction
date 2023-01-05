import re

from .database_utils import split_fasta

REGEX_FRAGMENT = re.compile(r"\(Fragment\)")


def filter_partial_sequence(file):
    entries = split_fasta(file)
    entry_title = [entry[0] for entry in entries]
    entry_sequence = [entry[1] for entry in entries]
    non_fragment_sequence = []
    for index, element in enumerate(entry_title):
        if REGEX_FRAGMENT.search(element) is None:
            non_fragment_sequence.append(index)

    result = [[entry_title[i], entry_sequence[i]]
              for i in non_fragment_sequence]
    print(f"Fragment entries: {len(entry_title) - len(non_fragment_sequence)}\n" \
          f"Total entries: {len(entry_title)}")

    return result
