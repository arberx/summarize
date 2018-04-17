#!/usr/bin/env python
from math import sqrt
# This file uses a probabilistic method similar to naiveBayes to score
# sentences within a document, using the full article as the class.

# Given a list of sentences, returns a dictionary of unique tokens
def getVocabularySingleClass(sentences):
	uniqueTokens = {}

	# Iterate through sentences
	for sentence in sentences:

		# Get the unique tokens in all of the sentences
		for token in sentence.tokens:
			# Add to the general dictionary
			if token not in uniqueTokens:
				uniqueTokens[token] = 1.0
			else:
				uniqueTokens[token] += 1.0

	return uniqueTokens

# Given a list of sentences, return the size of the text in number of words
# (not necessarily unique).
def getTextLength(sentences):
	# Sum the text of all the sentences
	textLength = 0
	for sentence in sentences:
		textLength += len(sentence.tokens)

	return textLength

# Input: A list of sentences that comprise a document
# Output: A dictionary with conditional probabilities and other
# 	parameters.
# NOTE: There will only be one "class" to place the words into.
def trainNaiveBayes(sentences):
	tokenDict = getVocabularySingleClass(sentences)
	vocabulary = len(tokenDict)

	probDict = {}

	textLen = getTextLength(sentences)

	# Calculate the conditional probability for each word
	for xk, value in tokenDict.items():
		probDict[xk] = (value) / float(textLen)

	return probDict

# Scores sentences based on their probability of being in the defined class (the article).
def probability_scoring(sentences):

	# "Train" using all the sentences
	# Each sentence is an important part of the class (article),
	# so we include all of them in the training process
	probDict = trainNaiveBayes(sentences)

	vocabulary = len(probDict)

	# Score all the sentences based on their likelihood of being in the class
	for sentence in sentences:

		if len(sentence.tokens) == 0:
			continue

		for token in sentence.tokens:
			# Based on the algorithm, all words SHOULD be in the probability
			# dictionary. However, if they are not, use 1 / vocabulary
			if token not in probDict:
				sentence.score += 1.0 / float(vocabulary)

			# Add the conditional probabiliies for each word
			else:
				sentence.score += probDict[token]

			#sentence.score /= len(sentence.tokens)

