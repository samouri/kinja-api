#!/usr/bin/env python

from __future__ import print_function

from dataset import *
from transformers import *

import numpy as np

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

###############################################################################
# Setup
###############################################################################

data = ArticleDataset(labeled=True, length=3000, year="13")

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
                ('vect', TfidfVectorizer(binary=True, stop_words='english'))
            ])),

        ]
    )),

    ('dense', DenseTransformer()),
    # Uncomment following line to reduce dimensions
    # ('pca', PCA(n_components=150)),
    ('shape', ShapeTransformer()),
    # Use logistic regression classifier on the combined features
    ('classifier', SVC(kernel='rbf', verbose=3))
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

# for i, pred in enumerate(y_pred):
#     print("Predicted: %d, Actual: %d" % (pred, y_test[i]))

print(classification_report(y_pred, y_test, target_names=ArticleDataset.Label_Names[3]))

