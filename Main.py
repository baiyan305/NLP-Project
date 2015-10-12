from XMLParser import XMLParser
from SenseCluster import SenseCluster
from SenseGenerator import SenseGenerator

input = "/Users/Yan/IdeaProjects/WordSense/src/charged.xml"

#parse XML to get all instances
xmlparser = XMLParser()
xmlparser.parse(input)
instances_raw = xmlparser.get_raw_text()
instances_clean = xmlparser.get_clean_text()

#cluster instances
sense_cluster = SenseCluster()
sense_cluster.cluster(instances_clean)
groups = sense_cluster.get_groups() #all clusters
common_words = sense_cluster.get_commonwords() #common words for each cluster

#generate sense
senseGenerator = SenseGenerator()
examples = senseGenerator.generate_example(groups)
#print examples

commonwords= senseGenerator.collect_topWords(senseGenerator.simplify_lists(common_words))
#print commonwords

definitions=senseGenerator.generate_definition(commonwords)
#print definitions

senseGenerator.display_results(examples, definitions)