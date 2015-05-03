# encoding: utf-8

require 'ostruct'
require 'json'
require 'pp'

source = "../output/articles.json"
articles = []

File.open(source, "r:UTF-8") { |f|
	articles = JSON.parse(f.read)
}
