
import re, sys

class ReadDocuments:
    def __init__(self,file):
        self.collection_file = file

    def __iter__(self):
        startdoc = re.compile('<document docid\s*=\s*(\d+)\s*>')
        enddoc = re.compile('</document\s*>')
        readingDoc = False
        abstract = []
        with open(self.collection_file) as input_fs:
            for line in input_fs:
                m = startdoc.search(line)
                if m:
                    readingDoc = True
                    doc = Document()
                    abstract = []
                    doc.docid = int(m.group(1))
                elif enddoc.search(line):
                    doc.abstract = ' '.join(abstract)
                    readingDoc = False
                    yield doc
                elif readingDoc:
                    doc.lines.append(line)
                    if line.startswith('CACM '):
                        doc.post_date = line
                    if doc.post_date != '':
                        abstract.append(line)
# .*, .\.


class Document:
    def __init__(self):
        self.docid = 0
        self.lines = []
        self.post_date = ''
        self.author = ''
        self.title = ''
        self.abstract = ''

    def printDoc(self):
        print("\n[DOCID: %d]" % self.docid)
        for line in self.lines:
            print(line)
