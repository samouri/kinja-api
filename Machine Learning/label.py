#!/usr/bin/env python
"""
====================
Labeling the Dataset
====================

This script is used to label, and relabel, the dataset. Articles are labeled
according to the year they were published in and the number of views they
received.

Each year has its popularity cutoffs. These cutoffs are calculated before labeling.
There can be 3 or 5 divisions of popularity:
    - Unpopular, Average, Popular
    - VeryUnpopular, Unpopular, Average, Popular, VeryPopular

The number of divisions is set by NUM_CUTOFFS. After labeling, the articles are
written to a JSON file.
"""

import json
import re

from dataset import *
from collections import defaultdict

from pprint import pprint as pp

###############################################################################
# Label Class
###############################################################################

class Label:
    VeryUnpopular, Unpopular, Average, Popular, VeryPopular = range(1, 6)
    five = [VeryUnpopular, Unpopular, Average, Popular, VeryPopular]
    three = [Unpopular, Average, Popular]
    div = {3: three, 5: five}

###############################################################################
# Setup
###############################################################################

OUTPUT_FILENAME = '../Dataset/output/articles_labeled.json'
YEAR_REGEX      = r'\d+\/\d+\/(\d+)'
NUM_CUTOFFS     = 3

data = ArticleDataset(labeled=False)

###############################################################################
# Build Boundaries
###############################################################################

cutoffs         = defaultdict(dict)
uniquedict      = defaultdict(list)
nonuniquedict   = defaultdict(list)

for article in data:
    year = article['date_published'].split()[0].split('/')[2]
    uniquedict[year].append(article['views']['unique'])
    nonuniquedict[year].append(article['views']['nonunique'])

for dictionary in (uniquedict, nonuniquedict):
    for year in sorted(dictionary):
        num_segments = NUM_CUTOFFS
        arr = np.array(dictionary[year])
        percentiles = []
        for i in range(1, num_segments):
            percent = (i * 100) / num_segments
            x = int(np.percentile(arr, percent))
            percentiles.append(x)
        
        percentiles.append(100000000) # last level is anything below 100,000,000 views

        if dictionary == uniquedict:
            cutoffs["unique"][year] = percentiles
        else:
            cutoffs["nonunique"][year] = percentiles

###############################################################################
# Label
###############################################################################

def label(year, article, view_type="unique"):
    views = article['views'][view_type]
    level = cutoffs[view_type][year]
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

with open(OUTPUT_FILENAME, 'w') as outfile:
    json.dump(data.articles, outfile)
