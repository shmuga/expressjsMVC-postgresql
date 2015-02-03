import re
from utils import *
from entities.record import Record


def __extractTag(text):
    """
        Extracts tag from record.
        @tag

        @param {string} text.

        @return {string} tag.
    """
    return re.match('@\w+', text).group(0)


def __extractType(text, tag):
    """
        Extracts type expression from record.
        {type}

        @param {string} text.
        @param {string} tag.

        @return {string} Type expression.
    """
    typeExpression = extractTextBetweenTokens(text, '{')
    return typeExpression


def __extractName(text, tag):
    """
        Extracts name of variable from record.

        @param {string} text.
        @param {string} tag.

        @return {string} Name.
    """
    name = None
    if tag not in {'@return', '@inheritDoc'}:
        name = text.split(' ')[0]
    return name


def __extractDescription(text, tag):
    """
        Extracts description of variable from record without newlines.

        @param {string} text.
        @param {string} tag.

        @return {string} Description.
    """
    return text.replace('\n', ' ')


def extractRecord(text):
    """
        Extracts from code a record object, which contain such information as
        tag, type, name of variable abd its description.

        @param {string} text.

        @return {jsCodeParser.record.Record} Record
    """
    tag = __extractTag(text)
    position = text.find(tag) + len(tag)
    text = text[position:]

    recordMap = {
        'type': {
            'extractor': __extractType,
            'value': ''
        },
        'name': {
            'extractor': __extractName,
            'value': ''
        },
        'description': {
            'extractor': __extractDescription,
            'value': ''
        }
    }

    while text:
        for key in ['type', 'name', 'description']:
            extractor = recordMap[key]['extractor']
            value = extractor(text, tag)
            if value:
                recordMap[key]['value'] = value
                position = text.find(value) + len(value)
                text = text[position:]
            text = text.strip('. ')

    typeExpression = recordMap['type']['value']
    name = recordMap['name']['value']
    description = recordMap['description']['value']

    return Record(tag, typeExpression, name, description)


