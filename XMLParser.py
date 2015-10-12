import xml.etree.ElementTree as ET
import string

class XMLParser:

    raw_text = []
    clean_text = []

    def get_raw_text(self):
        return self.raw_text

    def get_clean_text(self):
        return self.clean_text

    #strip punctuation in string
    def _strip_puctuation(self, str):
        delset = string.punctuation
        return str.translate(None, delset)

    def parse(self, input):
        tree = ET.parse(input)
        root = tree.getroot()

        for context in root.iter('context'):
            self.raw_text.append(context.text)
            self.clean_text.append(self._strip_puctuation(context.text))