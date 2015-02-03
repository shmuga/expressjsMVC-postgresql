#!/usr/bin/python

import os
from optparse import OptionParser
from extractors.elementsExtractor import extractElements


def getExternsFromFiles(paths):
    externs = ''
    for path in paths:
        for element in extractElements(path):
            if not (element.isPrivate() or element.isTest()):
                externs += element.getExterns()
                externs += '\n\n'
    externs += '\n'
    return externs


def main():
    usage = "usage: externs-extractor [--o output]"
    parser = OptionParser(usage)
    parser.add_option("-o", "--output",
                      action="store",
                      default=None,
                      dest="output",
                      help="Input path to externs file.")
    (options, args) = parser.parse_args()
    externs = getExternsFromFiles(args)
    if options.output:
        output = open(options.output, 'w')
        output.write(externs)
        output.close()
    else:
        print(externs)


if __name__ == "__main__":
    main()


