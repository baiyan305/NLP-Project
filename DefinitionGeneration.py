#Author: Bharath Kumar Bommana
# This class is for generating the definitions for each cluster.
# The idea is that the definitions of a word in a context depends on the collocated words
# In each cluster, we collect the 5 words present on either side of the target word in the context and
# form a list that contains all collocated words
# From the list of collocated words, we get the top 2 most repeated words and use them in generating the definitions
# Once we have the top2 words for each clustr, we POS_TAG those two words and then use appropriate template to generate a
# easily readable complete sentence.
#
#input: 1. clusters - list of lists
#          example : [[1,3,7], [2,6,8], [4,5,9,10]]
#
#       2. cleaned_instances - list of lists
#           example : [['word1', 'word2','word3'], ['word4','word1', 'word3',], ['word1', 'word2','word3', 'word5']]
#
#      output: Definitions- a list
#           example : [refers to an action similar to word1, refers to the name of a place, entity or quality similar to word2]
#-------------------------------------------------------------------------------------------------------------------------------

import random
class DefinitionGeneration:


    def get_collocated_words(self, clusters, cleaned_instances, target):
        collocatedWords = []
        for cluster in clusters:
            wordsInCluster = []
            for index in cluster:
                context = cleaned_instances[index]
                templist = []
                position = 1 #edit -> 25
                size = 1   # edit -> 5
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

    def sentence_completion (self, topWords):
        str1 =  "refers to an action similar to "
        str2 = "refers to name of an entity, place or quality similar to "
        str3 = "refers to the property or quality similar to "
        s_list=[str1,str2,str3]
        #print s_list
        definitions = []
        for top2 in topWords:
            definitions.append(random.choice(s_list)+" "+ top2[0] +" AND/OR "+ top2[1] )
        return definitions

    def get_Definitions (self, clusters, cleaned_instances, target):

        list1= self.get_collocated_words(clusters, cleaned_instances, target)

        topwords = self.findTopWords(list1)

        return self.sentence_completion(topwords)





