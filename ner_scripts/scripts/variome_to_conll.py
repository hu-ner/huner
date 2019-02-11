### NEEDS PATCHED INPUT FILE ###

import argparse

import extractors
import utils

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("type")
args = parser.parse_args()


all_sentences = []
all_entities = []
types = args.type.split(',')

with open(args.input, 'r') as f_in:
    sentences, entities, document_ids = extractors.extract_from_biocreative(f_in, types, split_sentences=True)

with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
