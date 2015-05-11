#!/usr/bin/env python

# Various tests of different classifiers.  was used as a temp file to test out classifiers and features

import sys
from dataset import *

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import explained_variance_score
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm, cross_validation, datasets
from sklearn.metrics import classification_report
from sklearn import preprocessing
from sklearn.feature_selection import VarianceThreshold
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import *

###############################################################################
# Ensemble Methods
###############################################################################

def combine_features(*features):
    if len(features) == 1:
        return features[0]
    zipped = zip(*features)
    concat = lambda elem: reduce(lambda e1,e2: list(e1)+list(e2), elem, [])
    return map(concat, zipped)


if __name__ == "__main__":
    print "loading dataset"
    data = ArticleDataset(length=2000, year="08")
    print "loaded ", len(data), " articles"
    count_vectorizer = CountVectorizer() 
    bigram_vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words="english")
    dict_vectorizer = DictVectorizer()
    tfidf_transformer = TfidfTransformer()

    print "vectorizing and weighting data"
    content = data.get_feature('content')
    title = data.get_feature('title')
    author = data.get_feature('author')
    tags = data.get_feature('tags')
    X1 = tfidf_transformer.fit_transform(count_vectorizer.fit_transform(content))
    X2 = tfidf_transformer.fit_transform(count_vectorizer.fit_transform(title))
    X3 = dict_vectorizer.fit_transform(author)
    X4 = tfidf_transformer.fit_transform(count_vectorizer.fit_transform(tags))
    X5 = data.get_feature('content_length')

    X = combine_features(map(lambda x: [x], X5))
#    X = combine_features(X2.toarray(), X4.toarray())
    print("orig: ", len(X), len(X[0]))
    # feature selection
    #print("selecting features now")
    #var_sel = VarianceThreshold(threshold=(.9 * (1 - .9)))
    #X = var_sel.fit_transform(X)
    #Y_labels = data.get_feature('label')
    #forest_clf = ExtraTreesClassifier(n_estimators=1000, n_jobs=-1, max_depth=None, max_features=100)
    #X = forest_clf.fit(X,Y_labels).transform(X)
    print("after feature selection: ", len(X), len(X[0]))

    #print "training forest regressor"
    #Y = data.get_feature('views', view_type="nonunique")
    #X_train, X_test, y_train, y_test = train_test_split(X, Y)
    #forest_estimator = RandomForestRegressor(n_estimators=100, n_jobs=-1)
    #forest_estimator.fit(X_train,y_train)    
    #print "scoring forest regressor:"
    #print "score for forest regressor is: ", forest_estimator.score(X_test, y_test)

    
    print "training logistic classifier"
    Y_labels = data.get_feature('label')
    X_train, X_test, y_train, y_test = train_test_split(X, Y_labels)
    log_clf = LogisticRegression()
    log_clf.fit(X_train,y_train)
    y_pred = log_clf.predict(X_test)
    print "scoring logisistic classifier:"
    print "score is: ", log_clf.score(X_test, y_test)
    print(classification_report(y_test, y_pred, target_names=ArticleDataset.Label_Names[5]))

    print "training forest classifier"
    Y_labels = data.get_feature('label')
    X_train, X_test, y_train, y_test = train_test_split(X, Y_labels)
    forest_clf = RandomForestClassifier(n_estimators=250, n_jobs=-1, max_depth=None)
    forest_clf.fit(X_train,y_train)
    y_pred = forest_clf.predict(X_test)
    print "scoring forest classifier:"
    print "score is: ", forest_clf.score(X_test, y_test)
    print(classification_report(y_test, y_pred, target_names=ArticleDataset.Label_Names[5]))

    print "training extra-trees forest classifier"
    Y_labels = data.get_feature('label')
    X_train, X_test, y_train, y_test = train_test_split(X, Y_labels)
    forest_clf = ExtraTreesClassifier(n_estimators=250, n_jobs=-1, max_depth=None)
    forest_clf.fit(X_train,y_train)
    y_pred = forest_clf.predict(X_test)
    print "scoring extra-trees classifier:"
    print "score is: ", forest_clf.score(X_test, y_test)
    print(classification_report(y_test, y_pred, target_names=ArticleDataset.Label_Names[5]))

    print "training SVM classifier"
    Y_labels = data.get_feature('label')
    X_train, X_test, y_train, y_test = train_test_split(X, Y_labels)
    svm_clf = svm.SVC()
    svm_clf.fit(X_train, y_train)
    print "scoring SVM classifier:"
    y_pred = svm_clf.predict(X_test)
    print "score is: ", svm_clf.score(X_test, y_test)
    print(classification_report(y_test, y_pred, target_names=ArticleDataset.Label_Names[5]))
