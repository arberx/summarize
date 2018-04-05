#!/usr/bin/python

'''
Assignment 1 For EECS 486
Author: Arber Xhindoli
'''
import os
import math
import sys
import operator

FILES = ['English', 'French', 'Italian']

# vocabulary size in each language
LANG_V = []
UNIQ_WORDS = {}

# certain punctuation I want removed
PUNCTUATION = r"""!"#$%&(),.-'*+/:;<=>?@[\]^_`{|}~"""

def clean_text(text):
    '''cleans the list'''
    # make it all lower case
    text = text.lower()
    text = ' '.join(text.split('\n'))

    word_list = []
    is_space = False
    new_word = ''

    # creates word list and preserves whitespace
    for char in text:

        if char == ' ':
            is_space = True
            new_word += char 
            word_list.append(new_word)
            new_word = ''

        elif is_space:
            new_word += ' '
            is_space = False
            new_word += char
        else:
            new_word += char

    # remove certain punctuation
    new_list = []   
    for it in word_list:
        new_list.append(''.join(ch for ch in it if ch not in PUNCTUATION))

    return new_list


def trainBigramLanguageModel(text):
    '''Takes character bigram, and makes two dictionaries'''
    unigram_dict = {}
    bigrahm_dict = {}

    new_list = clean_text(text)

    # # make unigram dictionary with counts
    for word in new_list:

        # count uniq words
        if word not in UNIQ_WORDS.keys():
            UNIQ_WORDS[word] = 1
        else:
            UNIQ_WORDS[word] += 1

        # loop through each character in the word, make bigrahm/unigram
        for i, char in enumerate(word):
            # unigrahm
            if char not in unigram_dict.keys():
                unigram_dict[char] = 1
            else:
                unigram_dict[char] += 1

            # bigrahm
            if i + 1 < len(word) - 1:
                bigrahm = word[i] + word[i+1]
                if bigrahm not in bigrahm_dict.keys():
                    bigrahm_dict[bigrahm] = 1
                else:
                    bigrahm_dict[bigrahm] += 1

    # return character frequencies and bigrahm frequencies
    return unigram_dict, bigrahm_dict

def identifyLanguage(text, lang, l_of_ugrams, l_of_bgrams):
    '''Takes string, langanguages, ugrams, bgrams position i corresponds to same lange all lists '''
    # cleans list, removes newlines
    text = text.lower()
    new_list = text.split('\n')
    new_list = filter(None, new_list)

    # for each line, we go through the languages
    directory = os.getcwd()
    file = open(directory + '/results', 'w+')
    for k,word in enumerate(new_list):
        list_probs = []
        for i in range(len(lang)):
            # get bigrahms, calculate probabilities
            tot_prob = 0.0
            for j, char in enumerate(str(word)):
                if j + 1 < len(word) - 1:
                    bigrahm = char + word[j+1]
                    # find bigrahm in langugage dict
                    num = 0.0
                    den = 0.0
                    if bigrahm in l_of_bgrams[i].keys():
                        num = float(l_of_bgrams[i][bigrahm] + 1)
                        # print("num {}". format(num))
                        if char in l_of_ugrams[i].keys():
                            den = float(l_of_ugrams[i][char] + LANG_V[i])

                    if num and den:
                        tot_prob += math.exp(float(math.log(float((num / den)))))

            list_probs.append(tot_prob)
        max_index, max_value = max(enumerate(list_probs), key=operator.itemgetter(1))
        file.write("{} {}\n".format(k + 1, FILES[max_index]))
    file.close()

if __name__ == '__main__':

    directory = os.getcwd() + '/languageIdentification.data' + '/training'
    l_of_ugrams = []
    l_of_bgrams = []

    for filename in FILES:
        with open(directory + '/' + filename, 'r') as read_data:
            # pass the entire contents of the file, and write
            u1, b2 = trainBigramLanguageModel(read_data.read())
            l_of_ugrams.append(u1)
            l_of_bgrams.append(b2)

            # append total, num of uniq words
            LANG_V.append(len(UNIQ_WORDS.keys()))
            UNIQ_WORDS.clear()

    testData = os.getcwd() + '/' + str(sys.argv[1])
    with open(testData , 'r') as read_data:
        identifyLanguage(read_data.read(), FILES, l_of_ugrams, l_of_bgrams)
