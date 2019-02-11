import argparse
import utils
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("sentences")
parser.add_argument("tags")
parser.add_argument("output")
args = parser.parse_args()

sentences = {}
sentence_ids_in_order = []
entities_per_sentence = defaultdict(list)
document_ids = []

with open(args.sentences) as f_in:
    for line in f_in:
        sentence_id = line.split()[0]
        document_ids.append(sentence_id)

        if not len(sentence_ids_in_order) or sentence_ids_in_order[-1] != sentence_id:
            sentence_ids_in_order.append(sentence_id)
        sentence = " ".join(line.split()[1:])

        assert sentence_id not in sentences or sentences[sentence_id] == sentence
        sentences[sentence_id] = sentence

with open(args.tags) as f_in:
    for line in f_in:
        split = line.split('|')
        sentence_id = split[0]
        sentence = sentences[sentence_id]
        start_idx, end_idx = [int(i) for i in split[1].split()]
        entity = split[2].strip()

        non_whitespaces_chars = 0
        new_start_idx = None
        new_end_idx = None
        for i, char in enumerate(sentence):
            if char != ' ':
                non_whitespaces_chars += 1
            if new_start_idx is None and non_whitespaces_chars == start_idx+1:
                new_start_idx = i
            if non_whitespaces_chars == end_idx+1:
                new_end_idx = i+1
                break
        entities_per_sentence[sentence_id].append((new_start_idx, new_end_idx))


with open(args.output, 'w') as f_out:
    sentences = [sentences[s_id] for s_id in sentence_ids_in_order]
    entities = [utils.merge_overlapping_entities(entities_per_sentence[s_id]) for s_id in sentence_ids_in_order]
    utils.write_to_conll(sentences, entities, document_ids, f_out)
