'''
Final Project EECS486

runTests.py
'''


import preprocess
import sys
from helpers import create_occurrences_dict
from centroid import centroid_scoring
from sumMary import create_sentences, tokenize_sentences, score_tf_sentences, rank_sentences
from probability import probability_scoring
import os


if __name__ == '__main__':
    files = os.listdir('../../summaries/articleTexts/')
    if ".DS_Store" in files:
		files.remove(".DS_Store")

    # index of article
    index = 0

    # probability(p), centroid(c) or regular tf(tf)
    for algo in ['tf', 'c', 'p']:
        for file in sorted(files):
            with open('../../summaries/articleTexts/'+file, 'r') as read_data:
                article = read_data.read()

                # run the summarizer
                sentences = create_sentences(article)
                tokenize_sentences(sentences)

                # Main algorithm to score
                if algo == 'tf':
                    score_tf_sentences(sentences, article)

                elif algo == 'p':
                    probability_scoring(sentences)

                else:
                    centroid_scoring(article, sentences)

                # write top five sentences
                sorted_sentences = rank_sentences(sentences, 5)

                # make file name
                fileName = file[0] + str(index % 10) + '_' + algo

                with open('../../summaries/evaluation/' + fileName, 'w+') as file:
                    for sen in sorted_sentences:
                        file.write("{}\n".format(sen.original))

                index += 1
