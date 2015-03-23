#!/bin/bash

#sitemaps= curl http://gawker.com/sitemap.xml | grep -oP "http:(.*?)endTime.{20}"

curl --silent http://gawker.com/sitemap.xml | grep -oP "http:(.*?)endTime.{20}" | while read -r line ; do
    curl --silent  "$line" | grep -oP "<loc><!\[CDATA\[http:(.*?)\]" | sed "s/<loc><!\[CDATA\[//" | sed "s/\]//" &
done