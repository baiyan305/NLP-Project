from lxml import etree
import string
import re

class XMLParser:

    instances_data = []
    raw_text = []
    clean_text = []

    def get_instances_data(self):
        return instances_data

    def get_raw_text(self):
        return self.raw_text

    def get_clean_text(self):
        return self.clean_text

    #strip punctuation in string
    def _strip_punctuation(self, str):
        return re.sub(r'[.,:#"!?;()-/\']',"",str)
    
    def parse(self, input):
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(input, parser=parser)
        root = tree.getroot()
        
        for instance in root.findall('.//instance'):
            instance_data = []
            instance_id = instance.get("id")
            children = list(instance)
            answer = children[0]
            context = children[1]
            sense_id = answer.get("senseid")
            context_in_string = etree.tostringlist(context,encoding="us-ascii",method="xml")[0]
            context_raw_text = context_in_string[10:-11]
            context_fine_text = self._strip_punctuation(context_raw_text)
            instance_data.extend(instance_id)
            instance_data.extend(sense_id)
            instance_data.extend(context_raw_text)
            self.raw_text.append(context_raw_text)
            self.clean_text.append(context_fine_text) 
