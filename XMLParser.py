from lxml import etree
import string
import re

class XMLParser:

    instances_data = []
    raw_text = []
    clean_text = []
    global_input = None
    global_targetword = None

    def get_instances_data(self):
        return self.instances_data

    def get_raw_text(self):
        return self.raw_text

    def get_clean_text(self):
        return self.clean_text

    def get_input_path(self):
        return self.global_input

    def get_targetword():
        return self.global_targetword

    #strip punctuation in string
    def _strip_punctuation(self, str):
        pattern = re.compile(u'[.,:#"!?;()-/\']')
        return re.sub(pattern,"",str.decode("utf-8"))
    
    def parse(self, inputfile, targetword):
        self.global_input = inputfile
        self.global_targetword = targetword
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(inputfile, parser=parser)
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
            instance_data = []
            instance_data.append(instance_id)
            instance_data.append(sense_id)
            instance_data.append(context_raw_text)
            self.instances_data.append(instance_data)
            self.raw_text.append(context_raw_text)
            self.clean_text.append(context_fine_text) 
