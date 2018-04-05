#!/usr/bin/env python
'''
Assignment 4 486

By: Arber Xhindoli uniqname: axhindol

Naive bayes Classifier.
'''

from os import getcwd, listdir
from pprint import pprint
from sys import argv
import datetime
import operator
from math import log
from random import randint
from porterstemmer import PorterStemmer
from threading import Thread, Lock

# punctuation that we want removed
PUNCTUATION = r"""!"#$%&()*+/:;<=>?@[\]^_`{|}~"""

'''
Some of the most common English contractions taken from
https://www.thoughtco.com/contractions-commonly-used-informal-english-1692651
'''
CONTR = {
    'I\'m': 'I am',
    'don\'t': 'do not',
    'didn\'t': 'did not',
    'we\'ll': 'we all',
    'can\'t': 'cannot',
    'I\'ve': 'I have',
    'hadn\'t': 'had not',
    'he\'s': 'he is',
    'she\'s': 'she is',
    'it\'s': 'it is',
    'there\'s': 'there is'
}
# List of stop words
LIST_OF_STOP = ['a', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be',
                'been', 'but', 'by', 'few', 'from', 'for', 'have', 'he', 'her',
                'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its',
                'many', 'me', 'my', 'none', 'of', 'on', 'or', 'our', 'she',
                'some', 'the', 'their', 'them', 'there', 'they', 'that',
                'this', 'to', 'us', 'was', 'what', 'when', 'where',
                'which', 'who', 'why', 'will', 'with', 'you', 'your']

# List contains the result of tokenized text
RETURN_LIST = []

# Directory of bestfriend files
DIRECTORY = getcwd()

# Number of documents
NUMDOCS = 0.0

# INDEX to skip
SKIPINDEX = 0

# TOKENS to files, dict of filename to tokenlist
TOKENFILE = {}

# CORRECT COUNT
CORRECTCOUNT = 0

'''
Dicitonary of dictionaries :
{
    category1 : {
                    word1 : count,
                },
    category2 : {
                    word1 : count
                }
}
'''
CATEGORYCOUNT = {}

UNIQWORDS = set()


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
    if word.endswith('\'s'):
        RETURN_LIST.append(word.split('\'')[0])


def check_contractions(word):
    '''checks if word has a contraction, if so, returns list of word'''
    '''check if possessive'''
    if word in CONTR.keys():
        if len(CONTR[word]) == 1:
            RETURN_LIST.append(CONTR[word].split(' '))
        else:
            RETURN_LIST.append(CONTR[word])


def check_period(word):
    '''checks if it has more than one period, if not, should be removed'''
    cCount = 0
    for char in word:
        if char == '.':
            cCount += 1

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
    '''Runs tests to tokenize words'''
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


def tokenizeText(text):
    '''Function tokenizes the text, returns list of these tokens'''
    # makes lower case, start tokenizing
    text = text.lower()
    no_new_line = text.replace('\n', ' ')
    token_list = no_new_line.split(' ')

    # remove emptyspaces
    token_list = filter(None, token_list)

    # removes certain PUNCTUATION
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

    # Uncomment below to remove stop words and stem
    # new_list = removeStopwords(new_list)
    # new_list = stemwords(new_list)
    return new_list


def removeStopwords(lis):
    '''removes stopwords'''
    return [x for x in lis if x not in LIST_OF_STOP]


def stemwords(lis):
    '''word stemmer'''
    porter_stemmer = PorterStemmer()
    end_list = []
    for word in lis:
        end_list.append(porter_stemmer.stem(word, 0, len(word) - 1))
    return end_list


def countWords(tokenText, category):
    """Counts uniq words, per category"""
    global CATEGORYCOUNT
    global UNIQWORDS

    categ = category

    # check category and update word count dicitonary
    if categ not in CATEGORYCOUNT.keys():
        CATEGORYCOUNT[categ] = {}

    for word in tokenText:
        if word not in CATEGORYCOUNT[categ].keys():
            CATEGORYCOUNT[categ][word] = 1
        else:
            CATEGORYCOUNT[categ][word] += 1

        UNIQWORDS.add(word)


def getStringCat(filename):
    """returns category from filename"""
    for i, s in enumerate(filename):
        if s.isdigit():
            return filename[:i]


def trainNaivebayes(fileNames):
    """This function is used to train on input filenames.
     Output is a dictionary with conditional probabilities/other parameters.
    """
    global CATEGORYCOUNT
    global UNIQWORDS
    global SKIPINDEX
    global TOKENFILE

    # clear dicitonaries for new Training session
    CATEGORYCOUNT.clear()
    UNIQWORDS.clear()

    # total word count in category
    wordCount = {}

    # class probabilites dictionary(will return)
    classProb = {}

    # open bestfriend files, start readin one by one, apply preprocess
    for ind, filename in enumerate(fileNames):

        # if the test file, skip using as training
        if ind == SKIPINDEX:
            # print("To skip: {}".format(filename))
            continue

        with open(DIRECTORY + '/' + filename, 'r') as read_data:

            if filename in TOKENFILE.keys():
                tokenText = TOKENFILE[filename]
            else:
                # pass to tokenizeText(function is ASSIGNMENT 2)
                tokenText = tokenizeText(read_data.read())
                TOKENFILE[filename] = tokenText

            # get category
            category = getStringCat(filename)

            # increment class count, total word count
            if category in classProb.keys():
                classProb[category] += 1.0
                wordCount[category] += len(tokenText)
            else:
                classProb[category] = 1.0
                wordCount[category] = len(tokenText)

            countWords(tokenText, category)

    # calculate class probabilites
    for category in classProb.keys():
        classProb[category] = float(classProb[category]) / (float(NUMDOCS))

    # create return dictionary with word conditional probabilites.
    for category in CATEGORYCOUNT.keys():
        # loop through all the UNIQWORDs, and calculate conditional probabilities
        for word in UNIQWORDS:
            tempVal = 0.0
            if word in CATEGORYCOUNT[category].keys():
                tempVal = CATEGORYCOUNT[category][word]
            # calculation of individual word category probabilty(addone smoothing)
            CATEGORYCOUNT[category][word] = float(tempVal + 1.0) / (float(wordCount[category]) + float(len(UNIQWORDS)))

    return classProb, CATEGORYCOUNT


def testNaiveBayes(testFile, classProb):
    """ Tests one file, input is a testfile, classProbabilties dictionary"""
    global CATEGORYCOUNT
    global CORRECTCOUNT

    maxCat = {}
    # open the testFile
    with open(DIRECTORY + '/' + testFile, 'r') as read_data:
        # pass to tokenizeText(function is ASSIGNMENT 2)
        tokenText = tokenizeText(read_data.read())
        for category in CATEGORYCOUNT.keys():

            # set the intial probabilty to 0(since addition because of log this is okay.)
            if category not in maxCat.keys():
                maxCat[category] = 0

            # add by the classProbability
            maxCat[category] += float(log(classProb[category], 10))
            for word in tokenText:
                if word in CATEGORYCOUNT[category].keys():
                    # multiple by probabilty of that word in the category
                    maxCat[category] += float(log(CATEGORYCOUNT[category][word], 10))

    category = getStringCat(testFile)

    # max finds the most probable one
    maxCatNum = max(maxCat.values())

    # reverse dictionary
    d2 = dict((v, k) for k, v in maxCat.iteritems())

    # increment count guess agrees
    if category == d2[maxCatNum]:
        CORRECTCOUNT += 1

    # return guessed category
    return d2[maxCatNum]


def main(args):
    """Main starts the preprocessing."""
    global DIRECTORY
    global NUMDOCS
    global SKIPINDEX
    global CORRECTCOUNT

    # add directory name
    DIRECTORY += str(args[0])

    # assign number of documents
    NUMDOCS = len(listdir(DIRECTORY))

    # dirctory list
    dctList = listdir(DIRECTORY)
    dctList = sorted(dctList)

    # file to write
    outputFile = open("naivebayes.output", "w")

    # loop through
    for ind in dctList:

        # train, result is multiple datastructures
        classProb, wordConditionalProb = trainNaivebayes(dctList)

        # test on SKIPINDEX file
        guessedCat = testNaiveBayes(dctList[SKIPINDEX], classProb)

        # print("to Test: {}".format(dctList[SKIPINDEX]))

        # write to file
        outputFile.write("{} {}\n".format(dctList[SKIPINDEX], guessedCat))

        # increment skipIndex
        SKIPINDEX += 1

    # print sorted order highest word conditional probabilities
    # dicts = wordConditionalProb['lie']
    # a1_sorted_keys = sorted(dicts, key=dicts.get, reverse=True)
    # i = 0
    # for r in a1_sorted_keys:
    #     if i > 9:
    #         break
    #     print "{}. {} : {}".format(i, r, dicts[r])
    #     i += 1

    print("Accuracy is {}".format(float(CORRECTCOUNT)/float(NUMDOCS)))

if __name__ == '__main__':
    """ Program arguments: filenames"""
    main(argv[1:])
    # main(['/bestfriend.deception/'])
