from utils import *


class Element:
    """
        Some element of the code, which has JsDoc.

        @param {string} code Code of an element.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc JsDoc object of an element.

        @attribute {string} code Code of an element.
        @attribute {jsCodeParser.jsDoc.JsDoc} jsDoc JsDoc object of an element.
        @attribute {string} name Name of an element.
    """
    def __init__(self, code, jsDoc):
        self.code = code
        self.jsDoc = jsDoc
        self.description = self.jsDoc.getDescription()

    def getName(self):
        name = self.code
        eqPos = name.find('=')
        if eqPos != -1:
            name = name[:eqPos]
        if name[:3] == 'var':
            name = name[3:]
        name = name.strip('; ')
        return name

    def getShortName(self):
        name = self.getName()
        if 'prototype' in name:
            name = name.split('prototype')[-1]
        elif '.' in name:
            name = name.split('.')[-1]
        name = name.strip('.')
        return name

    def getParentName(self):
        name = self.getName()
        if 'prototype' in name:
            name = name.split('prototype')[0]
        elif '.' in name:
            name = name[:name.rfind('.')]
        name = name.strip('.')
        return name

    def getDescription(self):
        return self.description

    def getCode(self):
        return self.code

    def getJsDoc(self):
        return self.jsDoc

    def getExterns(self):
        jsDoc = self.jsDoc.getText()
        externs = jsDoc + '\n' + self.code + '\n'
        indent = self.jsDoc.getIndent()
        externs = addIndent(externs, indent)
        return externs

    def isPublic(self):
        if not (self.isProtected() or self.isPrivate()):
            return True
        else:
            return False

    def isProtected(self):
        name = self.getShortName()
        if name[0] == '_' and name[1] != '_':
            return True
        else:
            return False

    def isPrivate(self):
        nameParts = self.getName().split('.')
        for part in nameParts:
            if part[:2] == '__':
                return True
        return False

    def isTest(self):
        words = self.getName().split('.')
        return len(words) > 1 and words[1][:4] == 'test'


class Namespace(Element):
    """
        Element, which has JsDoc with '@namespace' tag.

        @param {string} code Code of an element.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc JsDoc object of an element.

        @attribute {Array.<jsCodeParser.elements.Namespace>} children
        @attribute {Array.<jsCodeParser.elements.Class>} classes
        @attribute {Array.<jsCodeParser.elements.Interface>} interfaces
        @attribute {Array.<jsCodeParser.elements.Method>} methods
        @attribute {Array.<jsCodeParser.elements.Property>} properties
        @attribute {Array.<jsCodeParser.elements.Typedef>} typedefs
        @attribute {Array.<jsCodeParser.elements.Enumeration>} enums
    """
    def __init__(self, code, jsDoc):
        Element.__init__(self, code, jsDoc)


class Constructor(Element):
    """
        Constructor of a class or method.

        @param {string} code Code of an element.
        @param {jsCodeParser.jsDoc.JsDoc} jsDoc JsDoc of an element.

        @attribute {Array.<{'name': string,
                            'type': jsCodeParser.types.Type,
                            'description': string }>} parameters.
        @attribute {Array.<jsCodeParser.elements.Element>} attributes
    """
    def __init__(self, code, jsDoc):
        Element.__init__(self, code, jsDoc)
        self.attributes = list()

    def getName(self):
        code = self.code
        end = code.find('(')
        start = code[:end].rfind(' ')
        name = code[start: end].strip()
        if name == 'function':
            end = code.find('=')
            name = code[:end].strip()
        return name

    def getExterns(self):
        code = self.code
        parameters = extractTextBetweenTokens(code, '(')
        realizationStart = code.find(parameters) + len(parameters)
        realizationStart = code.find('{', realizationStart)
        definition = code[:realizationStart]
        realization = '{'
        attributes = self.attributes
        if attributes:
            realization += '\n'
            for attribute in attributes:
                attributeExterns = '\n'
                attributeExterns += attribute.getExterns()
                attributeExterns += '\n'
                realization += attributeExterns
        realization += '};\n'
        externs = self.jsDoc.getText() + '\n' + definition + realization
        indent = self.jsDoc.getIndent()
        externs = addIndent(externs, indent)
        return externs

    def getParameters(self):
        records = self.jsDoc.getRecords(tag='@param')
        if records:
            return [{
                'name': record.getName(),
                'type': record.getType(),
                'description': record.getDescription()
            } for record in records]
        return None

    def getAttributes(self):
        return self.attributes

    def getRealization(self):
        return extractTextBetweenTokens(self.code, '{')

    def getSignature(self):
        parameters = extractTextBetweenTokens(self.code, '(')
        parameters = clearTokens(parameters.replace('\n', ''))
        return self.getName() + parameters

    def setAttributes(self, attributes):
        self.attributes = attributes


class Class(Constructor):
    """
       Element, which has JsDoc with '@constructor' tag.

       @param {string} code Code of an element.
       @param {jsCodeParser.jsDoc.JsDoc} jsDoc JsDoc of an element.

       @attribute {Array.<jsCodeParser.elements.Class>} parents.
       @attribute {Array.<jsCodeParser.elements.Method>} methods.
       @attribute {Array.<jsCodeParser.elements.Interface>} interfaces.
    """
    def __init__(self, code, jsDoc):
        Constructor.__init__(self, code, jsDoc)


class Method(Constructor):
    """
       Element, which represented as function in code.

       @param {string} code Code of an element.
       @param {jsCodeParser.jsDoc.JsDoc} jsDoc JsDoc of an element.

       @attribute {Array.<jsCodeParser.elements.Method>} implementation
            Method which this element implements.
    """
    def __init__(self, code, jsDoc):
        Constructor.__init__(self, code, jsDoc)

    def getResult(self):
        records = self.jsDoc.getRecords(tag='@return')
        if records:
            return [{
                        'type': record.getType(),
                        'description': record.getDescription()
                    } for record in records][0]
        return None


class Interface(Element):
    """
       Element, which has JsDoc with '@interface' tag.

       @param {string} code Code of an element.
       @param {jsCodeParser.jsDoc.JsDoc} jsDoc JsDoc of an element.

       @attribute {Array.<{'name': string,
                            'type': jsCodeParser.types.Type,
                            'description': string }>} parameters.
       @attribute {Array.<jsCodeParser.elements.Interface>} parents.
       @attribute {Array.<jsCodeParser.elements.Method>} methods.
       @attribute {Array.<jsCodeParser.elements.Class>} users.
    """
    def __init__(self, code, jsDoc):
        Element.__init__(self, code, jsDoc)

    def getName(self):
        code = self.code
        end = code.find('(')
        start = code[:end].rfind(' ')
        name = code[start: end].strip()
        if name == 'function':
            end = code.find('=')
            name = code[:end].strip()
        return name

    def getParameters(self):
        records = self.jsDoc.getRecords(tag='@param')
        if records:
            return [{
                'name': record.getName(),
                'type': record.getType(),
                'description': record.getDescription()
            } for record in records]
        else:
            return None


class Property(Element):
    """
       Element, which has JsDoc with '@type' tag.

       @param {string} code Code of an element.
       @param {jsCodeParser.jsDoc.JsDoc} jsDoc JsDoc of an element.

       @attribute {string} value.
       @attribute {jsCodeParser.types.Type} type.
    """
    def __init__(self, code, jsDoc):
        Element.__init__(self, code, jsDoc)

    def __getValue(self):
        start = self.code.find('=') + 1
        return self.code[start:].strip(' ;')

    def getExterns(self):
        end = self.code.find('=')
        definition = self.code[:end].strip(' \n')
        externs = self.jsDoc.getText() + '\n' + definition + ';'
        indent = self.jsDoc.getIndent()
        return addIndent(externs, indent)


class Typedef(Element):
    """
       Element, which has JsDoc with '@typedef' tag.

       @param {string} code Code of an element.
       @param {jsCodeParser.jsDoc.JsDoc} jsDoc JsDoc of an element.

       @attribute {jsCodeParser.types.Type} type.
    """
    def __init__(self, code, jsDoc):
        Element.__init__(self, code, jsDoc)


class Enumeration(Element):
    """
       Element, which has JsDoc with '@enum' tag.

       @param {string} code Code of an element.
       @param {jsCodeParser.jsDoc.JsDoc} jsDoc JsDoc of an element.

       @attribute {{key: value}} enum.
       @attribute {jsCodeParser.types.Type} type.
    """
    def __init__(self, code, jsDoc):
        Element.__init__(self, code, jsDoc)
