import argparse
import utils
from lxml import etree

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

sentences = []
entities = []

with open(args.input, 'r') as f_in:
    tree = etree.parse(f_in)
    for document in tree.xpath('.//document'):
        assert len(document.xpath('passage/text')) == 1
        text = document.xpath('passage/text')[0].text
        tmp_sentences = text.split('\n')
        tmp_entities = [[] for x in tmp_sentences]
        for annotation in document.xpath('.//annotation'):
            prot = False
            for infon in annotation.xpath('.//infon'):
                prot |= ((infon.get('key') == 'type') & (infon.text[0:2] == 'pm'))
            if not prot:
                continue
            offset = int(annotation.xpath('.//location')[0].get('offset'))
            length = int(annotation.xpath('.//location')[0].get('length'))
            i = 0
            while offset > len(tmp_sentences[i]):
                offset -= len(tmp_sentences[i])+1
                i += 1
            tmp_entities[i] += [(offset, offset+length)]
        sentences += tmp_sentences
        entities += tmp_entities

with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, f_out)
