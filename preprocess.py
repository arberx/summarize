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

# punctuation that we want removed
PUNCTUATION = r"""!"#$%&()*+/:;<=>?@[\]^_`{|}~"""

'''
Some of the most common English contractions taken from https://www.thoughtco.com/contractions-commonly-used-informal-english-1692651
'''
CONTR = {
    'I\'m' : 'I am',
    'don\'t' : 'do not',
    'didn\'t' : 'did not',
    'we\'ll' : 'we all',
    'can\'t' : 'cannot',
    'I\'ve' : 'I have',
    'hadn\'t' : 'had not',
    'he\'s' : 'he is',
    'she\'s' : 'she is',
    'it\'s' : 'it is',
    'there\'s' : 'there is' 
}

# List of stop words
LIST_OF_STOP = ['a', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'been', 'but', 'by', 'few', 'from', 'for', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its', 'many', 'me', 'my', 'none', 'of', 'on', 'or', 'our', 'she', 'some', 'the', 'their', 'them', 'there', 'they', 'that', 'this', 'to', 'us', 'was', 'what', 'when', 'where', 'which', 'who', 'why', 'will', 'with', 'you', 'your']

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
        # print("isNum: {}".format(word))
        RETURN_LIST.append(word)
        return RETURN_LIST

    if check_if_date(word):
        # print("isDate: {}".format(word))
        RETURN_LIST.append(word)
        return RETURN_LIST

    if check_if_hyphen(word):
        # print("ishyphen: {}".format(word))
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
            new_list.append(item)

    # finally remove stray "" from list
    while '' in new_list:
        new_list.remove('')

    # print(new_list)
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
    return end_list

def compute(files):
    '''returns total_num, and unique'''

    end_list = []
    tot_words = 0
    uniq_words = {}
    num_uniq = 0

    for filename in files:
        with open(DIRECTORY + '/' + filename, 'r') as read_data:
            # pass the entire contents of the file, and write
            no_SGML = removeSGML(read_data.read())

            # pass to tokenizeText
            token_text = tokenizeText(no_SGML)

            # pass to remove stopwords
            no_stop = removeStopwords(token_text)

            # stemmer
            complete = stemwords(no_stop)
            
            # print("Endlist: ", complete)
            # append to end_list
            end_list += complete

    tot_words = len(end_list)

    # unique words
    for i in end_list:
        if i not in uniq_words.keys():
            uniq_words[i] = 1
        else:
            uniq_words[i] += 1
        
    # num uniq 
    num_uniq = len(uniq_words.keys())

    return tot_words, num_uniq, uniq_words

if __name__ == '__main__':

    # assign directory
    DIRECTORY = os.getcwd() + str(sys.argv[1])

    # get total, and uniq values
    tot_words, num_uniq, uniq_words = compute(os.listdir(DIRECTORY))

    print("Words {}".format(tot_words))
    print("Vocabulary {}".format(num_uniq))

    # # sort dict in acsending order
    sorted_dict = sorted(uniq_words.items(), key=operator.itemgetter(1), reverse=True)

    # print top 50:
    print("Top 50 words")
    for i in range(0,50):
        print(sorted_dict[i])

    # proportion accounting for 25%
    proportion = 0.25
    maxi = proportion * tot_words

    curr_tot = 0
    for n_min, key in enumerate(sorted_dict):
        curr_tot += key[1]
        if curr_tot > maxi:
            n_min += 1
            break

    print ("The minimum unique words accounting for {} of total number of words is {}".format (proportion,n_min))    

    # compute betaK from random sample
    # partion files in directory randomly, pick 200 files and 900 files
    l1 = []
    l2 = []

    while (len(l1) != 200 and len(l2) != 900):
        i = randint(0,1399)
        j = randint(0,1399)
        l1.append(os.listdir(DIRECTORY)[i])
        l2.append(os.listdir(DIRECTORY)[j])

    # calculate values
    n1, v1, uniq_words = compute(l1)
    n2, v2, uniq_words = compute(l2)

    # n is total words, v is vocab
    beta = (math.log(v1) - math.log(v2)) / float(math.log(n1) - math.log(n2))
    k = float(v1) / n1**beta

    print "K value is:    {}".format(k)
    print "beta value is: {}".format(beta)

    # use these values to compute Vocab size if corpus was increased
    for i in [1000000, 1000000000]:
        print "Predicted vocab size for {} is {}".format(i, k*i**beta)
