#!/usr/bin/env ruby

require 'open-uri'
require 'nokogiri'
require 'ostruct'
require 'pp'
require 'watir'



###############################################################################
# 1 Setup
###############################################################################

HOST            = 'http://gawker.com'
browser 		= Watir::Browser.new :chrome

branch_regex 	= /(\w+).gawker/

###############################################################################
# 2 Scrape
###############################################################################

page 	= Nokogiri::HTML(open(HOST))
links 	= []

# get article links on page
for h1 in page.css('h1.headline.h5.hover-highlight.entry-title') do links << h1.css('a')[0]['href'] end

# get attributes from each article
for link in links

	browser.goto link + '/all'
	
	begin
		browser.wait

		begin
			article_page 		= Nokogiri::HTML.parse(browser.html)

			title 		= article_page.css('h1.headline a')[0].text
			likes 		= article_page.css('.js_like_count').text
			views 		= article_page.css('.view-counts').text
			content 	= article_page.css('div.post-content.entry-content p').map { |e| e.text }.join('\n')
			author 		= article_page.css('.author a').text
			published 	= article_page.css('.published,.updated').text
			pic_count 	= article_page.css('article img').length
			tags 		= article_page.css('a.first-tag,div#taglist').text.split("\t") # TODO: handle cases of 0 or 1 tag
			branch 		= (branch_regex =~ link) ? "#{$1}" : "gawker"
			sponsored 	= (article_page.css('.sponsored-label').length) ? true : false

		rescue NoMethodError
			sleep(0.1)
			retry
		end

		comments = []

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
			
			comments << res
		}

	rescue TimeoutError
		# handle when browser wait timesout
		retry
	end
	
end

browser.close

