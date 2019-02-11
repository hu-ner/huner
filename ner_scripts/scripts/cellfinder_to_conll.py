import argparse
import utils
import os
from opennlp_wrapper import SentenceSplitter

parser = argparse.ArgumentParser()
parser.add_argument("input_dir")
parser.add_argument("type")
parser.add_argument("output")
args = parser.parse_args()

opennlp_path = os.environ['OPENNLP']
sentence_splitter = SentenceSplitter(opennlp_path, 'en-sent.bin')

sentences = []
entities = []
document_ids = []

ann_files = [file for file in os.listdir(args.input_dir) if file[-4:]=='.ann']

for ann_file in ann_files:
    txt_file = ann_file[:-4] + '.txt'
    with open(os.path.join(args.input_dir, ann_file)) as f_ann:
        with open(os.path.join(args.input_dir, txt_file)) as f_txt:
            document_id = os.path.basename(txt_file).strip('.txt')
            tmp_sentences = sentence_splitter.split(f_txt.read())
            tmp_entities = [[] for _ in tmp_sentences]
            for line in f_ann:
                if not line:
                    continue
                line = line.split('\t')
                line = [line[0]] + line[1].split() + [line[2]]
                if line[1] != args.type:
                    continue
                id, start, end = sentence_splitter.map_offsets(int(line[2]), int(line[3]))
                while len(tmp_sentences[id]) < end:
                    tmp_sentences = sentence_splitter.merge_sentences(id)
                    tmp_entities[id] += tmp_entities[id + 1]
                    del tmp_entities[id + 1]
                    id, start, end = sentence_splitter.map_offsets(int(line[2]), int(line[3]))
                assert tmp_sentences[id][start:end] == line[4].strip()
                tmp_entities[id] += [(start, end)]
    sentences += tmp_sentences
    document_ids += [document_id] * len(tmp_sentences)
    entities += tmp_entities

with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
