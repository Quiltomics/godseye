import json
from collections import OrderedDict, defaultdict
import codecs
from xml.etree import ElementTree
import xmltodict


class Mainparser:
    def __init__(self, *args, **kwargs):
        self.json_file_name = kwargs['jfn']
        self.xml_file_name = kwargs['xfn']

    def parse_journals(self):
        def looper(iterable):
            for node in iterable:
                if node.text.strip():
                    yield (node.tag, node.text)
                else:
                    yield from looper(node)

        with open(self.xml_file_name) as f:
            tree = ElementTree.parse(f)
        root = tree.getroot()
        for n, neighbor in enumerate(root.iter('MedlineCitation')):
            d = defaultdict(list)
            for i, j in looper(neighbor.getchildren()):
                d[i].append(j)
            yield n, d

    def create_dict(self):
        return OrderedDict(self.parse_journals())

    def create_json(self, dictionary):
        with codecs.open(self.json_file_name, 'w', encoding='UTF-8') as f:
            json.dump(dictionary, f, indent=4)

    def xml_to_json(self):
        with open(self.xml_file_name) as f:
            d = xmltodict.parse(f.read())
        return d

if __name__ == '__main__':
    MP = Mainparser(xfn='../godseye-files/pubmed18n0001.xml',
                    jfn='../godseye-files/articles.json')

    # d = MP.create_dict()
    d = MP.xml_to_json()
    MP.create_json(d)
