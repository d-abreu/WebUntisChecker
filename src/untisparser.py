from html.parser import HTMLParser
import string
import hashlib

class UntisHTMLParser(HTMLParser):
    _textToHash = ''
    _isRecording = False
    _counter = 0

    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def get_hash(self):
        return self._textToHash

    def _record(self,tag,attrs):
        self._textToHash += tag
        self._counter += 1
        if attrs is None:
            return;

        for attr in attrs:
            name = attr[0]
            value = attr[1]
            self._textToHash += name + value

    def handle_starttag(self, tag, attrs):
        if self._isRecording:
            self._record(tag,attrs)

        if tag == 'div':
            for attr in attrs:
                name = attr[0]
                value = attr[1]
                if name == 'data-dojo-attach-point' and value == '_timetableContainer':
                    self._isRecording = True
                    self._record(tag,attrs)

    def handle_endtag(self, tag):
        if not self._isRecording:
            return
        else:
            self._record(tag,None)

        self._counter -= 2
        if self._counter == 0:
            self._isRecording = False

def parse(text):
    parser = UntisHTMLParser()
    parser.feed(text)
    parser.close()
    theHash =  hashlib.md5(parser.get_hash().encode('utf-8'))
    return theHash.hexdigest()
