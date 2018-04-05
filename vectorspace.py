#!/usr/bin/env python
'''
Assignment 2 for EECS486
Author: Arber Xhindoli, uniqname: axhindol
'''
import sys
import math
import os
import pprint
import numpy
import operator
from preprocess import removeSGML, tokenizeText, removeStopwords, stemwords

DIRECTORY = os.getcwd() + '/'
DOCID = 1
'''
Gold standard is a dictionary From:
query : set(DOCID)
''' 
GOLD_STANDARD = {}

# TOP DOCUMENTS DICT
# holds 10, 50, 100, 500 precision and recall lists
TOP_LIST = { 10 : [],
             50 : [],
             100: [],
             500: [] }


def indexDocument(docText, docW, queryW, iIndex):
    """ Takes in 4 inputs, creates inverted index """

    global DOCID

    # apply Project 1 tokenizing funcitons
    docText = applyPreProccess(docText.read())

    iIndex[2][DOCID] = {}

    '''
    1) Loop through and count all occurances of word for this docid
    2) Count number of docs that contain this word
    3) DOCID: { word: tf}
    '''
    for word in docText:

        # create word to DOCID, tf 
        if word not in iIndex[0].keys():
            iIndex[0][word] = {DOCID : 1}

        elif DOCID not in iIndex[0][word].keys():
             iIndex[0][word][DOCID] = 1
        
        else:
            iIndex[0][word][DOCID] += 1

        # add DOCID for word(only add if not seen)
        if word not in iIndex[1].keys():
            iIndex[1][word] = [DOCID]
        else:
             if iIndex[1][word][-1] != DOCID:
                iIndex[1][word].append(DOCID)
        
        # DOCID to word frequency
        if word not in iIndex[2][DOCID].keys():
            iIndex[2][DOCID][word] = 1

        else:
            iIndex[2][DOCID][word] += 1
    
    DOCID += 1

def retrieveDocuments(query, iIndex, docW, queryW):
    """ 
        Takes in 4 inputs, calculates simscore
        Output is DOCID : SIMSCORE

        Two weighting schemes supported:
        tfidf and bfx bfx
    """

    # apply Project 1 tokenizing funcitons
    query = applyPreProccess(query)
    query_num = query[0] 

    # remove the line number
    del query[0]

    # set of documents 
    common_docs = set()

    # dictionary of query idf values
    idf_query = {}

    '''
    Determine the set of documents that that 
    include at least one token from the query
    Also calculate idf for query term
    '''
    for word in query:
        if str(word) in iIndex[1].keys():
            for i in iIndex[1][str(word)]:
                common_docs.add(i)
        if word not in idf_query.keys():
            idf_query[word] = calculateIDF(word, iIndex)

    # make query vector
    query_vec_weighted = []
    
    for word in query:
        # account for different weighting schemes
        if queryW == 'tfidf':
            temp = query.count(word)
        else:
            temp = 1.0
        query_vec_weighted.append(float(temp) * float(idf_query[word]))

    # make document vectors
    doc_vector_list = {}

    for doc in common_docs:
        doc_vector_list[doc] = []
        for word in query:
            if word in iIndex[2][doc].keys():
                # take into account different weighting schemes
                if docW == 'tfidf':
                    temp = float(iIndex[2][doc][word])
                else:
                    temp = 1.0
                doc_vector_list[doc].append(temp * float(idf_query[word]))
            else:
                doc_vector_list[doc].append(0)

    # loop through take the dot product of the vectors
    res_dict = {}   
    for docid in doc_vector_list.keys():
        dj = doc_vector_list[docid]
        di = query_vec_weighted
        djn = numpy.array(dj)
        din = numpy.array(di)

        # normalized sim score
        norm_score = numpy.dot(dj, di) / (numpy.sqrt(djn.dot(djn)) * numpy.sqrt(din.dot(din)))

        # no similarity, don't include score
        if norm_score == 0:
            continue
        else:
            res_dict[docid] = norm_score    

    return sorted(res_dict.items(), key=operator.itemgetter(1), reverse=True), query_num

def main(args):
    """ Main function that runs the program"""

    docWeight = args[0]
    queryWeight = args[1]
    inputDir = args[2]
    testQuery = args[3]

    # create gold standard
    makeGoldStandard()

    '''
    List of dictionaries
    First entry will be a dictionary word to {docid: tf}
    Second entry will be dictionary of word to list of docid's it appears in
    Third entry will be dictionary from DOCID to {word: tf}
    '''
    iIndex = [{},{},{}]

    # loop through all files in Crain data set
    for filename in sorted(os.listdir(DIRECTORY + str(inputDir))):
         with open(DIRECTORY + str(inputDir) + '/' + filename, 'r') as read_data:
             indexDocument(read_data, docWeight, queryWeight, iIndex)

    output_file = open(DIRECTORY + 'cranfield.'+docWeight+'.'+queryWeight+'.ouput', 'w+')
    # open query file, and run retreive documents
    with open(DIRECTORY + testQuery, 'r') as read_data:
        # split by newline
        listOfQuery = filter(None,read_data.read().split('\n'))
        # loop through all queries and compute similarity
        for query in listOfQuery:
            result, query_num = retrieveDocuments(query, iIndex, docWeight, queryWeight)

            # # # write to output file
            for docid, freq in result:
                output_file.write("{} {} {}\n".format(query_num,docid,freq))

            # # # calculate and store precision and recall for query
            calculateRP(result,query_num)

    printMACRO(len(listOfQuery))

def applyPreProccess(text_items):
    '''take in text items, return preprocessed token list'''
    # pass the entire contents of the file, and write
    no_SGML = removeSGML(text_items)

    # pass to tokenizeText
    token_text = tokenizeText(no_SGML)

    # pass to remove stopwords
    no_stop = removeStopwords(token_text)

    # stemmer
    complete = stemwords(no_stop)

    return complete

def calculateIDF(word, iIndex):
    """ Calculate IDF values"""
    global DOCID

    if word in iIndex[1].keys():
        temp = len(iIndex[1][word])
        return math.log(float(DOCID) / (temp))
    return 0

def calculateRP(result, query_num):
    """ takes in result, and sorted tuple docid, freq """
    global TOP_LIST
    global GOLD_STANDARD

    for TOP in TOP_LIST.keys():
        w = 0
        y = 0
        count = 0
        # calculate Precision for this query
        while (count < TOP) and (count < len(result)):
            if str(result[count][0]) in GOLD_STANDARD[query_num]:
                w += 1
            else:
                y += 1
            count += 1

        # LIST OF [PRECISION, RECALL]
        temp_list = []
        temp_list.append(float(w)/float((y+w)))
        temp_list.append(float(w)/float(len(GOLD_STANDARD[query_num])))

        TOP_LIST[TOP].append(temp_list)

def printMACRO(totQuerys):
    """ prints macro average of precision and recall """    
    global TOP_LIST

    for TOP in sorted(TOP_LIST.keys()):
        PRECISION = 0.0
        RECALL = 0.0
        for i in TOP_LIST[TOP]:
            PRECISION += i[0]
            RECALL += i[1]

        print "Top {} Documents: PRECISION = {} , RECALL = {}".format(TOP, float(PRECISION)/float(totQuerys), float(RECALL)/float(totQuerys) )

def makeGoldStandard():
    """ Make gold standard set from reljudge """
    global GOLD_STANDARD
    
    with open(DIRECTORY + 'cranfield.reljudge') as read_data:
        listOfQuery = filter(None,read_data.read().split('\n'))
        for l_s in listOfQuery:
            l_s = l_s.split(' ')
            if l_s[0] not in GOLD_STANDARD.keys():
                GOLD_STANDARD[l_s[0]] = set()

            GOLD_STANDARD[l_s[0]].add(l_s[1])

if __name__ == "__main__":
    '''
    Two weighting schemes:
    tfidf and classic idf scheme: bfx*bfx
    '''
    main(sys.argv[1:])