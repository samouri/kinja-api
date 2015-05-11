#!/usr/bin/env python
"""
===================
Custom Transformers
===================

The transformers described in this module are used to do either one of two
things. Certian transormers, such as the PictureCountTransformer, are used
to fully convert raw features into feature vectors. Others, like
AuthorTransformer, prepare raw features for the next transformer, to then be
fully converted into feature vectors (in the Author scenario, AuthorTransformer
prepares the author feature for the DictVecotrizer by creating a dictionary
for each sample).
"""

from dataset import *
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

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
        return map(lambda x: [x], pic_counts)

class AuthorTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, authors, **transform_params):
        return map(lambda x: {"author":x}, authors)

class TagTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, tags, **transform_params):
        return map(lambda tag_list:" ".join(tag_list), tags)

class TitleStats(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, titles, **transform_params):
        return [{   'length': len(title),
                    'questions': title.count('?')}
                for title in titles]

class ContentTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, contents, **transform_params):
        return contents

class ContentStatsTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, contents, **transform_params):
        return [{   'length': len(content)}
                for content in contents]

class DateTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, dates, **transform_params):
        return map(lambda x: {"date":x}, dates)

class HourTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, hours, **transform_params):
        return map(lambda x: [x], hours)

class IsWeekendTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, is_weekends, **transform_params):
        def f(is_weekend):
            if is_weekend:
                return [1]
            else:
                return [0]

        return map(f, is_weekends)

class DenseTransformer(BaseEstimator, TransformerMixin):

    def transform(self, X, y=None, **fit_params):
        # print(X.todense().shape)
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        # print(X.shape)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self

class ShapeTransformer(BaseEstimator, TransformerMixin):

    def transform(self, X, y=None, **fit_params):
        return X

    def fit_transform(self, X, y=None, **fit_params):
        print(X.shape)
        return X

    def fit(self, X, y=None, **fit_params):
        return self
