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

files = set(os.listdir(os.path.join(args.input_dir, 'text')))
files = set(fname for fname in files if not fname.startswith('.'))

with open(os.path.join(args.input_dir, 'gold.txt'), 'r') as f_in:
    last_doc = ''
    tmp_sentences = []
    tmp_entities = []
    for line in f_in:
        if not line:
            continue
        line = line.split('\t')
        if line[0] != last_doc:
            document_id = os.path.basename(last_doc).strip('.txt')
            sentences += tmp_sentences
            entities += tmp_entities
            document_ids += [document_id] * len(tmp_sentences)
            last_doc = line[0]
            with open(os.path.join(args.input_dir, 'text', last_doc), 'r') as doc:
                files.remove(last_doc)
                tmp_sentences = sentence_splitter.split(doc.read())
                tmp_entities = [[] for _ in tmp_sentences]
        id, start, end = sentence_splitter.map_offsets(int(line[1]), int(line[2]))
        while len(tmp_sentences[id])<end:
            tmp_sentences = sentence_splitter.merge_sentences(id)
            tmp_entities[id] += tmp_entities[id+1]
            del tmp_entities[id+1]
            id, start, end = sentence_splitter.map_offsets(int(line[1]), int(line[2]))
        assert tmp_sentences[id][start:end] == line[3]
        tmp_entities[id] += [(start, end)]

    document_id = os.path.basename(last_doc).strip('.txt')
    sentences += tmp_sentences
    entities += tmp_entities
    document_ids += [document_id] * len(tmp_sentences)


for file in files:
    with open(os.path.join(args.input_dir, 'text', file), 'r') as doc:
        tmp_sentences = sentence_splitter.split(doc.read())
        tmp_entities = [[] for _ in tmp_sentences]
        sentences += tmp_sentences
        entities += tmp_entities
        document_ids += [os.path.basename(file).strip('.txt')] * len(tmp_sentences)


with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
