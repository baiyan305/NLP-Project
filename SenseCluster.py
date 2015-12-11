# author: Yan Bai
# 
# this class clusters instances and picks common words shared by instances in same cluster.
# common words will be used to generate sense.
#
# the general idea of clustering is based on common words among instances.

from collections import Counter
import scipy.cluster.hierarchy as hac
import matplotlib.pyplot as plt
import string
import re
import math

class SenseCluster:

    #store clusters. It is a list of lists. Each list indicates a cluster.
    groups = []

    #store common words of cluters. We use common words of instances in a cluster to generate sense.
    groups_commonwords = []

    #A matrix to store similarities of each instance pair. Similarity in this context is a number of common words of 2 instaces.
    similarities = []

    #A matrix to store common words of each instance pair.
    commonwords = []

    #clusters
    clusters = []

    #dimensions
    dimensions = []

    def get_clusters(self):
        return self.clusters

    def get_dimensions(self):
        return self.dimensions

    #cluster contexts
    def cluster(self, instances):
        self.extract_dimensions(instances)
        contexts_vectors = self.generate_context_vector(instances)
        res = self.hierarchy_cluster(contexts_vectors)

        num_of_cluster = max(res)

        for i in range(0, num_of_cluster):
            self.clusters.append([])

        for index in range(0, len(res)):
            self.clusters[res[index]-1].append(index)

    def generate_context_vector(self, instances):
        contexts_vector = []
        for instance in instances:
            context_vector = []
            for dimension in self.dimensions:
                count = instance.count(dimension)
                context_vector.append(count)
            contexts_vector.append(context_vector)

        return contexts_vector

    def extract_dimensions(self, instances):
        wordcount = {}
        for context in instances:
            for word in context:
                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word] += 1

        counter = Counter(wordcount)

        for index in range(0, len(instances)):
            self.dimensions.append(counter.most_common()[index][0])

    def hierarchy_cluster(self, contexts_vectors):
        dist_matrix = hac.linkage(contexts_vectors, "ward")
        clusters = hac.fcluster(dist_matrix, 10, criterion='distance')

        #plt.figure()
        #data = hac.dendrogram(dist_matrix)

        #print(data)
        #plt.show()

        return clusters

    #return clusters
    def get_groups(self):
        return self.groups

    #return common words
    def get_commonwords(self):
        return self.groups_commonwords

    #calculate similarities of two instances. Output similarity to list 'similarities' and common word to list 'commonwords'
    def _get_similarities(self, source, dest, words, similarities, commonwords):
        if(source != dest):
            words_of_source = set(words[source])
            words_of_dest = set(words[dest])

            num_of_common = 0
            common_words = []
            for word_source in words_of_source:
                for word_dest in words_of_dest:
                    if( word_source == word_dest and (not re.match("head.*head", word_source)) ):
                        num_of_common = num_of_common + 1
                        common_words.append(word_dest)
            similarities.append(num_of_common)
            commonwords.append(common_words)

        else:
            similarities.append(0);
            commonwords.append([]);

    #strip punctuation in string
    def _strip_puctuation(self, str):
        delset = string.punctuation
        return str.translate(None, delset)

    #skip words in blacklist when compare words between 2 instances. Because these word can not help generate sense.
    def _strip_words_inblacklist(self, list_of_words):
        blacklist = ["and", "or", "no", "yes", "in", "at", "that", "the", "to", "for", "if", "while", "until", "it", "i",
                     "he", "you", "his", "they", "this", "that", "she", "her", "we", "all", "which", "their", "what", "my"
                     "him", "me", "who", "them", "some", "other", "your", "its", "our", "these", "any", "more", "many",
                     "such", "those", "us", "how", "another", "where", "something", "each", "both", "last", "every", "one",
                     "much", "few", "why", "once", "none", "youll", "thats", "as", "a", "are", "of", "be", "is", "on", "into",
                     "but", "did", "was", "were", "when", "out", "so", "an", "by", "from", "before", "about", "very", "has",
                     "been", "then", "with", "not", "will", "had", "not", "soon", "got", "never", "dont", "him", "up", "down",
                     "just", "than", "went", "himself", "herself", "itself", "themselves", "have", "has", "had", "except", 
                     "thought", "do", "does", "does", "doing", "done", "Mr", "Mrs", "others", "down", "should", "shall", 
                     "whose", "now", "later", "seen", "too", "also", "will", "would", "can", "could", "there", "here",
                     "over", "being", "between", "may", "might", "only", "back", "under", "even", "because", "still",
                     "my", "after"]
        prog = re.compile("<head>.*<head>")  #skip target word
        prog.search()

        for word in list_of_words:

            print(prog.search(word))

            if( (word.lower() not in blacklist) and not (prog.match(word)) ):
                new_list.append(word)
        
        return new_list
