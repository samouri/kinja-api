#!/usr/bin/env python
"""
=================================================
Attempting Classification with Multiple Features
=================================================

This script uses Scikit-learn's Pipeline and FeatureUnion classes. They
simplify the process of transofrming features and combining them. Here,
different subsets of features were tried to achieve a high performing
classifier, along with various classifiers.

Running this script creates a pipeline with the chosen features,
fits the resulting feature matrix to the given classifer, uses
the classifier to predict on the test data, and prints the results
using scikit-learn's built in classification report method.
"""

from __future__ import print_function
from pprint import pprint

from dataset import *
from transformers import *

import numpy as np
np.set_printoptions(threshold=np.nan)

import matplotlib.pyplot as plt

from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.pipeline import FeatureUnion, Pipeline

# Classifiers
from sklearn.linear_model import *
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

###############################################################################
# Setup
###############################################################################

data = ArticleDataset(labeled=True, length=20000, year="09")

X_train, X_test, y_train, y_test = train_test_split(data.articles, data.get_feature('label'))

###############################################################################
# Pipeline
###############################################################################

pipeline = Pipeline([
    ('feature_dict', FeatureDictExtractor()),
    ('features', FeatureUnion(
        transformer_list=[

            ('pic_count', Pipeline([
                ('selector', ItemSelector(key='pic_count')),
                ('transform', PictureCountTransformer())
            ])),

            ('title_bow', Pipeline([
                ('selector', ItemSelector(key='title')),
                ('tfidf', TfidfVectorizer(binary=True, stop_words='english'))
            ])),

            ('title_stats', Pipeline([
                ('selector', ItemSelector(key='title')),
                ('stats', TitleStats()),
                ('vect', DictVectorizer(sparse=False))
            ])),

            ('author', Pipeline([
                ('selector', ItemSelector(key='author')),
                ('transform', AuthorTransformer()),
                ('vect', DictVectorizer(sparse=False))
            ])),

            ('tags', Pipeline([
                ('selector', ItemSelector(key='tags')),
                ('transform', TagTransformer()),
                ('vect', TfidfVectorizer(binary=True, ngram_range=(1, 3), stop_words='english'))
            ])),

            ('content_bow', Pipeline([
                ('selector', ItemSelector(key='content')),
                ('transform', ContentTransformer()),
                ('vect', TfidfVectorizer(ngram_range=(1, 3), token_pattern=r'\b\w+\b', min_df=50, stop_words='english'))
            ])),

            ('content_stats', Pipeline([
                ('selector', ItemSelector(key='content')),
                ('transform', DateTransformer()),
                ('vect', DictVectorizer(sparse=False))
            ])),

            ('date', Pipeline([
                ('selector', ItemSelector(key='date_published')),
                ('transform', ContentStatsTransformer()),
                ('vect', DictVectorizer(sparse=False))
            ])),

            ('weekend', Pipeline([
                ('selector', ItemSelector(key='is_weekend')),
                ('transform', IsWeekendTransformer())
            ])),

            ('hour', Pipeline([
                ('selector', ItemSelector(key='hour')),
                ('transform', HourTransformer())
            ]))

        ]
    )),

    # ('dense', DenseTransformer()),  # changes sparse to dense
    # Uncomment following line to reduce dimensions
    # ('pca', PCA(n_components=150)),
    # Uncomment the following line to print the final shape of matrix
    ('shape', ShapeTransformer()),
    # Use logistic regression classifier on the combined features
    ('classifier', LogisticRegression(verbose=3))
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
print(classification_report(y_pred, y_test, target_names=ArticleDataset.Label_Names[3]))
