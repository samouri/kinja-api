#!/bin/bash

# This script downloads all of the gawker article viewcounts and outputs it to stdout in json format.  also uses xargs for multithreading

json() { 
  regex="([0-9]{5,20})"
  url="$1";
  [[ $url =~ $regex ]];
  id="${BASH_REMATCH[1]}"; # article id
  viewcount="$(curl --silent "http://kinja.com/api/analytics/stats/post?id=$id")"
  unique="$( echo "${viewcount}" | grep -Po '"unique":.*?[^\\],' | sed 's/[^0-9]*//g')"
  nonUnique="$( echo "${viewcount}" | grep -Po '"nonUnique":.*?[^\\],' | sed 's/[^0-9]*//g')"
  
  if [ ${#unique} -eq 0 ]; then unique=0; fi
  if [ ${#nonUnique} -eq 0 ]; then nonUnique=0; fi

  echo "\"$id\": {\"unique\": $unique, \"nonUnique\": $nonUnique},";
}
export -f json


echo "{"

cat ../input/filtered_gawker_urls.txt | xargs -I {} -P 20 -n 1 -s 9999999999  bash -c "json {}"

echo "\"-1\": {\"finished\": true }"
echo "}"

