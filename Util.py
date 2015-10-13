#author swetha
import os

#The Util class has the methods for generating key file, SemEval2Format, answer file
class Util:

    # The generate_key_file method generates the key file that is input for Senseclusters
    @staticmethod
    def generate_key_file(data, word, directory, name):
    #Creation of a directory using the command.
        if not os.path.exists(directory):
            os.makedirs(directory)
    #opening the file in write mode.
        f = open(directory+name, "w")
    #for each of the items in data, instance_id and sense_id are stored.
        for instance in data:
            instance_id = instance[0]
            sense_id = instance[1]
        #The name of th eline is the append of word, intance_id and sense_id
            line = word + " " + word + "." + str(instance_id) + " " + word + "." + str(sense_id)
            f.write(line+"\n")
        f.close()

    @staticmethod
    # This method generates the SemEval2Format by  input of raw, clusters, directory and name
    def generate_SemEval2Format(raw, clusters, directory, name):#, definitions, word): 
        if not os.path.exists(directory):
            os.makedirs(directory)
    #opening the directory in write mode
        f = open(directory+name, 'w')
        f.write('<corpus lang="english">\n')
        f.write('<lexelt item="LEXELT">\n')
    #for each of the items in the range of length of raw, writing the output to the file.
        for items in range(len(raw)):
            f.write('<instance id="%s">\n' %items)
            f.write('<answer instance="%s"'%items)
    #for each of the items in range of length of clusters, output to file.
            for i in range(len(clusters)):
                if(items in clusters[i]):
                    senseId=i
            f.write(' senseid="%s"/>\n'%senseId)
            f.write('<context>\n')
            f.write((raw[items]).decode(encoding="UTF-8"))
            f.write('\n')
            f.write('</context>\n')
            f.write('</instance>\n')
        f.write('</lexelt>\n')
        f.write('</corpus>\n')
        f.close()

    @staticmethod
    #This method generates the answer file using the word, definition, example, directory and name.
    def generate_answer_file(word, definition, example, directory, name):
        #create directory if one does not exist 
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(directory+name, "w")
        f.write(word+"\n\n")
        #output the senseid, definition and example
        for i in range(len(definition)):
            f.write("sense id: "+str(i)+"\n")
            f.write("definition: "+definition[i]+"\n")
            f.write("example:\n"+example[i].decode(encoding="UTF-8")+"\n\n")
        f.close() 
