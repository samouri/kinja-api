#!/bin/bash

# This script uses xargs in order to download all of the gawker url articles.  xargs is used as an easy way to multithread (-P feature of xargs).

html() { 
  url="$1";
  regex="[^0-9a-z.-]"
  filename="$(echo $url | sed s/"$regex"//g)"

   curl --silent "${url}" > "../output/htmls/${filename}"
}
export -f html

cat ../input/filtered_gawker_urls.txt | xargs -I {} -P 20 -n 1 -s 9999999999  bash -c "html {}"

