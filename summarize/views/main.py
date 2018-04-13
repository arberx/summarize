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
from sumMary import create_sentences, tokenize_sentences, sum_scores, rank_sentences
from porterstemmer import PorterStemmer
from preprocess import stemwords, removeStopwords, removeSGML, tokenizeText


def main(article):
    '''Input is file that text we want to summarize'''

    sentences = create_sentences(article)

    tokenize_sentences(sentences)

    sum_scores(sentences, article)

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

        context['returnList'] = main(text)

    return flask.render_template('summary.html', context=context)


if __name__ == '__main__':
    '''Run through the command line take in arguments'''
