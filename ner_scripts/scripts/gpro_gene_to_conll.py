import argparse

from tqdm import tqdm

import utils
import os
from opennlp_wrapper import SentenceSplitter

parser = argparse.ArgumentParser()
parser.add_argument("text")
parser.add_argument("annotations")
parser.add_argument("output")
args = parser.parse_args()

opennlp_path = os.environ['OPENNLP']
sentence_splitter = SentenceSplitter(opennlp_path, 'en-sent.bin')

sentences = []
entities = []
document_ids = []

with open(args.text, 'r') as f_text:
    with open(args.annotations, 'r') as f_annotations:
        texts = {}
        for line in f_text:
            if not line:
                continue
            parts = line.split('\t')
            texts[parts[0]] = (parts[1], parts[2])
        last_doc = ''
        tmp_sentences = []
        tmp_entities = []
        for line in tqdm(f_annotations):
            if not line:
                continue
            line = line.split('\t')
            if line[0] != last_doc:
                sentences += tmp_sentences
                entities += tmp_entities
                document_ids += [last_doc] * len(tmp_sentences)
                if last_doc:
                    del texts[last_doc]
                last_doc = line[0]
                tmp_sentences = sentence_splitter.split(texts[line[0]][1])
                tmp_sentences += [texts[line[0]][0]]
                tmp_entities = [[] for _ in tmp_sentences]
            if line[1] == 'T':
                tmp_entities[-1] += [(int(line[2]), int(line[3]))]
                assert tmp_sentences[-1][int(line[2]):int(line[3])] == line[4]
            else:
                id, start, end = sentence_splitter.map_offsets(int(line[2]), int(line[3]))
                while (len(tmp_sentences[id])<end):
                    tmp_sentences = sentence_splitter.merge_sentences(id)
                    tmp_entities[id] += tmp_entities[id+1]
                    del tmp_entities[id+1]
                    id, start, end = sentence_splitter.map_offsets(int(line[2]), int(line[3]))
                assert tmp_sentences[id][start:end] == line[4]
                tmp_entities[id] += [(start, end)]
        sentences.append(tmp_sentences[-1])
        sentences += tmp_sentences[:-1]
        entities.append(tmp_entities[-1])
        entities += tmp_entities[:-1]
        document_ids += [last_doc] * len(tmp_sentences)

    for document_id, text in texts.items():
        tmp_sentences = [text[0]]
        tmp_sentences += sentence_splitter.split(text[1])
        tmp_entities = [[] for _ in tmp_sentences]
        sentences += tmp_sentences
        entities += tmp_entities
        document_ids += [document_id] * len(tmp_sentences)

with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
