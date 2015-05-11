#!/bin/bash

# This script outputs all of the urls listed in the gawker sitemap
# First it downloads the sitemap of sitemaps and then iterates through all of the sitemaps therein
# For each sitemap of articles it curls and greps from only URLS which are then sent to stdout.  It can be redirected

curl --silent http://gawker.com/sitemap.xml | grep -oP "http:(.*?)endTime.{20}" | while read -r line ; do
    curl --silent  "$line" | grep -oP "<loc><!\[CDATA\[http:(.*?)\]" | sed "s/<loc><!\[CDATA\[//" | sed "s/\]//" &
done
