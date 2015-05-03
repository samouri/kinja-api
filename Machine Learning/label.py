
import json
import re

from dataset import *
from collections import defaultdict

from enum import Enum
from pprint import pprint as pp

###############################################################################
# Setup
###############################################################################

YEAR_REGEX = r'\d+\/\d+\/(\d+)'

class Label:
    VeryUnpopular, Unpopular, Average, Popular, VeryPopular = range(1, 6)

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
        num_segments = 5
        arr = np.array(dictionary[year])
        percentiles = []
        for i in range(1, num_segments):
            percent = (i * 100) / num_segments
            x = int(np.percentile(arr, percent))
            percentiles.append(x)

        if dictionary == uniquedict:
            boundaries["unique"][year] = percentiles
        else:
            boundaries["nonunique"][year] = percentiles


###############################################################################
# Label
###############################################################################

def label(year, article, view_type="unique"):
    level = boundaries[view_type][year]

    if year == "05":
        if views < level[0]:
            article[u'label'] = Label.VeryUnpopular
        elif views < level[1]:
            article[u'label'] = Label.Unpopular
        elif views < level[2]:
            article[u'label'] = Label.Average
        elif views < level[3]:
            article[u'label'] = Label.Popular
        else:
            article[u'label'] = Label.VeryPopular
    
    elif year == "06":
        if views < level[0]:
            article[u'label'] = Label.VeryUnpopular
        elif views < level[1]:
            article[u'label'] = Label.Unpopular
        elif views < level[2]:
            article[u'label'] = Label.Average
        elif views < level[3]:
            article[u'label'] = Label.Popular
        else:
            article[u'label'] = Label.VeryPopular
    
    elif year == "07":
        if views < level[0]:
            article[u'label'] = Label.VeryUnpopular
        elif views < level[1]:
            article[u'label'] = Label.Unpopular
        elif views < level[2]:
            article[u'label'] = Label.Average
        elif views < level[3]:
            article[u'label'] = Label.Popular
        else:
            article[u'label'] = Label.VeryPopular
    
    elif year == "08":
        if views < level[0]:
            article[u'label'] = Label.VeryUnpopular
        elif views < level[1]:
            article[u'label'] = Label.Unpopular
        elif views < level[2]:
            article[u'label'] = Label.Average
        elif views < level[3]:
            article[u'label'] = Label.Popular
        else:
            article[u'label'] = Label.VeryPopular

    elif year == "09":
        if views < level[0]:
            article[u'label'] = Label.VeryUnpopular
        elif views < level[1]:
            article[u'label'] = Label.Unpopular
        elif views < level[2]:
            article[u'label'] = Label.Average
        elif views < level[3]:
            article[u'label'] = Label.Popular
        else:
            article[u'label'] = Label.VeryPopular
    
    elif year == "10":
        if views < level[0]:
            article[u'label'] = Label.VeryUnpopular
        elif views < level[1]:
            article[u'label'] = Label.Unpopular
        elif views < level[2]:
            article[u'label'] = Label.Average
        elif views < level[3]:
            article[u'label'] = Label.Popular
        else:
            article[u'label'] = Label.VeryPopular
    
    elif year == "11":
        if views < level[0]:
            article[u'label'] = Label.VeryUnpopular
        elif views < level[1]:
            article[u'label'] = Label.Unpopular
        elif views < level[2]:
            article[u'label'] = Label.Average
        elif views < level[3]:
            article[u'label'] = Label.Popular
        else:
            article[u'label'] = Label.VeryPopular
    
    elif year == "12":
        if views < level[0]:
            article[u'label'] = Label.VeryUnpopular
        elif views < level[1]:
            article[u'label'] = Label.Unpopular
        elif views < level[2]:
            article[u'label'] = Label.Average
        elif views < level[3]:
            article[u'label'] = Label.Popular
        else:
            article[u'label'] = Label.VeryPopular
    
    elif year == "13":
        if views < level[0]:
            article[u'label'] = Label.VeryUnpopular
        elif views < level[1]:
            article[u'label'] = Label.Unpopular
        elif views < level[2]:
            article[u'label'] = Label.Average
        elif views < level[3]:
            article[u'label'] = Label.Popular
        else:
            article[u'label'] = Label.VeryPopular

    elif year == "14":
        if views < level[0]:
            article[u'label'] = Label.VeryUnpopular
        elif views < level[1]:
            article[u'label'] = Label.Unpopular
        elif views < level[2]:
            article[u'label'] = Label.Average
        elif views < level[3]:
            article[u'label'] = Label.Popular
        else:
            article[u'label'] = Label.VeryPopular

for article in data:
    views = article['views']['unique']
    year = re.match(YEAR_REGEX, article['date_published']).group(1)
    label(year, article, 'unique')

###############################################################################
# Write to file
###############################################################################

with open('../Dataset/output/articles_labeled.json', 'w') as outfile:
    json.dump(data.articles, outfile)
