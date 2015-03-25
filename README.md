This script extracts candidacy lists from the political parties as published by de Kiesraad or de Staatscourant in PDF and converts them to JSON and CSV.
The PDF files were taken from:

- Europese Parlementsverkiezingen
  - [2009](https://zoek.officielebekendmakingen.nl/stcrt-2009-7040.html)
  - [2014](https://www.kiesraad.nl/nieuws/uitspraak-beroepszaken-kandidaatstelling-europees-parlement)
- Tweede Kamerverkiezingen
  - [2010](https://zoek.officielebekendmakingen.nl/stcrt-2010-7565.html)
  - [2012](https://www.kiesraad.nl/nieuws/kandidatenlijsten-bekend) ([alternative](https://zoek.officielebekendmakingen.nl/stcrt-2012-16691.html))
- Eerste Kamerverkiezingen
  - [2007](https://zoek.officielebekendmakingen.nl/stcrt-2011-7988.html)
  - [2011](https://zoek.officielebekendmakingen.nl/stcrt-2011-7988.html)
- Provinciale Statenverkiezingen
  - [2015](https://www.kiesraad.nl/nieuws/kandidatenlijsten-provinciale-statenverkiezingen-definitief-vastgesteld)
- Waterschapsverkiezingen
  - [2015](https://www.kiesraad.nl/nieuws/kandidatenlijsten-waterschapsverkiezingen-definitief-vastgesteld)
- Gemeenteraadsverkiezingen
  - 2014
    - [Amsterdam](http://archief10.archiefweb.eu/archives/archiefweb/20140328204930/http://www.amsterdam.nl/verkiezingen/geldige-lijsten/)

Elections which have not yet been processed (listing PDF file if available):

- all others before 1998 :)
- [1998 Tweede Kamerverkiezingen](https://zoek.officielebekendmakingen.nl/stcrt-1998-69-p0-SC13361.html)
- [1999 Eerste Kamerverkiezingen](https://zoek.officielebekendmakingen.nl/stcrt-1999-90-p10-SC18872.html)
- [1999 Europese Parlementsverkiezingen](https://zoek.officielebekendmakingen.nl/stcrt-1999-91-p7-SC18884.html)
- [2002 Tweede Kamerverkiezingen](https://zoek.officielebekendmakingen.nl/stcrt-2002-75-p22-SC34204.html)
- 2003 Tweede Kamerverkiezingen 
- 2003 Eerste Kamerverkiezingen
- [2004 Europese Parlementsverkiezingen](https://zoek.officielebekendmakingen.nl/stcrt-2004-92-p32-SC65111.html)
- [2006 Tweede Kamerverkiezingen](https://zoek.officielebekendmakingen.nl/stcrt-2006-207-p18-SC77436.html) ([rectification](https://zoek.officielebekendmakingen.nl/stcrt-2006-209-p10-v1-SC77469.html))
- 2014 Gemeenteraadsverkiezingen
  - Amsterdam [stadsdeel Centrum](http://archief10.archiefweb.eu/archives/archiefweb/20140328184006/http://www.amsterdam.nl/verkiezingen/geldige-lijsten/kandidatenlijsten/)
  - Amsterdam [stadsdeel Nieuw-West](http://archief10.archiefweb.eu/archives/archiefweb/20140328184006/http://www.amsterdam.nl/verkiezingen/geldige-lijsten/kandidatenlijsten-0/)
  - Amsterdam [stadsdeel Noord](http://archief10.archiefweb.eu/archives/archiefweb/20140328184006/http://www.amsterdam.nl/verkiezingen/geldige-lijsten/kandidatenlijsten-1/)
  - Amsterdam [stadsdeel Oost](http://archief10.archiefweb.eu/archives/archiefweb/20140328184006/http://www.amsterdam.nl/verkiezingen/geldige-lijsten/kandidatenlijsten-2/)
  - Amsterdam [stadsdeel West](http://archief10.archiefweb.eu/archives/archiefweb/20140328184006/http://www.amsterdam.nl/verkiezingen/geldige-lijsten/kandidatenlijsten-3/)
  - Amsterdam [stadsdeel Zuid](http://archief10.archiefweb.eu/archives/archiefweb/20140328184006/http://www.amsterdam.nl/verkiezingen/geldige-lijsten/kandidatenlijsten-4/)
  - Amsterdam [stadsdeel Zuidoost](http://archief10.archiefweb.eu/archives/archiefweb/20140328184006/http://www.amsterdam.nl/verkiezingen/geldige-lijsten/kandidatenlijsten-5/)

This [Wikipedia page](https://nl.wikipedia.org/wiki/Categorie:Kandidatenlijsten_verkiezingen_in_Nederland) lists the candidates for EK, TK and EP elections back till 1994, but only with first name and last name (so no initials, gender or place of residence)

Requirements
============

1. `pdftotext` (install xpdf)
