import preprocess
import sys
from helpers import create_occurrences_dict
from centroid import centroid_scoring
from sumMary import create_sentences, tokenize_sentences, score_tf_sentences, rank_sentences
import os


if __name__ == '__main__':
    files = os.listdir('../../summaries/articleTexts/')
    # print(sorted(files))

    # index of article
    index = 0

    # centroid(c) or regular tf(tf)
    for algo in ['tf', 'c']:
        for file in sorted(files):
            with open('../../summaries/articleTexts/'+file, 'r') as read_data:
                article = read_data.read()

                # run the summarizer
                sentences = create_sentences(article)
                tokenize_sentences(sentences)

                # Main algorithm to score
                if algo == 'tf':
                    score_tf_sentences(sentences, article)
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
