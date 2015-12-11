# @author: Yan Bai
# 
# This class clusters instances. The idea of approach using here is from a paper named "Automatic
# Word Sense Discrimination" by Hinrich Schutze. Our understanding is included in README file.
#
# Usage:
#      1. First call cluster() function. Pass instances to cluster() function.
#      2. After that call get_cluster() function to get clusters.

from collections import Counter
import scipy.cluster.hierarchy as hac

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
        #get dimensions
        self.extract_dimensions(instances)
        #get contexts vectors
        contexts_vectors = self.generate_context_vector(instances)
        #clustering
        res = self.hierarchy_cluster(contexts_vectors)

        num_of_cluster = max(res)

        #push clusters to list 'clusters'
        for i in range(0, num_of_cluster):
            self.clusters.append([])
        for index in range(0, len(res)):
            self.clusters[res[index]-1].append(index)

        #create new instances data based on clustering
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

        return clusters
