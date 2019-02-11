import argparse
import os
from glob import glob

from opennlp_wrapper import OpenNLP

opennlp_path = os.environ['OPENNLP']

parser = argparse.ArgumentParser()
parser.add_argument("input_dir")
parser.add_argument("output")
args = parser.parse_args()

pos_tagger = OpenNLP(opennlp_path, 'POSTagger', 'en-pos-maxent.bin')
input_files = glob(args.input_dir)
if os.path.exists(args.output):
    os.remove(args.output)

for fname in input_files:
    with open(fname, 'r') as f_in:
        with open(args.output, 'a') as f_out:
            document_id = os.path.basename(fname).strip('.conll')
            tokens = []
            entities = []
            for line in f_in:
                line = line.strip()
                if not line:
                    pos_tags = pos_tagger.parse(' '.join(tokens)).decode().split()
                    for pos_tag, token, entity in zip(pos_tags, tokens, entities):
                        f_out.write(document_id + ' ' + token + ' ' + pos_tag.split('_')[-1] + ' ' + entity + '\n')
                    f_out.write('\n')
                    tokens = []
                    entities = []
                else:
                    parts = line.split()
                    tokens += [parts[1].strip()]
                    entity = parts[0].strip()
                    if len(entity) == 4:
                        entity = entity[:-2] + 'NP'
                    entities += [entity]
