import argparse
import utils
from collections import defaultdict
from lxml import etree

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

sentences = {}
sentence_ids_in_order = []
entities_per_sentence = defaultdict(list)
token_ids_per_sentence = {}

with open(args.input) as f_in:
    tree = etree.parse(f_in)
    sentence_elems = tree.xpath('//sentence')
    for sentence in sentence_elems:
        sentence_id = sentence.attrib['id']
        sentence_ids_in_order.append(sentence_id)
        token_ids = []
        token_offsets = []
        sentence_text = ""

        all_entity_token_ids = []
        entities = (sentence.xpath(".//entity[@type='Individual_protein']") +
                    sentence.xpath(".//entity[@type='Gene/protein/RNA']") +
                    sentence.xpath(".//entity[@type='Gene']") +
                    sentence.xpath(".//entity[@type='Protein_family_or_group']") +
                    sentence.xpath(".//entity[@type='Protein_complex']") +
                    sentence.xpath(".//entity[@type='DNA_family_or_group']"))
        for entity in entities:
            valid_entity = True
            entity_token_ids = set()
            for subtoken in entity.xpath('.//nestedsubtoken'):
                token_id = '.'.join(subtoken.attrib['id'].split('.')[1:3])
                entity_token_ids.add(token_id)

            if valid_entity:
                all_entity_token_ids.append(entity_token_ids)

        for token in sentence.xpath('.//token'):
            token_text = ''.join(token.xpath('.//subtoken/@text'))
            token_id = '.'.join(token.attrib['id'].split('.')[1:])
            token_ids.append(token_id)
            token_offsets.append(len(sentence_text)+1)
            sentence_text += ' ' + token_text

        assert sentence_id not in sentences or sentences[sentence_id] == sentence_text
        sentences[sentence_id] = sentence_text

        for entity_token_ids in all_entity_token_ids:
            entity_start = None
            for token_idx, (token_id, token_offset) in enumerate(zip(token_ids, token_offsets)):
                if token_id in entity_token_ids:
                    if entity_start is None:
                        entity_start = token_offset
                else:
                    if entity_start is not None:
                        entities_per_sentence[sentence_id].append((entity_start, token_offset - 1))
                        entity_start = None


with open(args.output, 'w') as f_out:
    sentences = [sentences[s_id] for s_id in sentence_ids_in_order]
    entities = [utils.merge_overlapping_entities(entities_per_sentence[s_id]) for s_id in sentence_ids_in_order]
    def tokenizer(sentence):
        return sentence.split()
    utils.write_to_conll(sentences, entities, [str(x) for x in range(0, len(sentence_ids_in_order))], f_out, tokenizer=tokenizer)
