# author: Yan Bai
#
# this class extracts data from XML files and converts to required Python data structure.
# data generated in this class will be used for SenseCluster.py and SenseGenerator.py

from lxml import etree
import string
import re

class XMLParser:

    instances_data = []         #store instance information including instance id, sense id and instance text
    raw_text = []               #store raw text of instances
    clean_text = []             #store text of instances without punctuation
    global_input = None
    global_targetword = None

    #return list of instances data.
    #
    #return data format:
    #[
    #  [instance_id, sense_id, instance_text],
    #  [0, 0, text_of_instance_0],
    #  [1, 0, text_of_instance_1],
    #  ...
    #]
    def get_instances_data(self):
        return self.instances_data
    
    #return list of instance text
    def get_raw_text(self):
        return self.raw_text

    #return list of instance text without punctuation
    def get_clean_text(self):
        return self.clean_text

    #return input file path
    def get_input_path(self):
        return self.global_input
    
    #return target word
    def get_targetword():
        return self.global_targetword

    #strip punctuation in string
    def _strip_punctuation(self, str):
        pattern = re.compile(u'[.,:#"!?;()-/\']')
        return re.sub(pattern,"",str.decode("utf-8"))
    
    #use lxml library to parse XML file to extract data
    def parse(self, inputfile, targetword):
        self.global_input = inputfile
        self.global_targetword = targetword
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(inputfile, parser=parser)
        root = tree.getroot()
        
        for instance in root.findall('.//instance'):
            instance_data = []
            instance_id = instance.get("id")        #extract instance id
            children = list(instance)
            answer = children[0]
            context = children[1]
            sense_id = answer.get("senseid")        #extract sense id
            context_in_string = etree.tostringlist(context,encoding="us-ascii",method="xml")[0]
            context_raw_text = context_in_string[10:-11]        #extract instance text
            context_fine_text = self._strip_punctuation(context_raw_text)       #instance text without punctuation
            instance_data = []
            instance_data.append(instance_id)         #push instance id to list
            instance_data.append(sense_id)            #push sense id to list   
            instance_data.append(context_raw_text)    #push instance text to list
            self.instances_data.append(instance_data) #push instance itself to bigger list 
            self.raw_text.append(context_raw_text)
            self.clean_text.append(context_fine_text) 
