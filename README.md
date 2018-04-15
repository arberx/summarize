# sumMarize
Final Project for EECS486 at the University of Michigan - Ann Arbor

**Authors**: *Arber Xhindoli, Dillion Kesto,  Caroline Saab, Trevor Rees*

# Directory

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

1) Create and activate a python2 virtual enviroment by (optional):

    `virtualenv env --no-site-packages -p python`
    `source env/bin/activate`

2) Install the summarize package:

    `pip install -e .`

3) Make the bash script executable:

    `chmod +x summarizerun`

4) Run the python flask app(from top level directory):

    `./summarizerun`

You should now be running the the app at [localhost:8000](localhost:8000)

# Command Line





# Overview Of sumMarize

# File Explanation

# References