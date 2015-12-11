#Author: Bharath Kumar Bommana
#Main.py is the file that has all the function calls and ensure the sequential flow of data through the system,

from XMLParser import XMLParser
from SenseCluster import SenseCluster
from ExampleGenerator import ExampleGenerator
from DefinitionGeneration import DefinitionGeneration
from time import strftime
from Util import Util
import sys
import os
import time
import shutil

def time():
    return strftime("%Y-%m-%d %H:%M:%S")

#delete output folder
shutil.rmtree("out", ignore_errors=True)

inputpath = sys.argv[1]
print(time()+" ===================Process start==================")
print(time()+" input file: " + inputpath)

#parse XML to get all instances
print(time()+" Parsing XML...")
xmlparser = XMLParser()
xmlparser.parse(inputpath)
instances_text_raw = xmlparser.get_raw_text()           #instances_raw contains the (context)entire text between context tags in xml file
instances_text_clean = xmlparser.get_clean_text()       #instances_clean contains the text between context tags in xml file but this text is cleaned-> extra symbols are removed
instances_data_old = xmlparser.get_instances_data()     #instances_data_old contains instance ids and sense ids. Use it to generate key file.
targetword = xmlparser.get_targetword()
print(time()+" Parsing XML finish.")
print(time()+" target word: " + targetword)
print(time() + " "+str(len(instances_text_raw))+" instances found.")

#cluster instances
print(time()+" Clustering instances...")
sense_cluster = SenseCluster()
sense_cluster.cluster(instances_text_clean)
clusters = sense_cluster.get_clusters()
dimensions = sense_cluster.get_dimensions()
instances_data_new = sense_cluster.get_instance_data()
print(time()+" Clustering instances finish...")
print(time()+" "+str(len(clusters)) + " clusters was generated.")

#generate definition
print(time()+" Generating definitions...")
definitions_gen = DefinitionGeneration();
definitions = definitions_gen.get_Definitions(clusters, instances_text_clean)

#generate example
print(time()+ " Generating examples...")
example_gen = ExampleGenerator()
examples = example_gen.get_examples(clusters, instances_text_clean)

#All the output files will be stored in ./out directory

#output definitions and examples
print(time()+" write defitions and example to "+"/out/"+targetword+".answer.txt")
Util.generate_answer_file(targetword, instances_text_raw, definitions, examples, "./out/", targetword+".answer.txt")

#output senseval-2
print(time()+ "write instances to "+"/out/"+targetword+"_Semeval2.xml")
Util.generate_SemEval2Format(instances_text_raw, clusters, "./out/", targetword+"_Semeval2.xml");

#output original key file
print(time()+" write key file of input to "+"/out/"+targetword+".old.key")
Util.generate_key_file(instances_data_old, targetword, "./out/", targetword+".old.key")

print(time()+" write key file of ouput to "+"/out/"+targetword+".new.key")
#output new key file
Util.generate_key_file(instances_data_new, targetword, "./out/", targetword+".new.key")


#call sensecluster_score.sh
print(time()+" sensecluters_scorer.sh in running...")
command1 = "./senseclusters_scorer.sh" +  " ../out/"+targetword+".new.key" + " ../out/"+targetword+".old.key"

#to make sure the execution of command1 waits until writing into the files is finished. 
while not (os.path.exists("./out/"+targetword+".old.key") or os.path.exists("./out/"+targetword+".new.key")):
    time.sleep(10)
#change directory
os.chdir(os.getcwd()+"/senseclusters_scorer/")
#run sensecluster_scorer program
os.system(command1)

print(time()+" ========================Done======================")
