#!/usr/bin/env python

import sys
import json
import re
import numpy as np
from pprint import pprint
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model

###############################################################################
# Read In Article Data
###############################################################################

filename = "../Dataset/output/articles_complete.json"

''' this section is for reading a json file with multiple json objects in it (ruby does this but python does not allow it)
    this was ripped from stackoverflow: http://stackoverflow.com/questions/22112439/valueerror-extra-data-while-loading-json '''
nonspace = re.compile(r'\S')
def iterparse(j):
    decoder = json.JSONDecoder()
    pos = 0
    while True:
        matched = nonspace.search(j, pos)
        if not matched:
            break
        pos = matched.start()
        decoded, pos = decoder.raw_decode(j, pos)
        yield decoded

# read the json articles into data
with open(filename) as data_file:
    data = list(iterparse(data_file.read()))[0]

###############################################################################
# Machine Learning
###############################################################################

def get_feature(data, key, viewType="unique"):
    if key == 'title' or key == 'content':
        return map(lambda x:x[key], data)
    elif key == 'views':
        return map(lambda x:[x['views'][viewType]], data)        
    elif key == 'author':
        return map(lambda x:{'author': x['author']}, data)
    elif key == 'tags':
        return map(lambda x:" ".join(x['tags']), data)
    else:
        return map(lambda x:[x[key]], data)
def print_predictions(model, X_test, y_test, tag=""):
    if tag:
        print tag.upper()

    print "  prediction is:         ", model.predict(X_test)[0][0]
    print "  actual view count was: ", y_test[0]
    print "----------------------------------------"
def split_data(X, y):
    # for this second... training dataset = everything but the last element
    # and i test the accuracy using just the last element.  what good industry practice!!

    X_test  = X[-1]
    y_test  = y[-1]
    X       = X[:-1]
    y       = y[:-1]

    return X, y, X_test, y_test
def content_filter(x): 
    if 'content' in x:
        return True
    else:
        print x['id']
        return False

""" KEEP FILTERED DATA LENGTH TO LESS THAN 10,000 """
filtered = filter(content_filter, data)[0:1001]

#######################################
# Pic Count Model
#######################################

X = get_feature(filtered, 'pic_count')
y = get_feature(filtered, 'views')

X, y, X_test, y_test = split_data(X, y)

model = linear_model.LinearRegression()
model.fit(X, y)

print_predictions(model, X_test, y_test, 'pic count')

#######################################
# Author Model
#######################################

onehot_encoder = DictVectorizer()

X = onehot_encoder.fit_transform(get_feature(filtered, 'author'))
y = get_feature(filtered, 'views')

X, y, X_test, y_test = split_data(X, y)

model = linear_model.LinearRegression()
model.fit(X, y)

print_predictions(model, X_test, y_test, 'author')

#######################################
# Tags Model
#######################################

vectorizer  = CountVectorizer(binary=True, stop_words='english')
corpus      = get_feature(filtered, 'tags') 

X = vectorizer.fit_transform(corpus)
y = get_feature(filtered, 'views')

X, y, X_test, y_test = split_data(X, y)

model = linear_model.LinearRegression()
model.fit(X, y)

print_predictions(model, X_test, y_test, 'tags')

#######################################
# Title Model
#######################################

"""
ngram_range: tuple of min ngram size and max ngram size
token_pattern: regexp denoting what constitutes a token
min_df: ignore words that have a document frequency less than the given threshold
stop_words: ignore common English words ("the", "a", ...)
"""
vectorizer  = TfidfVectorizer(binary=True, ngram_range=(1, 1), token_pattern=r'\b\w+\b', min_df=1, stop_words='english')
corpus      = get_feature(filtered, 'title')

X = vectorizer.fit_transform(corpus)
y = get_feature(filtered, 'views')

X, y, X_test, y_test = split_data(X, y)

clf = linear_model.Ridge (alpha = .5)
clf.fit(X.toarray(),y)
clf.predict(X_test)

print_predictions(clf, X_test, y_test, "title")

#print(' '.join(vectorizer.inverse_transform(X_test)[0]))

#######################################
# Content Model
#######################################

"""
ngram_range:    tuple of min ngram size and max ngram size
token_pattern:  regexp denoting what constitutes a token
min_df:         ignore words that have a document frequency less than the given threshold
stop_words:     ignore common English words ("the", "a", ...)
"""
vectorizer  = TfidfVectorizer(ngram_range=(1, 1), token_pattern=r'\b\w+\b', min_df=1, stop_words='english')
corpus      = get_feature(filtered, 'content')

X = vectorizer.fit_transform(corpus)
y = get_feature(filtered, 'views')

X, y, X_test, y_test = split_data(X, y)

clf = linear_model.Ridge (alpha = .5)
clf.fit(X.toarray(),y)
clf.predict(X_test)

print_predictions(clf, X_test, y_test, "content")

