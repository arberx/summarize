# preprocess.py

import sys
import re
import os
from porterstemmer import PorterStemmer
from collections import deque

contractionsDict = {
	'ain\'t' : ['aint'],
	'amn\'t' : ['am', 'not'],
	'aren\'t' : ['are', 'not'],
	'can\'t' : ['can','not'],
	'could\'ve' : ['could', 'have'],
	'couldn\'t' : ['could', 'not'],
	'daren\'t' : ['dare', 'not'],
	'daresn\'t' : ['dare', 'not'],
	'dasen\'t' : ['dare', 'not'],
	'didn\'t' : ['did', 'not'],
	'doesn\'t' : ['does', 'not'],
	'don\'t' : ['do', 'not'],
	'e\'er' : ['ever'],
	'hadn\'t' : ['had', 'not'],
	'hasn\'t' : ['has' 'not'],
	'haven\'t' : ['have', 'not'],
	'he\'d' : ['he', 'would'],
	'he\'ll' : ['he', 'will'],
	'he\'s' : ['he', 'is'],
	'how\'d' : ['how', 'did'],
	'how\'ll' : ['how', 'will'],
	'how\'s' : ['how', 'is'],
	'i\'d' : ['i', 'would'],
	'i\'ll' : ['i', 'will'],
	'i\'m'  : ['i', 'am'],
	'i\'m\'a' : ['i', 'am', 'going', 'to'],
	'i\'ve' : ['i', 'have'],
	'isn\'t' : ['is', 'not'],
	'it\'d' : ['it', 'would'],
	'it\'ll' : ['it', 'will'],
	'it\'s' : ['it', 'is'],
	'let\'s' : ['let', 'us'],
	'ma\'am' : ['madam'],
	'mayn\'t' : ['may', 'not'],
	'may\'ve' : ['may', 'have'],
	'mightn\'t' : ['might', 'not'],
	'might\'ve' : ['might', 'have'],
	'mustn\'t' : ['must', 'not'],
	'must\'ve' : ['must', 'have'],
	'needn\'t' : ['need', 'not'],
	'ne\'er' : ['never'],
	'o\'clock' : ['of', 'the', 'clock'],
	'o\'er' : ['over'],
	'ol\'' : ['old'],
	'oughtn\'t' : ['ought', 'not'],
	'shan\'t' : ['shall', 'not'],
	'she\'d' : ['she', 'would'],
	'she\'ll' : ['she', 'will'],
	'she\'s' : ['she', 'is'],
	'should\'ve' : ['should', 'have'],
	'shouldn\'t' : ['should', 'not'],
	'something\'s' : ['something', 'is'],
	'that\'ll' : ['that', 'will'],
	'that\'re' : ['that', 'are'],
	'that\'s' : ['that', 'has'],
	'that\'d' : ['that', 'would'],
	'there\'d' : ['there', 'would'],
	'there\'re' : ['there', 'are'],
	'there\'s' : ['there', 'is'],
	'these\'re' : ['these', 'are'],
	'they\'d' : ['they', 'would'],
	'they\'ll' : ['they', 'will'],
	'they\'re' : ['they', 'are'],
	'they\'ve' : ['they', 'have'],
	'this\'s' : ['this', 'is'],
	'those\'re' : ['those', 'are'],
	'\'tis' : ['it', 'is'],
	'\'twas' : ['it', 'was'],
	'wasn\'t' : ['was', 'not'],
	'we\'d' : ['we', 'would'],
	'we\'d\'ve' : ['we', 'would', 'have'],
	'we\'ll' : ['we', 'will'],
	'we\'re' : ['we', 'are'],
	'we\'ve' : ['we', 'have'],
	'weren\'t' : ['were', 'not'],
	'what\'d' : ['what', 'would'],
	'what\'ll' : ['what', 'will'],
	'what\'re' : ['what', 'are'],
	'what\'s' : ['what' , 'is'],
	'what\'ve' : ['what', 'have'],
	'when\'s' : ['when', 'is'],
	'where\'d': ['where', 'would'],
	'where\'re' : ['where', 'are'],
	'where\'s' : ['where', 'is'],
	'where\'ve' : ['where', 'have'],
	'which\'s' : ['which', 'is'],
	'who\'d' : ['who', 'would'],
	'who\'d\'ve' : ['who', 'would', 'have'],
	'who\'ll' : ['who', 'will'],
	'who\'re' : ['who', 'are'],
	'who\'s' : ['who', 'is'],
	'who\'ve' : ['who', 'have'],
	'why\'d' : ['why', 'would'],
	'why\'re' : ['why' , 'are'],
	'why\'s' : ['why', 'is'],
	'won\'t' : ['will', 'not'],
	'would\'ve' : ['would', 'have'],
	'wouldn\'t' : ['would', 'have'],
	'y\'all' : ['you', 'all'],
	'you\'d' : ['you', 'would'],
	'you\'ll' : ['you', 'will'],
	'you\'re' : ['you', 'are'],
	'you\'ve' :['you', 'have']
}

# List of stop words
LIST_OF_STOP = ['a', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'been', 'but', 'by', 'few', 'from', 'for', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its', 'many', 'me', 'my', 'none', 'of', 'on', 'or', 'our', 'she', 'some', 'the', 'their', 'them', 'there', 'they', 'that', 'this', 'to', 'us', 'was', 'what', 'when', 'where', 'which', 'who', 'why', 'will', 'with', 'you', 'your']

# Many more stopwords. can choose between the two
with open( os.getcwd() + '/' + "stopwords.txt") as stop_words_file:
    LIST_OF_STOP = stop_words_file.read().split()

# Punctiation to consider to be the end of a sentence
STOP_PUNCTUATION = ['.']

# Blacklist of words that have periods in them
BLACK_LIST_WORDS = ["u.s.a.", "u.s.", "col.", "mr.", "mrs.", "ms.", "prof.", "dr.", "gen.", "rep.", "sen.", "st.", "sr.", "jr.", "ph.", "ph.d.", "m.d.", "b.a.", "m.a.", "d.d.", "d.d.s." "b.c.", "a.m.", "p.m.", "a.d.", "b.c.e.", "c.e.", "i.e.", "etc.", "e.g.", "al."]

def removeSGML(text):
	tagRemover = re.compile('<.*?>')
	noTags = re.sub(tagRemover, '', text)
	return noTags

def tokenizeText(text):
	# First, split on ' ' to remove spaces
	initial = text.split(' ')

	# Next, split on \n and remove empty strings
	noReturnsOrEmpty = []
	for word in initial:
		noReturns = word.split('\n')
		for token in noReturns:
			if token != '':
				noReturnsOrEmpty.append(token)

	# Make all words lowercase
	lowercase = []
	for word in noReturnsOrEmpty:
		word = word.lower()
		lowercase.append(word)

	# Deal with commas
	commasTokenized = []
	for word in lowercase:
		if ',' not in word:
			commasTokenized.append(word)
			continue

		if word == ',':
			continue

		# Remove commas at ends of words
		if word[-1] == ',':
			word = word[0:-1]

		# Check if the word is a valid number
		# Commas and periods are okay, but must contain at least one digit
		validNumber = True
		oneNumber = False
		for idx in word:
			if not (idx.isdigit() or idx == ',' or idx == '.'):
				validNumber = False
			if idx.isdigit():
				oneNumber = True

		# Valid numbers are kept together but the commas are removed
		if validNumber and oneNumber:
			word = re.sub(',', '', word)
			commasTokenized.append(word)
			continue

		else:
			commaSplit = word.split(',')

			for chunk in commaSplit:
				if chunk != '':
					commasTokenized.append(chunk)
			continue

	# Deal with hyphens
	hyphensTokenized = []
	for word in commasTokenized:
		if '-' not in word:
			hyphensTokenized.append(word)
			continue

		word = re.sub('-', '', word)

		if word == '':
			continue

		hyphensTokenized.append(word)

	# Deal with periods
	periodsTokenized = []
	for word in hyphensTokenized:
		if '.' not in word:
			periodsTokenized.append(word)
			continue

		if word[-1] == '.':
			word = word[0:-1]


		if word == '.' or word == '':
			continue

		# Check for numbers
		validNumber = True
		oneNumber = False
		for idx in word:
			if not (idx.isdigit() or idx == '.'):
				validNumber = False
			if idx.isdigit():
				oneNumber = True

		if validNumber and oneNumber:
			periodsTokenized.append(word)
			continue

		# Check for abbreviations
		numEmpty = 0
		numOne = 0
		periodSplit = word.split('.')
		for chunk in periodSplit:
			if len(chunk) == 0:
				numEmpty += 1
			if len(chunk) == 1:
				numOne += 1

		if numEmpty <= 1 and numOne >= 2:
			word = re.sub('.', '', word)
			periodsTokenized.append(word)
			continue

		for chunk in periodSplit:
			if chunk != '':
				periodsTokenized.append(chunk)


	# Deal with apostrophes (single quotes: ')
	apostrophesTokenized = []
	for word in periodsTokenized:
		if '\'' not in word:
			apostrophesTokenized.append(word)
			continue

		if word in contractionsDict:
			separate = contractionsDict[word]
			for chunk in separate:
				apostrophesTokenized.append(chunk)
			continue

		if len(word) < 4:
			word = re.sub('\'', '', word)
			apostrophesTokenized.append(word)
			continue

		if word[-2:] == '\'s':
			word = word[0:-2]
			apostrophesTokenized.append(word)
			apostrophesTokenized.append('s')
			continue

		if word[-3:] == '\'ll':
			word = word[0:-3]
			apostrophesTokenized.append(word)
			apostrophesTokenized.append('will')
			continue

		if word[-2:] == '\'d':
			word = word[0:-2]
			apostrophesTokenized.append(word)
			apostrophesTokenized.append('would')
			continue

		if word[-3:] == '\'re':
			word = word[0:-3]
			apostrophesTokenized.append(word)
			apostrophesTokenized.append('are')
			continue

		if word[-3:] == '\'ve':
			word = word[0:-3]
			apostrophesTokenized.append(word)
			apostrophesTokenized.append('have')
			continue

		word = re.sub('\'', '', word)
		apostrophesTokenized.append(word)

	slashesTokenized = []
	for word in apostrophesTokenized:
		if '/' not in word:
			slashesTokenized.append(word)
			continue

		if word[-1] == '/':
			word = word[0:-1]

		if word == '':
			continue

		numSlashes = 0
		wasSlash = False
		valid = True
		for idx in word:
			if not(idx.isdigit() or idx == '/'):
				valid = False
			if idx == '/':
				if (wasSlash):
					valid = False
				numSlashes += 1
				wasSlash = True
			else:
				wasSlash = False

		if numSlashes > 2:
			valid = False

		if valid:
			slashesTokenized.append(word)
			continue

		word = re.sub('/', '', word)
		slashesTokenized.append(word)

	final = []
	for word in slashesTokenized:
		word = re.sub('[\?!\\\\\(\)\[\]\{\}]', '', word)
		if word != '':
			final.append(word)

	final_final = []
	for word in final:
		final_final.append(''.join(ch for ch in word if ch.isalnum()))

	final_final_final = []
	for word in final_final:
		if word != '':
			final_final_final.append(word)

	return final_final_final

def removeStopwords(tokens):
    """Removes stopwords in tokens."""
    stopwordsRemoved = []

	# Remove all tokens that are stopwords
    for token in tokens:
	    if token not in LIST_OF_STOP:
		    stopwordsRemoved.append(token)

    return stopwordsRemoved

def stemWords(tokens):
    """Stems tokens."""
    stemmer = PorterStemmer()
    stemmedWords = []
    for token in tokens:
        stemmed = stemmer.stem(token, 0, len(token)-1)
        stemmedWords.append(stemmed)
    return stemmedWords

def preprocess_text(string):
    """Preprocess text, including tokenizing, stopword removal, and stemming."""
    tokens = tokenizeText(string)
    tokens = removeStopwords(tokens)
    return stemWords(tokens)

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

		# last word, add it
		if i == len(words) - 1:
			sentences.append(" ".join(words[sentence_start:i + 1]))
			continue

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

