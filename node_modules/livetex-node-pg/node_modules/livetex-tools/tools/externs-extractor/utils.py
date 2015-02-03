import os
import json
from collections import OrderedDict


def __getPosition(token, text, pos):
    """
        Returns the position of a certain token, but not in string.

        @param {string} token Token to find.
        @param {string} text Text in which the token is.
        @param {number} pos Start position for searching.

        @return {number} Position.
    """
    position = text.find(token, pos + 1)
    if isInString(position, text):
        position = __getPosition(token, text, pos + 1)
    if position == -1:
        position = len(text)
    return position


def getFiles(paths):
    result = list()
    for path in paths:
        if os.path.exists(path):
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        result.append(root + os.sep + file)
            elif os.path.isfile(path):
                result.append(path)
        else:
            print("WARN: " + path + " doesn't exist.")
    return result


def getLast(text, signs):
    """
        Returns a position of the sign which occurs the last.

        @param {string} text.
        @param {Array.<string>} signs.

        @return {number} Position.
    """
    positions = [text.rfind(sign) for sign in signs if text.rfind(sign) != -1]
    if positions:
        return max(positions)
    else:
        return -1


def getFirst(text, signs):
    """
        Returns a position of the sign which occurs the first.

        @param {string} text.
        @param {Array.<string>} signs.

        @return {number} Position.
    """
    positions = [text.find(sign) for sign in signs if text.find(sign) != -1]
    if positions:
        return min(positions)
    else:
        return -1


def getProjectsNames(configPath):
    """
        Returns the list of projects mentioned in config file.

        @param {string} configPath Path to projects configurations.

        @return {Array.<string>} Projects names.
    """
    file = open(configPath, 'r')
    config = json.load(file)
    projects = list(config.keys())
    projects.remove('default')
    return projects


def isInLink(text, start, end):
    """
        Checks whether the string in link or not.

        @param {string} text Text containing a string.
        @param {number} start Start position of a string.
        @param {number} end End position of the string.

        @result {boolean} True if a string is in link.
                False if it's not.
    """
    linkStart = text[:start].rfind('<a href="')
    linkEnd = text.find('</a>', linkStart)
    if -1 not in [linkStart, linkEnd] and linkStart < start < end < linkEnd:
        return True
    return False


def isInTag(text, start, end):
    """
        Checks whether the string in link or not.

        @param {string} text Text containing a string.
        @param {number} start Start position of a string.
        @param {number} end End position of the string.

        @result {boolean} True if a string is in tag.
                False if it's not.
    """
    if text[start - 1] in '</&' and text[end] in '>;':
        return True
    return False


def isInString(position, text):
    """
        Checks whether the sign from a certain position in text is in string
        or not.

        @param {number} position.
        @param {string} text.

        @return {boolean} True if sign is in string.
                          False if it's not.
    """
    for quote in {'"', "'"}:
        textCopy = text.replace('\\' + quote, '||')
        textBeforeToken = textCopy[:position]
        textAfterToken = textCopy[position + 1:]
        if textBeforeToken.count(quote) % 2 != 0 and \
                                textAfterToken.count(quote) % 2 != 0:
            return True
    return False


def isTheOnlyOne(elements):
    """
        Checks whether there is the only one true positive object or not.

        @param {Array.<*>} elements.

        @return {boolean} True, if there is the only one element,
                which is not None, empty or 0.
                False if it's not.
    """
    count = 0
    for element in elements:
        if element:
            count += 1
    if count == 1:
        return True
    return False


def isWhole(text, start, end):
    """
        Checks whether the string is a whole word or not.

        @param {string} text Text containing a string.
        @param {number} start Start position of a string.
        @param {number} end End position of the string.

        @result {boolean} True if a string is a whole word.
                False if it's not.
    """
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    if end - start == len(text):
        return True
    if start:
        start -= 1
    if (text[start].lower() in alpha or text[end].lower() in alpha) or \
            (text[start] == '#' and (text[end] == '(' or end == len(text))) or \
            (text[start] == '.' or text[end] == '.'):
        return False
    return True


def extractTextBetweenTokens(text, openToken, closeToken=None):
    """
        Extracts text between tokens with these tokens.

        @param {string} text.
        @param {string} openToken.
        @param {(string|None)} closeToken.

        @return {(string|None)} Text between tokens.
    """
    if not closeToken:
        tokens = {
            '(': ')',
            ')': '(',
            '[': ']',
            ']': '[',
            '{': '}',
            '}': '{',
            '<': '>',
            '>': '<'
        }
        closeToken = tokens[openToken]
    start = text.find(openToken)
    pos = start + 1
    summ = 1
    while summ != 0 and pos < len(text):
        if text[pos] == openToken:
            summ += 1
        if text[pos] == closeToken:
            summ -= 1
        pos += 1
    if summ == 0:
        return text[start:pos]
    return None


def extractString(text, quote):
    """
        Extracts string in specified quotes.

        @param {string} text.
        @param {string} quote.

        @return {string} Text in quotes with these quotes.
    """
    textCopy = text.replace('\\' + quote, '||')
    start = textCopy.find(quote)
    end = textCopy.find(quote, start + 1) + 1
    return text[start:end].strip()


def findEnd(text):
    """
        Finds th position where some logical item ends.
        It can be ';'   a semicolon or
                  '\n'  a newline or
                  the end of a whole text.

        @param {string} text.

        @return {number} Position of the end.
    """
    semicolonPos = text.find(';')
    newlinePos = text.find('\n')
    textEnd = len(text)
    minimum = min(semicolonPos, newlinePos)
    maximum = max(semicolonPos, newlinePos)
    if minimum != -1:
        end = minimum
    elif maximum != -1:
        end = maximum
    else:
        end = textEnd
    if end != textEnd:
        end += 1
    return end


def convertStringToDict(string, delimiter, separator):
    """
        Converts string to not nested dictionary.

        @param {string} string String to convert.
        @param {string} delimiter Delimiter of key and value.
        @param {string} separator Separator for key-value pairs.

        @return {{key: value}} A dictionary.
    """
    if string[0] == '{' and string[-1] == '}':
        string = string[1:-1].replace('\n', '').replace(' ', '')
    dictionary = OrderedDict()
    pos = 0
    while pos < len(string):
        delimiterPos = __getPosition(delimiter, string, pos)
        key = string[pos: delimiterPos].strip()
        separatorPos = __getPosition(separator, string, delimiterPos)
        value = string[delimiterPos + 1:separatorPos].strip()
        pos = separatorPos + 1
        dictionary.__setitem__(key, value)
    return dictionary


def revertOrder(elements):
    """
        Makes an array from elements in reverse order.

        @param {Array.<*>} elements.

        @return {Array.<*>} Elements in reverse.
    """
    simpleOrder = sorted(elements)
    reverseOrder = list()
    i = len(elements) - 1
    while i:
        reverseOrder.append(simpleOrder[i])
        i -= 1
    return reverseOrder


def mergeDictsItems(final, aux):
    """
        Adds elements from aux dictionary
        which are not in final dictionary to it.

        @param {Object.<*>} final Final dictionary.
        @param {Object.<*>} aux Auxiliary dictionary.

        @return {Object.<*>} Merged dictionary.
    """
    for key in aux.keys():
        if not final.__contains__(key):
            final[key] = aux[key]
        elif type(final[key]) == dict:
            final[key] = mergeDictsItems(final[key], aux[key])
    return final


def clearTokens(text):
    """
        Clears text from '*' signs and extra spaces.

        @param {string} text.

        @return {string} Clean text.
    """
    position = 0
    while position < len(text):
        if text[position] == '*' and not isInString(position, text):
            text = text[:position] + text[position + 1:]
        else:
            position += 1
    position = 0
    while position < len(text):
        if position + 1 < len(text) and \
                text[position] == ' ' and text[position + 1] == ' ':
            text = text[:position] + text[position + 1:]
        else:
            position += 1
    return text


def getExtension(path):
    """
        Extracts extension of file from path.

        @param {string} path

        @return {string} Extension.
    """
    extension = ''
    templateName = os.path.basename(path)
    if '.' in templateName:
        extension = '.' + str(templateName.split('.')[-1])
    return extension


def cutExtension(path):
    """
        Cuts extension in path.

        @param {string} path

        @return {string} Path without extension.
    """
    extension = getExtension(path)
    position = len(path)
    if extension:
        position = path.rfind(extension)
    return path[:position]


def addIndent(text, indent):
    """
        @param {string} text
        @param {number} indent
        @return {string}
    """
    result = ''
    lines = text.splitlines()
    for line in lines:
        result += ' ' * indent
        result += line
        result += '\n'
    return result


def removeIndent(text):
    """
        @param {string} text
        @return {string}
    """
    result = ''
    lines = text.splitlines()
    for line in lines:
        result += line.strip()
        result += '\n'
    return result


def indentJsDoc(text):
    """
        @param {string} jsDoc
        @return {string}
    """
    result = ''
    if text:
        text = removeIndent(text)
        lines = text.splitlines()
        result = lines[0] + '\n'
        for line in lines[1:]:
            result += addIndent(line, 1)
    result = result.strip('\n ')
    return result