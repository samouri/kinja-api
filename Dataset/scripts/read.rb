# encoding: utf-8

require 'ostruct'
require 'json'
require 'pp'

source = "../output/articles_labeled.json"

articles = JSON.parse(File.read(source, :encoding => "UTF-8"))

# 132,973 articles
pp articles.length