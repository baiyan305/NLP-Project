import SensevalParser
import SenseCluster


input = "/Users/Yan/IdeaProjects/WordSense/src/model/xml"

parser = SensevalParser()
parser.parse(input)

sense_cluster = SenseCluster()
sense_cluster.parse(parser.get_clean_instance)
group = sense_cluster.get_group()
sense_cluster.get_commonwords()


