#!/bin/sh

for i in ../pdf/*.pdf; do
  fn=`basename "$i" .pdf`
  echo $fn
  pdftohtml -noframes -c "$i"
done
mv ../pdf/*.html ../html/