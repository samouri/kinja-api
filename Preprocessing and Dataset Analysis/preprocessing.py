import codecs
import json
import nltk
import re
from collections import Counter
import os.path
import datetime

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

DATASET_FNAME = "articles_labeled.json"

def init_tags():
	tags = {}
	for wordtype in WORD_TYPES:
		typelist = WORD_TYPES[wordtype]
		for tag in typelist:
			tags[tag] = []

	return tags

def clean_text(text):
	text = text.replace("\\n", " ")
	text = text.replace("\n", " ")
	return text

def get_proper_nouns(tokens):
	currProper = []
	proper_nouns = {}
	for index, tup in enumerate(tokens):
		(val, kind) = tup

		if kind == 'NNP':
			s = re.sub(r'[^-\w\.\']','', val)
			s.strip(" ")

			if (len(s) != 0):
				currProper.append(val)

		elif kind == 'POS' and len(currProper) != 0:
			nextToken = index + 1
			if (nextToken != len(tokens)) and (tokens[nextToken][1] == 'NNP'):
				currProper[-1] = currProper[-1] + val

		elif len(currProper) != 0:
			if len(currProper) == 1:
				s = currProper[0]
			else:
				s = " ".join(currProper)

			if s in proper_nouns:
				proper_nouns[s] += 1
			else:
				proper_nouns[s] = 1

			currProper = []

	return proper_nouns

def get_tagged_dict(tokens):
	tags = init_tags()
	for index, tup in enumerate(tokens):
		(val, kind) = tup
		s = re.sub(r'[^\w\-\.]','', val)

		if not kind in tags:
			tags[kind] = []

		tags[kind].append(val)

	return tags

def get_word_stats(article_text):
	article_text = article_text.lower()
	fd = nltk.FreqDist()
	stats = dict()
	
	sentences = nltk.sent_tokenize(article_text)
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

	charfreq = Counter(article_text.strip())

	stats['?'] = charfreq['?']
	stats['!'] = charfreq['?']
	stats['.'] = charfreq['?']
	stats[','] = charfreq['?']
	stats[':'] = charfreq['?']
	stats[';'] = charfreq['?']
	stats[' '] = charfreq['?']
	stats['['] = charfreq['?']
	stats['sentences'] = len(sentences)
	stats['unique'] = len(vocabulary)
	stats['words'] = totalwords
	stats['avgwordlength'] = 0 if totalwords == 0 else (totalchars/float(totalwords))
	stats['avgsentencelength'] = 0 if len(sentences) == 0 else (totalwords / float(len(sentences)))
	vocabulary = dict()
	for s in fd:
		if len(s) > 2:
			vocabulary[s] = fd[s]

	return stats, vocabulary

# Write statistics and vocabularies for each article
# Takes an extremely long time to run (24 hours or so)
def write_article_stats_and_words():
	articles = json.load(codecs.open(DATASET_FNAME, encoding='utf-8'))
	if os.path.isfile("article_stats_copy.json"):
		w = codecs.open("article_stats_copy.json", encoding='utf-8')
		articlestats = json.load(w)
	else:
		articlestats = dict()

	if os.path.isfile("article_words_copy.json"):
		w = codecs.open("article_words_copy.json", encoding='utf-8')
		articlewords = json.load(w)
	else:
		articlewords = dict()

	counter = 0
	totalnum = len(articles)
	for article in articles:
		counter += 1
		print counter, '/', totalnum
		if article['id'] in articlestats and article['id'] in articlewords:
			continue
		if not 'content' in article:
			continue

		article_text = clean_text(article['content'])
		untagged = nltk.word_tokenize(article_text)
		tokens = nltk.pos_tag(untagged)

		d = dict()

		d['propernouns'] = get_proper_nouns(tokens)
		#d['taggedwords'] = get_tagged_dict(tokens)
		stats, d['vocabulary'] = get_word_stats(article_text)

		articlewords[article['id']] = d
		articlestats[article['id']] = stats


	with codecs.open("article_stats_copy.json", 'w', encoding='utf-8') as w:
		json.dump(articlestats, w, indent=4)

	with codecs.open("article_words_copy.json", 'w', encoding='utf-8') as w:
		json.dump(articlewords, w, indent=4)

def write_time_fields():
	data = json.load(codecs.open(DATASET_FNAME, encoding="utf-8"))

	result = dict()
	for article in data:
		idnum = article['id']
		datearr = article['date_published'].split()[0].split('/')
		print datearr
		d = datetime.datetime(int(datearr[2]), int(datearr[0]), int(datearr[1]))
		isweekend = d.weekday() == 5 or d.weekday() == 6
		time = article['date_published'].split()[1]
		if time.endswith(u'am'):
			hour = int(time.split(u':')[0])
		elif time.endswith(u'pm'):
			hour = int(time.split(u':')[0]) + 12

		result[idnum] = {'hour': hour, 'isweekend': isweekend}

	json.dump(result, codecs.open("article_times.json", 'w', encoding='utf-8'), indent=4)


write_article_stats_and_words()













