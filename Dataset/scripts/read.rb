# encoding: utf-8

require 'ostruct'
require 'json'
require 'pp'

filename = "../output/output.json"
articles = []

File.open(filename, "r:UTF-8") { |f|
	articles = f.readlines.map { |e| OpenStruct.new(JSON.parse(e.chomp!)) }
}
 
pp articles



