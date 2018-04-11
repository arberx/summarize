#!/usr/bin/env python

# sentenceSeparator.py
# EECS 486 Final Project
# splits a given block of text into sentences.

abbreviations = {
	"mr." : 1,
	"mrs." : 1,
	"ms." : 1,
	"dr." : 1,
	"sr." : 1,
	"jr." : 1,
	"st." : 1,
}

def findPunctuation(text, start)
	locations = []

	period = text.find('.', start)
	question = text.find('?', start)
	exclamation = text.find('!', start)
	newline = text.find('\n', start)

	if (period != -1):
		locations.append(period)

	if (question != -1):
		locations.append(question)

	if (exclamation != -1):
		locations.append(exclamation)

	if (newline != -1):
		locations.append(newline)

	if (len(locations) == 0):
		return -1
	else:
		return min(locations)

def findAbbreviation(text, start):
	for i in range(2, 4):
		if punctuationIdx >= i:
			if text[punctuationIdx - i : punctuationIdx] in abbreviations:
				return true

def sentenceSeparator(text):
	sentences = []
	text = text.lower

	# Index of the beginning of a sentence
	sentenceStart = 0

	punctuationIdx = findPunctuation(text, sentenceStart)

	while(punctuationIdx != -1):
		# Handling for newlines (right now, always sentence separators)
		if text[punctuationIdx] == '\n':
			sentences.append(text[sentenceStart:punctuationIdx])
			sentenceStart = punctuationIdx + 1
			punctuationIdx = findPunctuation(text, sentenceStart)
			continue

		# Handling for question marks (right now, always sentence separators)
		elif text[punctuationIdx] == '?':
			sentences.append(text[sentenceStart:punctuationIdx])
			sentenceStart = punctuationIdx + 1
			punctuationIdx = findPunctuation(text, sentenceStart)
			continue

		# Handling for exclamation marks (right now, always sentence separators)
		elif text[punctuationIdx] == '!':
			sentences.append(text[sentenceStart:punctuationIdx])
			sentenceStart = punctuationIdx + 1
			punctuationIdx = findPunctuation(text, sentenceStart)
			continue

		# Handling for periods (these will require the most exception-checking)
		else:
			if findAbbreviation(text, punctuationIdx):
				punctuationIdx = findPunctuation(text, punctuationIdx + 1)
				continue
					
			sentences.append(text[sentenceStart:punctuationIdx])
			sentenceStart = punctuationIdx + 1
			punctuationIdx = findPunctuation(text, sentenceStart)
			continue


	return sentences

# Quick main function for testing
if __name__ == '__main__':
	text = 