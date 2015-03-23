# $ruby htmls.rb INPUT-FILE HOST
# 
# This script takes in a list of urls (input) and a host website string, and it
# downloads the htmls of each page to a separate file.
#
# Html files are placed in subfolder: ./articles, with a number for the name.
# The host werbsite needs to be one of the Kinja sites. URLs need to be in a valid
# format, as indicated in VALID_REGEX. The script handles invalid urls (ex. gaw.com).
# 
# Defaults:
# * INPUT-FILE= "./input/gawker_urls.txt"
# * HOST= "gawker"

require 'open-uri'
require 'nokogiri'
require 'watir'
require 'pp'


###############################################################################
# 1 Setup
###############################################################################

NUM_THREADS		= 5

host 			= "gawker"
input 			= '../input/filtered_gawker_urls.txt'
output			= "../output/1000-article-htmls/"
links 			= []


if ARGV.length > 0 then input = ARGV[0] end
if ARGV.length > 1 then host = ARGV[1] end

VALID_REGEX		= /^http:\/\/\w*\.?#{Regexp.quote(host)}.com\/\d+\/([\w-]+)/ # http://gawker.com/111361/penguins-march-on-hollywood

###############################################################################
# 2 Scrape
###############################################################################

# get article links from text file, split into suba-rrays to give to each thread
links = File.readlines(input).map { |e| e.chomp!  } # 140,431 links
links = links.each_slice( (links.size / NUM_THREADS.to_f).round ).to_a

#  threading
threads = (0...NUM_THREADS).map do |i|
    Thread.new(i) do |i|

    	browser = Watir::Browser.new :chrome

		for link in links[i]
			begin
				browser.goto link
				Watir::Wait.until {browser.html.include? "\"view-count\""}

				if browser.html.length == 0 or !(browser.html.include? "\"view-count\"")
					# handles when nothing was loaded, or view-count still isn't there
					pp "redoing"
					redo
				end

				if link =~ VALID_REGEX
					title = $1
				else
					raise "invalid link"
				end

				File.open("#{output}#{title}.html", 'w+') {|f| f.write(browser.html) }

			rescue Watir::Wait::TimeoutError
				# handles when browser wait times out
				pp "retrying"
				retry

			end
		end

		browser.close

  	end
end
 
threads.each {|t| t.join}

