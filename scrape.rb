#!/usr/bin/env ruby

require 'open-uri'
require 'nokogiri'
require 'ostruct'
require 'pp'

###############################################################################
# 1 Setup
###############################################################################

HOST            = 'http://gawker.com'


###############################################################################
# 2 Scrape
###############################################################################

page = Nokogiri::HTML(open(HOST))

links = []
for h1 in page.css('h1.headline.h5.hover-highlight.entry-title') do links << h1.css('a')[0]['href'] end

for link in links 
  article_page = Nokogiri::HTML(open(link))

  title = article_page.css('h1.headline.hover-highlight.entry-title a')[0].text
  likes = article_page.css('.js_like_count').text
  # views = article_page.xpath('')
  content = article_page.css('div.post-content.entry-content p').map { |e| e.text  }.join('\n')
  author = article_page.css('.author a').text
  published = article_page.css('.published,.updated').text
  pic_count = article_page.css('article img').length
end

