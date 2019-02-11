import argparse
import os
from tqdm import tqdm
from lxml import etree

import utils
from opennlp_wrapper import SentenceSplitter

parser = argparse.ArgumentParser()
parser.add_argument("input_dir")
parser.add_argument("types")
parser.add_argument("output")
args = parser.parse_args()

types = args.types.split(',')

opennlp_path = os.environ['OPENNLP']
sentence_splitter = SentenceSplitter(opennlp_path, 'en-sent.bin')

files = []

files = [os.path.join(args.input_dir, 'xml', 'TYPE', file) for file in
         os.listdir(os.path.join(args.input_dir, 'xml', types[0])) if file[-4:] == '.xml']

sentences = []
entities = []
document_ids = []

for file in tqdm(files):
    txt_path = os.path.join(args.input_dir, 'articles', 'txt', os.path.basename(file)[:12])
    annotations = []
    for t in types:
        f_ann = open(file.replace('TYPE', t), 'r')
        ann_tree = etree.parse(f_ann)
        annotations += ann_tree.xpath('//annotation')
    with open(txt_path, 'r') as f_txt:
        document_id = os.path.basename(file).split('.')[0]
        text = f_txt.read()
        tmp_sentences = sentence_splitter.split(text)
        tmp_entities = [[] for _ in tmp_sentences]
        for ann in annotations:
            span = ann.xpath('span')[0]
            entity = ann.xpath('spannedText')[0].text
            o_start = int(span.get('start'))
            o_end = int(span.get('end'))
            id, start, end = sentence_splitter.map_offsets(o_start, o_end)
            while len(tmp_sentences[id]) < end:
                tmp_sentences = sentence_splitter.merge_sentences(id)
                tmp_entities[id] += tmp_entities[id + 1]
                del tmp_entities[id + 1]
                id, start, end = sentence_splitter.map_offsets(o_start, o_end)

            if (tmp_sentences[id][start:end] != text[o_start:o_end].replace('\n', ' ') or
                    tmp_sentences[id][start:end] != entity):
                if entity.find('...') == -1:
                    print(f'Encountered error in file {file} for entity {entity}')
                    break
            else:
                tmp_entities[id] += [(start, end)]

        sentences += tmp_sentences
        entities += tmp_entities
        document_ids += [document_id] * len(tmp_sentences)

with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
