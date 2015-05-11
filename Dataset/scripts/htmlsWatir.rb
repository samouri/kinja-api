# performs the same job as htmls.sh EXCEPT this uses a browser driver and waits until viewcounts is part of the html. deemed a bad solution compared to separately performing the query for viewcounts because this is slow

# DEPRECATED FILE

require 'open-uri'
require 'nokogiri'
require 'watir'
require 'pp'


###############################################################################
# 1 Setup
###############################################################################

NUM_THREADS		= 8

host 			= "gawker"
input 			= '../input/filtered_gawker_urls.txt'
output			= "../output/1000-article-htmls/"
links 			= []

if ARGV.length > 0 then input = ARGV[0] end
if ARGV.length > 1 then host = ARGV[1] end

VALID_REGEX		= /^http:\/\/\w*\.?#{Regexp.quote(host)}.com\/\d+\/([\w-]+)/ # http://gawker.com/111361/penguins-march-on-hollywood

###############################################################################
# 2 Download
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
            File.open("#{output}#{path}.html", 'w+') {|f| f.write(browser.html) }
		end
  	end
end

threads.each {|t| t.join}

