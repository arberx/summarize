#!/usr/bin/python

'''
Summarize application made for EECS486 Project 4
'''

import sys
import os
import re
import pprint
import operator
import flask
# import summarize
from summarize import app
from porterstemmer import PorterStemmer
from preprocess import stemwords, removeStopwords, removeSGML, tokenizeText


DIRECTORY = os.getcwd()


class Sentence(object):
    '''
    Class contains:
        original sentence (string)
        preprocessed list of tokens
        sentence score (float)
    '''
    def __init__(self, sentence, tokens, score):
        '''initalize members'''
        self.sentence = sentence
        self.tokens = tokens
        self.score = score


def main(args):
    '''Input is file that text we want to summarize'''
    with open(DIRECTORY + '/' + str(args[0]), 'r') as read_data:

        read_data = read_data.readlines()[0]

        # make a list of the sentences(currently doesn't take into account Mr.)
        sentences = re.findall("[A-Z].*?[\.!?]", read_data, re.MULTILINE | re.DOTALL )

        # uniq words dictionary
        uniqWords = {}
        tokens = tokenizeText(read_data)

        for tok in tokens:
            if tok not in uniqWords:
                uniqWords[tok] = 1
            else:
                uniqWords[tok] += 1

        finalList = []

        # list of Sentences
        for sentence in sentences:
            toks = tokenizeText(sentence)
            score = 0
            for token in toks:
                score += uniqWords[token]

            finalList.append(Sentence(sentence, toks, score))


        sortedList = sorted(finalList, key=operator.attrgetter('score'))

        for top in sortedList:
            print(top.sentence)


@app.route('/', methods=['GET', 'POST'])
def mainRoute():
    '''Main route for now'''
    return flask.render_template('summary.html')


if __name__ == '__main__':
    '''Run through the command line take in arguments'''
    # main(sys.argv[1:])
    main(['test.txt'])
