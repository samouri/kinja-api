#!/usr/bin/env python

import sys
from dataset import *

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score


###############################################################################
# Grid Search
###############################################################################

pipeline = Pipeline([
    ('clf', LogisticRegression())
])
parameters = {
    'clf__penalty': ('l1', 'l2'),
    'clf__C': (0.01, 0.1, 1, 10)
    }

if __name__ == "__main__":

    data = ArticleDataset(length=4000, year="08")

    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1, scoring='accuracy', cv=3)
    
    X = data.get_feature('pic_count')
    y = data.get_feature('label')

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    grid_search.fit(X_train, y_train)

    print 'Best score: %0.3f' % grid_search.best_score_
    print 'Best parameters set:'
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
       print '\t%s: %r' % (param_name, best_parameters[param_name])
    predictions = grid_search.predict(X_test)
    print 'Accuracy:', accuracy_score(y_test, predictions)
    print 'Precision:', precision_score(y_test, predictions)
    print 'Recall:', recall_score(y_test, predictions)


