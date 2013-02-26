This is a small set of script to extract candidcacy lists from the political parties and convert them into a json format.
The PDF files were taken from http://www.kiesraad.nl/nieuws/kandidatenlijsten-bekend

Requirements
============

1. `pdftotext` (install xpdf)

Installation
============

1. Clone the git repository

Usage
=====

1. `cd $OPENKANDIDATELIJST_HOME/bin`
2. `mkdir ../text && mkdir ../json`
2. `./convert.sh`
3. `cd ../json #contains json files`
