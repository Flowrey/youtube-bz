"""
This is a Python implementation of the levenshtein distance.
Levenshtein distance is a string metric for measuring the
difference between two sequences.

For doctests run following command:
python -m doctest -v levenshtein-distance.py
or
python3 -m doctest -v levenshtein-distance.py

For manual testing run:
python levenshtein-distance.py

This code came from: https://github.com/TheAlgorithms/Python
"""


def levenshtein_distance(first_word: str, second_word: str) -> int:
    """Implementation of the levenshtein distance in Python.
    :param first_word: the first word to measure the difference.
    :param second_word: the second word to measure the difference.
    :return: the levenshtein distance between the two words.
    Examples:
    >>> levenshtein_distance("planet", "planetary")
    3
    >>> levenshtein_distance("", "test")
    4
    >>> levenshtein_distance("book", "back")
    2
    >>> levenshtein_distance("book", "book")
    0
    >>> levenshtein_distance("test", "")
    4
    >>> levenshtein_distance("", "")
    0
    >>> levenshtein_distance("orchestration", "container")
    10
    """
    # The longer word should come first
    if len(first_word) < len(second_word):
        return levenshtein_distance(second_word, first_word)

    if len(second_word) == 0:
        return len(first_word)

    previous_row = list(range(len(second_word) + 1))

    for i, c1 in enumerate(first_word):
        current_row = [i + 1]

        for j, c2 in enumerate(second_word):
            # Calculate insertions, deletions and substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            # Get the minimum to append to the current row
            current_row.append(min(insertions, deletions, substitutions))

        # Store the previous row
        previous_row = current_row

    # Returns the last element (distance)
    return previous_row[-1]
