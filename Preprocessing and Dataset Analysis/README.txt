network_functions.py

	This file contains functions to create and analyze the tag and links networks.
	Required modules:
		networkx, json, codecs, numpy, community, os.path
	

	Tag network functions:
		get_tags_network(remove_rare_tags=False, save_gml=False)
			Description: 
				creates and returns the tags network.
				Each node represents a tag
				Each edge represents an article that shares two tags
				Edges are weighted based on how many articles share those two tags

			Parameters:
				remove_rare_tags - removes any tags that aren't present in more
					than 5 separate articles.
				save_gml - if true, saves the graph to gml file for viewing in
					prorams like Gephi.

			Returns:
				tag network graph as networkx graph object

		partition_tag_graph(remove_small_partitions=True)
			Description: uses the Louvain method to partition tag graph into
				communities

			Parameters:
				remove_small_partitions - if True, removes all partitions
					with fewer than 20 nodes

			Returns:
				nothing. Outputs to communities.json file

		print_community_data(print_tag_data=False)
			Description: 
				finds the popularity of each community
				If there does not exist a communities.json file, will call
					partion_tag_graph to make one
				Popularity of community c = 
					# popular articles in c / total num articles in c

			Parameters:
				print_tag_data - if True, prints number of popular, unpopular
					and average articles associated with each tag (lots of output)

			Returns:
				Nothing. Prints statistics about each community.

		Girvan_Newman_cluster(Graph, k, write_to_file=False)
			Description: 
				Cluster the raph using G-N algorithm learned in class
				Can use either my or networkx's betweenness implementation
				Single nodes are removed on each pass
				Extremely slow, too slow to test on tag graph
				Test with nx.dorogovtsev_goltsev_mendes_graph(5) and k=5 instead

			Parameters:
				Graph: the graph to cluster
				k: the number of clusters to split graph into
				write_to_file: write result to GML file
				use_nx_betweenness: if true, use networkx's implementation
					of betweenness

			Returns:
				the graph split into cluster (with removed edges)

		get_betweenness(G):
			Description:
				Finds the betweenness of every edge in a graph
				Used in each step of the Girvan-Newman algorithm
				Functionally equivalaent to networkx's edge_betweenness_centrality

	Article link network functions:
		create_article_network(save_gml=False)
			Description: 
				Creates a network where nodes represent articles
					and directed edges are links btw articles
				Requires the "linkgraph.json" file because the 
					linkdata is not part of main dataset


			Parameters:
				save_gml: saves network to gml file if True

			Returns:
				the graph created

		print_popularity_by_indegree()
			Description:
				Prints a summary of how popularity probability reates to article indegree
				NOTE: indegree 0 is not all articles with indegree 0, only the 
					subset of articles found in the linkgraph.

			Returns:
				Nothing but prints popularity data for each indegree level.

preprocessing.py

	This file contains functions that were used to find word stats of each article.
	Was used to create the data in the article_times, article_vocabulary, 
		and article_stats json files.

	Required modules:
		codecs
		json
		re
		nltk
		Counter
		datetime
