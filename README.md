Predicting Gawker
===================

To follow is a list of the directory structure and the meaning behind it:

1. Dataset
    1.a Inputs
    1.b Outputs
    2.c Scripts
2. Machine Learning
3. Preprocessing

Datasets
----------
This folder contains three folders within it.  All of the files within it are related to generating the dataset or the graphs.  This means downloading html, scraping, etc.

    Inputs
    -------
    This has all of the text files that we generated that act as inputs to scripts.  Really just the URLs for gawker articles

    Outputs
    --------
    This is where all of the outputs from the scripts when.  For example all of the htmls, the linkgraph, articles.json, etc.
    
    Scripts
    --------
    This is where we placed all of the bash and ruby scripts that performed all of the work.  
    htmls.sh  --> downloads all of the html when given the url-list
    htmlsWatir.rb --> deprecated file.  Was a proposed solution to the viewcounts issue. By using a chromium webdriver to run the AJAX and wait for viewcounts to exist
    urls.sh   --> generates the url list from the sitemap
    scrape.rb --> scrapes all of the html 
    viewcounts.sh --> dowmloads all of the viewcounts and prints to stdout in json format
    generate_linkgraph.rb --> reads through htmls and generates a directed graph where nodes are articles and edges are links between them
    add_viewcounts.rb/add_weekend_hour.rb --> adds to articles.json extra data

Preprocessing
-------------
This folder contains all of the NTLK scripts

Machine Learning
---------------
This folder contains all of the work we did to create machine learning algorithms to predict viewcount based on article features

dataset.py --> A file we included in every other file.  It imports the dataset and provides helper functions to access it in useful ways
pipeline.py --> Our most thourough attempt at utilizing all of the features

