#!/usr/bin/env python

from __future__ import print_function

import numpy as np
from pprint import pprint as pp
from dataset import *
import matplotlib.pyplot as plt
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline

###############################################################################
# Setup
###############################################################################

data = ArticleDataset(labeled=True, length=4)

X_train, X_test, y_train, y_test = train_test_split(data.articles, data.get_feature('label'))

###############################################################################
# Transformers
###############################################################################

class FeatureDictExtractor(BaseEstimator, TransformerMixin):

    def fit(self, x, y=None):
        return self

    def transform(self, articles):
		return ArticleDataset.to_feature_dict_from_articles(articles)

class ItemSelector(BaseEstimator, TransformerMixin):
    """For data grouped by feature, select subset of data at a provided key.

    The data is expected to be stored in a 2D data structure, where the first
    index is over features and the second is over samples.  i.e.

    >> len(data[key]) == n_samples

    Please note that this is the opposite convention to sklearn feature
    matrixes (where the first index corresponds to sample).

    ItemSelector only requires that the collection implement getitem
    (data[key]).  Examples include: a dict of lists, 2D numpy array, Pandas
    DataFrame, numpy record array, etc.

    >> data = {'a': [1, 5, 2, 5, 2, 8],
               'b': [9, 4, 1, 4, 1, 3]}
    >> ds = ItemSelector(key='a')
    >> data['a'] == ds.transform(data)

    ItemSelector is not designed to handle data grouped by sample.  (e.g. a
    list of dicts).  If your data is structured this way, consider a
    transformer along the lines of `sklearn.feature_extraction.DictVectorizer`.

    Parameters
    ----------
    key : hashable, required
        The key corresponding to the desired value in a mappable.
    """
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]

class PictureCountTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, pic_counts, **transform_params):
        return pic_counts

###############################################################################
# Pipeline
###############################################################################


pipeline = Pipeline([
	('feature_dict', FeatureDictExtractor()),
	('features', FeatureUnion(
		transformer_list=[

			# Pipline for pulling pic_count feature
			('pic_count', Pipeline([
				('selector', ItemSelector(key='pic_count')),
				('transform', PictureCountTransformer())
			]))
			
			# # Pipeline for pulling features from article title
			# ('title', Pipeline([
			# 	('selector', ItemSelector(key='title')),
			# 	('tfidf', TfidfVectorizer())
			# ]))
		]
	)),

	# Use logistic regression classifier on the combined features
	('classifier', LogisticRegression())
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
print(classification_report(y_pred, y_test))

