Predicting Gawker
===================

To follow is an outline of the directory structure and a description 
of its components:

1. Dataset
    1.a Input
    1.b Output
    2.c Scripts
2. Machine Learning
3. Preprocessing

Dataset
----------
This folder contains This means downloading html,
scraping, etc.

    Input
    -------
    Contains article url files used as input to the scripts.

    Output
    --------
    Contains the json representation of our dataset (articles_labeled.json),
    and other files used to create the full dataset. These are the results
    of the script files. Files in the Output folder are generally used for
    processing in our attempts in Machine Learning. 
    
    Scripts
    --------
    Contains bash and ruby scripts used to build the dataset and graphs.

    * htmls.sh  				Downloads all of the html when given the url-list.
    
    * htmlsWatir.rb 			(Deprecated file) Was a proposed solution to the
    							viewcounts issue. By using a chromium webdriver
		    					to run the AJAX and wait for viewcounts to exist.
    
    * urls.sh   				Generates list of article urls from the sitemap.
    
    * scrape.rb 				Scrapes article html for relevant article 
    							characteristics.
    
    * viewcounts.sh 			Dowmloads viewcounts for every article and prints
    							to stdout in json format.
    
    * generate_linkgraph.rb 	Reads through htmls and generates a directed graph where
    							nodes are articles and edges are links between them.
    
    * add_viewcounts.rb 		Adds article view counts to article dataset. Each
    							article is given the number of views it received.
    							Usese the result from viewcounts.sh.
    
    * add_weekend_hour.rb 		Adds to time information to article dataset. Article
    							objects are given a boolean describing whether they
    							were published on a weekend and the hour in which they
    							were published on a 24-hour clock.

Preprocessing and Dataset Analysis
-------------
Contains the Python files that were used to create and analyze tag and
link networks and to preprocess the data.

Machine Learning
---------------
This folder contains all of the work we did to create machine learning
algorithms to predict viewcount based on article features

dataset.py --> A file we included in every other file.  It imports the dataset
and provides helper functions to access it in useful ways
pipeline.py --> Our most thourough attempt at utilizing all of the features

