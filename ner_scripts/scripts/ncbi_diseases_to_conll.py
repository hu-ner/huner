import argparse
import os

import utils
from opennlp_wrapper import SentenceSplitter

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

opennlp_path = os.environ['OPENNLP']
sentence_splitter = SentenceSplitter(opennlp_path, 'en-sent.bin')

sentences = []
entities = []
document_ids = []

with open(args.input, 'r') as f_in:
    c = 1
    text = ''
    tmp_sentences = []
    tmp_entities = []
    document_id = ''
    for line in f_in:
        line = line.strip()
        if not line:
            sentences += tmp_sentences
            entities += tmp_entities
            document_ids += [document_id] * len(tmp_sentences)
            c=1
            continue
        if c==1:
            text = line.split('|')[2] + ' '
            document_id = line.split('|')[0]
        elif c==2:
            text += line.split('|')[2]
            tmp_sentences = sentence_splitter.split(text)
            tmp_entities = [[] for _ in tmp_sentences]
        else:
            line = line.split('\t')
            o_start = int(line[1])
            o_end = int(line[2])
            id, start, end = sentence_splitter.map_offsets(o_start, o_end)
            while len(tmp_sentences[id]) < end:
                tmp_sentences = sentence_splitter.merge_sentences(id)
                tmp_entities[id] += tmp_entities[id + 1]
                del tmp_entities[id + 1]
                id, start, end = sentence_splitter.map_offsets(o_start, o_end)
            assert tmp_sentences[id][start:end] == text[o_start:o_end]
            assert tmp_sentences[id][start:end] == line[3]
            tmp_entities[id] += [(start, end)]
        c += 1

    if c != 1:
        sentences += tmp_sentences
        entities += tmp_entities
        document_ids += [document_id] * len(tmp_sentences)

with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
