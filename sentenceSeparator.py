#!/usr/bin/env python

# sentenceSeparator.py
# EECS 486 Final Project
# splits a given block of text into sentences.

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


def sentenceSeparator(text):
	sentences = []

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
			



	return sentences

# Quick main function for testing
if __name__ == '__main__':
	text = 