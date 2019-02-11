import argparse
import os
from tqdm import tqdm

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

dirs = [file for file in os.listdir(args.input_dir) if os.path.isdir(os.path.join(args.input_dir, file))]
files = []
for directory in dirs:
    files += [os.path.join(directory, file) for file in os.listdir(os.path.join(args.input_dir, directory)) if file[-4:]=='.ann']

sentences = []
entities = []
document_ids = []

for file in tqdm(files):
    with open(os.path.join(args.input_dir, file), 'r') as f_ann:
        with open(os.path.join(args.input_dir, file[:-4]+'.txt'), 'r') as f_txt:
            document_id = os.path.basename(file).split('_')[0]
            text = f_txt.read()
            tmp_sentences = sentence_splitter.split(text)
            tmp_entities = [[] for _ in tmp_sentences]
            for line in f_ann:
                if line[-1] == '\n':
                    line = line[:-1]
                if not line:
                    continue
                line = line.split('\t')
                mid = line[1].split()
                line = [line[0], mid[0], mid[1], mid[-1], line[2]]
                if line[1] not in types:
                    continue
                o_start = int(line[2])
                o_end = int(line[3])
                id, start, end = sentence_splitter.map_offsets(o_start, o_end)
                while (len(tmp_sentences[id]) < end):
                    tmp_sentences = sentence_splitter.merge_sentences(id)
                    tmp_entities[id] += tmp_entities[id + 1]
                    del tmp_entities[id + 1]
                    id, start, end = sentence_splitter.map_offsets(o_start, o_end)
                assert tmp_sentences[id][start:end] == text[o_start:o_end].replace('\n', ' ')
                assert tmp_sentences[id][start:end] == line[4]
                tmp_entities[id] += [(start, end)]
            sentences += tmp_sentences
            document_ids += [document_id] * len(tmp_sentences)
            entities += tmp_entities

with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
