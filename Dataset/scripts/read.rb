# encoding: utf-8

require 'ostruct'
require 'json'
require 'pp'

source = "../output/articles_complete.json"
articles = []

File.open(source, "r:UTF-8") { |f|
	articles = JSON.parse(f.read)
}

# 97848 articles_complete
# pp articles.length