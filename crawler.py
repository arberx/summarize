#!/usr/bin/env python
'''
Assignment 3 486

By: Arber Xhindoli uniqname: axhindol

Runs in about 3.5-4 minutes without creating optional.output
'''
from sys import argv
from requests import get
from pprint import pprint
from os import getcwd, path
from urlparse import urlparse, parse_qs, urljoin
from lxml import html
import requests

# current working directory
DIRECTORY = getcwd() + '/'

# urlList will be a queue of url's that need to be visited
urlList = []

# urlSet will be a set of url's visited
urlSet = set()

# contains source_url, url pairs
sourceUrl = []

# Number of links passed in
NUM_LINKS = 0

def check_url(source, url_to_check):
    """series of checks that make sure we stay within umich domain"""
    global urlSet
    global urlList

    # pass to urlparse, to get domain, check if part of eecs.umich domain
    parsed_uri = urlparse( url_to_check )

    temp_set = set(parsed_uri.netloc.split('.'))

    if ('eecs' not in temp_set) or ('umich' not in temp_set):
        return False

    url = url_to_check.replace("http://", "")
    url = url.replace("www.", "")

    # check for file extension is not .jpg, .pdf
    ext = path.splitext(parsed_uri.path)[1]

    if (url in urlSet) or (url in urlList):
        sourceUrl.append((source, url))
        return False

    if ext == '.jpg' or ext == '.pdf':
        return False

    return True


def main(args):
    """ Uses lxml, and requests library to request and get links from sites """
    global urlList
    global urlSet
    global NUM_LINKS

    # read in input seed file, push back to urlList
    with open(DIRECTORY + args[0], 'r') as input_seeds:
        for url in input_seeds.readlines():
            url = url.replace("http://", "")
            url = url.replace("www.", "")
            urlList.append(url)

    NUM_LINKS = int(args[1])

    ind = 0
 
    while len(urlSet) < NUM_LINKS and len(urlList):

        # next Link in queue
        url = urlList[ind]
        ind += 1

        # Try to request the page
        try:
            temp_url = "http://www." + url
            content = get(temp_url, timeout=0.2)
            content.raise_for_status()
        except requests.RequestException:
            continue
    
        if "html" in content.headers['content-type']:
            htmlContent = html.fromstring(content.text)
            urlSet.add(url)

            # Finds all href links, push back to list
            allLinks = htmlContent.iterlinks()
            for link in allLinks:
                good_link = urljoin( temp_url, link[2] )
                temp_list = list(good_link)

                # check if https, if so normalize to http
                if temp_list[4] == 's':
                    del temp_list[4]
                    good_link = ''.join(temp_list)

                if check_url(url, good_link):
                    good_link = good_link.replace("http://", "") 
                    good_link = good_link.replace("www.", "")
                    urlList.append(good_link)
                    sourceUrl.append((url, good_link))


    need_out = open( DIRECTORY + 'crawler.output', 'w+')
    for i in urlSet:
        need_out.write("{}\n".format(i))

    op_out = open( DIRECTORY + 'optional.output', 'w+')
    # loop through list of tuples, only output urls, in both lists
    for source,url in sourceUrl:
        if source in urlSet and url in urlSet:
            op_out.write("{},{}\n".format(source,url))

if __name__ == '__main__':
    '''Main runs webcrawler'''
    main(argv[1:])