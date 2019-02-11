import argparse
import os
from opennlp_wrapper import OpenNLP, SentenceSplitter

opennlp_path = os.environ['OPENNLP']

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

pos_tagger = OpenNLP(opennlp_path, 'POSTagger', 'en-pos-maxent.bin')
sentence_splitter = SentenceSplitter(opennlp_path, 'en-sent.bin')

with open(args.input, 'r', encoding='iso-8859-1') as f_in:
    with open(args.output, 'w') as f_out:
        tokens = []
        entities = []
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            if line[:3]=='###':
                i = 0
                for sentence in sentence_splitter.split(' '.join(tokens)):
                    sentence_start = i
                    length = 0
                    while length < len(sentence):
                        length += len(tokens[i])+1
                        i+=1
                    pos_tags = [x.split('_')[-1] for x in pos_tagger.parse(' '.join(tokens[sentence_start:i])).decode().split()]
                    for pos_tag, token, entity in zip(pos_tags, tokens[sentence_start:i], entities[sentence_start:i]):
                        f_out.write(document_id + ' ' + token + ' ' + pos_tag.split('_')[-1] + ' ' + entity + '\n')
                    f_out.write('\n')
                tokens = []
                entities = []
                document_id = line.strip('#').strip()
            else:
                parts = line.split('|')
                tokens += [parts[0].split('\t')[0].strip()]
                entity = parts[1].strip()
                if len(entity)>1:
                    entity = entity[:2]+'NP'
                entities += [entity]
