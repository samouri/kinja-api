#!/bin/bash

html() { 
  url="$1";
  regex="[^0-9a-z.-]"
  filename="$(echo $url | sed s/"$regex"//g)"

   curl --silent "${url}" > "../output/htmls/${filename}"
}
export -f html

cat ../input/filtered_gawker_urls.txt | xargs -I {} -P 20 -n 1 -s 9999999999  bash -c "html {}"

