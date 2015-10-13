#Author- Bharath Kumar Bommana
#...............................
#SenseGenerator class selects an example for every cluster
#and generates meaning for each cluster in the clusters(groups) obtained from SenseCluster.py class
#
#Example: clusters = [[0,1,2,3,4,5,6],[7,8,9,10,11,12],[13,14,15,16,17,18],[19,20,21]]
#			 In the above Example: the contexts belonging to instanceIds 0,1,2,3,4,5,6 belong to cluster 1 and the target word in
#			 this cluster are expected to have the same/similar sense.
#In this class, we pick one instance randomly as the example context for this cluster.
#
#Definition is generated from the list of common words.
#
#CommonWords -> SenseCluster class outputs the list of the words common(repeated) among the contexts in a cluster
#Example: common = [['eat', 'dog', 'eat', 'apple', 'juice', 'taste', 'fruit', 'fruit', 'taste', 'juice', 'eat', 'fruit', 'is', 'was', 'sweet'], ['company', 'laptop', 'ipad', 'ipod', 'ceo', 'innovation', 'expensive', 'laptop', 'company', 'iphone', 'iphone', 'ipad', 'hiring', 'objectiveC'], ['orchard', 'tree', 'farm', 'tree', 'farm', 'grow', 'seed', 'tree', 'grow']]

#in the above example, for cluster 1, the commonly repeated words are eat, dog, eat, apple, juice, taste, fruit, fruit, taste, juice, taste....., sweet

#SenseGenerator class finds the top 5 most repeated words in this list and constructs a definition out of those 5 words and returns this definition as the
#sense for this cluster.
#
#

import random
#random is to select one instance randomly from a list.
class SenseGenerator:
   
 
    #generate_example:  selects a random sentence from each cluster
    #groups contains instance_ids categorized into clusters
    #raw_text contains all the contexts read from xml input file
    def generate_example(self, groups, raw_text):
        examples = []
        examples_in_raw = []
        for group in groups:
	    #one random choice is selected from each cluster and appended to examples list.
            choice = random.choice(group)
            examples.append(choice)
        for example in examples:
            for instance_data in raw_text:
		#examples list contain instanceIds of examples
		#instaceIds will be replaced with corresponding actual contexts
                if(example == int(instance_data[0])):
                    examples_in_raw.append(instance_data[2])
       #list of example senteces is returned 
        return examples_in_raw
       

    #to convert list of list of lists returned by get_commonwords function to a simpler list of lists
    #This function is just a utility function to help in processing the common words list.
    def simplify_lists(self, list1):
        simple_list=[]
        for items in list1:
            for item in items:
                simple_list.append(item)
        return simple_list

    #collect_topWords: collects top 5 most repeated words for each sense in the common words list- from similarity matrix
    #list2 is a list of commonwords in each cluster
    #example=[[s1,s2,s3,s1,s2,s4,s1,s2,s1,s2],[s7,s6,s5,s7,s7,s3,s8,s9,s6,s6,s7,s5],[s,p,l,m,k,l,s,r,p,m,k,d,s,l,p,k,v]]
    #output: [[s1,s2,s3] [s6,s7,s5],[s,l,m]]
    def collect_topWords(self, list2):
        mostcommonwords=[]
        for items in list2:
            word_counter = {}
            for word in items:
                if word in word_counter:
                    word_counter[word]+=1
                else:
                    word_counter[word]=1
	    #based on count of each word, popular words are sorted in decreasing order
            popular_words= sorted(word_counter, key = word_counter.get, reverse = True)
            top5=popular_words[:5]
	    #pick top5 words
            mostcommonwords.append(top5)
        return mostcommonwords


    #generate_definition: generates meaning for the sense from the top words collected
    #example input: [[s1,s2,s3], [s5,s6,s7], [s,l,m]]
    #example output: [s1 s2 s3, s5 s6 s7, s l m]
    def generate_definition(self, list3):
        definitions=[]
        for items in list3:
            meanings=' '.join(items)
            definitions.append(meanings)
        return definitions 
    
    #this function is a utility function that generates a list that can be used in generating ouput key file in the next class
    #output format: instanceID senseID None
    def generate_instance_sense_pairs(self, clusters):
        list_Of_Pairs=[]

        for i in range(len(clusters)):
            for j in clusters[i]:
                pair = [j,i, None]
                list_Of_Pairs.append(pair)
        return list_Of_Pairs

    #display_results: displays results in the form of a dictinary
    #this function is used during the development of the system to test the output periodically.
    def display_results(self, list4, list5):
        for items in range(len(list4)):
            print("definition: "+list5[items])
            print("example: %s" %list4[items])
