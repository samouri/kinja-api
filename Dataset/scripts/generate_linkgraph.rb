#!/usr/bin/env ruby

require 'open-uri'
require 'nokogiri'
require 'json'
require 'pp'
require 'ruby-progressbar'

###############################################################################
# 1 Setup
###############################################################################

host           	= 'gawker'
input			= '../output/htmls'
output			= File.open("../output/linkgraph.json","w+")

if ARGV.length > 0 then input = ARGV[0] end
if ARGV.length > 1 then host = ARGV[1] end
if ARGV.length > 2 then output = File.open(ARGV[2], "w+") end

VALID_REGEX		= /^http:\/\/\w*\.?#{Regexp.quote(host)}.com\/(\d+)\/[\w-]+/ # http://gawker.com/111361/penguins-march-on-hollywood
BRANCH_REGEX 	= /(\w+).#{Regexp.quote(host)}.com/

filepaths = Dir.glob("#{input}/*")
num_articles = filepaths.length

pb = ProgressBar.create(:format     => '%a %B %p%% %r articles/sec', :total => num_articles)

for filepath in filepaths
    f = File.open(filepath)
    if f.size == 0 then next end #pp "NO HTML"; next end
    article_page = Nokogiri::HTML(f)
    f.close

    # link
    link = ""
    if (nodeset = article_page.css('.headline.entry-title a')).length > 0
        link = nodeset.first['href']
    else
        #pp "NO LINK"
        next
    end

    # id
    id  = VALID_REGEX.match(link)[1]
    # article content
    nodeset = article_page.css('div.post-content.entry-content p')

    if (nodeset.length == 0) #handles oldstyle where was not in p tags
        nodeset = article_page.css('div.post-content.entry-content')
    end
    links = nodeset.at('a').to_a.keep_if { |e| e[1].include?("gawker.com") && !e[1].include?("window.open") && !e[1].include?("mailto")}
    links.map! do | e | 
        lnk = e[1]
        lnk_id = VALID_REGEX.match(lnk)
        lnk_id = lnk_id[1] unless lnk_id.nil?
        scanned = lnk.scan(/\d+$/).first  
        scanned = nil if ! scanned.nil? && scanned.length < 5
        (lnk_id.nil?)? scanned : lnk_id
    end
    links.delete_if do |e| e.nil? end
    adjacency_hash[id] = links
    pb.increment()
end  	

# write JSON to output
output.puts(adjacency_hash.to_json)

p "done generating adjacency grap"
