import argparse
import os
from opennlp_wrapper import OpenNLP

opennlp_path = os.environ['OPENNLP']

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("types")
parser.add_argument("output")
args = parser.parse_args()

types = args.types.split(',')

pos_tagger = OpenNLP(opennlp_path, 'POSTagger', 'en-pos-maxent.bin')

with open(args.input, 'r') as f_in:
    with open(args.output, 'w') as f_out:
        tokens = []
        entities = []
        for line in f_in:
            line = line.strip()
            if line[:3] == '###':
                document_id = line.split(':')[-1]
                f_in.__next__()
                continue
            if not line:
                pos_tags = pos_tagger.parse(' '.join(tokens)).decode().split()
                for pos_tag, token, entity in zip(pos_tags, tokens, entities):
                    f_out.write(document_id + ' ' + token + ' ' + pos_tag.split('_')[-1] + ' ' + entity + '\n')
                f_out.write('\n')
                tokens = []
                entities = []
            else:
                parts = line.split()
                tokens += [parts[0].strip()]
                entity = parts[1].strip()
                if entity[2:] in types:
                    entity = entity[:2]+'NP'
                else:
                    entity = 'O'
                entities += [entity]
