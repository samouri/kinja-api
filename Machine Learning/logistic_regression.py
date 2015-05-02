#!/usr/bin/env python

import numpy as np
from pprint import pprint as pp
from dataset import *
import matplotlib.pyplot as plt
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.cross_validation import train_test_split, cross_val_score

###############################################################################
# Setup
###############################################################################

def print_predictions(model, X_test, y_test, tag=""):
    if tag:
        print tag.upper()
    print "  prediction is:         ", model.predict(X_test)[0][0]
    print "  actual view count was: ", y_test[0]
    print "----------------------------------------"
def show_confusion_matrix(y_test, y_pred):
    confusion_matrix = confusion_matrix(y_test, y_pred)
    plt.matshow(confusion_matrix)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
def print_precision_recall(classifier, X_train, y_train):
    precisions = cross_val_score(classifier, X_train, y_train, cv=5, scoring='precision')
    print 'Precision', np.mean(precisions), precisions
    recalls = cross_val_score(classifier, X_train, y_train, cv=5, scoring='recall')
    print 'Recalls', np.mean(recalls), recalls
def print_accuracy(classifier, X_train, y_train):
    scores = cross_val_score(classifier, X_train, y_train, cv=5)
    print 'Accuracy', np.mean(scores), scores
def print_f1(classifier, X_train, y_train, cv=5):
    f1s = cross_val_score(classifier, X_train, y_train, cv=cv, scoring="f1")
    print 'F1', np.mean(f1s), f1s
def print_classification_report(y_test, predictions):
    print 'Classification Report:', classification_report(y_test, predictions)

data = ArticleDataset(labeled=True, length=1000)

PIC_COUNT   = 0
TITLE       = 1
AUTHOR      = 0

#######################################
# Pic Count Model
#######################################
if PIC_COUNT:
    print "___Using pic_count___"

    X = data.get_feature('pic_count')
    y = data.get_feature('label')

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    print_accuracy(classifier, X_train, y_train)
    print_precision_recall(classifier, X_train, y_train)
    print_f1(classifier, X_train, y_train)

#######################################
# Title Model
#######################################
"""
ngram_range: tuple of min ngram size and max ngram size
token_pattern: regexp denoting what constitutes a token
min_df: ignore words that have a document frequency less than the given threshold
stop_words: ignore common English words ("the", "a", ...)
"""
if TITLE:
    print "___Using title___"

    vectorizer  = TfidfVectorizer(binary=True, ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1, stop_words='english')
    corpus      = data.get_feature('title')

    X = vectorizer.fit_transform(corpus)
    y = data.get_feature('label')

    print np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    print 'Confusion Matrix:', confusion_matrix(y_test, y_pred)
    print_classification_report(y_test, y_pred)

#######################################
# Author Model
#######################################
if AUTHOR:
    print "___Using author___"

    onehot_encoder = DictVectorizer()

    X = onehot_encoder.fit_transform(data.get_feature('author'))
    y = data.get_feature('views')

    X_train, X_test, y_train, y_test = train_test_split(X, y)
    
    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    print_accuracy(classifier, X_train, y_train)
    print_precision_recall(classifier, X_train, y_train)
    print_f1(classifier, X_train, y_train)

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

