import argparse
import os
import json
from opennlp_wrapper import SentenceSplitter
import tqdm

import utils

parser = argparse.ArgumentParser()
parser.add_argument("input_dir")
parser.add_argument("types")
parser.add_argument("output")
args = parser.parse_args()

sentences = []
entities = []
document_ids = []
types = args.types.split(',')

opennlp_path = os.environ['OPENNLP']
sentence_splitter = SentenceSplitter(opennlp_path, 'en-sent.bin')

files = [file for file in os.listdir(args.input_dir) if file[-5:]=='.json']

for file in tqdm.tqdm(files):
    document_id = os.path.basename(file).strip('.json')
    with open(os.path.join(args.input_dir, file), 'r') as f_in:
        data = json.load(f_in)
        tmp_sentences = sentence_splitter.split(data['text'])
        tmp_entities = [[] for _ in tmp_sentences]
        if 'denotations' in data.keys():
            for ann in data['denotations']:
                o_start = ann['span']['begin']
                o_end = ann['span']['end']
                if not ann['obj'].split(':')[0] in types:
                    continue
                id, start, end = sentence_splitter.map_offsets(o_start, o_end)
                while (len(tmp_sentences[id]) < end):
                    tmp_sentences = sentence_splitter.merge_sentences(id)
                    tmp_entities[id] += tmp_entities[id + 1]
                    del tmp_entities[id + 1]
                    id, start, end = sentence_splitter.map_offsets(o_start, o_end)
                assert tmp_sentences[id][start:end] == data['text'][o_start:o_end]
                tmp_entities[id] += [(start, end)]
        sentences += tmp_sentences
        document_ids += [document_id] * len(tmp_sentences)
        entities += tmp_entities

with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
