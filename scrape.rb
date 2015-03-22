#!/usr/bin/env ruby

require 'open-uri'
require 'nokogiri'
require 'ostruct'
require 'watir'
require 'pp'


###############################################################################
# 1 Setup
###############################################################################

HOST            = 'http://gawker.com'
VALID_REGEX		= /^http:\/\/\w*\.?gawker.com\/\d+\/[\w-]+/ # http://gawker.com/111361/penguins-march-on-hollywood
BRANCH_REGEX 	= /(\w+).gawker.com/

input			= 'gawker_urls.txt'
output			= File.open("output.json","w+")
browser 		= Watir::Browser.new :chrome
links 			= []
get_comments	= false

if ARGV.length > 0 then input = ARGV[0] end
if ARGV.length > 1 then output = ARGV[1] end
if ARGV.length > 2 then get_comments = ARGV[2].to_b end

###############################################################################
# 2 Scrape
###############################################################################

# get article links from homepage
# page = Nokogiri::HTML(open(HOST))
# for h1 in page.css('h1.headline.h5.hover-highlight.entry-title') do links << h1.css('a')[0]['href'] end

# get article links from text file
links = File.readlines(input).map { |e| e.chomp!  }

# get attributes from each article
for link in links

	if !(link =~ VALID_REGEX) then next end

	browser.goto link
	article = OpenStruct.new
	
	article.link = link

	begin
		browser.wait

		begin
			article_page 			= Nokogiri::HTML.parse(browser.html)

			article.title 			= article_page.css('h1.headline a')[0].text
			article.author 			= article_page.css('.author a').first.text
			article.date_published 	= article_page.css('.published,.updated').first.text
			article.likes 			= article_page.css('span.js_like_count').first.text
			article.views 			= article_page.css('.view-count').first.text
			article.tags 			= article_page.css('a.first-tag,div#taglist').text.split("\t") # TODO: handle cases of 0 or 1 tag
			article.branch 			= (BRANCH_REGEX =~ link) ? "#{$1}" : "gawker"
			article.is_sponsored 	= (article_page.css('.sponsored-label').length != 0) ? true : false
			article.pic_count 		= article_page.css('article img').length
			article.content 		= article_page.css('div.post-content.entry-content p').map { |e| e.text }.join('\n')

		rescue NoMethodError
			sleep(0.1)
			retry

		end

		# if comments are requested for
		if get_comments == true
			article.comments = []
			
			browser.link(:text => "All replies").when_present(5).click
			browser.wait
			sleep(5)

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
				
				article.comments << res
			}

		end

	output.write(article.to_json)

	break

	rescue TimeoutError
		# handles when browser wait times out
		retry

	end
end

browser.close

