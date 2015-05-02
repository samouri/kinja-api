
import json
from dataset import *

from enum import Enum
from pprint import pprint as pp

###############################################################################
# Label
###############################################################################

class Label:
    VeryUnpopular, Unpopular, Average, Popular, VeryPopular = range(1, 6)

data = ArticleDataset(labeled=False)
for article in data:
    views = article['views']['unique']
    if views < 5000:
        article[u'label'] = Label.VeryUnpopular
    elif views < 10000:
        article[u'label'] = Label.Unpopular
    elif views < 20000:
        article[u'label'] = Label.Average
    elif views < 50000:
        article[u'label'] = Label.Popular
    else:
        article[u'label'] = Label.VeryPopular

###############################################################################
# Write to file
###############################################################################

with open('../Dataset/output/articles_labeled.json', 'w') as outfile:
    json.dump(data.articles, outfile)
