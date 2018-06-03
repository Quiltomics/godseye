import json
from collections import OrderedDict
import codecs
from xml.etree import ElementTree
from itertools import chain
from operator import itemgetter


class Mainparser:
    def __init__(self, *args, **kwargs):
        self.json_file_name = kwargs['jfn']
        self.xml_file_name = kwargs['xfn']

    def journals(self):
        with open(self.xml_file_name) as f:
            tree = ElementTree.parse(f)
        root = tree.getroot()
        for n, neighbor in enumerate(root.iter('MedlineCitation')):
            
            sub = {node.tag: {node.tag: node.text}
                    if node.text != '\n' 
                    else {el.tag: el.text if el.text != '\n'
                                          else {e.tag: e.text for e in el}
                    for el in node.getchildren()}
                    for node in neighbor.getchildren()}
            
            if neighbor.text:
                yield n, sub

    def create_dict(self):
        return OrderedDict(self.journals())

    def create_json(self):
        the = self.create_dict()
        with codecs.open(self.json_file_name, 'w', encoding='UTF-8') as f:
            json.dump(the, f, indent=4)


if __name__ == '__main__':
    MP = Mainparser(xfn='../godseye-files/pubmed18n0001.xml',
                    jfn='../godseye-files/articles.json')

    MP.create_json()



