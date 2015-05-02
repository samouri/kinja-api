#!/usr/bin/env python

import sys
import json
import re
from itertools import islice
import numpy as np

complete_filename = "../Dataset/output/articles_complete.json"
labeled_filename = "../Dataset/output/articles_labeled.json"

class ArticleDataset:

    _features = ['pic_count', 'title', 'author', 'content', 'tags', 'label']

    def __init__(self, labeled=True, length=None, articles=None):
        if articles is not None:
            self.articles = articles
        else:
            self.articles = list(islice(self._read_in_dataset(labeled), length))

    def __iter__(self):
        return iter(self.articles)

    def _iterparse(self, j):
        """ this section is for reading a json file with multiple json objects in it (ruby does this but python does not allow it)
        this was ripped from stackoverflow: http://stackoverflow.com/questions/22112439/valueerror-extra-data-while-loading-json """
        nonspace = re.compile(r'\S')
        decoder = json.JSONDecoder()
        pos = 0
        while True:
            matched = nonspace.search(j, pos)
            if not matched:
                break
            pos = matched.start()
            decoded, pos = decoder.raw_decode(j, pos)
            yield decoded
    def _content_filter(self, x):
        if 'content' in x:
            return True
        else:
            # print x['id']
            return False
    def _read_in_dataset(self, labeled=True):
        # read the json articles into data
        if labeled:
            filename = labeled_filename
        else:
            filename = complete_filename

        with open(filename) as data_file:
            data = list(self._iterparse(data_file.read()))[0]
        
        filtered = filter(self._content_filter, data)

        return filtered

    def get_feature(self, key, viewType="unique"):
        if key == 'title' or key == 'content':
            return map(lambda x:x[key], self.articles)
        elif key == 'views':
            return map(lambda x:x['views'][viewType], self.articles)        
        elif key == 'author':
            return map(lambda x:{'author': x['author']}, self.articles)
        elif key == 'tags':
            return map(lambda x:" ".join(x['tags']), self.articles)
        elif key == 'label':
            return map(lambda x:x['label'], self.articles)
        else:
            return map(lambda x:[x[key]], self.articles)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.articles, indent=4)

    def to_feature_dict(self):
        """ Creates a dictionary of features.
        Key: Feature
        Val: Array of samples

        >> len(data[key]) == n_samples

        >> data =   {   'pic_count' : [1,3,3],
                        'title' : ['Kanye freaks out!', 'Jake and Jb have a blast.', 'Halloween']    }

        """
        return {feature:self.get_feature(feature) for feature in self._features}

    @classmethod
    def to_feature_dict_from_articles(cls, articles):
        features = np.recarray(shape=(len(articles),),
                               dtype=[(feature, object) for feature in cls._features])
        for i, article in enumerate(articles):
            for feature in cls._features:
                features[feature][i] = article[feature]

        return features




