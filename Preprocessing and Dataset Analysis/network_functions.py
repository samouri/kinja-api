import networkx as nx
import json
import codecs
import numpy as np
import community
import os.path

POPULAR = 4
AVERAGE = 3
UNPOPULAR = 2

DATASET_FNAME = "../Dataset/Output/articles_labeled.json"

# Used in each step of the Girvan-Newman clustering algorithm
# Functionally equivalaent to networkx's edge_betweenness_centrality(G, normalized=False)
def get_betweenness(G):
	betweenness = dict()
	for node in G.nodes():
		levels = {node: 0}
		tree = nx.bfs_edges(G, node)
		numshortest = dict()
		maxlevel = 0
		for t in tree:
			if t[1] not in levels:
				newlevel = levels[t[0]] + 1
				levels[t[1]] = newlevel
				if newlevel > maxlevel:
					maxlevel = newlevel

		l2 = dict()
		for l in levels:
			num = levels[l]
			if num not in l2:
				l2[num] = []
			l2[num].append(l)
		
		prev = node
		numshortest = {node: 1}
		for i in range(1, maxlevel + 1):
			for prev_node in l2[i - 1]:
				for curr_node in l2[i]:
					if curr_node not in numshortest:
						numshortest[curr_node] = 0

					if G.has_edge(prev_node, curr_node):
						numshortest[curr_node] += numshortest[prev_node]

		nodeflow = dict()
		edgeflow = dict()
		for n in l2[maxlevel]:
			nodeflow[n] = 1


		for i in range(maxlevel, 0, -1):
			for k in l2[i]:
				neighborsabove = [s for s in G.neighbors(k) if levels[s] == i - 1]
				totalshortest = sum([numshortest[neighbor] for neighbor in neighborsabove])
				for neighbor in neighborsabove:
					if k not in nodeflow:
						nodeflow[k] = 1
					if neighbor not in nodeflow:
						nodeflow[neighbor] = 1

					edgeflow[(k, neighbor)] = float(nodeflow[k] * numshortest[neighbor]) / totalshortest


					nodeflow[neighbor] += edgeflow[(k,neighbor)]

		for edge in edgeflow:
			sor = tuple(sorted(edge))
			if sor not in betweenness:
				betweenness[sor] = 0
			betweenness[sor] += edgeflow[edge]
	for e in betweenness:
		betweenness[e] = betweenness[e] / 2

	return betweenness

def remove_single_nodes(G):
	toremove = set()
	for node in G:
		if len(G.neighbors(node)) == 0:
			toremove.add(node)
	for r in toremove:
		G.remove_node(r)

# Cluster the graph in an accurate but extremely slow way
# k = minimum number of clusters to split graph into
# This is too slow to test on tag graph, try testing with
# nx.dorogovtsev_goltsev_mendes_graph(5) and k=5 instead
def Girvan_Newman_cluster(Graph, k, write_to_file=False, use_nx_betweeness=False):
	print "Finding Girvan Newman communities."
	G = Graph.copy()

	while(True):

		remove_single_nodes(G)
		i = nx.number_connected_components(G)

		if i >= k or len(G.edges()) == 0:
			break

		if use_nx_betweeness:
			# Below is networkx's implementation of betweeness. 
			# Mine returns identical results but is slower
			betweenness = nx.edge_betweenness_centrality(G, normalized=False)
		else:
			# My betweenness function
			betweenness = get_betweenness(G)

		most_between = sorted(betweenness, key=lambda key: betweenness[key], reverse=True)[0]

		G.remove_edge(most_between[0], most_between[1])

	if write_to_file:
		print "Writing Girvan Newman graph to a file."
		nx.write_gml(G, "GirvanNewman.gml")

	return G

# Each node represents a tag
# Each edge represents an article that shares two tags
# Edges are weighted based on how many articles share those two tags
def get_tags_network(remove_rare_tags=False, save_gml=False):
	print "Creating the tags network."
	with codecs.open(DATASET_FNAME, encoding='utf-8') as f:
		data = json.load(f)

	G = nx.Graph()
	for d in data:
		if len(d['tags']) == 0:
			continue

		firstTag = d['tags'][0]
		for i in range(1, len(d['tags'])):
				t1 = d['tags'][i]
				t2 = firstTag
				try:
					str(t1)
					str(t2)
				except:
					continue

				for t in (t1, t2):
					if G.has_node(t):
						G.node[t]['occurrences'] += 1
					else:
						G.add_node(t, occurrences = 1)

				if  G.has_edge(t1,t2):
					G[t1][t2]['weight'] += 1
				else:
					G.add_edge(t1,t2,weight=1)

	G = G.to_undirected()

	if remove_rare_tags:
		toremove = set()
		for g in  G.nodes():
			if G.node[g]['occurrences'] <= 5:
				toremove.add(g)
				continue
			print g
		print "Removing ", len(toremove)
		for r in toremove:
			G.remove_node(r)

	if save_gml:
		print "Writing tag_graph.gml"
		nx.write_gml(G,"tag_graph.gml")

	return G

# creates and partitions the tag graph into communities
def partition_tag_graph(remove_small_partitions=True):
	print "Partitioning tag graph."
	G = get_tags_network()
	partition = community.best_partition(G)

	count = 0
	for com in set(partition.values()):
		count += 1
	print "Found", count, "partitions."

	x = dict()
	for node in partition:
		c = partition[node]
		if c not in x:
			x[c] = []
		x[c].append({'tag':node, 'strength':G.node[node]['occurrences']})

	if remove_small_partitions:
		toremove = set()
		for l in x:
			if len(x[l]) < 20:
				toremove.add(l)

		for r in toremove:
			del x[r]

	json.dump(x, codecs.open("communities.json",'w', encoding='utf-8'), indent=4)

# Popularity of community c = # popular articles in c / total num articles in c
def print_community_data(print_tag_data=False):
	if not os.path.isfile("communities.json"):
		partition_tag_graph()

	communities = json.load(codecs.open("communities.json", encoding='utf-8'))
	data = json.load(codecs.open(DATASET_FNAME, encoding='utf-8'))

	tagvals = dict()
	popularities = dict()

	for d in data:
		for t in d['tags']:
			if t not in tagvals:
				tagvals[t] = []
				popularities[t] = {'unpopular':0, 'average':0, 'popular':0}
			tagvals[t].append(d['views']['nonunique'])
			if d['label'] == UNPOPULAR:
				popularities[t]['unpopular'] += 1
			elif d['label'] == AVERAGE:
				popularities[t]['average'] += 1
			elif d['label'] == POPULAR:
				popularities[t]['popular'] += 1

	if print_tag_data:
		for t in popularities:
			print t
			print "   unpopular:", popularities[t]['unpopular']
			print "   average:", popularities[t]['average']
			print "   popular:", popularities[t]['popular']
			print

	comstats = dict()
	for c in communities:
		comstats[c] = []
		compops = {'unpopular':0, 'average':0, 'popular':0}
		for tag in communities[c]:
			tag = tag['tag']
			if tag not in tagvals:
				continue
			compops['unpopular'] += popularities[tag]['unpopular']
			compops['average'] += popularities[tag]['average']
			compops['popular'] += popularities[tag]['popular']
			comstats[c].extend(tagvals[tag])
		total = float(compops['unpopular'] + compops['popular'] + compops['average'])
		print "Community", c, 'popularity', compops['popular']/total
		print "Community", c, 'unpopularity', compops['unpopular']/total
		print

	print 'community, num_articles, std_dev, mean, median'
	for i in comstats:
		num_articles = len(comstats[i])
		std_dev = np.std(comstats[i])
		mean = np.mean(comstats[i])
		median = np.median(comstats[i])
		#plt.hist(comstats[i], bins=range(0,500000, 500))
		#plt.show()
		print i, num_articles, std_dev, mean, median

# Creates a network where nodes represent articles and directed edges
# are links between articles.
def create_article_network(save_gml=False):
	print "Creating article network."
	with codecs.open("linkgraph.json", encoding='utf-8') as f:
		data = json.load(f)

	with codecs.open(DATASET_FNAME, encoding='utf-8') as f:
		articles = json.load(f)

	d = dict()
	for article in articles:
		d[article['id']] = (article['title'], article['views']['nonunique'])

	G = nx.DiGraph()

	for idnum in data:
		for link in data[idnum]:
			if link == idnum or idnum not in d or link not in d:
				continue
			try:
				str(d[idnum][0])
				str(d[link][0])
			except:
				continue

			G.add_node(idnum, size=d[idnum][1])
			G.add_node(link, size=d[link][1])
			G.add_edge(idnum, link)

	ccs = nx.connected_components(G.to_undirected())
	ccs = sorted(ccs, lambda x,y: cmp(len(x), len(y)), reverse=True)
	H = nx.Graph()
	for i in range(20):
		comp1 = ccs[i]
		for i in ccs[i]:
			H.add_edges_from(G.out_edges(i))

	if save_gml:
		nx.write_gml(H, "linkgraph.gml")

	return G

# Prints a summary of how popularity probability reates to article indegree
# NOTE: indegree 0 is not all articles with indegree 0, only the subset of articles
# found in the linkgraph.
def print_popularity_by_indegree():
	G = create_article_network()
	degrees = dict()
	for i in G.nodes():
		indeg = G.in_degree(i)
		if indeg not in degrees:
			degrees[indeg] = []

		degrees[indeg].append(i)

	data = json.load(codecs.open(DATASET_FNAME, encoding="utf-8"))
	d2 = dict()

	totalpop = 0
	totalunpop = 0
	for d in data:
		d2[d['id']] = d
		if d['label'] == UNPOPULAR:
			totalunpop += 1
		elif d['label'] == POPULAR:
			totalpop += 1

	popularity = float(totalpop) / len(data)
	unpopularity = float(totalunpop) / len(data)
	print "Total average popularity =", popularity
	print "Total avearage unpopularity =", unpopularity

	data = d2
	for i in degrees:
		ipop = 0
		iunpop = 0
		for idnum in degrees[i]:
			if data[idnum]['label'] == UNPOPULAR:
				iunpop += 1
			elif data[idnum]['label'] == POPULAR:
				ipop += 1

		popularity = float(ipop) / len(degrees[i])
		unpopularity = float(iunpop) / len(degrees[i])
		print len(degrees[i]), "articles wtih indegree", i
		print "    Popularity =", popularity
		print "    Unpopularity =", unpopularity
		# print '\t'.join([str(len(degrees[i])), str(i), str(popularity), str(unpopularity)])

print_community_data()





