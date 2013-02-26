#!/usr/bin/env python
# encoding: utf-8
"""
convert_list.py

Created by Breyten Ernsting on 2013-02-26.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import sys
import getopt
import codecs
import re
import json

help_message = '''
Converts text files containing political candidates data (from pdf files) to xml/json
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


class Runner(object):
    def run(self, input_file, output):
        ifile = codecs.open(input_file, "r", "iso-8859-1")
        #ifile = open(input_file, "r")
        contents = ifile.read()
        line_count = 0
        in_description = False
        description_extracted = False
        data = {
            'title': u'',
            'description': u'',
            'members': []
        }
        for line in contents.split("\n"):
            line_contents = line.strip()
            if line_count == 0:
                data['title'] = line_contents
            if line_contents == u'':
                if in_description:
                    description_extracted = True
                in_description = False
            else:
                if line.startswith('Nr '):
                    continue
                if (line_count > 1) and not description_extracted:
                    in_description = True
                if in_description:
                    data['description'] += u' %s' % (line_contents,)
                if description_extracted and (re.search('^\d+\s+', line_contents)):
                    member = {
                        'first_name': u'',
                        'last_name': u'',
                        'full_name': u'',
                        'gender': u'',
                        'position': None,
                        'place': u''
                    }
                    position,info,member['place'] = re.split('\s{2,}', line_contents, 2)
                    member['position'] = int(position)
                    match = re.match('([^,]+),\s+([A-Z\.]+)\s+\(([^\)]+)\)\s+\(([m|v])\)', info)
                    if match is not None:
                        member['last_name'] = match.group(1)
                        member['full_name'] = "%s %s" % (match.group(2), match.group(1))
                        member['first_name'] = match.group(3)
                        member['gender'] = match.group(4)
                    data['members'].append(member)
            line_count += 1
        ifile.close()
        print json.dumps(data)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hi:o:v", ["help", "input=", "output="])
        except getopt.error, msg:
            raise Usage(msg)

        input_file = None
        output = None

        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option in ("-i", "--input"):
                input_file = value

        runner = Runner()
        runner.run(input_file, output)

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
