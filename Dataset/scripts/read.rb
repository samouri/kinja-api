# encoding: utf-8

require 'ostruct'
require 'json'
require 'pp'

source = "articles_complete.json"
articles = []

File.open(source, "r:UTF-8") { |f|
	articles = JSON.parse(f.read)
}

pp articles[0]