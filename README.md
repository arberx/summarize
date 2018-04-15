# sumMarize
Final Project for **EECS-486** at the University of Michigan - Ann Arbor
Professor Rada

**Authors**: *Arber Xhindoli, Dillion Kesto,  Caroline Saab, Trevor Rees*

# Table of Contents

* [Getting Started](#Getting-Started)
* [Run from a Web Interface](#Web-Interface)
* [Run from the Command Line](#Command-Line)
* [Overview of the Project](#Overview-Of-SumMarize)
* [References](#References)

### Project Directory Structure
```shellsession
.
├── ./README.md
├── ./setup.py
├── ./spec.txt
├── ./stopwords.txt
├── ./summarize
│   ├── ./summarize/__init__.py
│   ├── ./summarize/static
│   │   └── ./summarize/static/css
│   │       └── ./summarize/static/css/main.css
│   ├── ./summarize/templates
│   │   ├── ./summarize/templates/base.html
│   │   └── ./summarize/templates/summary.html
│   └── ./summarize/views
│       ├── ./summarize/views/centroid.py
│       ├── ./summarize/views/evaluate.py
│       ├── ./summarize/views/helpers.py
│       ├── ./summarize/views/__init__.py
│       ├── ./summarize/views/main.py
│       ├── ./summarize/views/porterstemmer.py
│       ├── ./summarize/views/preprocess.py
│       ├── ./summarize/views/probability.py
│       ├── ./summarize/views/runTests.py
│       ├── ./summarize/views/stopwords.txt
│       └── ./summarize/views/sumMary.py
└── ./summarizerun
```
# Getting Started

The project can be run in two ways:

1) [Through a web interface.](#Web-Interface)

2) [Run from the Command Line](#Command-Line)

Please continue to relative sections.

# Web Interface

This will walk you through running the web interface of the project. Please be in the [top level directory](#Project-Directory-Structure), when running the commands.

1) Create and activate a python2 virtual enviroment by (optional, requires virtualenv package):

    `virtualenv env --no-site-packages -p python`
    `source env/bin/activate`

2) Install the summarize package:

    `pip install -e .`

3) Make the bash script executable:

    `chmod +x summarizerun`

4) Run the python flask app(from top level directory):

    `./summarizerun`

You should now be running the the app at [localhost:8000](http://localhost:8000)

# Command Line

Project uses the click library to help with command line arguments, before we walk through the commands please run:

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

The above output described the
# File Explanation