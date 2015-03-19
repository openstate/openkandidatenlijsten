#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
convert_list.py

Created by Breyten Ernsting on 2013-02-26.
Extended by Sicco van Sas in March 2015.
"""

import codecs
import cStringIO
import csv
import getopt
import glob
import json
import os
import re
import sys

help_message = '''
Converts text files containing political candidates data (from PDF files)
to JSON and CSV files

Usage:
    ./convert_list.py -i <folder> [-x -n -h]

options:
    -i, --input        specify root folder containing the PDF file(s) (the actual file(s) should be in the subfolder 'original_pdf')
    -x, --index        creates an index.json listing the URIs for each JSON file on GitHub
    -n, --no_pdf_name  don't use the PDF name in the filenames of the JSON/CSV files; only use the Lijst/Partijnaam; useful when all party's are from the same PDF (e.g. EP elections)
    -h, --help         show this help message
'''


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


class Runner(object):
    def __init__(self, no_pdf_name=False):
        self.no_pdf_name = no_pdf_name

    # Create an index.json file listing the URIs of all json files on GitHub
    # Note: input_dir is expected to have the same name as the folder holding
    # the JSON files in the openkandidatenlijsten-data Git repository
    def create_index(self, input_dir):
        index = {'URIs': []}

        if input_dir[-1] != '/':
            input_dir += '/'

        for filename in sorted(glob.glob('json/*.json')):
            if 'index.json' in filename:
                continue
            index['URIs'].append(
                'https://raw.githubusercontent.com/openstate/'
                'openkandidatenlijsten-data/master/'
                + input_dir + 'json/' + filename.split('/')[-1]
            )

        with codecs.open('json/' + 'index.json', 'w' 'utf-8') as OUT:
            json.dump(index, OUT, indent=4, sort_keys=True, ensure_ascii=False)

    # Save the data to JSON and CSV files
    def save_data(self, data, pdf_filename, use_orig_filename):
        print_title = re.sub(' ', '_', data['title'])
        # Remove any potential slashes
        print_title = re.sub('/', '-', print_title)

        filename_format = "%s-%s"
        if pdf_filename.startswith('Lijst') or self.no_pdf_name:
            filename_format = "%s%s"
            pdf_filename = ''

        with codecs.open(('json/' + filename_format + '.json') % (pdf_filename, print_title), 'w', 'utf-8') as OUT:
            json.dump(data, OUT, indent=4, ensure_ascii=False)

        with open(('csv/' + filename_format + '.csv') % (pdf_filename, print_title), 'w') as OUT:
            csv_writer = UnicodeWriter(OUT)
            csv_writer.writerow(
                [
                    'title',
                    'description',
                    'position',
                    'full_name',
                    'first_name',
                    'last_name',
                    'gender',
                    'place'
                ]
            )
            description = data['description']
            title = data['title']
            for candidate in data['candidates']:
                csv_writer.writerow(
                [
                    title,
                    description,
                    str(candidate['position']),
                    candidate['full_name'],
                    candidate['first_name'],
                    candidate['last_name'],
                    candidate['gender'],
                    candidate['place']
                ]
            )

    def run(self):
        for filename in glob.glob('original_pdf/*.pdf'):
            os.system(
                "pdftotext -layout -nopgbrk -q "
                "'%s' 'pdftotext/%s.txt'" % (
                        filename, filename.split('/')[-1][:-4]
                )
            )

        for filename in glob.glob('pdftotext/*.txt'):
            with codecs.open(filename, "r", "utf-8") as IN:
                lines = IN.readlines()

            # Strip '.txt' extension from filename and replace whitespaces
            raw_filename = re.sub(
                ' ',
                '_',
                os.path.split(filename)[1]
            )[:-4]
            # Strip superfluous info from filename
            raw_filename = re.sub(
                r'Definitieve_kandidatenlijst(en)?_',
                '',
                raw_filename
            )

            layout_specific_regex = ''
            # Layout 1 needs a comma
            if re.match("^\s*CENTRAAL STEMBUREAU", lines[0]) or re.match("^Lijst", lines[0]) or re.match('^\s*STAATSCOURANT', lines[0]):
                layout_specific_regex = ','
            # Layout 2 does not need a comma
            elif re.match("^Overzicht definitieve kandidatenlijsten", lines[3]):
                layout_specific_regex = ''

            # Are we in the description section (between header and candidates)?
            in_description = False
            # Did we extract a description?
            description_extracted = False
            # Are we in a header (i.e. the start of a new party)?
            in_header = True

            # Data structure in which the candidates + related info are saved
            data = {
                'title': u'',
                'description': u'',
                'candidates': []
            }

            use_orig_filename = False
            header_match = ''
            kieskring_count = 0
            # For some reason the Kiesraad swithes between two different PDF
            # layouts :s.
            # Layout 1 indicates the start of a party name with 'Lijst'.
            for line in lines:
                if re.match('\s*Lijst', line):
                    header_match = '^\s*Lijst '
                if line.startswith('Kieskring'):
                    kieskring_count += 1

            if kieskring_count > 1:
                header_match = '^Kieskring \d+'
                use_orig_filename = True
                break

            # Layout 2 indicates a party name simply with a position number and
            # the party's name
            if header_match == '':
                header_match = '^\d+\s+(\S\s?)+$'

            kieskring = ''
            for line in lines:
                line_contents = line.strip()

                if re.match('^Kieskring', line_contents):
                    kieskring = re.sub('\s+', ' ', line_contents)

                # If we find a new header and we were not in a header then we must
                # have finished collecting candidates for a party so we write it
                # to a JSON file and retrieve the new header data
                if re.match(header_match, line):
                    if not in_header:
                        self.save_data(data, raw_filename, use_orig_filename)
                    title = re.sub(r'\s+', ' ', line_contents)
                    title = re.sub(u'–', '-', title)
                    if use_orig_filename:
                        title = raw_filename + '-' + title
                    if 'Lijst' not in title:
                        title = 'Lijst_' + title

                    title = kieskring + '-' + title

                    data = {
                        'title': title,
                        'description': u'',
                        'candidates': []
                    }

                    # After the header section we enter the description section
                    in_description = True
                    in_header = False
                    continue

                # This indicates the start of a tables holding candidates and thus
                # the end of a description section
                if line_contents.startswith('Nr ') or line_contents.startswith('---') or line_contents.startswith('   '):
                    if in_description:
                        description_extracted = True
                    in_description = False
                    continue

                # The Provinciale Statenverkiezingen and Waterschapsverkiezingen
                # might only contain extra information concerning whether a party
                # has a combined list with another party
                if in_description and 'Gecombineerd' in line_contents:
                    data['description'] = line_contents
                    description_extracted = True
                    in_description = False

                # Skip the footer lines on a page
                if line_contents.startswith('pagina') or line_contents.startswith('naam'):
                    continue

                candidate = {
                    'first_name': u'',
                    'last_name': u'',
                    'full_name': u'',
                    'gender': u'',
                    'position': None,
                    'place': u''
                }

                match = re.match(
                    """
                    ^(\d+)\s+          # position number
                    ((\S\s?)+)         # last name\n
                    """
                    + layout_specific_regex +
                    """
                    \s+                # layout 1 has a comma, layout 2 does not
                    ([^(]+)\s+         # initials
                    (\([^)]{2,}\)\s+)? # optional first_name
                    (\([mvf]\)\s+)?    # optional gender
                    (.*)$              # place of residence
                    """,
                    line_contents,
                    re.VERBOSE
                )

                if match is not None:
                    candidate['position'] = int(match.group(1))
                    candidate['last_name'] = match.group(2).strip()
                    candidate['full_name'] = "%s %s" % (
                        re.sub(' ', '', match.group(4).strip()),
                        match.group(2).strip()
                    )
                    if match.group(5) is not None:
                        candidate['first_name'] = re.sub(
                            r'[()]',
                            '',
                            match.group(5).strip()
                        )
                    if match.group(6) is not None:
                        gender = re.sub(r'[()]', '', match.group(6).strip())
                        # At least one party uses 'f' instead of 'v' :s
                        if gender == 'f':
                            gender = 'v'
                        candidate['gender'] = gender
                    candidate['place'] = match.group(7).strip()

                    data['candidates'].append(candidate)

            self.save_data(data, raw_filename, use_orig_filename)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(
                argv[1:],
                "hi:xnv",
                ["help", "input=", "index", "no_pdf_name"]
            )
        except getopt.error, msg:
            raise Usage(msg)

        input_file = None

        # option processing
        create_index = False
        no_pdf_name = False
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-i", "--input"):
                input_dir = value
            if option in ("-x", "--index"):
                create_index = True
            if option in ("-n", "--no_pdf_name"):
                no_pdf_name = True

        os.chdir(input_dir)

        if not os.path.exists('pdftotext'):
            os.mkdir('pdftotext')
        if not os.path.exists('json'):
            os.mkdir('json')
        if not os.path.exists('csv'):
            os.mkdir('csv')

        runner = Runner(no_pdf_name)
        runner.run()
        if create_index:
            runner.create_index(input_dir)

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
