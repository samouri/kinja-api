# encoding: utf-8

# This script adds externally computed time information to the articles JSON.
# Each article is given new fields:
# * 'is_weekend': boolean value describing if the article was published on 
# 	a weekend.
# * 'hour' : integer describing the hour the article was published on, on
# 	a 24-hour clock

require 'json'
require 'pp'

article_source = "../output/articles_labeled.json"
times_source = "../output/article_times.json"

ID_REGEX = /^http:\/\/\w*\.?gawker.com\/(\d+)\/[\w-]+/

articles = JSON.parse(File.read(article_source, :encoding => "UTF-8"))
times 	= JSON.parse(File.read(times_source))

articles.keep_if{ |e| 

	e['id'] = ID_REGEX.match(e['link'])[1]
	
	if times.key?(e['id'])
		e['is_weekend'] = times[e['id']]['isweekend']
		e['hour'] = times[e['id']]['hour']

		true	
	else
		pp e['id'], e['link']

		false
	end

}

File.open(article_source, "w+") { |f|
	f.puts(articles.to_json)
}

