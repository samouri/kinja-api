#!/usr/bin/env python

import json
import re
import numpy as np
from pprint import pprint
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model

filename = "../output/output.json"

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
     data = list(iterparse(data_file.read()))


vectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
corpus = map(lambda x:x['content'], data)
X = vectorizer.fit_transform(corpus)
analyze = vectorizer.build_analyzer()

counts = X.toarray()
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(counts)

#pprint(X)
Y = map(lambda x:x['views'], data)
T = map(lambda x:x['title'], data)
L = map(lambda x:x['link'], data)


# for this second... training dataset = everything but the last element
# and i test the accuracy using just the last element.  what good industry practice!!
lastX = X[-1]
lastY = Y[-1]
X = X[:-1]
Y = Y[:-1]

#print(Y)
#print(X)


#clf = RandomForestRegressor(n_estimators=10)
clf = linear_model.Ridge (alpha = .5)
clf.fit(X.toarray(),Y)
clf.predict(lastX)
print("prediction is: ", clf.predict(lastX)[0])
print("actual views# was: ", lastY)


#print(T[-1])
#print(L[-1])
#print(' '.join(vectorizer.inverse_transform(lastX)[0]))

