import os

class Util:

    @staticmethod
    def generate_key_file(data, word, directory, name):
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(directory+name, "w")
        for instance in data:
            instance_id = instance[0]
            sense_id = instance[1]
            line = word + " " + word + "." + str(instance_id) + " " + word + "." + str(sense_id)
            f.write(line+"\n")
        f.close()

    @staticmethod
    def generate_SemEval2Format(raw, clusters, directory, name):#, definitions, word): 
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(directory+name, 'w')
        f.write('<corpus lang="english">\n')
        f.write('<lexelt item="LEXELT">\n')
        for items in range(len(raw)):
            f.write('<instance id="%s">\n' %items)
            f.write('<answer instance="%s"'%items)
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
    def generate_answer_file(word, definition, example, directory, name):
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(directory+name, "w")
        f.write(word+"\n\n")
        for i in range(len(definition)):
            f.write("sense id: "+str(i)+"\n")
            f.write("definition: "+definition[i]+"\n")
            f.write("example:\n"+example[i].decode(encoding="UTF-8")+"\n\n")
        f.close() 
