#!/usr/bin/env python

import json
import re

from dataset import *
from collections import defaultdict

from pprint import pprint as pp

###############################################################################
# Setup
###############################################################################

YEAR_REGEX = r'\d+\/\d+\/(\d+)'

class Label:
    VeryUnpopular, Unpopular, Average, Popular, VeryPopular = range(1, 6)
    five = [VeryUnpopular, Unpopular, Average, Popular, VeryPopular]
    three = [Unpopular, Average, Popular]
    div = {3: three, 5: five}

data = ArticleDataset(labeled=False)

###############################################################################
# Build Boundaries
###############################################################################

boundaries      = defaultdict(dict)
uniquedict      = defaultdict(list)
nonuniquedict   = defaultdict(list)

for article in data:
    year = article['date_published'].split()[0].split('/')[2]
    uniquedict[year].append(article['views']['unique'])
    nonuniquedict[year].append(article['views']['nonunique'])

for dictionary in (uniquedict, nonuniquedict):
    for year in sorted(dictionary):
        num_segments = 3
        arr = np.array(dictionary[year])
        percentiles = []
        for i in range(1, num_segments):
            percent = (i * 100) / num_segments
            x = int(np.percentile(arr, percent))
            percentiles.append(x)
        
        percentiles.append(100000000) # last level is anything below 100,000,000 views

        if dictionary == uniquedict:
            boundaries["unique"][year] = percentiles
        else:
            boundaries["nonunique"][year] = percentiles

###############################################################################
# Label
###############################################################################

def label(year, article, view_type="unique"):
    views = article['views'][view_type]
    level = boundaries[view_type][year]
    labels = Label.div[len(level)]

    for i in xrange(len(level)):
        if views < level[i]:
            article[u'label'] = labels[i]
            break

for article in data:
    year = re.match(YEAR_REGEX, article['date_published']).group(1)
    label(year, article, 'unique')

###############################################################################
# Write to file
###############################################################################

with open('../Dataset/output/articles_labeled.json', 'w') as outfile:
    json.dump(data.articles, outfile)
