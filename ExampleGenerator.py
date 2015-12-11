#Author: Swetha Naidu
# This class is for generating the best example for each cluster.
# Our idea is  based on the idea discussed in this paper: Graph Based Ranking Algorithms for Sentence Extraction Applied to Text Summarization
# link : http://www.aclweb.org/anthology/P04-3020
#
#Our idea is that the best example among the contexts depends on lexical similarity between the instances
#
#Among every two instances we calculate the intersection between any two instances based on the function.
#        >>>>>>>>>>>>>>>sentences_intersection(self,s1,s2) function<<<<<<<<<<<<<<<<

# In each cluster, we collect the sentence ranks by calling the following function. It assigns the weight for each edge between every two instances
#  >>>>>>>>>>>>>>>>>>>>>>>get_sentence_ranks(self, content, temporary) function<<<<<<<<<<<<<<<<
#
#Firstly, the stop words are removed from the list of instances. We also tried to stem the words to increase the similarity coefficient between every two instances.
#But since we had issues with installing NLTK, we had to skip that part. 
# We also wanted to get better example by including the top n common words (where n is a normalized value which is 1/10th of the number of words between in the given input list.) and giving a score based on the frequency of those words in our instances 
#But, as we had some issues in the code which could not be fixed on time we skip that part.
# input: 1. clusters - list of lists
#             example : [[1,3,7], [2,6,8]]
#           instances - list of lists
#             example : [['word1', 'word2','word3'], ['word4','word1', 'word3',], ['word1', 'word2','word3', 'word5']....]
#       2.  output:  list of examples
#               example_list : [12,34,67]    >>>>represents the index of the best example in our cluster
# When we tried to compute the time, it took 3 minutes for the 10,000 instances set.
#Time Complexity: O(n^2)
#-------------------------------------------------------------------------------------------------------------------------------
#import nltk
#from nltk.stem import *
#from nltk.stem.porter import *

from __future__ import division
import re

class ExampleGenerator(object):
         # Takes the clusters and cleaned_instances as input and generates the example_list as output 
         # input for this function :
    	 # 1. clusters - list of lists
    	 #     example : [[1,3,7], [2,6,8], [4,5,9,10]]
         #
         # 2. cleaned_instances - list of lists
         #     example : [['word1', 'word2','word3'], ['word4','word1', 'word3',], ['word1', 'word2','word3', 'word5']]
         #
         # Output for this function:
         #       example_list = [12,34,56,78]
         #ps=PorterStemmer()   >>>>based on our initial idea
    	def sentences_intersection(self,s1,s2):
		return len(set(s1).intersection(s2))/((len(s1)+len(s2))/2)
        # This function is to get the similarity coefficient between the instances and get the similarity weight associated with each vertex.
	def get_sentence_ranks(self,content,temporary):
		#print(content[6])
		n=len(content)
		max=0
		global inkjuif
		#values stores the similarity weight between every two instances with indices i and j
		values=[[0 for x in xrange(n)] for x in xrange(n)]
		
		for i in range(0,n):
			score=0
			for j in range(0,n):
				if(i==j):
					continue
				if(values[j][i]>0):
					values[i][j]=values[j][i]
					#score represents the similarity rank for each instance
					score+=values[i][j]				
				else:			
					values[i][j]=self.sentences_intersection(content[i],content[j])
					score+=values[i][j]			
			#the below line is based on idea to assign frequency score along with similaity score to each instance.
			#score+=get_frequency_score(content,i)
			#score represents the similarity score of each instance.
			if(score>=max):
				max=score
				inkjuif=i
		return temporary[inkjuif]

	#This commented part is based on our idea which we could not implement due to some issues. 
	#The main idea is to better example generation by taking another metric of frequency of most common words
	#Each instance is given a weight based on the the number of frequent words that the sentence has among the top most common words.
	def get_length(self,content):
		length=0
		for listitem in content:
			length=length+len(listitem)
		return length
	#This function returns the top words that are common in our cluster
	def collect_topwords(self,content):
		mostcommonwords=[]
		for items in content:
			word_counter={}
			for word in items:
				if word in word_counter:
					word_counter[word]+=1
				else:
					word_counter[word]=1
			popular_words=sorted(word_counter,key=word_counter.get,reverse=True)
			normalizedcount=self.get_length(content)/10 #This is used to get the normalized count t select the number of common words based on length of instnce
			topn=popular_words[:normalizedcount]
			mostcommonwords.append(topn)
		return mostcommonwords
	
	#This function returns a frequency_score which is added to the score for each instance.
	def get_frequency_score(self,content,i):
		thematicwords=self.collect_topwords(content)
		return len(set(content[i]).intersection(thematicwords))/((len(content[i])+len(thematicwords))/2)

        #This function generates the example by taking the following 
        #input:
        #clusters: list of lists [[1,2,3],[4,5,6]]
        #instances: list of instacnes example : [['word1', 'word2','word3'], ['word4','word1', 'word3',], ['word1', 'word2','word3', 'word5']....]
	#output:
	#example_list:[12,34,56]
	#We did not want to change the input clusters file. So we took two newlists viz temporary and cluster2
	#Finally, we append the examples in a list and return that list.
	def get_examples(self, clusters,instances):
		example_list=[]
		temporary=[]
		for cluster in clusters:
		        length=len(cluster)
		        temporary=cluster[:]
		        cluster2=cluster[:]
		        #These lines were based on our previous idea to stem the words using NLTK.
		        #for word in cluster2:
		        	#word=ps.stem(word)
                        for index1 in range(0,length):
                                replace=cluster[index1]
				cluster2[index1]=instances[replace-1]
                        example_list.append(self.get_sentence_ranks(cluster2,temporary))
		return example_list
