from preprocess import preprocess_text


def create_occurrences_dict(string):
    """Given a string, count occurences of preprocessed tokens."""

    # Keeps track of preprocessed tokens count
    occurrences = {}
    tokens = preprocess_text(string)

    # Count occurences of tokens in string
    for token in tokens:
        if token not in occurrences:
            occurrences[token] = 0
        occurrences[token] += 1

    return occurrences
