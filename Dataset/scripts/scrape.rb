#!/usr/bin/env ruby

# encoding: utf-8

# $ruby scrape.rb INPUT-FOLDER HOST OUTPUT GET-COMMENTS
# 
# This script takes in a list of urls (input) and a host website string, and 
# it creates json object sfor each article. It then prints each JSON object to
# the given output file.
#
# The host werbsite needs to be one of the Kinja sites. URLs need to be in a valid
# format, as indicated in VALID_REGEX. The script handles invalid urls (ex. gaw.com).
# 
# GET-COMMENTS is a boolean that tells the script whether to also process comments.
# 
# Defaults
# * INPUT-FOLDER= "../output/1000-article-htmls/"
# * HOST= "gawker"
# * OUTPUT= "output.json"
# * GET-COMMENTS= false

require 'open-uri'
require 'nokogiri'
require 'json'
require 'pp'
require 'ruby-progressbar'

###############################################################################
# 1 Setup
###############################################################################

NUM_THREADS 	= 1

host           	= 'gawker'
input			= '../output/htmls'
output			= File.open("../output/articles.json","w+")
get_comments	= false

if ARGV.length > 0 then input = ARGV[0] end
if ARGV.length > 1 then host = ARGV[1] end
if ARGV.length > 2 then output = File.open(ARGV[2], "w+") end
if ARGV.length > 3 then get_comments = ARGV[3].to_b end

VALID_REGEX		= /^http:\/\/\w*\.?#{Regexp.quote(host)}.com\/\d+\/[\w-]+/ # http://gawker.com/111361/penguins-march-on-hollywood
BRANCH_REGEX 	= /(\w+).#{Regexp.quote(host)}.com/

filepaths = Dir.glob("#{input}/*")
num_articles = filepaths.length
filepaths = filepaths.each_slice( (filepaths.length / NUM_THREADS.to_f).round ).to_a

output.sync = true

###############################################################################
# 2 Scrape
###############################################################################

pb = ProgressBar.create(:format     => '%a %B %p%% %r articles/sec', :total => num_articles)

#  threading
threads = (0...NUM_THREADS).map do |i|
    Thread.new(i) do |i|

        for filepath in filepaths[i]

            f = File.open(filepath)
            if f.size == 0 then next end #pp "NO HTML"; next end
            article_page = Nokogiri::HTML(f)
            f.close

            begin
                article = {}

                # link
                if (nodeset = article_page.css('.headline.entry-title a')).length > 0
                    article['link'] = nodeset.first['href']
                else
                    #pp "NO LINK"
                    next
                end

                # title
                article['title'] 			= article_page.css('.headline.entry-title a').first.text

                # author
                if (nodeset = article_page.css('.author a')).length > 0
                    article['author'] = nodeset.first.text
                else
                    #pp "NO AUTHOR"
                    next
                end

                # date published
                if (nodeset = article_page.css('.published,.updated')).length > 0
                    article['date_published'] = nodeset.first.text
                else
                    #pp "NO DATE PUBLISHED"
                    next
                end

                # like count
                if (nodeset = article_page.css('span.js_like_count')).length > 0
                    if (text = nodeset.first.text).length > 0
                        article['likes'] = text.scan(/\d+/).join().to_i
                    else
                        article['likes'] = 0
                    end
                else
                    #pp "NO LIKE COUNT"
                    next
                end
=begin
                # view count
                if (nodeset = article_page.css('.view-count')).length > 0
                    if (text = nodeset.first.text).length > 0
                        article.views = text.scan(/\d+/).join().to_i
                    else
                        article.views = 0
                    end
                else
                    #pp "NO VIEW COUNT"
                    next
                end
TODO: add viewcount in 
=end
                # tags
                if (nodeset = article_page.css('a.first-tag,div#taglist')).length > 0
                    article['tags'] = nodeset.text.split("\t")
                else
                    #pp "NO TAGS"
                    next
                end

                # branch from main site
                article['branch'] 			= (BRANCH_REGEX =~ article['link']) ? $1 : "gawker"

                # is a sponsored article
                article['is_sponsored'] 	= (article_page.css('.sponsored-label').length != 0) ? true : false

                # article pic count
                article['pic_count'] 		= article_page.css('.post-content img').length

                # article content
                if (nodeset = article_page.css('div.post-content.entry-content p')).length > 0
                    article['content'] = nodeset.map { |e| e.text }.join('\n')
                elsif (nodeset = article_page.css('div.post-content.entry-content')).length > 0
                    # handles old format where text isn't in p tags
                    article['content'] = nodeset.text
                end

            rescue NoMethodError => e
                if e.backtrace.inspect =~ /scrape.rb:(\d+)/
                    pp "Skipping #{filepath} because of NoMethodError; line #{$1}"
                end
                next
            end

            # if comments are requested for
            if get_comments == true

                article['comments'] = []

                # for each branch
                article_page.css('div.js_branch').map { |branch|

                    author 			= branch.css('.js_reply')[0]['data-authorname']
                    author_comment 	= branch.css('.js_reply div.reply-content').text
                    res 			= [[author, author_comment]]

                    # for each reply in branch
                    branch.css('section.timeline-replies .js_reply').map { |reply|
                        a = reply.css('.display-name a').text
                        c = reply.css('div.reply-content').text

                        res << [a,c]
                    }

                    article['comments'] << res
                }

            end

            # write JSON to output
            output.puts(article.to_json)
            pb.increment()
        end  	
    end
end

threads.each {|t| t.join}

