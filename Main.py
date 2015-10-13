#Author: Bharath Kumar Bommana
#Main.py is the file that has all the function calls and ensure the sequential flow of data through the system,

from XMLParser import XMLParser
from SenseCluster import SenseCluster
from SenseGenerator import SenseGenerator
from Util import Util
import subprocess
import sys
import os
import time
import shutil
#subprocess is used to keep the linux commands waited until all the required files are generated(command1 at the bottom of this file)
#os is used to execute to linux commands from python script
#sys for commandline args

#delete output folder
shutil.rmtree("out", ignore_errors=True)

num_of_argv = len(sys.argv)
inputpath = sys.argv[1]
targetword = None

#our program takes either two or 3 commands based on the number of target words in the input file
#to run name_conflate pair - we will have 3 arguments: input_file-name targetword1 targetword2
#to run noun/verb file - we have two arguments: input_file-name targetword
if(num_of_argv == 3):
    targetword = sys.argv[2]
elif(num_of_argv == 4):
    targetword = (sys.argv[2])[0] + "_" + (sys.argv[3])[0]

print("===================Process start==================")
print("input file: " + inputpath)
print("target word: " + targetword)

print("Parsing XML...")
#parse XML to get all instances
xmlparser = XMLParser()
xmlparser.parse(inputpath, targetword)
instances_raw = xmlparser.get_raw_text()
#instances_raw contains the (context)entire text between context tags in xml file
instances_clean = xmlparser.get_clean_text()
#instances_clean contains the text between context tags in xml file but this text is cleaned-> extra symbols are removed
instances_data_old = xmlparser.get_instances_data()
#instances_data_old-> contains [instance id, senseid]. This list can be used to generate .key file for the target word in question.

print( str(len(instances_data_old)) + " instances found.")

print("Clustering instances...")

#cluster instances
sense_cluster = SenseCluster()
sense_cluster.cluster(instances_clean)
groups = sense_cluster.get_groups() #all clusters
common_words = sense_cluster.get_commonwords() #common words for each cluster

print( str(len(groups)) + " clusters created.")
print("Generating definitions and examples...")

#generate sense
senseGenerator = SenseGenerator()
examples = senseGenerator.generate_example(groups, instances_data_old)
#list of examples picked for each cluster
commonwords = senseGenerator.collect_topWords(senseGenerator.simplify_lists(common_words))
definitions = senseGenerator.generate_definition(commonwords)
#generated definitions for each cluster


#All the output files will be stored in ./out directory

print("write defitions and example to "+"/out/"+targetword+".answer.txt")
#output definitions and examples
Util.generate_answer_file(targetword, definitions, examples, "./out/", targetword+".answer.txt")

print("write instances to "+"/out/"+targetword+"_Semeval2.xml")
#output senseval-2
Util.generate_SemEval2Format(instances_raw, groups, "./out/", targetword+"_Semeval2.xml");

print("write key file of input to "+"/out/"+targetword+".old.key")
#output original key file
Util.generate_key_file(instances_data_old , targetword, "./out/", targetword+".old.key")

print("write key file of ouput to "+"/out/"+targetword+".new.key")
#output new key file
instances_data_new = senseGenerator.generate_instance_sense_pairs(groups)
Util.generate_key_file(instances_data_new , targetword, "./out/", targetword+".new.key")

print("sensecluters_scorer.sh in running...")
#call sensecluster_score.sh
command1 = "./senseclusters_scorer.sh" +  " ../out/"+targetword+".new.key" + " ../out/"+targetword+".old.key"

#to make sure the execution of command1 waits until writing into the files is finished. 
while not (os.path.exists("./out/"+targetword+".old.key") or os.path.exists("./out/"+targetword+".new.key")):
    time.sleep(10)
#change directory
os.chdir(os.getcwd()+"/senseclusters_scorer/")
#run sensecluster_scorer program
os.system(command1)

print("========================Done======================")
