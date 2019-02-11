import argparse

import extractors
import utils

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()


with open(args.input, 'r') as f_in:
    sentences, entities, document_ids = extractors.extract_from_biocreative(f_in, 'Protein')

with open(args.output, 'w') as f_out:
    utils.write_to_conll(sentences, entities, document_ids, f_out)
