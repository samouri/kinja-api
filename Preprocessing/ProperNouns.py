import nltk
import sys
import re

# Fixes encoding issues
reload(sys)
sys.setdefaultencoding('UTF8')

fname = "roadtomontgomery.txt"

with open(fname) as f:
	topics = {}
	for line in f:
		line = line.replace(u'\u2014',' ')
		line = line.replace(u'\u2013',' ')

		tokens = nltk.word_tokenize(line)
		tokens = nltk.pos_tag(tokens)

		currProper = []

		for index, tup in enumerate(tokens):
			(val, kind) = tup

			if kind == 'NNP':
				s = re.sub(r'[^\w\-\.]','', val)
				s.strip(" ")

				if (len(s) != 0):
					currProper.append(s)

			elif kind == 'POS' and len(currProper) != 0:
				nextToken = index + 1
				if (nextToken != len(tokens)) and (tokens[nextToken][1] == 'NNP'):
					currProper[-1] = currProper[-1] + val

			elif len(currProper) != 0:
				if len(currProper) == 1:
					s = currProper[0]
				else:
					s = " ".join(currProper)

				if s in topics:
					topics[s] += 1
				else:
					topics[s] = 1

				currProper = []

	for t in topics:
		print t, topics[t]









