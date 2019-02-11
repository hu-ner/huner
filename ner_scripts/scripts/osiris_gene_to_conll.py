import argparse
import os
from lxml import etree
from opennlp_wrapper import SentenceSplitter
import tqdm

import utils

parser = argparse.ArgumentParser()
parser.add_argument("input_dir")
parser.add_argument("types")
parser.add_argument("output")
args = parser.parse_args()

types = args.types.split(',')

sentences = []
entities = []
document_ids = []

opennlp_path = os.environ['OPENNLP']
sentence_splitter = SentenceSplitter(opennlp_path, 'en-sent.bin')

files = [file for file in os.listdir(args.input_dir) if file[-4:]=='.ann']

for file in tqdm.tqdm(files):
    with open(os.path.join(args.input_dir, file), 'r') as f_ann:
        with open(os.path.join(args.input_dir, file[:-4]), 'r') as f_txt:
            text = f_txt.read()
            document_id = text.split('\n\n')[0]
            tmp_sentences = sentence_splitter.split(text)
            tmp_entities = [[] for _ in tmp_sentences]
            tree = etree.parse(f_ann)
            for annotation in tree.xpath(".//Annotation"):
                if not annotation.get('type') in types:
                    continue
                o_start, o_end = [int(x) for x in annotation.get('span').split('..')]
                id, start, end = sentence_splitter.map_offsets(o_start, o_end)
                while (len(tmp_sentences[id]) < end):
                    tmp_sentences = sentence_splitter.merge_sentences(id)
                    tmp_entities[id] += tmp_entities[id + 1]
                    del tmp_entities[id + 1]
                    id, start, end = sentence_splitter.map_offsets(o_start, o_end)
                assert tmp_sentences[id][start:end] == text[o_start:o_end]
                tmp_entities[id] += [(start, end)]
            sentences += tmp_sentences[1:]
            entities += tmp_entities[1:]
            document_ids += [document_id] * (len(tmp_sentences) - 1)

with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
