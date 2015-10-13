from XMLParser import XMLParser
from SenseCluster import SenseCluster
from SenseGenerator import SenseGenerator
from Util import Util
import subprocess
import sys
import os
import time

num_of_argv = len(sys.argv)
inputpath = sys.argv[1]
targetword = None

if(num_of_argv == 3):
    targetword = sys.argv[2]
elif(num_of_argv == 4):
    targetword = (sys.argv[2])[0] + "_" + (sys.argv[3])[0]

#parse XML to get all instances
xmlparser = XMLParser()
xmlparser.parse(inputpath, targetword)
instances_raw = xmlparser.get_raw_text()
instances_clean = xmlparser.get_clean_text()
instances_data_old = xmlparser.get_instances_data()

#cluster instances
sense_cluster = SenseCluster()
sense_cluster.cluster(instances_clean)
groups = sense_cluster.get_groups() #all clusters
common_words = sense_cluster.get_commonwords() #common words for each cluster

#generate sense
senseGenerator = SenseGenerator()
examples = senseGenerator.generate_example(groups, instances_data_old)
commonwords = senseGenerator.collect_topWords(senseGenerator.simplify_lists(common_words))
definitions = senseGenerator.generate_definition(commonwords)

#output definitions and examples
Util.generate_answer_file(targetword, definitions, examples, "./out/", targetword+".answer.txt")

#output senseval-2
Util.generate_SemEval2Format(instances_raw, groups, "./out/", targetword+"_Semeval2.xml");

#output original key file
Util.generate_key_file(instances_data_old , targetword, "./out/", targetword+".old.key")

#output new key file
instances_data_new = senseGenerator.generate_instance_sense_pairs(groups)
Util.generate_key_file(instances_data_new , targetword, "./out/", targetword+".new.key")

#call sensecluster_score.sh
command1 = "./senseclusters_scorer.sh" +  " ../out/"+targetword+".new.key" + " ../out/"+targetword+".old.key"

while not (os.path.exists("./out/"+targetword+".old.key") or os.path.exists("./out/"+targetword+".new.key")):
    time.sleep(10)
os.chdir(os.getcwd()+"/senseclusters_scorer/")
os.system(command1)
