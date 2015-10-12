from lxml.etree import parse,tostring

class SensevalParser:
    cleanedlist =[]
    uncleanedlist=[]

    def get_raw_instance():
        return uncleanedlist

    def get_clean_instance():
        return cleanedlist

    def parse(input):
        doc=parse(input)
        element=doc.xpath('//context')
        for c in element:
            cleanedlist.append(tostring(c).replace('<%s>'%c.tag,'',1).replace('</%s>'%c.tag,'',-1).replace(".","").replace("!","").replace("@","").replace("#","").replace("$","").replace("%","").replace("^","").replace("&","").replace("*","").replace("(","").replace(")","").replace("[","").replace("]","").replace("{","").replace("}","").replace(";","").replace(":","").replace(",","").replace("/","").replace("<","").replace(">","").replace("?","").replace("|","").replace("`","").replace("~","").replace("-","").replace("=","").replace("_","").replace("+","").replace("headApplehead","hAppleh").replace("headapplehead","happleh"))
        for c in element:
            uncleanedlist.append(tostring(c).replace('<%s>'%c.tag,'',1).replace('</%s>'%c.tag,'',-1).replace("headApplehead","hAppleh").replace("headapplehead","happleh"))
