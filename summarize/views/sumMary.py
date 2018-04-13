
import preprocess
import sys


class Sentence:
    """Sentence class to help keep track of sentences and their properties"""
    def __init__(self, original_sentence, orig_order):
        self.original = original_sentence
        self.tokens = []
        self.score = 0.0
        self.order = orig_order

def create_sentences(article):
    """Creates a list of sentences representing the article"""
    sentences = []
    original_sentences = preprocess.split_into_sentences(article)
    for i, sen in enumerate(original_sentences):
        sentences.append(Sentence(sen, i))

    return sentences


def tokenize_sentences(sentences):
    """Tokenizes sentences using Preprocessor"""
    for sen in sentences:
        sen.tokens = preprocess.tokenizeText(sen.original)


def sum_scores(sentences, article):
    """Calculates the scores for all sentences"""

    # Records occurences of tokens in text
    occurrences = {}
    tokens = preprocess.tokenizeText(article)

    # Calculate occurences of tokens in text
    for token in tokens:
        if token not in occurrences:
            occurrences[token] = 0
        occurrences[token] += 1

    for sentence in sentences:
        score = 0.0
        for token in sentence.tokens:
            score += occurrences[token]

        # Normalize score with the length of the sentences
        score /= len(sentence.tokens)
        sentence.score = score


def rank_sentences(sentences, k):
    """Returns a list of the top k ranked sentences in descending order."""
    sorted_sens = sorted(sentences, key=lambda sen: sen.score, reverse=True)[:k]

    # Sort by order of appearence in document
    return sorted(sorted_sens, key=lambda sen: sen.order)


if __name__ == '__main__':

    article = ""
    with open(str(sys.argv[1:][0])) as f:
        article = f.read()

    sentences = create_sentences(article)
    tokenize_sentences(sentences)
    sum_scores(sentences, article)
    sorted_sentences = rank_sentences(sentences, 3)

    for sen in sorted_sentences:
        print("{}\n".format(sen.original))
