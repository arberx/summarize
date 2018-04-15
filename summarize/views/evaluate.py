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

	# Find |intersection of relevant and retrieved|
	relevant_and_retrieved = len(list(set(generated_summary) & set(manual_summary)))

	# Find |retrieved|
	retrieved = len(generated_summary)

	# Find |relevant|
	relevant = len(manual_summary)

	# Return precision, recall
	return float(relevant_and_retrieved)/retrieved, float(relevant_and_retrieved)/relevant

def main():
	weighting_schemes = ["tf","c","p"]

	# Get names of manual summary files
	generated_summaries_dir = os.path.abspath(os.path.join(os.getcwd(),"../..", "summaries/evaluation/"))
	manual_summaries_dir = os.path.abspath(os.path.join(os.getcwd(),"../..", "summaries/sentences/"))
	#generated_summaries = os.listdir(generated_summaries_dir)
	manual_summaries = os.listdir(manual_summaries_dir)
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
		print "     ####### RESULTS FOR", scheme, "#######"
		for g, m in zip(generated_summaries[start:end], manual_summaries):
			precision, recall = precisionAndRecall(g,m)
			print g, "Precision:", precision, "  |  Recall:", recall
		start = start + num_files
		end = end + num_files


if __name__ == "__main__":
	main()

# summaries_evaluation b0_tf

# # Tests
# generated_summaries = [["I love cats.","I love every kind of cat.", "I just want to hold all of them, but I can't.", "Can't hug every cat."],["I love cats.","I love every kind of cat."],["I love cats.","I love every kind of cat.","So anyway, I am a cat lover, and I love to run."]]
# file = "cats_manual_summary.txt"

#for generated_summary in generated_summaries:
	#print precision(generated_summary, file, 1_or_recall)

#fileToText("hello",1)
#fileToText("itsME",0)