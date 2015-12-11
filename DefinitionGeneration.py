#nput: 1. clusters - list of lists
#          example : [[1,3,7], [2,6,8], [4,5,9,10]]
#
#       2. raw_instances - list
#          example : [context1, context2, context3,......., context10]
#
#       3. cleaned_instances - list of lists
#           example : [['word1', 'word2','word3'], ['word4','word1', 'word3',], ['word1', 'word2','word3', 'word5']]
#
#       4. target :  target word
#            example : charged (just a word)
#

import nltk
from nltk.tag import pos_tag, map_tag

class DefinitionGeneration:


    def get_collocated_words(self, clusters, cleaned_instances, target):
        collocatedWords = []
        for cluster in clusters:
            wordsInCluster = []
            for index in cluster:
                context = cleaned_instances[index]
                templist = []
                position = 25 #edit -> 25
                size = 5   # edit -> 5
                if (position > 1):
                   templist = context[position-size:position+1]
                else:
                    templist= context[0:position+1]
                if (position+size < len(context)-1):
                    templist = templist +context[position+1: position+size+1]
                else:
                    templist = templist +context[position+1:len(context)]
                for word in templist:
                    wordsInCluster.append(word)
            collocatedWords.append(wordsInCluster)
        return collocatedWords


    def collect_topWords(self, list2):
        mostcommonwords=[]
        counter = {}
        for item in list2:
                if item in counter:
                        counter[item]+=1
                else:
                        counter[item]=1
        mostcommonwords = sorted(counter, key = counter.get, reverse = True)
        top2= mostcommonwords[:2]
        return top2


    def findTopWords(self, collocatedWords):
        topWords = []
        for words in collocatedWords:
            temp = self.collect_topWords(words)
            topWords.append(temp)
        return topWords


    def pos_tagging(self, list2):
        str1 = ' '.join(list2)
        tokens= nltk.word_tokenize(str1)
        posTagged = pos_tag(tokens)
        simplifiedTags = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in posTagged]
        return (simplifiedTags)


    def get_pos_tags (self, topWords):
        topWords_with_tags = []
        for tops in topWords:
             topWords_with_tags.append(self.pos_tagging(tops))
        return topWords_with_tags


    def definitions(self, words_with_tags):
        definitions = []
        for words in words_with_tags:
            #print words
            defs = []
            for word in words:
                list1 = list(word)
                self.complete_sentence(list1)
                defs.append(list1[0])
            #print(defs)
            definitions.append(defs[0]+" AND/OR " +defs[1])
        return definitions


    def complete_sentence (self, words):
        if (words[1] == 'VERB'):
                words[0]= "refers to an action similar to "+ ' '.join(words[0])
        elif (words[1] == 'NOUN'):
                words[0]= "refers to name of an entity, place or quality similar to "+  ' '.join(words[0])
        else:
                words[0]= "refers to the property or quality similar to "+ ' '.join(words[0])
    
    def get_Definitions (self, clusters, cleaned_instances, target):

        list1= self.get_collocated_words(clusters, cleaned_instances, target)

        topwords = self.findTopWords(list1)

        words_with_tags= self.get_pos_tags(topwords)
        return self.definitions(words_with_tags)
