#!/usr/bin/python

'''
Assignment 1 For EECS 486
Author: Arber Xhindoli
'''

import sys
import re
import os
import datetime
import operator
import math
from random import randint
from porterstemmer import PorterStemmer
from collections import deque

# punctuation that we want removed
PUNCTUATION = r"""!"#$%&()*+/:;<=>?@[\]^_`{|}~"""

# https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
CONTR = {"she'll": "she will", "don't": "do not", "should've": "should have", "won't": "will not", "that'll": "that will", "daren't": "dare not", "he's": "he is", "when's": "when is", "we've": "we have", "he'd": "he would", "ma'am": "madam", "daresn't": "dare not", "haven't": "have not", "cain't": "cannot", "'tis": "it is", "who's": "who is", "gonna": "going to", "they'd": "they would", "oughtn't": "ought not", "I'd": "I would", "you've": "youhave", "I'm": "I am", "these're": "these are", "who'd": "who would", "those're": "those are", "we'll": "we will", "mayn't": "may not", "they've": "they have", "somebody's": "somebody is", "could've": "could have", "what've": "what have", "who'd've": "who would have", "mustn't": "must not", "isn't": "is not", "it'll": "it will", "y'all": "you all", "why's": "why is", "you'd": "you would", "we'd": "we would", "why'd": "why did", "this's": "this is", "shan't": "shall not", "there'd": "there would", "ne'er": "never", "needn't": "need not", "o'clock": "of the clock", "why're": "why are", "there's": "there is", "shouldn't": "should not", "they'll": "they will", "mightn't": "might not", "ol'": "old", "who're": "who are", "may've": "may have", "what'll": "what will", "hadn't": "had not", "aren't": "are not", "something's": "something is", "wouldn't": "would not", "amn't": "am not", "weren't": "were not", "would've": "would have", "someone's": "someone is", "we'd've": "we would have", "can't": "cannot", "dasn't": "dare not", "which's": "which is", "couldn't": "could not", "how'll": "how will", "I'm'a": "I am going to", "doesn't": "does not", "how's": "how is", "I've": "I have", "it's": "it is", "how'd": "how did", "there're": "there are", "we're": "we are", "it'd": "it would", "what're": "what are", "what's": "what is", "ain't": "is not", "who'll": "who will", "what'd": "what did", "must've": "must have", "I'll": "I will", "they're": "they are", "o'er": "over", "wasn't": "was not", "gotta": "got to", "hasn't": "has not", "where're": "where are", "e'er": "ever", "that're": "that are", "didn't": "did not", "where've": "where have", "let's": "let us", "'twas": "it was", "you're": "you are", "who've": "who have", "where'd": "where did", "where's": "where is", "might've": "might have", "he'll": "he will", "that'd": "that would", "she'd": "she would", "you'll": "you will", "she's": "she is", "that's": "that is"}

# List of stop words
LIST_OF_STOP = ['a', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'been', 'but', 'by', 'few', 'from', 'for', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its', 'many', 'me', 'my', 'none', 'of', 'on', 'or', 'our', 'she', 'some', 'the', 'their', 'them', 'there', 'they', 'that', 'this', 'to', 'us', 'was', 'what', 'when', 'where', 'which', 'who', 'why', 'will', 'with', 'you', 'your']

# Many more stopwords. can choose between the two
with open("stopwords.txt") as stop_words_file:
    LIST_OF_STOP = stop_words_file.read().split()

# Punctiation to consider to be the end of a sentence
STOP_PUNCTUATION = ['.']

# Blacklist of words that have periods in them
BLACK_LIST_WORDS = ["u.s.a.", "u.s.", "col.", "mr.", "mrs.", "ms.", "prof.", "dr.", "gen.", "rep.", "sen.", "st.", "sr.", "jr.", "ph.", "ph.d.", "m.d.", "b.a.", "m.a.", "d.d.", "d.d.s." "b.c.", "a.m.", "p.m.", "a.d.", "b.c.e.", "c.e.", "i.e.", "etc.", "e.g.", "al."]
    
RETURN_LIST = []

DIRECTORY = ''

def check_if_num(word):
    '''check if num'''
    try:
        float(word)
        return True
    except ValueError:
        return False

def check_if_date(word):
    '''check date'''
    if isinstance(word, datetime.date):
        return True
    else:
        return False

def check_if_hyphen(word):
    '''check hypen only in certain cases'''
    h_count = 0
    for let in word:
        if let == '-':
            h_count += 1

    # more detail
    if h_count == 1 or h_count == 2 and \
       word[0] != '-' and word[len(word)-1] != '-':
        return True
    return False

def check_posessive(word):
    '''check if possessive'''
    if word.endswith('\'s'):
        RETURN_LIST.append(word.split('\'')[0])

def check_contractions(word):
    '''checks if word has a contraction, if so, returns list of word'''
    if word in CONTR.keys():
        RETURN_LIST.append(CONTR[word].split(' '))

def check_period(word):
    '''checks if it has more than one period, if not, should be removed'''
    cCount = 0
    for char in word:
        if char == '.':
            cCount +=1
    
    if cCount == 0:
        return

    elif cCount == 1:
        RETURN_LIST.append(word.split('.')[0])

    else:
        if word[0] == '.' and word[len(word)-1] != '.':
            RETURN_LIST.append(word.split('.')[1])
        elif word[len(word)-1] == '.':
            RETURN_LIST.append(word.split('.')[0])
        else:
            return

def run_Tests(word):

    # clear list every run
    del RETURN_LIST[:]

    if check_if_num(word):
        # don't tokenize numbers
        RETURN_LIST.append(word)
        return RETURN_LIST

    if check_if_date(word):
        RETURN_LIST.append(word)
        return RETURN_LIST

    if check_if_hyphen(word):
        # has hyphen don't tokenize
        RETURN_LIST.append(word)
        return RETURN_LIST
    
    check_posessive(word)
    check_contractions(word)
    check_period(word)

    if RETURN_LIST:
        return RETURN_LIST
    else:
        # final check to remove uneccessary punctuation
        RETURN_LIST.append(''.join(ch for ch in word if ch not in PUNCTUATION))
        return RETURN_LIST


def removeSGML(text):
    '''Function removes SGML tags, replaces them with empty spaces'''
    return re.sub(re.compile('<.*?>'), '', text)

def tokenizeText(text):
    '''Function tokenizes the text, returns list of these tokens'''
    # makes lower case, start tokenizing
    text = text.lower()
    no_new_line = text.replace('\n', ' ')
    token_list = no_new_line.split(' ')

    # remove emptyspaces
    token_list = filter(None, token_list)

    #removes certain PUNCTUATION
    new_list = []    
    for it in token_list:
        new_list.append(''.join(ch for ch in it if ch not in PUNCTUATION))

    token_list = new_list

    # begin the process of tokenizing, by specifics specified in spec
    new_list = []
    for word in token_list:
        lis = run_Tests(word)
        for item in lis:
            new_list.extend(item)

    # finally remove stray "" from list
    while '' in new_list:
        new_list.remove('')

    return new_list

def removeStopwords(lis):
    '''removes stopwords'''
    # remove stop words list
    return [x for x in lis if x not in LIST_OF_STOP]

def stemwords(lis):
    '''word stemmer'''
    porter_stemmer = PorterStemmer()
    end_list = []
    for word in lis:
        end_list.append(porter_stemmer.stem(word, 0, len(word) - 1))
    return 
    
def split_into_sentences(string):
    """Given a string, split it into sentences."""

    # output, a list of strings representing sentences
    sentences = []

    # keeps track of the start of the current sentence
    sentence_start = 0

    # keeps track of quotes in a sentence to help keep them together
    quotes = deque()

    words = string.split()
    for i, word in enumerate(words):

        # Check for quotes to help keep words together        
        if '"' in word:
            if word.count('"') == 1:
                if quotes and quotes[-1] == '"':
                    quotes.pop()
                else:
                    quotes.append('"')

        # If none of the stop puncation characters are found at the end of the word, go to next word
        # In case you want sentences to end after words like end." (with the quotes in there as well)
        """or (len(word) > 1 and char == word[-2] and '"' == word[-1])"""
        if not any(char == word[-1]  for char in STOP_PUNCTUATION):
            continue

        # Check if word is in blacklist
        if word.lower() in BLACK_LIST_WORDS:
            continue

        # Check if next token starts with a capital
        if i != len(words) - 1 and words[i + 1][0].islower():
            continue

        # If the sentence is in the middle of a quoted phrase, keep going
        if quotes:
            continue
        
        # this token is likely to be the end of the sentence.
        sentences.append(" ".join(words[sentence_start:i + 1]))
        sentence_start = i + 1

    return sentences
    