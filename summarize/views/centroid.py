from helpers import create_occurrences_dict
import math

def create_optimal_sentence(article, k):
    """Create the optimal sentence using the k optimal words."""

    occurrences = create_occurrences_dict(article)

    # Get the top k tokens
    top_k_tokens = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)[:k]

    # Create a list of the top tokens
    top_tokens = []

    for word, _ in top_k_tokens:
        top_tokens.append(word)

    return top_tokens

def centroid_scoring(article, sentences):
    """Calculates cosine similarity for sentences against an optimal sentence."""

    num_words_for_optimal_sen = 14

    # Create the optimal sentence
    optimal_sentence = create_optimal_sentence(article, num_words_for_optimal_sen)

    for sentence in sentences:

        # Find token counts of sentences
        sentence_token_occurrences = {}
        for token in sentence.tokens:

            if token not in sentence_token_occurrences:
                sentence_token_occurrences[token] = 0
            sentence_token_occurrences[token] += 1

        # calculate dot product
        dot_product_of_sentences = 0.0
        for token in optimal_sentence:

            if token not in sentence_token_occurrences:
                continue

            dot_product_of_sentences += sentence_token_occurrences[token]

        # Calculate length of sentence vector
        sentence_length = 0.0
        for token in sentence_token_occurrences:
            sentence_length += (sentence_token_occurrences[token] ** 2)
        sentence_length = math.sqrt(sentence_length)

        # Length of optimal sentence
        # Each weight is one, so no need to sum squares
        optimal_sentence_length = math.sqrt(len(optimal_sentence))

        # Calculate cosign similarity
        if sentence_length != 0:
            sentence.score = dot_product_of_sentences / (optimal_sentence_length * sentence_length)
        else:
            sentence.score = 0.0
