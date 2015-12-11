from __future__ import division
import re

class ExampleGenerator(object):
	ps=PorterStemmer()
	def sentences_intersection(self,s1,s2):
		return len(set(s1).intersection(s2))/((len(s1)+len(s2))/2)
	
	def get_length(self,content):
		length=0
		for listitem in content:
			length=length+len(listitem)
		return length

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
			normalizedcount=self.get_length(content)/10
			topn=popular_words[:normalizedcount]
			mostcommonwords.append(topn)
		return mostcommonwords
	
	def get_frequency_score(self,content,i):
		thematicwords=self.collect_topwords(content)
		return len(set(content[i]).intersection(thematicwords))/((len(content[i])+len(thematicwords))/2)
		
	def get_sentence_ranks(self,content,temporary):
		#print(content[6])
		n=len(content)
		max=0
		global inkjuif
		#print(n)
		values=[[0 for x in xrange(n)] for x in xrange(n)]
		for i in range(0,n):
			score=0
			for j in range(0,n):
				if(i==j):
					continue
				if(values[j][i]>0):
					values[i][j]=values[j][i]
					score+=values[i][j]				
				else:			
					values[i][j]=self.sentences_intersection(content[i],content[j])
					score+=values[i][j]
			score+=self.get_frequency_score(content,i)			
			if(score>=max):
				max=score
				inkjuif=i
		return temporary[inkjuif]

	def get_examples(self, clusters,instances):
		example_list=[]
		temporary=[]
		for cluster in clusters:
		        length=len(cluster)
		        temporary=cluster[:]
		        cluster2=cluster[:]
		        for word in cluster2:
		        	word=ps.stem(word)
                        for index1 in range(0,length):
                                replace=cluster[index1]
				cluster2[index1]=instances[replace-1]
                        example_list.append(self.get_sentence_ranks(cluster2,temporary))
		return example_list
