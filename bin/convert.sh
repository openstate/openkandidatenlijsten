#!/bin/sh

for i in ../pdf/*.pdf; do
  fn=`basename "$i" .pdf`
  echo $fn
  pdftotext -layout -nopgbrk -q "$i" "../text/$fn.txt"
done
