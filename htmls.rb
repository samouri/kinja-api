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
# * INPUT-FILE= "gawker_urls.txt"
# * HOST= "gawker"

require 'open-uri'
require 'nokogiri'
require 'watir'
require 'pp'


###############################################################################
# 1 Setup
###############################################################################

host 			= "gawker"
input 			= 'gawker_urls.txt'
browser 		= Watir::Browser.new :chrome
links 			= []
i 				= 1

if ARGV.length > 0 then input = ARGV[0] end
if ARGV.length > 1 then host = ARGV[1] end

VALID_REGEX		= /^http:\/\/\w*\.?#{Regexp.quote(host)}.com\/\d+\/[\w-]+/ # http://gawker.com/111361/penguins-march-on-hollywood

###############################################################################
# 2 Scrape
###############################################################################

# get article links from text file
links = File.readlines(input).map { |e| e.chomp!  }

# write article html to file
for link in links

	# if link is not valid, skip
	if !(link =~ VALID_REGEX) then next end
	
	begin			
		browser.goto link
		browser.wait

		File.open("./articles/#{i}.txt", 'w+') {|f| f.write(browser.html) }

		i += 1

	rescue TimeoutError
		# handles when browser wait times out
		retry

	end
end

browser.close

