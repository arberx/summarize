'''
Final Project EECS486

evaluate.py
'''

import os

import sumMary


def fileToText(filename, manual):
	'''Returns the file as a string.
	Set manual = 0 for generated summary
	Set manual = 1 for manual summary
	Set manual = 3 for full article text'''
	if manual == 0:
		fullpath = os.path.join(os.getcwd(),"../..", "summaries/evaluation", filename)
	elif manual == 1:
			fullpath = os.path.join(os.getcwd(),"../..", "summaries/sentences", filename)
	elif manual == 2:
		fullpath = os.path.join(os.getcwd(),"../..", "summaries/articleTexts", filename)
	else:
		print "Non-binary value given for manual flag in fileToText"
		exit(1)
	fullpath = os.path.abspath(fullpath)
	infile = open(fullpath,'r')
	return infile.read()

def fileToSentences(filename, manual):
	text = fileToText(filename, manual)
	sentences = sumMary.create_sentences(text)
	originals = []
	for sentence in sentences:
		originals.append(sentence.original)
	return originals

def precisionAndRecall(generated_summary_file, manual_summary_file):
	'''Given the name of the generated summary file and the manual summary file,
	return the precision and recall as a tuple'''
	# Convert summary files into lists of sentences
	generated_summary = fileToSentences(generated_summary_file, 0)
	manual_summary = fileToSentences(manual_summary_file, 1)
	# print manual_summary
	# Find |intersection of relevant and retrieved|
	relevant_and_retrieved = len(list(set(generated_summary) & set(manual_summary)))

	# Find |retrieved|
	retrieved = len(generated_summary)

	# Find |relevant|
	relevant = len(manual_summary)

	# Return precision, recall
	return float(relevant_and_retrieved)/retrieved, float(relevant_and_retrieved)/relevant, relevant_and_retrieved, relevant, retrieved

def getAvg(values):
	total = 0
	for value in values:
		total += value
	return float(total)/len(values)

def printMicroAverages(precisions, recalls):
	print "MICRO AVERAGES"
	print "Precision: ", getAvg(precisions)
	print "Recall: ", getAvg(recalls)

def printMacroAverages(total_relevant_and_retrieved,total_relevant,total_retrieved):
	print total_relevant_and_retrieved, total_relevant, total_retrieved #DEBUG
	macro_precision = total_relevant_and_retrieved/total_retrieved
	macro_recall = total_relevant_and_retrieved/total_relevant

	print "MACRO AVERAGES"
	print "Precision: ", macro_precision
	print "Recall: ", macro_recall

def main():
	weighting_schemes = ["tf","c","p"]

	# Get names of manual summary files
	generated_summaries_dir = os.path.abspath(os.path.join(os.getcwd(),"../..", "summaries/evaluation/"))
	manual_summaries_dir = os.path.abspath(os.path.join(os.getcwd(),"../..", "summaries/sentences/"))

	manual_summaries = os.listdir(manual_summaries_dir)
	if ".DS_Store" in manual_summaries:
		manual_summaries.remove(".DS_Store")

	# Get names of generated summary files
	generated_summaries = []
	for scheme in weighting_schemes:
		for file in manual_summaries:
			generated_summaries.append(file + "_" + scheme)

	num_files = len(manual_summaries)
	start = 0
	end = num_files

	# Compare the results of each weighting scheme to the manual summaries
	for scheme in weighting_schemes:
		# For macro averages
		precisions = []
		recalls = []

		# For the micro averages
		total_relevant_and_retrieved = 0
		total_relevant = 0
		total_retrieved = 0

		print "     ####### RESULTS FOR", scheme, "#######"
		for g, m in zip(generated_summaries[start:end], manual_summaries):
			precision, recall, inc_RnR, inc_Rel, inc_Ret = precisionAndRecall(g,m)
			precisions.append(precision)
			recalls.append(recall)
			if inc_Rel != 5:
				print g, total_relevant_and_retrieved, total_relevant, total_retrieved
				print inc_RnR, inc_Rel, inc_Ret
			total_relevant_and_retrieved += inc_RnR
			total_relevant += inc_Rel
			total_retrieved += inc_Ret
			print g, "Precision:", precision, "  |  Recall:", recall
		printMicroAverages(precisions, recalls)
		printMacroAverages(float(total_relevant_and_retrieved),total_relevant,total_retrieved)
		start = start + num_files
		end = end + num_files


if __name__ == "__main__":
	main()