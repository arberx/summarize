import preprocess
import click
import sys
from helpers import create_occurrences_dict
from centroid import centroid_scoring
import main
from evaluate import fileToText


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
        sen.tokens = preprocess.preprocess_text(sen.original)


def score_tf_sentences(sentences, article):
    """Calculates the scores for all sentences"""

    occurrences = create_occurrences_dict(article)

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


@click.command()
@click.option('--num_sentences', '-n', default=5, help='Number of sentences to return in summary')
@click.option('--weighting', '-w', default="tf", help='Weighting scheme to use. Options: tf term frequency, -p, -c centroid')
@click.argument('article_file')
def main(article_file, num_sentences, weighting):
    article = fileToText(article_file, 2) # the 2 option specifies the articleText directory
    main.main(article, num_sentences)

if __name__ == "__main__":
    main(sys.argv[1:])


# if __name__ == '__main__':

#     article = ""
#     with open(str(sys.argv[1:][0])) as f:
#         article = f.read()

#     sentences = create_sentences(article)
#     tokenize_sentences(sentences)

#     # Main algorithm to score
#     score_tf_sentences(sentences, article)
#     #centroid_scoring(article, sentences)

#     sorted_sentences = rank_sentences(sentences, 3)

#     for sen in sorted_sentences:
#         print("{}\n".format(sen.original))
