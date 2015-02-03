from extractors.recordsExtractor import extractRecord
from utils import *


class JsDoc:
    """
        A chunk of code which marked as multi-line comment '/** * */'.

        @param {string} text.

        @attribute {string} text.
        @attribute {Array.<jsCodeParser.jsDoc.Record>} records.
    """
    def __init__(self, text):
        self.original = text
        self.text = indentJsDoc(text)

    def getRecords(self):
        records = []
        jsDoc = self.text.strip('/* ').replace('\n', '')
        while '@' in jsDoc:
            start = jsDoc.find('@')
            end = jsDoc.find('@', start + 1)
            if end == -1:
                end = len(jsDoc)
            text = jsDoc[start:end].strip('* ')
            jsDoc = jsDoc[end:]
            record = extractRecord(text)
            records.append(record)
        return records

    def getText(self):
        return self.text

    def getOriginal(self):
        return self.original

    def getRecordsByTag(self, tag=None):
        records = self.getRecords()
        if tag:
            records = [record for record in records if record.getTag() == tag]
        return records

    def getDescription(self):
        lines = [line.strip('/* \n') for line in self.text.splitlines()
                 if '@' not in line]
        description = ' '.join(lines)
        return description

    def getIndent(self):
        text = self.original.strip(' \n')
        end = text.find('*/')
        start = text.rfind('\n')
        return end - start - 2

    def isInheritDoc(self):
        if '@inheritDoc' in self.text:
            return True
        return False
