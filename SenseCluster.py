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

    #instance data after clustering
    instances_data = []

    #return clusters
    def get_clusters(self):
        return self.clusters

    #return dimensions
    def get_dimensions(self):
        return self.dimensions

    #return instances data
    def get_instance_data(self):
        return self.instances_data

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

        for i in range(len(instances)):
            self.instances_data.append([])

        for i in range(len(self.clusters)):
            temp = self.clusters[i]
            for j in range(len(temp)):
                instanceid = temp[j]
                self.instances_data[instanceid].append(str(instanceid))
                self.instances_data[instanceid].append(str(i))

    #generate contexts vectors
    def generate_context_vector(self, instances):
        contexts_vector = []
        for instance in instances:
            context_vector = []
            for dimension in self.dimensions:
                count = instance.count(dimension)
                context_vector.append(count)
            contexts_vector.append(context_vector)

        return contexts_vector

    #pick top 100 most occuring words as dimension
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

    #use hierarchy clustring to cluster
    def hierarchy_cluster(self, contexts_vectors):
        threshold = 10
        if(len(contexts_vectors) > 2000):
            threshold = 20
        dist_matrix = hac.linkage(contexts_vectors, "ward")
        clusters = hac.fcluster(dist_matrix, threshold, criterion='distance')

        #plt.figure()
        #data = hac.dendrogram(dist_matrix)

        #print(data)
        #plt.show()

        return clusters