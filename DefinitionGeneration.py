#Author: Bharath Kumar Bommana
# This class is for generating the definitions for each cluster.
# Our idea is very loosely based on the idea discussed in this paper: Word Sense Induction Using Graphs of Collocations
# link : http://dl.acm.org/citation.cfm?id=1567349
#
# The idea is that the definitions of a word in a context depends on the collocated words
#
# In each cluster, we collect the 5 words present on either side of the target word in the context and
# form a list that contains all collocated words
#  ----> done in get_collocated_words(self, clusters, cleaned_instances, target) function <-----
#
# From the list of collocated words, we get the top 2 most repeated words and use them in generating the definitions
#  -----> done using findTopWords(self, collocatedWords) and collect_topWords(self, list2): functions  <----

# Once we have the top2 words for each cluster, Our initial idea was to POS_TAG those two words and then use appropriate template to generate a
# easily readable complete sentence.
#  But we were not able to test this feature on clean ubuntu machine due to some issues with the installation of NLTK
#
# So we are randomly choosing the template and generating definitions.
#  ----> done in sentence_completion (self, topWords) function <-----
#
# #
#input: 1. clusters - list of lists
#          example : [[1,3,7], [2,6,8]]
#
#       2. cleaned_instances - list of lists
#           example : [['word1', 'word2','word3'], ['word4','word1', 'word3',], ['word1', 'word2','word3', 'word5']....]

#       intermediate results:
#       collocatedWords = [[word1, word2, word2, word1, word3, word4, word5], ['word4','word1', 'word3',word3, word4] ]
#       topWords = [[word1, word2], [word3,word4]]
#
#      output: Definitions- a list
#           example : [refers to an action similar to word1 AND/OR word2, refers to the name of a place, entity or quality similar to word3 AND/OR word4]
#
#-------------------------------------------------------------------------------------------------------------------------------

#import nltk
#from nltk.tag import pos_tag, map_tag

import random
#random is to select one instance randomly from a list.

class DefinitionGeneration:

    # generates the list of words located on either side of target word in all the instances in a cluster
    # input for this function :
    #       1. clusters - list of lists
    #          example : [[1,3,7], [2,6,8], [4,5,9,10]]
    #
    #       2. cleaned_instances - list of lists
    #           example : [['word1', 'word2','word3'], ['word4','word1', 'word3',], ['word1', 'word2','word3', 'word5']]
    #
    # Output for this function:
    #       collocatedWords = [[word1, word2, word2, word1, word3, word4, word5],['word4','word1', 'word3',word3, word4]]
    #
    #
    def get_collocated_words(self, clusters, cleaned_instances):
        collocatedWords = []
        for cluster in clusters:
            wordsInCluster = []
            for index in cluster:
                #read the context corresponding to the index [instance id of the cluster]
                context = cleaned_instances[index]
                templist = []
                position = 25 #edit -> 25
                #taking the position of target word as 25 : XMLParser reads 50 words [25 on either side of target] in each context
                size = 5   # edit -> 5
                # reading 5 words on either side
                if (position > size):
                   templist = context[position-size:position+1]
                else:
                    templist= context[0:position+1]
                if (position+size < len(context)-1):
                    templist = templist +context[position+1: position+size+1]
                else:
                    templist = templist +context[position+1:len(context)]
                for word in templist:
                    wordsInCluster.append(word)
            #get collocated words in one cluster
            collocatedWords.append(wordsInCluster)
        return collocatedWords


    # generic function:
    # takes in a list and returns top2 most repeated elements in the list.
    # input : [word2, word1, word2, word1, word3,word4, word5]
    # output: [word2, word1]

    def collect_topWords(self, list2):
        mostcommonwords=[]
        counter = {}
        for item in list2:
                if item in counter:
                        counter[item]+=1
                else:
                        counter[item]=1
        #based on count of each word, words are sorted in decreasing order
        mostcommonwords = sorted(counter, key = counter.get, reverse = True)
        #pick top2 words
        top2= mostcommonwords[:2]
        return top2

    # get top2 words for each cluster
    def findTopWords(self, collocatedWords):
        topWords = []
        for wordslist in collocatedWords:
            temp = self.collect_topWords(wordslist)
            topWords.append(temp)
        return topWords

    # This function is to pos tag words and convert the penn tree pos tag into an UNIVERSAL pos tag
    # We were able to use this feature during development stage
    # Unfortunately we ran into issues with NLTK installation on a clean machine and hence, we are not using in our
    # final submission.

    #def pos_tagging(self, list2):
    #    str1 = ' '.join(list2)
    #    tokens= nltk.word_tokenize(str1)
    #    posTagged = pos_tag(tokens)
    #    posTagged = pos_tag(text)
    #    simplifiedTags = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in posTagged]
    #    return (simplifiedTags)
    #


    #this function is to get pos togs for each cluster

    #def get_pos_tags (self, topWords):
    #    topWords_with_tags = []
    #    for tops in topWords:
    #         topWords_with_tags.append(self.pos_tagging(tops))
    #    return topWords_with_tags


    # generating definitions

    #def definitions(self, words_with_tags):
    #    definitions = []
    #    for words in words_with_tags:
    #        #print words
    #        defs = []
    #        for word in words:
    #            list1 = list(word)
    #            self.complete_sentence(list1)
    #            defs.append(list1[0])
    #        #print(defs)
    #        definitions.append(defs[0]+" AND/OR " +defs[1])
    #    return definitions


    # based on the pos tag of each word, we generate a sentence for that word.
    #def complete_sentence (self, words):
    #    if (words[1] == 'VERB'):
    #            words[0]= "refers to an action similar to "+ ' '.join(words[0])
    #    elif (words[1] == 'NOUN'):
    #            words[0]= "refers to name of an entity, place or quality similar to "+  ' '.join(words[0])
    #    else:
    #            words[0]= "refers to the property or quality similar to "+ ' '.join(words[0])


    # since POS tags did not work, we chose to use random to generate final sentences
    # topWords = [[word1, word2], [word3,word4]]
    #
    # output: [refers to an action similar to word1 AND/OR word2, refers to the name of a place, entity or quality similar]

    def sentence_completion (self, topWords):
        str1 =  "refers to an action similar to "
        str2 = "refers to name of an entity, place or quality similar to "
        str3 = "refers to the property or quality similar to "
        s_list=[str1,str2,str3]
        #print s_list
        definitions = []
        for top2 in topWords:
            #randomly chose one of the template and form a complete sentence.
            try:
                definitions.append(random.choice(s_list)+" "+ top2[0] +" AND/OR "+ top2[1] )
            except IndexError:
                continue
        return definitions


    # function calls
    # wrapper function
    #returns the final definitions list
    ## output : ['refers to name of an entity, place or quality similar to  a AND/OR e', 'refers to name of an entity, place or quality similar to  p AND/OR k']

    def get_Definitions (self, clusters, cleaned_instances):

        list1= self.get_collocated_words(clusters, cleaned_instances)

        topwords = self.findTopWords(list1)

        #words_with_tags= self.get_pos_tags(topwords)
        #return self.definitions(words_with_tags)

        return self.sentence_completion(topwords)





