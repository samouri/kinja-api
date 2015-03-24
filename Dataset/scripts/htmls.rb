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

NUM_THREADS		= 1

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
browsers = (1..NUM_THREADS).map { |x| Watir::Browser.new :chrome }

#  threading
threads = (0...NUM_THREADS).map do |i|
    Thread.new do
    	browser = browsers[i]
		for link in links[i]
            browser.goto link
            sleep(0.1) until browser.html.include?("\"view-count\"")
            path = URI.parse(link).path.gsub(/[^0-9a-z.-]/i, '') # only keep alphanumeric
            p path
            File.open("#{output}#{path}.html", 'w+') {|f| f.write(browser.html) }
            p "successs"
		end
  	end
end

begin 
    threads.each {|t| t.join}
rescue SystemExit, Interrupt 
    p 'exiting because of siging'
ensure
    browsers.each do |b| b.close end
end
