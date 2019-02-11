import argparse
import utils
from lxml import etree

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("types")
parser.add_argument("output")
args = parser.parse_args()

sentences = []
entities = []
document_ids = []
types = args.types.split(',')

with open(args.input) as f_in:
    tree = etree.parse(f_in)
    for document in tree.xpath('.//document'):
        sentence_elems = document.xpath('.//sentence')
        for sentence in sentence_elems:
            sentences += [sentence.get('text')]
            document_ids += [document.get('id')]
            entities += [[]]

            for entity in sentence.xpath(".//entity"):
                if not entity.get('type') in types:
                    continue
                char_offset = entity.get('charOffset').split('-')
                entities[-1] += [(int(char_offset[0]), int(char_offset[1]))]


with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
