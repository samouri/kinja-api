# encoding: utf-8

# This script takes a viewcount JSON (made with viewcount.sh) and a JSON file of articles.
# It adds each article's view stats to its corresponding article hash and writes the 
# array of article JSONs to another JSON file

require 'ostruct'
require 'json'
require 'pp'

article_source = "../output/articles.json"
viewcount_source = "../output/viewcounts.json"
articles = []
viewcounts = []

ID_REGEX = /^http:\/\/\w*\.?gawker.com\/(\d+)\/[\w-]+/

f = File.open(article_source, "r:UTF-8") { |f| 
	articles = f.readlines.map { |e| JSON.parse(e.chomp!) }
}

viewcounts = JSON.parse(File.read(viewcount_source))

articles.keep_if{ |e| 

	e['id'] = ID_REGEX.match(e['link'])[1]
	
	if viewcounts.key?(e['id'])
		e['views'] = {}
		e['views']['unique'] = viewcounts[e['id']]["unique"]
		e['views']['nonunique'] = viewcounts[e['id']]['nonUnique']

		true	
	else
		pp e['id'], e['link']

		false
	end

}

File.open("../output/articles_complete.json", "w+") { |f|
	f.puts(articles.to_json)
}

