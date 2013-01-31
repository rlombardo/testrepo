#
# Read an xml file, write a json file 
#

from xml.etree import ElementTree
from pprint import pprint
import json
    
class XmlList(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag or element[0].items():
                    self.append(XmlDict(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlList(element))
            elif element.text:
                text = element.text.strip()
                
                if element.items():
                    el_dict = dict(element.items())
                    if text:
                        el_dict["value"] = text
                    
                    self.append(el_dict)
                else:
                    if text:
                        self.append(text)
                        
class XmlDict(dict):
    def __init__(self, parent_element):
        childrenNames = []
        for child in parent_element.getchildren():
            childrenNames.append(child.tag)
    
        if parent_element.items(): #attributes
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                #print len(element), element[0].tag, element[1].tag
                if len(element) == 1 or (element[0].tag != element[1].tag):
                    aDict = XmlDict(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlList(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
    
                if childrenNames.count(element.tag) > 1:
                    try:
                        currentValue = self[element.tag]
                        currentValue.append(aDict)
                        self.update({element.tag: currentValue})
                    except: 
                        self.update({element.tag: [aDict]}) 
                else:
                    self.update({element.tag: aDict})
            elif element.items():
                el_dict = dict(element.items())
                if element.text:
                    text = element.text
                    text = text.strip()
                    if text:
                        el_dict['value'] = text
                        
                self.update({element.tag: el_dict})
            else:
                if element.text:
                    text = element.text
                    text = text.strip()
                    if text:
                        self.update({element.tag: text})
                else:
                    self.update({element.tag: element.text})       

if __name__ == '__main__':
    wkdir = "C:/Users/db2admin/git/TestRepoGIT/TestRepoGIT/src/"
    outfile = "%s%s" % (wkdir, "movies.json")
    infile = "%s%s" % (wkdir, "sample_movies.xml")
    fw = open(outfile, "w")
    fw.write('{"movies" : [')
    for event, elem in ElementTree.iterparse(infile):
        if elem.tag == "movie":
            json_raw = XmlDict(elem)
            fw.write(str(json_raw)+ ", ")
            elem.clear()
    fw.write(']}')
    fw.close()
    
    print ""
    print "******** RESULTING FILE ***************"
    print
    fd = open(outfile)
    lines = fd.read()
    raw_json = eval(lines)
    pprint(raw_json)
   