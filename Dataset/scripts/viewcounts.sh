#!/bin/bash

#sitemaps= curl http://gawker.com/sitemap.xml | grep -oP "http:(.*?)endTime.{20}"
regex="([0-9]{5,20})"

echo "{"
while read url
do 
 (
  [[ $url =~ $regex ]]
  id="${BASH_REMATCH[1]}"

  viewcount="$(curl --silent "http://kinja.com/api/analytics/stats/post?id=$id")"
  unique="$( echo "${viewcount}" | grep -Po '"unique":.*?[^\\],' | sed 's/[^0-9]*//g')"
  nonUnique="$( echo "${viewcount}" | grep -Po '"nonUnique":.*?[^\\],' | sed 's/[^0-9]*//g')"
  
  echo "'$id': {'unique': $unique, 'nonUnique': $nonUnique}," )
done < "${1:-/dev/stdin}"

echo "'-1': {'finished': true }}"
