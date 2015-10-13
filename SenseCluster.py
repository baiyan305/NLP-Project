import string
import re

class SenseCluster:

    groups = []
    groups_commonwords = []
    similarities = []  #store similarities matrix
    commonwords = []   #store common words matrix

    #return group of sense
    def get_groups(self):
        return self.groups

    #return common words
    def get_commonwords(self):
        return self.groups_commonwords

    def cluster(self, instances):

        #strip punctuation first
        #index = 0
        #for instance in instances:
        #    instances[index] = self._strip_puctuation(instance)
        #    index = index + 1

        #divide every instance to words and save to list
        index = 0
        words = []  #store all words of all instances
        for instance in instances:
            words.append([])
            words[index] = instance.split()
            index = index + 1

        #strip words in blacklist
        for i in range(len(words)):
            words[i] = self._strip_words_inblacklist(words[i])

        #calculate similarities of each pair of instances
        size = len(words)
        for source in range(size):
            similarities_row = []
            commonwords_row = []
            for dest in range(size):
                self._get_similarities(source, dest, words, similarities_row, commonwords_row)
            self.similarities.append(similarities_row)
            self.commonwords.append(commonwords_row)

        best_matchs = []
        index = 0
        for similarity in self.similarities:
            #print similarity
            best_match = []
            big_num = max(similarity)
            big_num_index = similarity.index(big_num)
            best_match.append(index)
            best_match.append(big_num_index)
            best_matchs.append(best_match)
            index = index + 1

        processed = []
        for i in range(size):
            group = []
            group_commonword = []
            group_size = 0;

            if(i not in processed):
                group.append(best_matchs[i][0])
                group.append(best_matchs[i][1])
                group_commonword.append(self.commonwords[best_matchs[i][0]][best_matchs[i][1]])

                #forward
                while(group_size != len(group)):
                    group_size = len(group)
                    for j in range(size):
                        if( (i != j) and (j not in processed) ):
                            if( (best_matchs[j][0] in group) and (best_matchs[j][1] in group) ):
                                processed.append(j)
                            if( (best_matchs[j][0] in group) and (best_matchs[j][1] not in group)):
                                group.append(best_matchs[j][1])
                                group_commonword[0].extend(self.commonwords[best_matchs[j][0]][best_matchs[j][1]])
                                processed.append(j)
                            elif( (best_matchs[j][1] in group) and (best_matchs[j][0] not in group)):
                                group.append(best_matchs[j][0])
                                group_commonword[0].extend(self.commonwords[best_matchs[j][1]][best_matchs[j][0]])
                                processed.append(j)

            if(len(group) > 0):
                self.groups.append(group)
                self.groups_commonwords.append(group_commonword)

    #calculate similarities of two instances. Output similarity to list 'similarities' and common word to list 'commonwords'
    def _get_similarities(self, source, dest, words, similarities, commonwords):
        if(source != dest):
            words_of_source = set(words[source])
            words_of_dest = set(words[dest])

            #print words_of_source
            #print words_of_dest

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

    def _strip_words_inblacklist(self, list_of_words):
        blacklist = ["and", "or", "no", "yes", "in", "at", "that", "the", "to", "for", "if", "while", "until", "it", "i",
                     "he", "you", "his", "they", "this", "that", "she", "her", "we", "all", "which", "their", "what", "my"
                     "him", "me", "who", "them", "some", "other", "your", "its", "our", "these", "any", "more", "many",
                     "such", "those", "us", "how", "another", "where", "something", "each", "both", "last", "every", "one",
                     "much", "few", "why", "once", "none", "youll", "thats", "as", "a", "are", "of", "be", "is", "on", "into",
                     "but", "did", "was", "were", "when", "out", "so", "an", "by", "from", "before", "about", "very", "has",
                     "been", "then", "with", "not", "will", "had", "not", "soon", "got", "never", "dont", "him", "up", "down",
                     "just", "than", "went"]
        prog = re.compile("<head>.*<head>")
        new_list = []
        for word in list_of_words:
            if( (word.lower() not in blacklist) and not (prog.match(word)) ):
                new_list.append(word)
        
        return new_list
