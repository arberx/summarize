#!/usr/bin/env python
'''
Assignment 3 486

By: Arber Xhindoli uniqname: axhindol

pagerank.py
'''
from os import getcwd, path
from sys import argv
import operator
from pprint import pprint

# current working directory
DIRECTORY = getcwd() + '/'

# dict of page with initail value
pageRank = {}

# list_of_urls
pageRankUrl = []

# dictionary of source to list of urls
point_to = {}

# dictionary of url to list of urls that point to key
pointed_to_by = {}

# CRAWLER OUTPUT
CRAWLER_OUT = ''

# OPTIONAL PAGERANK FILE
OPTIONAL_FILE = ''

# convergence value **gets read in
CONV = 0.0

# inital PAGERANK
INITAL_PR = 0.25

def make_intial():
    '''makes inital dictionaries'''
    global pageRank
    global point_to
    global pointed_to_by
    global pageRankUrl
    global INITAL_PR

    with open(DIRECTORY + CRAWLER_OUT, 'r') as read_data:
        for line in read_data:
            pageRankUrl.append(line.rstrip('\n'))
            pageRank[line.rstrip('\n')] = INITAL_PR
    
    with open(DIRECTORY + OPTIONAL_FILE, 'r') as read_data:
        for line in read_data:
            line = line.rstrip('\n')
            source, url = line.split(',')
        
            if source not in point_to.keys():
                point_to[source] = [url]
            else:
                if url not in point_to[source]:
                    point_to[source].append(url)
            
            if url not in pointed_to_by.keys():
                pointed_to_by[url] = [source]

            else:
                if source not in pointed_to_by[url]:
                    pointed_to_by[url].append(source)

def check_diff(newPageDict):
    '''Function checks that the difference between new and old page rank is less than specified val'''
    global pageRank
    global pageRankUrl
    global CONV

    # loop through, if diff is <= to passed in value, return true, else return false
    for page in pageRankUrl:
        # if the difference is less than conv, continue calculating
        if abs(pageRank[page] - newPageDict[page]) > CONV:
            return False 
    return True

def calculatePageRank():
    '''calculates the pagerank of the 2000 unique links'''
    global pageRank
    global point_to
    global pointed_to_by
    global pageRankUrl
    
    # Damping factor
    D = 0.85
    D_N = (1 - D)/len(pageRankUrl)
    num_iter = 1

    # PageRank formula = (1-d)/N + d*(SUM(PR(Si)/outgoing))
    while True:
        num_iter += 1
        # new pageRank dict for round
        newPageRank = {}

        # loop through all unique links
        for page in pageRankUrl:
            sum_D = float(0.0)
            # loop through each url that points to this page
            for url in pointed_to_by[page]:
                # no self pointing links
                if page == url:
                    continue

                # get this url's pagerank
                url_pgR = float(pageRank[url])

                # divide this value by number of other urls it points too
                final_PR = float(url_pgR) / float(len(point_to[url]))

                # add to sum for this page
                sum_D += final_PR

            # after update this pages pagerank
            newPageRank[page] = D_N + D * sum_D 

        # after we have updated every pages pagerank, check that values are not less than convergence factor
        # if so then break
        if check_diff(newPageRank):
            pageRank = newPageRank
            break
        
        pageRank = newPageRank

    # reverse sorted order
    sorted_dict = sorted(pageRank.items(), key=operator.itemgetter(1), reverse=True)
    op_out = open( DIRECTORY + 'pagerank.output', 'w+')

    # write to output file
    for url,val in sorted_dict:
        op_out.write("{} {}\n".format(url,val))

def main(args):
    '''runs the main program'''
    global CRAWLER_OUT
    global CONV
    global OPTIONAL_FILE

    # reads crawler output name and convergence value
    CRAWLER_OUT = args[0]
    CONV = float(args[1])

    # optional pagerank output(which my program uses)
    OPTIONAL_FILE = args[2]
    
    # sets up dictionaries in order to calculate pageRank efficently
    make_intial()

    # calculate pageRank
    calculatePageRank()

if __name__ == '__main__':
    '''Main runs pagerank'''
    main(argv[1:])
