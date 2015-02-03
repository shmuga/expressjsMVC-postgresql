import re
from entities.elements import *
from entities.jsDoc import JsDoc


class externsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def __getElements(text):
    """
        Finds JsDocs and code of elements

        @param {string} text.

        @return {Set.<jsCodeParser.elements.Element>} Elements, which were
                found in code.
    """
    elements = list()
    position = 0
    jsDoc = __extractJsDoc(text)
    while jsDoc:
        jsDocText = jsDoc.getOriginal()
        position = text.find(jsDocText, position) + len(jsDocText)
        if __checkJsDoc(text, jsDocText):
            element = __extractElement(text[position:], jsDoc)
            elements.append(element)
            position = text.find(element.getCode(), position) + \
                       len(element.getCode())
        jsDoc = __extractJsDoc(text[position:])
    return elements


def __checkJsDoc(text, jsDoc):
    index = text.find(jsDoc) + len(jsDoc)
    if ord(text[index]) == ord(text[index + 1]) == 10:
        return False
    return True


def __extractJsDoc(text):
    """
        Extracts the first occurrence of JsDoc.

        @param {string} text.

        @return {(jsCodeParser.jsDoc.JsDoc|None)} JsDoc.
    """
    text = text.strip()
    jsDocPattern = '((\s*\/\*\*\n){1}( \s*\*.*\n)+( \s*\*\/))'
    match = re.search(jsDocPattern, text)
    if match:
        jsDocText = match.group(0).strip()
        return JsDoc(jsDocText)
    return None


def __extractElement(text, jsDoc):
    """
        Extracts an element, which has a certain JsDoc.

        @param {string} text.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc.

        @return {jsCodeParser.elements.Element} Element.
    """
    text = text.strip()

    extractor = None

    tags = ['@constructor', '@interface', '@namespace',
            '@typedef', '@type', '@enum']

    tagMap = {
        '@constructor': __extractClass,
        '@interface': __extractInterface,
        '@namespace': __extractNamespace,
        '@typedef': __extractTypedef,
        '@type': __extractProperty,
        '@enum': __extractEnum
    }

    for tag in tags:
        if tag in jsDoc.getText():
            extractor = tagMap[tag]
            break

    if not extractor:
        extractor = __extractMethod

    element = extractor(text, jsDoc)

    return element


def __extractNamespace(text, jsDoc):
    """
        Extracts namespace, which has JsDoc with '@namespace' tag.

        @param {string} text.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc.

        @return {jsCodeParser.elements.Namespace} Namespace.
    """
    end = text.find('=')
    if text[end + 1:].strip()[0] == '{':
        end = text.find('}') + 1
    if text[end + 1:].strip().find('require') == 0:
        end = text.find(')') + 1
    if text[end] == ';':
        end += 1
    code = text[:end].strip()
    return Namespace(code, jsDoc)


def __extractTypedef(text, jsDoc):
    """
        Extracts typedef, which has JsDoc with '@typedef' tag.

        @param {string} text.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc.

        @return {jsCodeParser.elements.Typedef} Typedef.
    """
    end = findEnd(text)
    code = text[:end].strip()
    return Typedef(code, jsDoc)


def __extractProperty(text, jsDoc):
    """
        Extracts property, which has JsDoc with '@type' tag.

        @param {string} text.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc.

        @return {jsCodeParser.elements.Property} Property.
    """
    recordType = jsDoc.getRecordsByTag('@type')[0].getType()
    if recordType.strip('?!.').find('function') == 0:
        function = __extractFunction(text, jsDoc, Method)
        if function:
            return function
    eqPos = text.find('=')
    value = text[eqPos + 1:].strip()

    if value[0] in ['[', '{']:
        value = extractTextBetweenTokens(value, value[0])
        end = text.find(value) + len(value)
    elif value[0] in ['"', "'"]:
        value = extractString(value, value[0])
        end = text.find(value) + len(value)
    else:
        end = text.find(value) + findEnd(value)
    if end != len(text) and text[end] == ';':
        end += 1

    code = text[:end].strip()
    element = Property(code, jsDoc)
    return element


def __extractEnum(text, jsDoc):
    """
        Extracts enumeration, which has JsDoc with '@enum' tag.

        @param {string} text.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc.

        @return {jsCodeParser.elements.Enumeration} Enumeration.
    """
    obj = extractTextBetweenTokens(text, '{')
    end = text.find(obj) + len(obj)
    if text[end] == ';':
        end += 1
    code = text[:end].strip()
    return Enumeration(code, jsDoc)


def __extractFunction(text, jsDoc, classConstructor):
    """
        Extracts a function depending of its pattern:

        'function declaration':
            function <name>(<parameters>) {
                <realization>
            }[;]

        'named function expression':
            <variable> = function <name>(<parameters>) {
                <realization>
            }[;]

        'unnamed function expression'.
            <variable> = function(<parameters>) {
                <realization>
            }[;]

        'alias function':
            <variable> = <name>(<parameters>)[;]

        @param {string} text.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc.
        @param {(jsCodeParser.elements.Class|jsCodeParser.elements.Method)}
                classConstructor.

        @return {(jsCodeParser.elements.Class|jsCodeParser.elements.Method)}
                Element.
    """
    parameters = extractTextBetweenTokens(text, '(')
    if not parameters:
        return None
    end = text.find(parameters) + len(parameters)
    realization = text[end:].strip()
    if realization[0] == '{':
        realization = extractTextBetweenTokens(realization, '{')
        end = text.find(realization) + len(realization)
    if end < len(text) and text[end] == ';':
        end += 1
    code = text[:end].strip()
    return classConstructor(code, jsDoc)


def __extractClass(text, jsDoc):
    """
        Extracts class, which has JsDoc with '@constructor' tag.
        Extracts its attributes and sets to class's structure.

        @param {string} text.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc.

        @return {jsCodeParser.elements.Class} Class.
    """
    element = __extractFunction(text, jsDoc, Class)
    realization = element.getRealization()
    if realization:
        attributes = [attribute for attribute in __getElements(realization)
                      if attribute.isPublic()]
        element.setAttributes(attributes)
    return element


def __extractMethod(text, jsDoc):
    """
        Extracts method and its attributes.

        @param {string} text.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc.

        @return {jsCodeParser.elements.Method} Method.
    """
    element = __extractFunction(text, jsDoc, Method)
    realization = element.getRealization()
    if realization:
        attributes = [attribute for attribute in __getElements(realization)
                      if not attribute.isPublic()]
        element.setAttributes(attributes)
    return element


def __extractInterface(text, jsDoc):
    """
        Delegates extraction of interface to __extractFunction method.

        @param {string} text.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc.

        @return {jsCodeParser.elements.Interface} Interface.
    """
    return __extractFunction(text, jsDoc, Interface)


def extractElements(path):
    """
        Gets elements from project files' code and adds it to project structure.

        @param {project.Project} project.
    """
    file = open(path, 'r')
    code = file.read()
    return __getElements(code)




