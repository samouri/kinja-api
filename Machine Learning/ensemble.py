#!/usr/bin/env python

import sys
from dataset import *

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import explained_variance_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm, cross_validation, datasets
from sklearn.metrics import classification_report

###############################################################################
# Ensemble Methods
###############################################################################


if __name__ == "__main__":
    print "loading dataset"
    data = ArticleDataset(length=500, year="08")
    print "loaded ", len(data), " articles"
    vectorizer = CountVectorizer(min_df=1) 
    bigram_vectorizer = CountVectorizer(ngram_range=(1, 2),
                                         token_pattern=r'\b\w+\b', min_df=1)
    transformer = TfidfTransformer()

    print "vectorizing and weighting data"
    content = data.get_feature('content')
    title = data.get_feature('title')
    X1 = transformer.fit_transform(bigram_vectorizer.fit_transform(content))
    X2 = transformer.fit_transform(bigram_vectorizer.fit_transform(title))
    Y = data.get_feature('views', view_type="nonunique")
    X = X2

    print "training forest regressor"
    X_train, X_test, y_train, y_test = train_test_split(X, Y)
    forest_estimator = RandomForestRegressor(n_estimators=100, n_jobs=-1, verbose=3)
    forest_estimator.fit(X_train.toarray(),y_train)
    
    print "scoring forest regressor:"
    print "score for forest regressor is: ", forest_estimator.score(X_test.toarray(), y_test)

    
    Y_labels = data.get_feature('label')
    X_train, X_test, y_train, y_test = train_test_split(X, Y_labels)

    print "training forest classifier"
    forest_clf = RandomForestClassifier(n_estimators=100, n_jobs=-1, verbose=3)
    forest_clf.fit(X_train.toarray(),y_train)
    y_pred = forest_clf.predict(X_test.toarray())
    print "scoring forest classifier:"
    print forest_clf.score(X_test.toarray(), y_test)
    print(classification_report(y_test, y_pred, target_names=ArticleDataset.Labels))
