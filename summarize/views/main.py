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
from summarize import app
from sumMary import create_sentences, tokenize_sentences, rank_sentences,\
    score_tf_sentences, centroid_scoring, probability_scoring

from porterstemmer import PorterStemmer
from preprocess import removeStopwords, removeSGML, tokenizeText


def main(article):
    '''Input is file that text we want to summarize'''

    sentences = create_sentences(article)

    tokenize_sentences(sentences)

    score_tf_sentences(sentences, article)

    sorted_sentences = rank_sentences(sentences, 10)

    return sorted_sentences


@app.route('/', methods=['GET', 'POST'])
def mainRoute():
    '''Main route for summary'''

    if flask.request.method == 'GET':
        context = {
            'type': True
        }
        return flask.render_template('summary.html', context=context)

    return 'Error'


@app.route('/submit', methods=['GET', 'POST'])
def submit():

    context = {
        'type': False
    }

    if flask.request.method == 'POST':

        # get the form contents
        text = flask.request.form['summary']

        # get option type
        option = flask.request.form['tf']

        sentences = create_sentences(text)
        tokenize_sentences(sentences)

        print(flask.request.form['tf'])

        if option == 'tf':
            score_tf_sentences(sentences, text)
        elif option == 'c':
            centroid_scoring(text, sentences)
        elif option == 'p':
            probability_scoring(text)

        # return the top five ranked sentences
        context['returnList'] = rank_sentences(sentences, 5)
        context['originalText'] = text

    return flask.render_template('summary.html', context=context)


if __name__ == '__main__':
    '''Run through the command line take in arguments'''
