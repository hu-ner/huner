import argparse
import os
from lxml import etree

import utils

parser = argparse.ArgumentParser()
parser.add_argument("input_dirs")
parser.add_argument("output")
args = parser.parse_args()

sentences = []
entities = []
document_ids = []

for dir in args.input_dirs.split(','):
    docs = [file for file in os.listdir(os.path.join(dir, 'mmax')) if os.path.isdir(os.path.join(dir, 'mmax', file))]
    for doc in docs:
        try:
            word_f = open(os.path.join(dir, 'mmax', doc, 'Basedata', 'Basedata.xml'), 'r')
            sentence_f = open(os.path.join(dir, 'mmax', doc, 'Markables', 'sentence.xml'), 'r')
            protein_f = open(os.path.join(dir, 'mmax', doc, 'Markables', 'proteins.xml'), 'r')
            id_f = open(os.path.join(dir, 'mmax', doc, 'Basedata.uri'), 'r')
            document_id = id_f.read().strip()
            word_tree = etree.parse(word_f)
            sentence_tree = etree.parse(sentence_f).getroot()
            protein_tree = etree.parse(protein_f).getroot()
        except:
            print('Skipped invalid XML')
            continue
        word_to_id = {}
        words = []
        for i, token in enumerate(word_tree.xpath('.//word')):
            words += [token.text]
            word_to_id[token.get('id')] = i
        word_pos = [(0,0) for _ in words]
        pre_sentences = []
        for sentence in sentence_tree:
            pre_sentences += [(int(sentence.get('id').split('_')[-1]), sentence.get('span'))]
        pre_sentences.sort()
        tmp_sentences = []
        for j, sentence in enumerate(pre_sentences):
            tmp_sentence = []
            akt_pos = 0
            start = word_to_id[sentence[1].split('..')[0]]
            end = word_to_id[sentence[1].split('..')[1]]
            for i in range(start, end+1):
                tmp_sentence += [words[i]]
                word_pos[i] = (j, akt_pos)
                akt_pos += len(words[i])+1
            tmp_sentences += [tmp_sentence]
        tmp_entities = [[] for _ in tmp_sentences]
        for protein in protein_tree:
            try:
                start = word_to_id[protein.get('span').split('..')[0]]
                end = word_to_id[protein.get('span').split('..')[-1]]
                tmp_entities[word_pos[start-1][0]] += [(word_pos[start-1][1], word_pos[end-1][1]+len(words[end-1]))]
            except:
                print('Skipped multipart entity')
        sentences += tmp_sentences
        entities += tmp_entities
        document_ids += [document_id] * len(tmp_sentences)

with open(args.output, 'w') as f_out:
    utils.write_to_conll([' '.join(x) for x in sentences], entities, document_ids, f_out, tokenizer=lambda x:x.split(' '))
