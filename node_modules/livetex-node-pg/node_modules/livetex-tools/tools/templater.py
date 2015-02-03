#!/usr/bin/python


import os
import re
from optparse import OptionParser
from subprocess import Popen, PIPE, check_call


def getTemplateText(templatePath):
    file = open(templatePath, 'r')
    text = file.read()
    file.close()
    return text


def getIndent(text, start):
    lineStart = text.rfind('\n', 0, start) + 1
    return start - lineStart


def addIndent(text, indent):
    indentedText = ''
    for line in text.splitlines():
        indentedLine = ' '*indent + line + '\n'
        indentedText += indentedLine
    return indentedText


def interpretAdvanced(templateText):
    templateText = templateText.replace('.js-compile',
                                        '.js-compile-advanced')
    templateText = templateText.replace('.js-compile-compressed',
                                        '.js-compile-advanced')
    templateText = templateText.replace('.js-externs-compile-compressed',
                                        '.js-compile-advanced')
    return templateText


def assemble(templateText):
    match = re.search('(\%\%.+\%\%)', templateText)
    while match:
        tag = match.group(0)
        cmd = tag.strip('%')
        check_call(cmd, shell=True, stdout=open(os.devnull, 'wb'))
        insertion = Popen(cmd, shell=True, stdout=PIPE).communicate()[0]
        insertion = addIndent(insertion, getIndent(templateText, match.start()))
        templateText = templateText.replace(tag, insertion.strip())
        match = re.search('(\%\%.+\%\%)', templateText)
    return templateText


def main():
    usage = "usage: templater [--a advanced] template"
    parser = OptionParser(usage)
    parser.add_option("-a", "--advanced",
                      action="store",
                      default=False,
                      dest="advanced",
                      help="Whether to interpret commands for advanced "
                           "compilation mode or not")

    (options, args) = parser.parse_args()

    templatePath = args[0]
    templateText = getTemplateText(templatePath)

    if options.advanced:
        templateText = interpretAdvanced(templateText)

    print(assemble(templateText))


if __name__ == "__main__":
    main()
