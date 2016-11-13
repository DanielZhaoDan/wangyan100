import re


class ReadDocuments:
    def __init__(self, file):
        self.collection_file = file
        self.all_content = []

    def __iter__(self):
        startdoc = re.compile('<document docid\s*=\s*(\d+)\s*>')
        enddoc = re.compile('</document\s*>')
        authordoc = re.compile(('^.*, .\.'))
        readingDoc = False
        abstract = []
        title = []
        with open(self.collection_file) as input_fs:
            for line in input_fs:
                line = line.lower()
                m = startdoc.search(line)
                if m:
                    readingDoc = True
                    doc = Document()
                    abstract = []
                    title = []
                    doc.docid = int(m.group(1))
                elif enddoc.search(line):
                    doc.abstract = ' '.join(abstract)
                    doc.title = ' '.join(title)
                    readingDoc = False
                    yield doc
                elif readingDoc:
                    doc.lines.append(line.strip())
                    self.all_content.append(line.strip())
                    if not doc.author and authordoc.search(line):
                        doc.author = line.strip().replace(' &', ',').split('., ')
                    if not authordoc.search(line) and not doc.author and line != '\n':
                        title.append(line.strip())
                    if line.startswith('CACM '):
                        doc.post_date = line.strip()
                    elif doc.post_date != '' and line != '\n':
                        abstract.append(line.strip())


class Document:
    def __init__(self):
        self.docid = 0
        self.lines = []
        self.post_date = ''
        self.author = []
        self.title = ''
        self.abstract = ''

    def printDoc(self):
        print("\n[DOCID: %d]" % self.docid)
        for line in self.lines:
            print(line)


class ReadQueries:
    def __init__(self,file):
        self.collection_file = file

    def __iter__(self):
        startdoc = re.compile('<document docid\s*=\s*(\d+)\s*>')
        enddoc = re.compile('</document\s*>')
        readingDoc = False
        with open(self.collection_file) as input_fs:
            for line in input_fs:
                line = line.lower()
                m = startdoc.search(line)
                if m:
                    readingDoc = True
                    doc = Query()
                    doc.queid = int(m.group(1))
                elif enddoc.search(line):
                    readingDoc = False
                    doc.content = ' '.join(doc.lines)
                    yield doc
                elif readingDoc:
                    doc.lines.append(line.strip())

class Query:
    def __init__(self):
        self.queid = 0
        self.lines = []
        self.content = ''

    def printDoc(self):
        print("\n[QUEID: %d]" % self.queid)
        for line in self.lines:
            print(line)

