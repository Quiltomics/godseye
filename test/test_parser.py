import json
from collections import OrderedDict, defaultdict
import codecs
from xml.etree import ElementTree
import xmltodict
from os import path as ospath
import test_config
import glob


class Mainparser:
    def __init__(self, *args, **kwargs):
        self.json_path = kwargs['json_path']
        self.xml_path = kwargs['xml_path']

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

    def create_jsons(self, dictionary, name):
        with codecs.open(ospath.join(self.json_path, name), 'w', encoding='UTF-8') as f:
            json.dump(dictionary, f, indent=4)

    def xml_to_json(self):
        for name in glob.glob(self.xml_path + "/*.xml"):
            with open(name) as f:
                d = xmltodict.parse(f.read())
            print("Finished {}".format(name))
            yield d, ospath.basename(name).split('.')[0] + '.json'
    
    def run(self):
        for dictionary, name in self.xml_to_json():
            self.create_jsons(dictionary, name)


if __name__ == '__main__':
    MP = Mainparser(
        xml_path=ospath.join(test_config.HOME_DIR, 'godseye-files/xml'),
        json_path=ospath.join(test_config.HOME_DIR, 'godseye-files/json')
        )

    # d = MP.create_dict()
    d = MP.xml_to_json()
    MP.run()
