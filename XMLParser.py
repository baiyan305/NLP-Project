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

    #return list of instance text without punctuations and stop words
    def get_clean_text(self):
        return self.clean_text

    #return input file path
    def get_input_path(self):
        return self.global_input
    
    #return target word
    def get_targetword(self):
        return self.global_targetword

    #remove punctuations and stop words and get 25 words left and right to target word
    def _strip_punctuation(self, context):
        stopwords = ["and", "or", "no", "yes", "in", "at", "that", "the", "to", "for", "if", "while", "until", "it", "i",
                     "he", "you", "his", "they", "this", "that", "she", "her", "we", "all", "which", "their", "what", "my"
                     "him", "me", "who", "them", "some", "other", "your", "its", "our", "these", "any", "more", "many",
                     "such", "those", "us", "how", "another", "where", "something", "each", "both", "last", "every", "one",
                     "much", "few", "why", "once", "none", "youll", "thats", "as", "a", "are", "of", "be", "is", "on", "into",
                     "but", "did", "was", "were", "when", "out", "so", "an", "by", "from", "before", "about", "very", "has",
                     "been", "then", "with", "not", "will", "had", "not", "soon", "got", "never", "dont", "him", "up", "down",
                     "just", "than", "went", "himself", "herself", "itself", "themselves", "have", "has", "had", "except",
                     "thought", "do", "does", "does", "doing", "done", "mr", "mrs", "others", "down", "should", "shall", "whose",
                     "now", "later", "seen", "too", "also", "will", "would", "can", "could", "there", "here", "over", "being",
                     "between", "may", "might", "only", "back", "under", "even", "because", "still", "my", "after", "since",
                     "couldnt", "recently", "often", "Im", "else", "away", "wasnt", "didnt", "usually", "doesnt", "a", "b"
                     "c", "d", "e", "f", "g", "h", "i", "g", "k", "l", "m", "n", "o", "p", "q", "s", "t", "u", "v", "w", "x"
                     "y", "z", "yet", "mays", "exactly"]

        #strip punctuation
        pattern = re.compile(u'[.,:#"!?;()-/\']')
        str_no_punc = re.sub(pattern, "", context.decode("utf-8"))  #strip punctuation

        #find index target word
        prog = re.compile("<head>.*<head>")
        index = 0
        words = str_no_punc.split()
        for word in words:
            if re.match(prog, word):
                break
            else:
                index += 1

        #extract 25 words to the left and the right from index of target word
        left = index - 1
        right = index + 1
        counter = 0
        available_words = []
        while(left>=0 and counter < 25):
            if words[left].lower() not in stopwords:
                available_words.append(words[left].lower())
                counter += 1
            left -= 1
        counter = 0
        while(right<=len(words)-1 and counter < 25):
            if words[right].lower() not in stopwords:
                available_words.append(words[right].lower())
                counter += 1
            right += 1

        return available_words

    def extract_target_word(self, instance):
        children = list(instance)
        context = children[1]
        context_in_string = etree.tostringlist(context, encoding="utf-8", method="xml")[0]
        context_raw_text = context_in_string[10:-11]        #extract instance text

        #strip punctuation
        pattern = re.compile(u'[.,:#"!?;()-/\']')
        str_no_punc = re.sub(pattern, "", context_raw_text.decode("utf-8"))  #strip punctuation

        #find target word
        prog = re.compile("<head>.*<head>")
        words = str_no_punc.split()
        for word in words:
            if re.match(prog, word):
                self.global_targetword = re.match(prog, word).string[6:-6]
                return

    
    #use lxml library to parse XML file to extract data
    def parse(self, inputfile, targetword):
        self.global_input = inputfile
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(inputfile, parser=parser)
        root = tree.getroot()

        instances = root.findall('.//instance')

        self.extract_target_word(instances[0])

        for instance in instances:
            instance_data = []
            instance_id = instance.get("id")        #extract instance id
            children = list(instance)
            answer = children[0]
            context = children[1]
            sense_id = answer.get("senseid")        #extract sense id
            context_in_string = etree.tostringlist(context, encoding="utf-8", method="xml")[0]
            context_raw_text = context_in_string[10:-11]        #extract instance text
            context_vector_words = self._strip_punctuation(context_raw_text)       #instance text without punctuation
            instance_data = []
            instance_data.append(instance_id)         #push instance id to list
            instance_data.append(sense_id)            #push sense id to list   
            instance_data.append(context_raw_text)    #push instance text to list
            self.instances_data.append(instance_data) #push instance itself to bigger list 
            self.raw_text.append(context_raw_text)
            self.clean_text.append(context_vector_words)
