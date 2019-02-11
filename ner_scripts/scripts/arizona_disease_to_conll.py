# Arizona disease is excluded from the automatic conversion and splitting process, due to its overlap with NCBI disease.
# Simultaneous evaluation on both corpora could lead to skewed results.
# The conversion script is still given, in case evaluation on this corpus is still intended.

import argparse
import utils
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

sentences = {}
sentence_ids_in_order = []
entities_per_sentence = defaultdict(list)
document_ids = []

with open(args.input, encoding='latin1') as f_in, open(args.output, 'w') as f_out:
    next(f_in)
    for line in f_in:
        document_id = line.split('\t')[0]
        pmid = line.split('\t')[1]
        sentence_no = line.split('\t')[2]

        sentence_id = pmid + '.' + sentence_no
        if not len(sentence_ids_in_order) or sentence_ids_in_order[-1] != sentence_id:
            sentence_ids_in_order.append(sentence_id)
            document_ids.append(document_id)
        sentence = line.split('\t')[3]

        assert sentence_id not in sentences or sentences[sentence_id] == sentence
        sentences[sentence_id] = sentence

        try:
            start_point = int(line.split('\t')[4]) - 1
            end_point = int(line.split('\t')[5])
        except ValueError:  # no annotation
            continue

        entities_per_sentence[sentence_id].append((start_point, end_point))

    sentences = [sentences[s_id] for s_id in sentence_ids_in_order]
    entities = [utils.merge_overlapping_entities(entities_per_sentence[s_id]) for s_id in sentence_ids_in_order]
    utils.write_to_conll(sentences, entities, document_ids, f_out)
