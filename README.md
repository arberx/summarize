# sumMarize
Final Project for **EECS-486** at the University of Michigan - Ann Arbor

sumMarize uses different numerical techniques to analyze and then produce the top 5 sentences that best summarize a piece of text. 

**Authors**: *Arber Xhindoli, Dillion Kesto,  Caroline Saab, Trevor Rees*

# Table of Contents

* [Getting Started](#getting-started)
* [Run with a Web Interface](#web-interface)
* [Run from the Command Line](#command-line)
* [Data Set](#data-set)
* [File Explanation](#file-explanation)

### Project Directory Structure
```shellsession
.
├── ./EECS486-final-report.tex
├── ./README.md
├── ./setup.py
├── ./spec.txt
├── ./stopwords.txt
├── ./summarize
│   ├── ./summarize/__init__.py
│   ├── ./summarize/static
│   │   ├── ./summarize/static/css
│   │   │   └── ./summarize/static/css/main.css
│   │   └── ./summarize/static/sumMarize_logo.png
│   ├── ./summarize/templates
│   │   ├── ./summarize/templates/base.html
│   │   └── ./summarize/templates/summary.html
│   └── ./summarize/views
│       ├── ./summarize/views/centroid.py
│       ├── ./summarize/views/evaluate.py
│       ├── ./summarize/views/evaluate_to_csv.py
│       ├── ./summarize/views/helpers.py
│       ├── ./summarize/views/__init__.py
│       ├── ./summarize/views/main.py
│       ├── ./summarize/views/porterstemmer.py
│       ├── ./summarize/views/preprocess.py
│       ├── ./summarize/views/probability.py
│       ├── ./summarize/views/runTests.py
│       ├── ./summarize/views/stopwords.txt
│       └── ./summarize/views/sumMary.py
├── ./summarizerun
└── ./summary-generic-text.pdf
```
* The above tree doesn't show testing files. Located in the **/summaries/** directory.

# Getting Started

The project can be run in two ways:

1) [Through a web interface.](#web-interface)

2) [Run from the Command Line](#command-line)

Please continue to relative sections.

# Web Interface

This will walk you through running the web interface of the project. Please be in the [top level directory](#project-directory-structure), when running the commands.

1) Create and activate a python2 virtual enviroment by (optional, requires virtualenv package):

    `virtualenv env --no-site-packages -p python`

    Activate the virtual enviroment by running:

    `source env/bin/activate`

2) Install the summarize package:

    `pip install -e .`

3) Make the bash script executable:

    `chmod +x summarizerun`

4) Run the python flask app(from top level directory) using the bash script:

    `./summarizerun`

You should now be running the the app at [localhost:8000](http://localhost:8000)

# Command Line

Project uses the click library to help with command line arguments, before we walk through the commands please run the below command in the [top level directory](#project-directory-structure):

 `pip install -e .`

Below is an output of the command: `python sumMary.py --help`

```shellsession
Usage: sumMary.py [OPTIONS] ARTICLE_FILE

  Input is file that text we want to summarize

Options:
  -n, --num_sentences INTEGER  Number of sentences to return in summary.
  -w, --weighting TEXT         Weighting scheme to use for scoring.
                               Methods:
                               tf - term frequency
                               p - probability
                               c - centroid
  --help                       Show this message and exit.
```

The above output describes the example usage of the sumMary.py. Examples commands would be:

 ```shellsession
    python sumMary.py -n 3 -w tf ../../summaries/articleTexts/b0
 ```

 This command would summarize this example article, using a **term frequency** scheme and output the **3** top sentences.

 ```shellsession
    python sumMary.py -n 10 -w p ../../summaries/articleTexts/b0
 ```

 This command would summarize this example article, using a **optimal sentence(centroid)** scheme and output the **10** top sentences.


# Data Set

The datasets used in the project were gathered manaully. They are located in the **/summaries/articleTexts/** folder. The sites we used to gather the article were: Bloomberg, CNN, Mgoblog, and Washington Post.

An example of the file naming scheme: 'b_0' which represents that this article was taken from Bloomberg.com. Similary 'm' for Mgoblog, 'c' for CNN, and 'w' for the Washington Post.

The articles were then manually summarized. This involved a person reading the article, and choosing the top 5 sentences in the text that best represent(summarize) the article. These 5 sentences were then used as a golden standard to compare our methods.

# File Explanation

Here we will describe the purpose of the main files of the summarize package. Most of which are inside the **/summarize/views/** directory.

*  [**main.py**](/summarize/views/main.py)

    - Contains the necessary code to run the web app, and render the correct html templates located in templates folder.

*  [**sumMary.py**](/summarize/views/sumMary.py)

    - This file is the main entry point into the project, it includes all the necessary algorithms from centroid.py, probabilty.py. It also includes the click library, which is useful for commandline arguments.

*  [**centroid.py**](/summarize/views/centroid.py)

    - Includes the centroid algorithm, which creates an optimal vector from the sentences in the document. Then uses cosine similarity to compare this 'optimal' sentence to the rest of the sentences.

*  [**probability.py**](/summarize/views/probability.py)

    - Includes the centroid algorithm, which uses naive bayes. It treats the document as a category, and tries to see which sentence has the highest probability of being in the category.

*  [**preprocess.py**](/summarize/views/preprocess.py), [**porterstemmer.py**](/summarize/views/porterstemmer.py)

    - These files were included from Assignment 1 done in class.

* [**evaluate.py**](/summarize/views/evaluate.py)

    - This file is used to calculate precision and recall comparing our algorihtms results with the manual results we generated (gold standard).


* [**runTests.py**](/summarize/views/runTests.py)

    - This file is used to create the test documents using in evalute.py to check the precision and recall values in evalute.py. These test documents are created in the directory: **/summaries/evaluation/**. The naming scheme of the file is "website_algorithm" where algorithm can be 'c', 'p', or 'tf'. This refers to the respective algorithms used to create the top 5 sentences.

* [**helpers.py**](/summarize/views/helpers.py)

    - Contains functions needed in the centroid.py, probability.py.
