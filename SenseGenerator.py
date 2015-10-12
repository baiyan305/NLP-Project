class SenseGenerator:

    #generate_example:  select a random sentence from each cluster
    def generate_example(self, list1):
        import random
        examples = []
        for items in list1:
            choice = random.choice(items)
            examples.append(choice)
        return examples

    #to convert list of list of lists returned by get_commonwords function to a simpler list of lists
    def simplify_lists(self, list1):
        simple_list=[]
        for items in list1:
            for item in items:
                simple_list.append(item)
        return simple_list

    #collect_topWords: collects top 3 most repeated words for each sense in the common words list- from similarity matrix
    def collect_topWords(self, list2):
        mostcommonwords=[]
        for items in list2:
            word_counter = {}
            for word in items:
                if word in word_counter:
                    word_counter[word]+=1
                else:
                    word_counter[word]=1
            popular_words= sorted(word_counter, key = word_counter.get, reverse = True)
            top3=popular_words[:3]
            mostcommonwords.append(top3)
        return mostcommonwords


    #generate_definition: generates meaning for the sense from the top words collected
    def generate_definition(self, list3):
        definitions=[]
        for items in list3:
            meanings=' '.join(items)
            definitions.append(meanings)
        return definitions


    #display_results: displays results in the form of a dictinary
    def display_results(self, list4, list5):
        for items in range(len(list4)):
            print "sense: %s" %items
            print "definition: "+list5[items]
            print "example: %s" %list4[items]
