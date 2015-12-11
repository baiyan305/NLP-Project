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
        clusters = hac.fcluster(dist_matrix, 1, criterion='distance')

        #plt.figure()
        #data = hac.dendrogram(dist_matrix)

        #print(data)
        #plt.show()

        return clusters