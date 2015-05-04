#!/usr/bin/env python

import sys
from dataset import *
from transformers import *

from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import scale
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import *
from sklearn.grid_search import GridSearchCV

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
                ('vect', TfidfVectorizer(binary=True, stop_words='english'))
            ])),

            # ('title_stats', Pipeline([
            #     ('selector', ItemSelector(key='title')),
            #     ('stats', TitleStats()),
            #     ('dict', DictVectorizer(sparse=False))
            # ])),

            # ('author', Pipeline([
            #     ('selector', ItemSelector(key='author')),
            #     ('transform', AuthorTransformer()),
            #     ('dict', DictVectorizer(sparse=False))
            # ])),

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
    ('clf', LogisticRegression())
])


if __name__ == '__main__':

	parameters = {
		'vect__max_df': (0.25, 0.5, 0.75),
		'vect__stop_words': ('english', None),
		'vect__max_features': (2500, 5000, 10000, None),
		'vect__ngram_range': ((1, 1), (1, 2)),
		'vect__use_idf': (True, False),
		'vect__norm': ('l1', 'l2'),
		'clf__C': (0.1, 0.3, 1, 3, 10, 30),
	}

	grid_search = GridSearchCV(pipeline, parameters, n_jobs=2, verbose=3, scoring='accuracy')
	grid_search.fit(X_train, y_train)
	print 'Best score: %0.3f' % grid_search.best_score_
	print 'Best parameters set:'
	best_parameters = grid_search.best_estimator_.get_params()
	for param_name in sorted(parameters.keys()):
		print '\t%s: %r' % (param_name, best_parameters[param_name])

	predictions = grid_search.predict(X_test)
	print classification_report(y_test, predictions)

