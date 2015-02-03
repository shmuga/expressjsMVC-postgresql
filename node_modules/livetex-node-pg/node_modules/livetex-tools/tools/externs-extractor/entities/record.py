

class Record:
    """
        One line of JsDoc or more, which contain such information as
        tag, type, name of variable abd its description.

        @param {string} text.

        @attribute {string} tag.
        @attribute {jsCodeParser.types.Type} typeExpression.
        @attribute {string} name.
        @attribute {string} description.

        @param {string} tag.
        @param {string} typeExpression.
        @param {string} name.
        @param {string} description.
    """
    def __init__(self, tag, typeExpression, name, description):
        self.tag = tag
        self.type = typeExpression
        self.name = name
        self.description = description

    def getTag(self):
        return self.tag

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description