import nltk
import sys
import re
from collections import Counter
from nltk.corpus import brown

WORD_TYPES = {
	'VERBS' : ['VB','VBD','VBG','VBN','VBP','VBZ'],
	'PREPOSITIONS' : ['IN'],
	'NOUNS' : ['NN', 'NNS','NNP','NNPS'],
	'PRONOUNS' : ['PRP','PRP$', 'WB', 'WP$'],
	'ADVERBS' : ['RB','RBR','RBS', 'WRB'],
	'NUMBERS' : ['CD'],
	'PUNCTUATION' : [',',':','.'],
	'DETERMINERS' : ['DT','WDT']
}

# Fixes encoding issues
reload(sys)
sys.setdefaultencoding('UTF8')

fname = "roadtomontgomery.txt"

def init_tags():
	tags = {}
	for wordtype in WORD_TYPES:
		typelist = WORD_TYPES[wordtype]
		for tag in typelist:
			tags[tag] = []

	return tags

with open(fname) as f:
	tags = init_tags()
	for line in f:
		line = line.replace(u'\u2014',' ')
		line = line.replace(u'\u2013',' ')
		tokens = nltk.word_tokenize(line)

		# uses Penn Treebank Tagset
		tokens = nltk.pos_tag(tokens)

		for index, tup in enumerate(tokens):
			(val, kind) = tup
			s = re.sub(r'[^\w\-\.]','', val)

			if not kind in tags:
				tags[kind] = []

			tags[kind].append(val)

with open(fname) as f:
	fd = nltk.FreqDist()
	text = f.read().lower()

	sentences = nltk.sent_tokenize(text)
	for sent in sentences:
		for word in nltk.word_tokenize(sent):
			fd[word] += 1

	vocabulary = fd.keys()

	totalwords = 0
	totalchars = 0
	for word in vocabulary:
		totalwords += fd[word]

		wordchars = len(word)
		totalchars += wordchars * fd[word]

	charfreq = Counter(text.strip())

	print "? = ", charfreq['?']
	print "! = ", charfreq['!']
	print ". = ", charfreq['.']
	print ", = ", charfreq[',']
	print ": = ", charfreq[':']
	print "; = ", charfreq[';']
	print "spaces = ", charfreq[' ']
	print "[] = ", charfreq['[']
	print "Sentences = ", len(sentences)
	print "Unique Words = ",len(vocabulary)
	print "Total Words = ", totalwords
	print "Avg word length = ", (totalchars/float(totalwords))
	print "Avg sentence length = ", (totalwords / float(len(sentences)))

	print "MOST COMMON WORDS"
	for s,f in fd.most_common(30):
		print s,f


for wordtype in WORD_TYPES:
	typelist = WORD_TYPES[wordtype]
	num = 0
	for tag in typelist:
		num += len(tags[tag])
	print wordtype + " = ", num










