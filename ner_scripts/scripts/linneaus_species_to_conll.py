import argparse
import utils
import os
from opennlp_wrapper import SentenceSplitter

parser = argparse.ArgumentParser()
parser.add_argument("input_dir")
parser.add_argument("output")
args = parser.parse_args()

opennlp_path = os.environ['OPENNLP']
sentence_splitter = SentenceSplitter(opennlp_path, 'en-sent.bin')

sentences = []
entities = []
document_ids = []

files = set(os.listdir(os.path.join(args.input_dir, 'txt')))

with open(os.path.join(args.input_dir, 'filtered_tags.tsv'), 'r') as f_in:
    next(f_in)
    last_doc = ''
    tmp_sentences = []
    tmp_entities = []
    for line in f_in:
        if not line:
            continue
        line = line.split('\t')
        if line[1] != last_doc:
            document_ids += [last_doc] * len(tmp_sentences)
            sentences += tmp_sentences
            entities += tmp_entities
            last_doc = line[1]
            with open(os.path.join(args.input_dir, 'txt', last_doc + '.txt'), 'r') as doc:
                files.remove(last_doc + '.txt')
                tmp_sentences = sentence_splitter.split(doc.read())
                tmp_entities = [[] for _ in tmp_sentences]
        id, start, end = sentence_splitter.map_offsets(int(line[2]), int(line[3]))
        while len(tmp_sentences[id])<end:
            tmp_sentences = sentence_splitter.merge_sentences(id)
            tmp_entities[id] += tmp_entities[id+1]
            del tmp_entities[id+1]
            id, start, end = sentence_splitter.map_offsets(int(line[2]), int(line[3]))
        assert tmp_sentences[id][start:end] == line[4]
        tmp_entities[id] += [(start, end)]
    document_ids += [last_doc] * len(tmp_sentences)
    sentences += tmp_sentences
    entities += tmp_entities

for file in files:
    with open(os.path.join(args.input_dir, 'txt', file), 'r') as doc:
        tmp_sentences = sentence_splitter.split(doc.read())
        tmp_entities = [[] for _ in tmp_sentences]
        sentences += tmp_sentences
        entities += tmp_entities
        document_ids += [file.strip('.txt')] * len(tmp_sentences)

with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
